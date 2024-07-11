import os
import pandas as pd
import numpy as np
from simulate_fleet import simulatePlants
from utils import get_usa_maps

# Constants
START_YEAR = 2014
END_YEAR = 2100
OUT_DIR = "out/simulation"
os.makedirs(OUT_DIR, exist_ok=True)

# Load data
typeChars = pd.read_csv("out/sim_data.csv", index_col="type")
currentGen = pd.read_csv("out/currentGen.csv")
totalEnergy = pd.read_csv("out/totalEnergy.csv")
totalCapacity = pd.read_csv("out/totalCapacity.csv")
addCapDiffProp = pd.read_csv("out/addCapDiffProp.csv", index_col="year")
usaMap, usaMap2 = get_usa_maps()

# Helper function to run simulations and save results
def run_simulation(scenario_name, **kwargs):
    print(f'Running simulation {scenario_name}')
    results, summary = simulatePlants(
        currentGen,
        typeChars,
        start_year=START_YEAR,
        end_year=END_YEAR,
        addCapDiffProp=addCapDiffProp,
        totalEnergy=totalEnergy,
        totalCapacity=totalCapacity,
        **kwargs
    )
    results.to_csv(f"{OUT_DIR}/{scenario_name}.csv", index=False)
    summary.index.name = 'year'
    summary.to_csv(f"{OUT_DIR}/{scenario_name}_summary.csv", index=True)

# 1. Initial exploratory runs
run_simulation("percent_0", percent_fusion=0, toReplace=["NGCT"])
run_simulation("percent_05_2030", percent_fusion=0.05, toReplace="all", afterYear=2030)
run_simulation("percent_10", percent_fusion=0.1)
run_simulation("percent_50_WNPC_2030", percent_fusion=0.5, toReplace=["Wind","NGCC","PV","Coal"], afterYear=2030)
run_simulation("percent_50_2030", percent_fusion=0.5, toReplace="all", afterYear=2030)
run_simulation("percent_99_WNPC_2030", percent_fusion=0.999, toReplace=["Wind","NGCC","PV","Coal"], afterYear=2030)
run_simulation("percent_99_2030", percent_fusion=0.999, toReplace="all", afterYear=2030)

# 2. Slow and steady or procrastinator?
run_simulation("percent_10_2025", percent_fusion=0.1, toReplace="all", afterYear=2025)
run_simulation("percent_15_2025", percent_fusion=0.15, toReplace="all", afterYear=2025)
run_simulation("percent_20_2025", percent_fusion=0.2, toReplace="all", afterYear=2025)
run_simulation("percent_25_2025", percent_fusion=0.25, toReplace="all", afterYear=2025)
run_simulation("percent_50_2040", percent_fusion=0.5, toReplace="all", afterYear=2040)
run_simulation("percent_50_2050", percent_fusion=0.5, toReplace="all", afterYear=2050)
run_simulation("percent_55_2050", percent_fusion=0.55, toReplace="all", afterYear=2050)
run_simulation("percent_60_2050", percent_fusion=0.6, toReplace="all", afterYear=2050)
run_simulation("percent_65_2050", percent_fusion=0.65, toReplace="all", afterYear=2050)
run_simulation("percent_90_2075", percent_fusion=0.9, toReplace="all", afterYear=2075)
run_simulation("percent_92_2075", percent_fusion=0.92, toReplace="all", afterYear=2075)
run_simulation("percent_94_2075", percent_fusion=0.94, toReplace="all", afterYear=2075)
run_simulation("percent_96_2075", percent_fusion=0.96, toReplace="all", afterYear=2075)

# 3. Different percent of sales, keep everything else the same
run_simulation("percent_10_2030", percent_fusion=0.1, toReplace="all", afterYear=2030)
run_simulation("percent_25_2030", percent_fusion=0.25, toReplace="all", afterYear=2030)
run_simulation("percent_25_2020", percent_fusion=0.25, toReplace="all", afterYear=2020)
run_simulation("percent_50_2030", percent_fusion=0.5, toReplace="all", afterYear=2030)
run_simulation("percent_99_2030", percent_fusion=0.99, toReplace="all", afterYear=2030)

# 4. What if fusion only replaces renewable energy?
renewable_types = ["Geothermal", "PV", "SolarThermal", "Wind", "WoodOtherBiomass", "Nuclear"]
run_simulation("percent_05_ren", percent_fusion=0.05, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_10_ren", percent_fusion=0.1, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_17_ren", percent_fusion=0.17, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_25_ren", percent_fusion=0.25, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_37_ren", percent_fusion=0.37, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_42_ren", percent_fusion=0.42, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_47_ren", percent_fusion=0.47, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_50_ren", percent_fusion=0.5, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_75_ren", percent_fusion=0.75, toReplace=renewable_types, afterYear=2030)
run_simulation("percent_99_ren", percent_fusion=0.99, toReplace=renewable_types, afterYear=2030)

