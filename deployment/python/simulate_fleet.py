import os
import warnings

import pandas as pd
import numpy as np
from plotnine import (ggplot, aes, geom_polygon, geom_point, theme, ggtitle, labs,
                      coord_cartesian, geom_bar, theme_void, element_text)
from sklearn.linear_model import LinearRegression
from utils import (energyTWhToCarbonOutputKG, capacityMWToEnergyTWh, s_curve, log_memory_usage,
                   get_usa_maps, kgToGTons, rsnorm)

warnings.filterwarnings("ignore", module="plotnine")


def simulatePlants(
        initial_fleet,  # initial fleet (currentGen)
        typeChars,  # plant characteristics
        start_year=2014,
        end_year=2050,
        percent_fusion=0,  # k, what the maximum percent fusion allowed is
        addCapDiffProp=None,  # a matrix containing the differences of proportion of capacity growth per plant per year; see dataprep.py for its creation
        totalEnergy=None,  # a DataFrame of energy per year from 2011-2040 from AEO. See dataprep.py for its creation
        totalCapacity=None,  # a DataFrame of capacity per year from 2011-2040 from AEO. See dataprep.py for its creation
        toReplace="all",  # a list of energy technologies fusion will replace
        afterYear=2015,  # when fusion is introduced
        percent_CCS=0,  # CCS component --> (future study)
        afterYearCCS=2020,  # CCS component --> (future study)
        T_ADOPT=10,  # width of s-curve; amount of time between .05k and .95k
        EV_Switch=False,  # Switch to turn on using EV
        EV_addition=0,  # addition of EV to add electricity demand
        EV_scenario="BAU",  # which column to use in EV scenario
        save_graphs=False,
        graph_output_dir='out/graphs'
):
    print(f"Starting simulation from years {start_year} to {end_year}")
    # checking to make sure percent_fusion is a decimal 0<percent_fusion<1, not 0<percent_fusion<100
    if percent_fusion > 1:
        percent_fusion=percent_fusion * .01

    # Initialize summary DataFrame with years as index
    summary = pd.DataFrame(index=range(start_year, end_year + 1), columns=[
        'totalCapacityAfterRetirement',  # numeric var explaining total fleet capacity each year after plants retire
        'totalEnergyAfterRetirement',  # numeric var explaining total fleet energy each year after plants retire
        'dearth_t_cap',  # numeric var summarizing the yearly dearth in capacity (i.e. the total required capacity - existing capacity after retirement)
        'dearth_t_energy',  # numeric var summarizing the yearly dearth in energy (i.e. the total required energy - existing energy after retirement)
        'NGCCGrowth',  # numeric var, sum of NGCC capacity in given year
        'WindGrowth',  # numeric var, sum of wind capacity in given year
        'NuclearGrowth',  # numeric var, sum of nuclear fission capacity in given year
        'PetroleumGrowth',  # numeric var, sum of petroleum capacity in given year
        'NGSTGrowth',  # numeric var, sum of NGST capacity in given year
        'NGCTGrowth',  # numeric var, sum of NGCT capacity in given year
        'PVGrowth',  # numeric var, sum of PV capacity in given year
        'HydroGrowth',  # numeric var, sum of Hydro capacity in given year
        'CoalGrowth',  # numeric var, sum of coal capacity in given year
        'fusionGrowth',  # numeric var, sum of fusion capacity in given year
        'NGCCDearth',  # numeric var, sum of NGCC capacity retiring in given year
        'WindDearth',  # numeric var, sum of Wind capacity retiring in given year
        'NuclearDearth',  # numeric var, sum of Nuclear fission capacity retiring in given year
        'PetroleumDearth',  # numeric var, sum of Petroleum capacity retiring in given year
        'NGSTDearth',  # numeric var, sum of NGST capacity retiring in given year
        'NGCTDearth',  # numeric var, sum of NGCT capacity retiring in given year
        'PVDearth',  # numeric var, sum of PV capacity retiring in given year
        'HydroDearth',  # numeric var, sum of Hydro capacity retiring in given year
        'CoalDearth',  # numeric var, sum of Coal capacity retiring in given year
        'fusionDearth',  # numeric var, sum of Nuclear fusion capacity retiring in given year
        'totalEnergyAfterAdding',  # numeric var, sum of fleetwide energy after new plants are added
        'carbonIntensity',  # average carbon intensity of the fleet
        'totalCarbon',  # total carbon emitted in a given year
        'newCap',  # new capacity added in a given year
        'newFusionAdditions',  # new fusion capacity added in a given year
        'totalPlants',  # count of the total plants in the fleet in a given year
        'demandGrowth',  # amount of new capacity added in a given year through growth of the capacity demand
        'replacementRetirements'  # amount of new capacity added in a given year through retirements
    ])

    usaMap, usaMap2 = get_usa_maps()

    totalEnergy, totalCapacity, addCapDiffProp, addWeightedCF = extend_datasets(
        totalEnergy, totalCapacity, addCapDiffProp, end_year)
    addCapDiffProp, addWeightedCF = set_up_fusion_and_add_to_addCapDiffProp(
        addCapDiffProp, addWeightedCF, afterYear, start_year, T_ADOPT, percent_fusion, toReplace)
    fleet_t, summary, yearlyWeightedCF = miscellaneous_preparation(
        summary, addWeightedCF, typeChars, totalCapacity, initial_fleet)

    for year in range(start_year, end_year + 1):
        print(f"Running year: {year}")

        # Simulate plant operations and get results
        fleet_t, summary = simulate_year(fleet_t, summary, typeChars, totalEnergy, addCapDiffProp, yearlyWeightedCF,
                                         year, afterYear, percent_fusion, percent_CCS, usaMap2, save_graphs, graph_output_dir)

        # Debugging statements
        # Print DataFrame shapes to check for unexpected growth or decay
        # print(f"Shape of fleet_t at year {year}: {fleet_t.shape}")
        # Print memory usage
        # log_memory_usage(f"year {year}")


    # Convert structured array back to DataFrame for final output
    results = pd.DataFrame(fleet_t)

    print("Ending simulation")
    return results, summary


