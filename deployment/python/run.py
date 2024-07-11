import os

import pandas as pd
from simulate_fleet import simulatePlants

# Load the necessary data
typeChars = pd.read_csv("out/sim_data.csv", index_col='type')
currentGen = pd.read_csv("out/currentGen.csv")
totalEnergy = pd.read_csv("out/totalEnergy.csv")
totalCapacity = pd.read_csv("out/totalCapacity.csv")
addCapDiffProp = pd.read_csv("out/addCapDiffProp.csv", index_col=0)

# Set simulation parameters
out_dir = "out/run"
os.makedirs(out_dir, exist_ok=True)
results_file = os.path.join(out_dir, "simulation_results.csv")
summary_file = os.path.join(out_dir, "simulation_summary.csv")
START_YEAR = 2014
END_YEAR = 2050
PERCENT_FUSION = 0.25
AFTER_YEAR = 2030
T_ADOPT = 10

# Run the simulation
results, summary = simulatePlants(
    initial_fleet=currentGen,
    typeChars=typeChars,
    start_year=START_YEAR,
    end_year=END_YEAR,
    percent_fusion=PERCENT_FUSION,
    addCapDiffProp=addCapDiffProp,
    totalEnergy=totalEnergy,
    totalCapacity=totalCapacity,
    toReplace="all",
    afterYear=AFTER_YEAR,
    percent_CCS=0,
    T_ADOPT=T_ADOPT,
)

results.to_csv(results_file, index=False)
summary.index.name = 'year'
summary.to_csv(summary_file, index=True)