# 4a. Limited to PV and Wind
sub_renewable_types = ["PV", "Wind"]
run_simulation("percent_05_ren_sub", percent_fusion=0.05, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_10_ren_sub", percent_fusion=0.1, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_17_ren_sub", percent_fusion=0.17, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_25_ren_sub", percent_fusion=0.25, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_37_ren_sub", percent_fusion=0.37, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_42_ren_sub", percent_fusion=0.42, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_47_ren_sub", percent_fusion=0.47, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_50_ren_sub", percent_fusion=0.5, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_75_ren_sub", percent_fusion=0.75, toReplace=sub_renewable_types, afterYear=2030)
run_simulation("percent_99_ren_sub", percent_fusion=0.99, toReplace=sub_renewable_types, afterYear=2030)

# 5. Different years of entry, hold the percent the same
run_simulation("percent_25_2030", percent_fusion=0.25, toReplace="all", afterYear=2030)
run_simulation("percent_25_2035", percent_fusion=0.25, toReplace="all", afterYear=2035)
run_simulation("percent_25_2040", percent_fusion=0.25, toReplace="all", afterYear=2040)
run_simulation("percent_25_2045", percent_fusion=0.25, toReplace="all", afterYear=2045)
run_simulation("percent_25_2050", percent_fusion=0.25, toReplace="all", afterYear=2050)
run_simulation("percent_25_2055", percent_fusion=0.25, toReplace="all", afterYear=2055)

# 6. Different market penetrations, year 2030
run_simulation("percent_00_2030", percent_fusion=0.0000000001, toReplace="all", afterYear=2030)
run_simulation("percent_10_2030", percent_fusion=0.1, toReplace="all", afterYear=2030)
run_simulation("percent_50_2030", percent_fusion=0.5, toReplace="all", afterYear=2030)
run_simulation("percent_99_2030", percent_fusion=0.99, toReplace="all", afterYear=2030)

# 6a. Different market penetrations, year 2050
run_simulation("percent_10_2050", percent_fusion=0.1, toReplace="all", afterYear=2050)
run_simulation("percent_50_2050", percent_fusion=0.5, toReplace="all", afterYear=2050)
run_simulation("percent_10_2070", percent_fusion=0.1, toReplace="all", afterYear=2070)
run_simulation("percent_50_2070", percent_fusion=0.5, toReplace="all", afterYear=2070)