#### 1.  extend datasets beyond their ending year (2040)
def extend_datasets(totalEnergy, totalCapacity, addCapDiffProp, end_year):
    new_years = np.arange(2041, end_year + 1)
    new_years_df = pd.DataFrame({'year': new_years})

    # Extend totalEnergy
    energy_model = LinearRegression()
    energy_model.fit(totalEnergy[['year']], totalEnergy['EnergyBillkWh'])
    predicted_energy = energy_model.predict(new_years_df)
    predicted_energy += 2 * (totalEnergy[totalEnergy['year'] == 2040]['EnergyBillkWh'].values[0] - predicted_energy[0])
    new_energy = pd.DataFrame({'year': new_years, 'EnergyBillkWh': predicted_energy})
    totalEnergy = pd.concat([totalEnergy, new_energy], ignore_index=True)

    # Extend totalCapacity
    capacity_model = LinearRegression()
    capacity_model.fit(totalCapacity[['year']], totalCapacity['capacity'])
    predicted_capacity = capacity_model.predict(new_years_df)
    new_capacity = pd.DataFrame({'year': new_years, 'capacity': predicted_capacity})
    totalCapacity = pd.concat([totalCapacity, new_capacity], ignore_index=True)

    # Modify addCapDiffProp
    if addCapDiffProp is None:
        addCapDiffProp = pd.DataFrame()
        addWeightedCF = pd.DataFrame()
    else:
        max_year = addCapDiffProp.index.max()
        last_three_years = [max_year-2, max_year-1, max_year]
        # Create a new DataFrame to hold the new rows
        new_rows = []
        for year in range(max_year + 1, end_year + 1):
            new_row = addCapDiffProp.loc[last_three_years].mean()
            new_row.name = year
            new_rows.append(new_row)
        new_ACDP = pd.DataFrame(new_rows)
        addCapDiffProp = pd.concat([addCapDiffProp, new_ACDP], ignore_index=False)
        addWeightedCF = addCapDiffProp.copy()

    return totalEnergy, totalCapacity, addCapDiffProp, addWeightedCF


