import pandas as pd
import numpy as np
import psutil
import os
from utils import energyTWhToCarbonOutputKG, capacityMWToEnergyTWh, kgToGTons, mav, s_curve


def log_memory_usage(step):
    process = psutil.Process(os.getpid())
    print(f"Memory usage at {step}: {process.memory_info().rss / 1024 ** 2:.2f} MB")


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
    fleet_t = initial_fleet.copy()
    results = []
    summary = pd.DataFrame(columns=['totalCapacityAfterRetirement', 'totalEnergyAfterRetirement',
                                    'newFusionAdditions', 'totalEnergyAfterAdding'])

    for year in range(start_year, end_year + 1):
        print(f"Running year: {year}")

        # Simulate plant operations and get results
        fleet_t, summary = simulate_year(fleet_t, summary, typeChars, year, afterYear, percent_fusion, percent_CCS)
        result = fleet_t.copy()
        result['year'] = year
        results.append(result)

        log_memory_usage(f"year {year}")

    # Concatenate all yearly results
    final_results = pd.concat(results, ignore_index=True)

    print("Ending simulation")
    return final_results, summary


def simulate_year(fleet_t, summary, typeChars, year, afterYear, percent_fusion, percent_CCS):
    # Example logic for updating fleet and calculating metrics
    # (this is placeholder logic and should be replaced with actual simulation steps)

    # Assume retirement happens based on some condition, e.g., age
    retiring_plants = fleet_t[fleet_t['age'] > 30]  # Example condition
    fleet_t = fleet_t[fleet_t['age'] <= 30]

    # Update the age of plants
    fleet_t.loc[:, 'age'] += 1

    missing_types = set(fleet_t['type']) - set(typeChars.index)
    if missing_types:
        print("Missing types in typeChars:", missing_types)
        raise ValueError(f"Missing types in typeChars: {missing_types}")

    # Calculate energy and capacity after retirement
    fleet_t.loc[:, 'energy'] = capacityMWToEnergyTWh(fleet_t, typeChars)
    fleet_t.loc[:, 'carbonOutput'] = energyTWhToCarbonOutputKG(fleet_t, typeChars, percent_CCS)

    summary.at[year, 'totalCapacityAfterRetirement'] = fleet_t['capacity'].sum()
    summary.at[year, 'totalEnergyAfterRetirement'] = fleet_t['energy'].sum()

    # Example of adding new fusion plants (simplified logic)
    if year >= afterYear:
        new_fusion_capacity = fleet_t['capacity'].sum() * percent_fusion
        new_plants = pd.DataFrame({
            'type': ['NuclearFusion'] * len(fleet_t),
            'capacity': new_fusion_capacity / len(fleet_t),
            'age': [0] * len(fleet_t),
            'energy': new_fusion_capacity * 8760  # Simplified example
        })
        fleet_t = pd.concat([fleet_t, new_plants], ignore_index=True)
    else:
        new_fusion_capacity = 0

    summary.at[year, 'newFusionAdditions'] = new_fusion_capacity
    summary.at[year, 'totalEnergyAfterAdding'] = fleet_t['energy'].sum()

    return fleet_t, summary
