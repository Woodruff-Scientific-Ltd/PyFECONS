import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_polygon
from sklearn.linear_model import LinearRegression
from utils import (energyTWhToCarbonOutputKG, capacityMWToEnergyTWh, kgToGTons,
                   s_curve, log_memory_usage, get_usa_maps)


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
):
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
    fleet_t, summary, yearlyWeightedCF, p = miscellaneous_preparation(
        summary, addWeightedCF, typeChars, totalCapacity, initial_fleet, usaMap)

    for year in range(start_year, end_year + 1):
        print(f"Running year: {year}")

        # Simulate plant operations and get results
        fleet_t, summary = simulate_year(fleet_t, summary, typeChars, year, afterYear, percent_fusion, percent_CCS)

        # Print DataFrame shapes to check for unexpected growth or decay
        print(f"Shape of fleet_t at year {year}: {fleet_t.shape}")

        # Debug memory usage
        log_memory_usage(f"year {year}")


    # Convert structured array back to DataFrame for final output
    results = pd.DataFrame(fleet_t)

    print("Ending simulation")
    return results, summary


#### 1.  extend datasets beyond their ending year (2040)
def extend_datasets(totalEnergy, totalCapacity, addCapDiffProp, end_year):
    print('Extending datasets')
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
    print('Setting up s-curve fusion growth')
    # setting up the s-curve fusion growth
    after_year_ind = after_year - start_year
    percent_fusion = s_curve(T_ADOPT=T_ADOPT, k=percent_fusion, t=(np.arange(1, len(addCapDiffProp) + 1) - after_year_ind))

    percent_fusion[np.isnan(percent_fusion)] = percent_fusion[0]
    percent_fusion[percent_fusion < 0] = percent_fusion[0]
    percent_fusion = np.concatenate([np.zeros(after_year_ind - 1), percent_fusion[after_year_ind - 1:]])
    percent_fusion = pd.Series(percent_fusion, index=addCapDiffProp.index)

    # adding in fusion to addCapDiffProp by taking away from the categories that it is supposed to replace
    if "All" in to_replace or "all" in to_replace:
        addCapDiffProp = addCapDiffProp.mul(1 - percent_fusion, axis=0)
    else:
        temp_inds = addCapDiffProp.columns.isin(to_replace)
        if len(to_replace) == 1:
            temp_sum = addCapDiffProp.iloc[:, temp_inds]
        else:
            temp_sum = addCapDiffProp.iloc[:, temp_inds].sum(axis=1)

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
def miscellaneous_preparation(summary, addWeightedCF, typeChars, totalCapacity, fleet0, usaMap):
    print('Miscellaneous preparation')

    # Tidying up some names
    CFs = typeChars.loc[addWeightedCF.columns, "CapFactor"]
    CFs = CFs.fillna(0)

    # Variable for weighted Carbon factor. Numeric vector.
    yearlyWeightedCF = addWeightedCF.to_numpy().dot(CFs.to_numpy())

    # First output generation
    summary['demandGrowth'] = np.maximum(0, np.diff(totalCapacity['capacity'], prepend=0))


    # Fleet0 is the initial fleet but is later updated in the for-loop
    fleet_dtype = [('type', 'U20'), ('capacity', float), ('startYear', int), ('age', int),
                   ('energy', float), ('carbonOutput', float), ('long', float), ('lat', float),
                   ('expRet', float), ('seqNum', int), ('isNew', bool)]

    fleet_t = np.zeros(fleet0.shape[0], dtype=fleet_dtype)
    for col in fleet0.columns:
        fleet_t[col] = fleet0[col].values
    fleet_t['seqNum'] = np.arange(1, len(fleet_t) + 1)
    fleet_t['isNew'] = False

    # Initialize graph (for making a map movie -- not included in the paper)
    # Note: Assuming usaMap is a DataFrame containing columns 'long', 'lat', and 'group'
    # Example: usaMap = pd.DataFrame({'long': ..., 'lat': ..., 'group': ...})
    p = (ggplot(usaMap, aes(x='long', y='lat')) + geom_polygon(aes(group='group')))

    return fleet_t, summary, yearlyWeightedCF, p


def simulate_year(fleet_t, summary, typeChars, year, afterYear, percent_fusion, percent_CCS):
    # Example logic for updating fleet and calculating metrics
    # (this is placeholder logic and should be replaced with actual simulation steps)

    # Assume retirement happens based on some condition, e.g., age
    retiring_mask = fleet_t['age'] > 30
    fleet_t = fleet_t[~retiring_mask]

    # Update the age of plants
    fleet_t['age'] += 1

    # Calculate energy and capacity after retirement
    fleet_t['energy'] = capacityMWToEnergyTWh(fleet_t['capacity'], fleet_t['type'], typeChars)
    fleet_t['carbonOutput'] = energyTWhToCarbonOutputKG(fleet_t['energy'], fleet_t['type'], typeChars, percent_CCS)

    summary.at[year, 'totalCapacityAfterRetirement'] = np.sum(fleet_t['capacity'])
    summary.at[year, 'totalEnergyAfterRetirement'] = np.sum(fleet_t['energy'])

    # Add new fusion plants if applicable
    new_fusion_capacity = 0
    if year >= afterYear:
        new_fusion_capacity = np.sum(fleet_t['capacity']) * percent_fusion

        if new_fusion_capacity > 0 and fleet_t.shape[0] > 0:
            # Determine the number of new plants to add
            avg_capacity_per_plant = new_fusion_capacity / fleet_t.shape[0]
            num_new_plants = max(1, int(new_fusion_capacity / avg_capacity_per_plant))

            new_plants = np.zeros(num_new_plants, dtype=fleet_t.dtype)
            new_plants['type'] = 'NuclearFusion'
            new_plants['capacity'] = new_fusion_capacity / num_new_plants
            new_plants['age'] = 0
            new_plants['energy'] = new_fusion_capacity * 8760  # Simplified example

            print(f"Year {year}: fleet_struct before adding new entries: {fleet_t.shape}")
            print(f"Year {year}: new entries: {new_plants.shape}")
            fleet_struct = np.concatenate([fleet_t, new_plants])
            print(f"Year {year}: fleet_struct after adding new entries: {fleet_struct.shape}")

    summary.at[year, 'newFusionAdditions'] = new_fusion_capacity
    summary.at[year, 'totalEnergyAfterAdding'] = np.sum(fleet_t['energy'])

    return fleet_t, summary