#### 2. Set up the fusion variable and adding it into the addCapDiffProp
def set_up_fusion_and_add_to_addCapDiffProp(addCapDiffProp, addWeightedCF, after_year, start_year, T_ADOPT, percent_fusion, to_replace):
    # Setting up the s-curve fusion growth
    after_year_ind = after_year - start_year
    percent_fusion = s_curve(T_ADOPT=T_ADOPT, k=percent_fusion, t=(np.arange(1, len(addCapDiffProp) + 1) - after_year_ind))

    percent_fusion[np.isnan(percent_fusion)] = percent_fusion[0]
    percent_fusion[percent_fusion < 0] = percent_fusion[0]
    percent_fusion = np.concatenate([np.zeros(after_year_ind - 1), percent_fusion[after_year_ind - 1:]])
    percent_fusion = pd.Series(percent_fusion, index=addCapDiffProp.index)

    # Adding in fusion to addCapDiffProp by taking away from the categories that it is supposed to replace
    if "All" in to_replace or "all" in to_replace:
        addCapDiffProp = addCapDiffProp.mul(1 - percent_fusion, axis=0)
    else:
        temp_inds = addCapDiffProp.columns.isin(to_replace)
        if len(to_replace) == 1:
            temp_sum = addCapDiffProp.iloc[:, temp_inds].squeeze()
        else:
            temp_sum = addCapDiffProp.iloc[:, temp_inds].sum(axis=1)

        # Align percent_fusion and temp_sum before comparison
        percent_fusion, temp_sum = percent_fusion.align(temp_sum, join='inner')

        if not percent_fusion.index.equals(temp_sum.index):
            raise ValueError("Indices of percent_fusion and temp_sum do not match after alignment")

        percent_fusion[temp_sum < percent_fusion] = temp_sum[temp_sum < percent_fusion]
        temp_multiple = 1 - percent_fusion / temp_sum
        for col in addCapDiffProp.columns[temp_inds]:
            addCapDiffProp.loc[:, col] = addCapDiffProp.loc[:, col] * temp_multiple

    addCapDiffProp["NuclearFusion"] = percent_fusion

    if "TotalTest" in addCapDiffProp.columns:
        addCapDiffProp = addCapDiffProp.drop(columns=["TotalTest"])

    if "TotalTest" in addWeightedCF.columns:
        addWeightedCF = addWeightedCF.drop(columns=["TotalTest"])

    return addCapDiffProp, addWeightedCF


### 3. Miscellaneous preparation ------------
def miscellaneous_preparation(summary, addWeightedCF, typeChars, totalCapacity, fleet0):
    # Tidying up some names
    CFs = typeChars.loc[addWeightedCF.columns, "CapFactor"]
    CFs = CFs.fillna(0)

    # Variable for weighted Carbon factor. Numeric vector.
    yearlyWeightedCF = addWeightedCF.to_numpy().dot(CFs.to_numpy())
    yearlyWeightedCF = pd.Series(yearlyWeightedCF, index=addWeightedCF.index)

    # First output generation
    summary['demandGrowth'] = np.maximum(0, np.diff(totalCapacity['capacity'], prepend=0))

    # Fleet0 is the initial fleet but is later updated in the for-loop
    fleet_dtype = [('type', 'U20'), ('capacity', float), ('startYear', int), ('age', int),
                   ('energy', float), ('carbonOutput', float), ('long', float), ('lat', float),
                   ('expRet', float), ('seqNum', int), ('isNew', bool), ('isFusion', bool), ('locCode', 'U25')]

    fleet_t = np.zeros(fleet0.shape[0], dtype=fleet_dtype)
    for col in fleet0.columns:
        fleet_t[col] = fleet0[col].values
    fleet_t['seqNum'] = np.arange(1, len(fleet_t) + 1)
    fleet_t['isNew'] = False

    return fleet_t, summary, yearlyWeightedCF


