import pandas as pd
import numpy as np
import os

def simulatePlants(currentGen, start_year, end_year, percent_fusion, toReplace, afterYear, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT):
    # Placeholder for the actual simulation function
    # This function should return a DataFrame similar to what the R function would return
    # Simulated data for demonstration
    years = np.arange(start_year, end_year + 1)
    totalCarbon = np.random.rand(len(years))
    return pd.DataFrame({'year': years, 'totalCarbon': totalCarbon})

# Load necessary data (assuming these are saved in CSV or other accessible formats)
currentGen = pd.read_csv("data/currentGen.csv")  # Example placeholder
totalEnergy = pd.read_csv("data/totalEnergy.csv")
totalCapacity = pd.read_csv("data/totalCapacity.csv")

# Parameters
addCapDiffProp = 0.1
T_ADOPT = 10

# Run Simulations
marketPenetration = [
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.25, toReplace="All", afterYear=2030, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.75, toReplace="All", afterYear=2030, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.25, toReplace="All", afterYear=2050, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.75, toReplace="All", afterYear=2050, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.25, toReplace="All", afterYear=2070, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0.75, toReplace="All", afterYear=2070, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT),
    simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace="All", afterYear=2070, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT)
]

# Save Results
os.makedirs("out/data", exist_ok=True)
for i, df in enumerate(marketPenetration):
    df.to_csv(f"out/data/marketPenetration_{i}.csv", index=False)

# Averaging Out Many Runs
iter = 100
CA2030_10 = []
CA2030_50 = []
CA2030_99 = []

for i in range(iter):
    CA2030_10.append(simulatePlants(currentGen, 2014, 2100, percent_fusion=0.1, toReplace="All", afterYear=2030, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT))
    CA2030_50.append(simulatePlants(currentGen, 2014, 2100, percent_fusion=0.5, toReplace="All", afterYear=2030, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT))
    CA2030_99.append(simulatePlants(currentGen, 2014, 2100, percent_fusion=0.99, toReplace="All", afterYear=2030, addCapDiffProp=addCapDiffProp, totalEnergy=totalEnergy, totalCapacity=totalCapacity, T_ADOPT=T_ADOPT))

# Convert lists to 3D numpy arrays for further analysis (if needed)
CA2030_10_array = np.array([df.values for df in CA2030_10])
CA2030_50_array = np.array([df.values for df in CA2030_50])
CA2030_99_array = np.array([df.values for df in CA2030_99])

# Save averaged results (as an example, here we are just saving the first iteration)
CA2030_10[0].to_csv("out/data/CA2030_10.csv", index=False)
CA2030_50[0].to_csv("out/data/CA2030_50.csv", index=False)
CA2030_99[0].to_csv("out/data/CA2030_99.csv", index=False)

# Combine all scenarios into a single DataFrame for further analysis or visualization
total_df_list = []
for i, df in enumerate(marketPenetration):
    temp_df = pd.DataFrame({
        'year': df['year'],
        'case': i,
        'GHG': df['totalCarbon']
    })
    total_df_list.append(temp_df)

total_df = pd.concat(total_df_list, ignore_index=True)
total_df.to_csv("out/data/total_df.csv", index=False)