# 7. Differing amounts of CCS
run_simulation("percent_00_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0, afterYearCCS=2020)
run_simulation("percent_05_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.05, afterYearCCS=2020)
run_simulation("percent_10_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.1, afterYearCCS=2020)
run_simulation("percent_25_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.25, afterYearCCS=2020)
run_simulation("percent_50_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.5, afterYearCCS=2020)
run_simulation("percent_75_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.75, afterYearCCS=2020)
run_simulation("percent_99_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=0.99, afterYearCCS=2020)
run_simulation("percent_100_CCS", percent_fusion=0, toReplace="all", afterYear=2030, percent_CCS=1, afterYearCCS=2020)

# 8. Vary runs by different lengths of S-curves
for T_ADOPT in range(5, 61, 5):
    run_simulation(f"SC_{T_ADOPT}", percent_fusion=0.9, toReplace="all", afterYear=2030, T_ADOPT=T_ADOPT)
run_simulation("SC_0.0001", percent_fusion=0.9, toReplace="all", afterYear=2030, T_ADOPT=0.0001)

# 9. Limited case of market penetration
for percent_fusion in [0.25, 0.75]:
    for afterYear in [2030, 2050, 2070]:
        run_simulation(f"marketPenetration_{percent_fusion}_{afterYear}", percent_fusion=percent_fusion, toReplace="all", afterYear=afterYear, T_ADOPT=10)
run_simulation("marketPenetration_BAU", percent_fusion=0, toReplace="all", afterYear=2070, T_ADOPT=10)

# 10. Average out many runs
def average_runs(prefix, percent_fusion, afterYear, T_ADOPT, num_runs=100):
    all_runs = []
    for i in range(num_runs):
        results, _ = simulatePlants(
            currentGen,
            typeChars,
            start_year=START_YEAR,
            end_year=END_YEAR,
            addCapDiffProp=addCapDiffProp,
            totalEnergy=totalEnergy,
            totalCapacity=totalCapacity,
            toReplace="all",
            afterYear=afterYear,
            percent_fusion=percent_fusion,
            T_ADOPT=T_ADOPT,
        )
        results["element"] = i
        all_runs.append(results)

    combined_df = pd.concat(all_runs)
    mean_df = combined_df.groupby("year").mean().reset_index()
    mean_df.to_csv(f"{OUT_DIR}/{prefix}_mean.csv", index=False)

average_runs("CA2030_10", 0.1, 2030, 10)
average_runs("CA2030_50", 0.5, 2030, 10)
average_runs("CA2030_99", 0.99, 2030, 10)
average_runs("CA2050_10", 0.1, 2050, 10)
average_runs("CA2050_50", 0.5, 2050, 10)
average_runs("CA2070_10", 0.1, 2070, 10)
average_runs("CA2070_50", 0.5, 2070, 10)


# Sensitivity analysis
def sensitivity_analysis(prefix, percent_fusion, afterYear, num_runs=50):
    all_runs = []
    for i in range(num_runs):
        results, _ = simulatePlants(
            currentGen,
            typeChars,
            start_year=START_YEAR,
            end_year=END_YEAR,
            addCapDiffProp=addCapDiffProp,
            totalEnergy=totalEnergy,
            totalCapacity=totalCapacity,
            toReplace="all",
            afterYear=afterYear,
            percent_fusion=percent_fusion,
        )
        results["element"] = i
        all_runs.append(results)

    combined_df = pd.concat(all_runs)
    combined_df.to_csv(f"{OUT_DIR}/{prefix}.csv", index=False)

sensitivity_analysis("p50_2030", 0.5, 2030)
sensitivity_analysis("pBAU", 0, 2030, num_runs=25)
sensitivity_analysis("p10_2030", 0.1, 2030, num_runs=25)
sensitivity_analysis("p99_2030", 0.99, 2030, num_runs=25)

# 11. Vary year and market penetration for inclusion in multiple probabilities
run_simulation("BAU", percent_fusion=0.0000000001, toReplace="all", afterYear=2030)
run_simulation("percent_10_10a", percent_fusion=0.1, toReplace="all", afterYear=2030, T_ADOPT=10)
run_simulation("percent_50_10a", percent_fusion=0.5, toReplace="all", afterYear=2030, T_ADOPT=10)
run_simulation("percent_99_10a", percent_fusion=0.99, toReplace="all", afterYear=2030, T_ADOPT=10)
run_simulation("percent_10_20a", percent_fusion=0.1, toReplace="all", afterYear=2030, T_ADOPT=20)
run_simulation("percent_50_20a", percent_fusion=0.5, toReplace="all", afterYear=2030, T_ADOPT=20)
run_simulation("percent_99_20a", percent_fusion=0.99, toReplace="all", afterYear=2030, T_ADOPT=20)
run_simulation("percent_10_30a", percent_fusion=0.1, toReplace="all", afterYear=2030, T_ADOPT=30)
run_simulation("percent_50_30a", percent_fusion=0.5, toReplace="all", afterYear=2030, T_ADOPT=30)
run_simulation("percent_99_30a", percent_fusion=0.99, toReplace="all", afterYear=2030, T_ADOPT=30)


# Hackathon: Double specific resource categories
def double_resource(df, category):
    temp_df = df.copy()
    var_to_double = temp_df[category] * 2
    doubled_var = np.minimum(1, var_to_double)
    temp_df[category] = doubled_var
    other_columns = temp_df.columns.difference([category])
    temp_df[other_columns] = temp_df[other_columns] * (1 - doubled_var[:, None])
    temp_df = temp_df.div(temp_df.sum(axis=1), axis=0)
    return temp_df


categories = ["Wind", "PV", "Nuclear", "Coal"]
resource_cases = ["1000", "0100", "0010", "0001", "1100", "1010", "1001", "0110", "0101", "0011", "1110", "1101", "1011", "0111", "1111"]

for cat in categories:
    case_name = f"case_{cat.lower()}"
    df = double_resource(addCapDiffProp, cat)
    run_simulation(case_name, percent_fusion=0.0000000001, toReplace="all", afterYear=2030, addCapDiffProp=df)

# Save total_df
total_df_list = []
for i, case in enumerate(resource_cases):
    case_name = f"case_{case}"
    df = pd.read_csv(f"{OUT_DIR}/{case_name}.csv")
    df["case"] = i
    df = df[["year", "case", "totalCarbon"]]
    df.rename(columns={"totalCarbon": "GHG"}, inplace=True)
    total_df_list.append(df)

total_df = pd.concat(total_df_list)
total_df.to_csv(f"{OUT_DIR}/total_df.csv", index=False)