def simulate_year(fleet_t, summary, typeChars, totalEnergy, addCapDiffProp, yearlyWeightedCF, year, afterYear,
                  percent_fusion, percent_CCS, usaMap2, save_graphs, graph_output_dir):
    # a. age the plants and calculate energy -------------------------
    fleet_t['age'] += 1

    # Calculate energy
    fleet_t['energy'] = capacityMWToEnergyTWh(fleet_t['capacity'], fleet_t['type'], typeChars)

    # Calculate carbon output
    fleet_t['carbonOutput'] = energyTWhToCarbonOutputKG(fleet_t['energy'], fleet_t['type'], typeChars, percent_CCS if year > afterYear else 0)

    # Identify fusion plants
    fleet_t['isFusion'] = fleet_t['type'] == 'NuclearFusion'

    # b. pick which plants to retire -----------------------------------
    retiring_indices = np.where(fleet_t['age'] > fleet_t['expRet'])[0]
    retiring_plants = fleet_t[retiring_indices]

    # Record summaries in the output DataFrame
    summary.loc[year, 'NGCCDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'NGCC']['capacity'])
    summary.loc[year, 'WindDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'Wind']['capacity'])
    summary.loc[year, 'NuclearDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'Nuclear']['capacity'])
    summary.loc[year, 'PetroleumDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'Petroleum']['capacity'])
    summary.loc[year, 'NGSTDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'NGST']['capacity'])
    summary.loc[year, 'NGCTDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'NGCT']['capacity'])
    summary.loc[year, 'PVDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'PV']['capacity'])
    summary.loc[year, 'HydroDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'Hydroelectric']['capacity'])
    summary.loc[year, 'CoalDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'Coal']['capacity'])
    summary.loc[year, 'fusionDearth'] = np.sum(retiring_plants[retiring_plants['type'] == 'NuclearFusion']['capacity'])
    summary.loc[year, 'replacementRetirements'] = np.sum(retiring_plants['capacity'])

    # Remove retiring plants from the fleet
    remaining_indices = np.setdiff1d(np.arange(fleet_t.shape[0]), np.where(retiring_indices)[0])
    fleet_t1 = fleet_t[remaining_indices]

    # c. Calculate dearth ------------------------------------------
    current_energy = np.sum(fleet_t1['energy'])
    energy_t = totalEnergy.loc[totalEnergy['year'] == year, 'EnergyBillkWh'].values[0]
    dearth_t_energy = energy_t - current_energy
    dearth_t_cap = (dearth_t_energy / (yearlyWeightedCF.loc[year] * 10**-2 * 8760)) * 10**6
    current_cap = np.sum(fleet_t1['capacity']) / 10**3

    # Record summaries in the output DataFrame
    summary.loc[year, 'dearth_t_cap'] = dearth_t_cap
    summary.loc[year, 'dearth_t_energy'] = dearth_t_energy
    summary.loc[year, 'totalCapacityAfterRetirement'] = current_cap
    summary.loc[year, 'totalEnergyAfterRetirement'] = current_energy
    summary.loc[year, 'NGCCGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'NGCC']['capacity'])
    summary.loc[year, 'WindGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'Wind']['capacity'])
    summary.loc[year, 'NuclearGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'Nuclear']['capacity'])
    summary.loc[year, 'PetroleumGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'Petroleum']['capacity'])
    summary.loc[year, 'NGSTGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'NGST']['capacity'])
    summary.loc[year, 'PVGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'PV']['capacity'])
    summary.loc[year, 'HydroGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'Hydroelectric']['capacity'])
    summary.loc[year, 'CoalGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'Coal']['capacity'])
    summary.loc[year, 'NGCTGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'NGCT']['capacity'])
    summary.loc[year, 'fusionGrowth'] = np.sum(fleet_t1[fleet_t1['type'] == 'NuclearFusion']['capacity'])
    summary.loc[year, 'carbonIntensity'] = np.sum(fleet_t['carbonOutput']) / (np.sum(fleet_t['energy']) * 10**9)
    summary.loc[year, 'totalCarbon'] = np.sum(kgToGTons(fleet_t['carbonOutput']))
    summary.loc[year, 'newCap'] = np.sum(fleet_t1[fleet_t1['isNew']]['capacity']) / 10**3
    summary.loc[year, 'totalPlants'] = len(fleet_t)

    # d. Generate new plants based to meet the dearth proportional to AEO's additions
    new_plants = np.zeros(0, dtype=fleet_t.dtype)
    dearth_types = dearth_t_cap * addCapDiffProp.loc[year]

    # Ensure there are no non-finite values before proceeding
    dearth_types = dearth_types.fillna(0)
    avg_capacity = typeChars.loc[dearth_types.index, 'AvgCapacityMW'].fillna(1)

    num_plants_types = (dearth_types / avg_capacity).round().astype(int)
    num_plants_types[num_plants_types < 0] = 0

    summary.loc[year, 'plantsAdded'] = num_plants_types.sum()

    if num_plants_types.sum() > 0:
        new_plants = np.zeros(num_plants_types.sum(), dtype=fleet_t.dtype)
        new_plants['type'] = np.repeat(num_plants_types.index, num_plants_types.values)
        new_plants['capacity'] = np.maximum(np.random.normal(typeChars.loc[new_plants['type'], 'AvgCapacityMW'].values,
                                                             typeChars.loc[new_plants['type'], 'StdDevCapacityMW'].values), 2)
        new_plants['locCode'] = np.random.choice(retiring_plants['locCode'], len(new_plants), replace=True)
        new_plants['age'] = 1
        new_plants['startYear'] = year
        new_plants['seqNum'] = np.arange(fleet_t['seqNum'].max() + 1, fleet_t['seqNum'].max() + 1 + len(new_plants))
        new_plants['expRet'] = rsnorm(len(new_plants),
                                      mean=typeChars.loc[new_plants['type'], 'AvgRetAge'].values,
                                      sd=typeChars.loc[new_plants['type'], 'StdDevRetAge'].values,
                                      xi=typeChars.loc[new_plants['type'], 'skewness'].values)
        new_plants['energy'] = capacityMWToEnergyTWh(new_plants['capacity'], new_plants['type'], typeChars)
        new_plants['carbonOutput'] = energyTWhToCarbonOutputKG(new_plants['energy'], new_plants['type'], typeChars, percent_CCS if year > afterYear else 0)

        for _ in range(5):
            to_change = np.isnan(new_plants['expRet']) | (new_plants['expRet'] < new_plants['age'])
            new_plants['expRet'][to_change] = rsnorm(to_change.sum(),
                                                     mean=typeChars.loc[new_plants['type'][to_change], 'AvgRetAge'].values,
                                                     sd=typeChars.loc[new_plants['type'][to_change], 'StdDevRetAge'].values,
                                                     xi=typeChars.loc[new_plants['type'][to_change], 'skewness'].values)

        nuclear_types = np.isin(new_plants['type'], ['Nuclear', 'NuclearFusion'])
        new_plants['expRet'][nuclear_types] = np.random.binomial(1, 0.5, nuclear_types.sum()) * 20 + 40
        new_plants['long'] = usaMap2.loc[new_plants['locCode'], 'long'].values + np.random.normal(0, 0.05, len(new_plants))
        new_plants['lat'] = usaMap2.loc[new_plants['locCode'], 'lat'].values + np.random.normal(0, 0.05, len(new_plants))
        new_plants['isFusion'] = new_plants['type'] == 'NuclearFusion'
        new_plants['isNew'] = True

        # e. add new plants into existing fleet -----------------------
        fleet_t = np.concatenate((fleet_t1, new_plants))

    summary.loc[year, 'newFusionAdditions'] = np.sum(new_plants[new_plants['type'] == 'NuclearFusion']['capacity'])
    summary.loc[year, 'totalEnergyAfterAdding'] = np.sum(fleet_t['energy'])

    fleet_t['isFusion'] = fleet_t['type'] == 'NuclearFusion'

    if save_graphs:
        create_graphs(fleet_t, graph_output_dir, usaMap2, year)

    return fleet_t, summary


def create_graphs(fleet_t, graph_output_dir, usaMap2, year):
    plot_data = pd.DataFrame(fleet_t)
    os.makedirs(graph_output_dir, exist_ok=True)

    # Create carbon output vs. capacity scatter plot
    g = (ggplot(plot_data[plot_data['carbonOutput'] < 1e+09])
         + geom_point(aes(x='capacity', y='carbonOutput', color='type'), size=1.5, alpha=0.2)
         + theme_void()
         + labs(y="Carbon Output", x="Capacity")
         + coord_cartesian(xlim=(0, 500), ylim=(0, 1e+09)))

    # Save the scatter plot
    g.save(os.path.join(graph_output_dir, f"{year}_scatter.png"))

    # Create type distribution bar plot
    g1 = (ggplot(plot_data[plot_data['carbonOutput'] < 1e+09])
          + geom_bar(aes(x='type', fill='type'))
          + theme_void()
          + labs(x="Type"))

    # Save the bar plot
    g1.save(os.path.join(graph_output_dir, f"{year}_bar.png"))

    # Initialize the base map plot
    # Initialize graph (for making a map movie -- not included in the paper)
    # Note: Assuming usaMap is a DataFrame containing columns 'long', 'lat', and 'group'
    # Example: usaMap = pd.DataFrame({'long': ..., 'lat': ..., 'group': ...})
    usaMap2['group'] = usaMap2.index
    p = (ggplot(usaMap2, aes(x='long', y='lat')) + geom_polygon(aes(group='group')))

    # Create the map plot with power plants
    p_combined = (p
                  + geom_point(aes(x='long', y='lat', color='type', size='capacity', shape='isFusion'), data=plot_data, alpha=0.4)
                  + ggtitle(f"Power Plants in year: {year}")
                  + theme(text=element_text(size=18)))

    # Save the map plot
    p_combined.save(os.path.join(graph_output_dir, f"{year}_map.png"))
