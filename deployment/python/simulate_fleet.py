import pandas as pd
import numpy as np
from utils import energyTWhToCarbonOutputKG, capacityMWToEnergyTWh, kgToGTons, mav, s_curve, log_memory_usage


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
    # Initialize summary DataFrame with years as index
    summary = pd.DataFrame(index=range(start_year, end_year + 1), columns=[
        'totalCapacityAfterRetirement', 'totalEnergyAfterRetirement',
        'newFusionAdditions', 'totalEnergyAfterAdding'
    ])

    for year in range(start_year, end_year + 1):
        print(f"Running year: {year}")

        # Simulate plant operations and get results
        fleet_t, summary = simulate_year(initial_fleet, summary, typeChars, year, afterYear, percent_fusion, percent_CCS)

        # Debug memory usage
        # log_memory_usage(f"year {year}")

    print("Ending simulation")
    return fleet_t, summary


def simulate_year(fleet_t, summary, typeChars, year, afterYear, percent_fusion, percent_CCS):
    # Example logic for updating fleet and calculating metrics
    # (this is placeholder logic and should be replaced with actual simulation steps)

    # Convert fleet_t to structured numpy arrays
    fleet_dtype = [('type', 'U20'), ('capacity', float), ('startYear', int),
                   ('age', int), ('energy', float), ('carbonOutput', float),
                   ('long', float), ('lat', float), ('expRet', float)]

    fleet_struct = np.zeros(fleet_t.shape[0], dtype=fleet_dtype)
    for col in fleet_t.columns:
        fleet_struct[col] = fleet_t[col].values

    # Assume retirement happens based on some condition, e.g., age
    retiring_mask = fleet_struct['age'] > 30
    fleet_struct = fleet_struct[~retiring_mask]

    # Update the age of plants
    fleet_struct['age'] += 1

    # Calculate energy and capacity after retirement
    fleet_struct['energy'] = capacityMWToEnergyTWh(fleet_struct['capacity'], fleet_struct['type'], typeChars)
    fleet_struct['carbonOutput'] = energyTWhToCarbonOutputKG(fleet_struct['energy'], fleet_struct['type'], typeChars, percent_CCS)

    summary.at[year, 'totalCapacityAfterRetirement'] = np.sum(fleet_struct['capacity'])
    summary.at[year, 'totalEnergyAfterRetirement'] = np.sum(fleet_struct['energy'])

    # Add new fusion plants if applicable
    new_fusion_capacity = 0
    if year >= afterYear:
        new_fusion_capacity = np.sum(fleet_struct['capacity']) * percent_fusion
        new_plants = np.zeros(fleet_struct.shape[0], dtype=fleet_dtype)
        new_plants['type'] = 'NuclearFusion'
        new_plants['capacity'] = new_fusion_capacity / fleet_struct.shape[0]
        new_plants['age'] = 0
        new_plants['energy'] = new_fusion_capacity * 8760  # Simplified example
        fleet_struct = np.concatenate([fleet_struct, new_plants])

    summary.at[year, 'newFusionAdditions'] = new_fusion_capacity
    summary.at[year, 'totalEnergyAfterAdding'] = np.sum(fleet_struct['energy'])

    # Convert structured array back to DataFrame for final output
    fleet_t = pd.DataFrame(fleet_struct)

    return fleet_t, summary
