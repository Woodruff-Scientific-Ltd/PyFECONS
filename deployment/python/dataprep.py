###############
#
# Dataprep.py
#
# Original Author: Lucas Spangher, ARPA-E
# Last updated: July 11th, 2017
# Ported by: Chris Raastad, ntTau Digital Ltd
# Ported: July 5th, 2024
# Purpose: to load in and tidy up all the necessary data

import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm
import geopandas as gpd

from utils import state_abbrev

# Path to the downloaded Natural Earth data
shapefile_path = "data/us_geo/us_counties.shp"

# change this directory as needed
# os.chdir("/Users/lucas.spangher/Documents/ARPA-E Files/PowerPlantModel")

print('Starting data prep')

print('1. Assemble and tidy a data frame of important characteristics for each type of plant')
### 1. Assemble and tidy a data frame of important characteristics for each type of plant
# -------------------

typeChars = pd.read_excel("data/generators_new.xlsx", sheet_name="CF_Operating_Retired_Data")

# tidy up the names
typeChars.columns = typeChars.columns.str.replace("[.]", "", regex=True)
typeChars.columns = typeChars.columns.str.replace("Average", "Avg")
typeChars.columns = typeChars.columns.str.replace("Retirement", "Ret")
typeChars.columns = typeChars.columns.str.replace("[(]", "", regex=True)
typeChars.columns = typeChars.columns.str.replace("[)]", "", regex=True)
typeChars.columns = typeChars.columns.str.replace("of", "")
typeChars.columns = typeChars.columns.str.replace(" ", "")

typeChars['RowLabels'] = typeChars['RowLabels'].str.replace(" ", "")
typeChars['RowLabels'] = typeChars['RowLabels'].str.replace("-", "")
typeChars.set_index('RowLabels', inplace=True)

# fill in any missing characteristics
typeChars['initialCarbonPerMW'] = np.nan  ## from IPCC
typeChars.loc["Coal", "initialCarbonPerMW"] = 9.6
typeChars.loc["Geothermal", "initialCarbonPerMW"] = 45
typeChars.loc["MunicipalSolidWaste", "initialCarbonPerMW"] = 1.6  ## assumption
typeChars.loc[["NGCC", "NGST", "NGCT"], "initialCarbonPerMW"] = 1.6
typeChars.loc["Nuclear", "initialCarbonPerMW"] = 18
typeChars.loc[["WoodOtherBiomass", "OtherGas"], "initialCarbonPerMW"] = 210  # assumption
typeChars.loc["Petroleum", "initialCarbonPerMW"] = 9.6  # same as coal... assumption
typeChars.loc["PV", "initialCarbonPerMW"] = 66
typeChars.loc["SolarThermal", "initialCarbonPerMW"] = 29
typeChars.loc["Wind", "initialCarbonPerMW"] = 15
typeChars.loc["Hydroelectric", "initialCarbonPerMW"] = 19
typeChars['initialCarbonPerMW'] = typeChars['initialCarbonPerMW'] * 8760 * 10 ** (
    -3) * 10 ** 3  # first year and in kg's and in MW
typeChars.loc["PV", "AvgRetAge"] = 20
typeChars.loc["PV", "StdDevAge"] = 5

# adding in characteristics for fusion --- most of these are simply translated from fission
fusionChars = typeChars.loc["Nuclear", :].copy()
fusionChars["CapFactor"] = 75
fusionChars["AvgCapacityMW"] = 500
fusionChars["StdDevCapacityMW"] = 150
fusionChars.name = "NuclearFusion"

# Use pd.concat instead of append
typeChars = pd.concat([typeChars, fusionChars.to_frame().T])

print('2. Load database of all retired plants.')
#### 2. Load database of all retired plants.
# Goal: this will be to calculate the skewed normal distribution of the
# age at which that power plant retired.

retiredGen = pd.read_excel("data/generators_new.xlsx", sheet_name="Retired and Canceled 2")
retiredGen.columns = retiredGen.columns.str.replace(" ", "").str.replace("[.]", "", regex=True)

retiredGen['Technology'] = retiredGen['Technology'].str.replace(" ", "")
retiredGen['Technology'] = retiredGen['Technology'].str.replace("-", "")

# Ensure RetirementAge is numeric
retiredGen['RetirementAge'] = pd.to_numeric(retiredGen['RetirementAge'], errors='coerce')

# Drop rows with NaN values in RetirementAge
retiredGen = retiredGen.dropna(subset=['RetirementAge'])

# Filter out RetirementAge values of 0
retiredGen = retiredGen[retiredGen['RetirementAge'] > 0]


# Function to fit skew normal distribution and handle errors
def fit_skewnorm(x):
    try:
        return skewnorm.fit(x)[0]
    except:
        return np.nan


# Apply the fitting function
typeChars['skewness'] = retiredGen.groupby('Technology')['RetirementAge'].apply(fit_skewnorm)

# set the skewness of fusion
typeChars.loc["NuclearFusion", "skewness"] = .3  # adapted from fission

# add in corrections for geothermal and MSW
typeChars.loc[["MunicipalSolidWaste", "Geothermal"], "BTUFuel/kWhelec"] = 10429
typeChars.loc[typeChars["BTUFuel/kWhelec"].isna(), "BTUFuel/kWhelec"] = 0

print('4. Load database of changing US capacity over time')
### 4. Load database of changing US capacity over time -------------
### Goal: This will be for predicting future capacity growth in the US
### This will then be broken up by type of plant.

addCap = pd.read_excel("data/AEOprojections.xlsx", sheet_name="Sheet3", header=None, index_col=0)

addCap.drop(columns=[27], inplace=True)
addCap.columns = range(2014, 2014 + addCap.shape[1])
addCap.index = addCap.index.str.replace(" ", "")
addCap = addCap.T
addCap.columns = addCap.columns.str.replace("[.]", "", regex=True)
addCap.columns = addCap.columns.str.replace("/", "")

### group plant types
ongs = ["NGST", "Petroleum"]
ctd = ["NGCT", "OtherGas"]
renewables = ["Geothermal", "Hydroelectric", "MunicipalSolidWaste", "PV",
              "SolarThermal", "Wind", "WoodOtherBiomass"]
ongsProps = typeChars.loc[ongs, "TotalCapacityMW"] / typeChars.loc[ongs, "TotalCapacityMW"].sum()
ctdProps = typeChars.loc[ctd, "TotalCapacityMW"] / typeChars.loc[ctd, "TotalCapacityMW"].sum()
renProps = np.array([.006, .06, .015, .188, .009, .798,
                     .06])  # comes from: typeChars[renewables, "TotalCapacityMW"]/sum(typeChars[renewables, "TotalCapacityMW"])
renProps /= renProps.sum()

# get the meta category capacity changes
addCap[ctd] = np.outer(addCap["CombustionTurbineDiesel"], ctdProps)
addCap[ongs] = np.outer(addCap["OilandNaturalGasSteam"], ongsProps)
addCap[renewables] = np.outer(addCap["RenewableSources"], renProps)

# label them appropriately
addCap.rename(columns={"CombinedCycle": "NGCC", "NuclearPower": "Nuclear"}, inplace=True)
addCap.drop(columns=["OilandNaturalGasSteam", "CombustionTurbineDiesel", "RenewableSources",
                     "PumpedStorage", "FuelCells", "DistributedGeneration", "Total"], inplace=True)
# could perform sanity check: row.names(typeChars)%in%names(addCap)==... TRUE!

# Take the difference capacities to get yearly capacity change
addCapDiff = addCap.diff().dropna()
addCapDiff["TotalTest"] = addCapDiff.sum(axis=1)  # this is to check that it all sums to 1
addCapDiffProp = addCapDiff.div(addCapDiff["TotalTest"], axis=0)
addCapDiffProp.columns = addCapDiffProp.columns.str.replace("X", "")
addCapDiffProp.loc[2014] = addCapDiffProp.loc[2015]
addCapDiffProp[addCapDiffProp < 0] = 0

# weighted capacity factors
addWeightedCF = addCapDiffProp.copy()
addWeightedCF.drop(columns=["TotalTest"], inplace=True)
CFs = typeChars.loc[addWeightedCF.columns, "CapFactor"]
CFs.fillna(0, inplace=True)

yearlyWeightedCF = addWeightedCF.to_numpy() @ CFs.to_numpy().reshape(-1, 1)

print('5. Tidy up and explore the database of current operating plants')
### 5. Tidy up and explore the database of current operating plants
### ------------------------------------------------------------

# Load the data
operable = pd.read_excel("data/generators_new.xlsx", sheet_name="Operable", skiprows=1)

# Clean the column names
operable.columns = operable.columns.str.replace(r"[.]", "", regex=True)
operable.columns = operable.columns.str.replace(r" ", "", regex=True)
operable.columns = operable.columns.str.replace(r"[(]", "", regex=True)
operable.columns = operable.columns.str.replace(r"[)]", "", regex=True)

# Proceed with further processing
currentGen = pd.DataFrame({
    'state': operable['State'],
    'county': operable['County'],
    'capacity': operable['SummerCapacityMW'],
    'startYear': operable['OperatingYear'],
    'type': operable['Technology'],
    'age': 2014 - operable['OperatingYear']
})

# Ensure there are no duplicates in the index
currentGen = currentGen.reset_index(drop=True)

# Exclude rows with specific type values
currentGen['type'] = currentGen['type'].str.replace(" ", "").str.replace("-", "")
currentGen = currentGen[~currentGen['type'].isin(['Batteries', 'Flywheels', 'HydroelectricPumpedStorage', 'AllOther'])]
currentGen.dropna(inplace=True)
currentGen['capacity'] = pd.to_numeric(currentGen['capacity'], errors='coerce')
currentGen.reset_index(drop=True, inplace=True)


# Ensure typeChars index has no duplicates
typeChars = typeChars[~typeChars.index.duplicated()]

# Perform the assignment operation
currentGen.loc[currentGen["capacity"].isna(), "capacity"] = currentGen.loc[currentGen["capacity"].isna(), "type"].map(
    typeChars["AvgCapacityMW"])
currentGen['energy'] = currentGen['capacity'] * currentGen['type'].map(typeChars["CapFactor"]) * 8760 / 10 ** 8
currentGen['carbonOutput'] = (currentGen['energy'] *
                              currentGen['type'].map(typeChars["BTUFuel/kWhelec"]) *
                              currentGen['type'].map(typeChars["kgCO2perMMBTU"]) *
                              10 ** -6 * 10 ** 9)

# Combine state and county to create location codes
currentGen['locCode'] = currentGen['state'].str.lower() + ',' + currentGen['county'].str.lower()

# Standardize naming for "st" to "st."
currentGen['locCode'] = currentGen['locCode'].str.replace('st ', 'st. ')

# Load map data for the USA
usaMap = gpd.read_file(shapefile_path)
usaMap['locCode'] = usaMap['STUSPS'].str.lower() + ',' + usaMap['NAME'].str.lower()

# Manual mapping for remaining mismatched locations
manual_mapping = {
    'la,desoto': 'la,de soto',
    'mo,st. louis city': 'mo,st. louis',
    'va,hopewell city': 'va,hopewell',
    'va,chesapeake city': 'va,chesapeake',
    'va,covington city': 'va,covington',
    'va,richmond city': 'va,richmond',
    'va,portsmouth city': 'va,portsmouth',
    'md,prince georges': 'md,prince george\'s',
    'ak,skagway hoonah angoon': 'ak,skagway',
    'ak,prince of wales ketchikan': 'ak,ketchikan gateway',
    'ak,matanuska susitna': 'ak,matanuska-susitna',
    'ak,valdez cordova': 'ak,chugach',
    'ak,wrangell petersburg': 'ak,wrangell',
    'va,lynchburg city': 'va,lynchburg',
    'va,suffolk city': 'va,suffolk',
    'il,dewitt': 'il,de witt',
    'va,hampton city': 'va,hampton',
    'va,virginia beach city': 'va,virginia beach',
    'va,alexandria city': 'va,alexandria',
    'md,baltimore city': 'md,baltimore',
    'fl,miami dade': 'fl,miami-dade',
    'nm,dona ana': 'nm,doña ana',
    'la,west. baton rouge': 'la,west baton rouge',
    'la,east. baton rouge': 'la,east baton rouge',
    'va,harrisonburg city': 'va,harrisonburg',
    'la,west. feliciana': 'la,west feliciana',
    'ak,southeast. fairbanks': 'ak,southeast fairbanks',
    'ak,northwest. arctic': 'ak,northwest arctic',
    'ak,wade hampton': 'ak,kusilvak',
    'ak,yukon koyukuk': 'ak,yukon-koyukuk',
    'va,manassas city': 'va,manassas',
    'va,salem city': 'va,salem',
    'md,queen annes': 'md,queen anne\'s',
    'mn,brookings': 'sd,brookings',
}

# Apply manual mapping
currentGen['locCode'] = currentGen['locCode'].replace(manual_mapping)

# Print mismatched location codes
mismatched_locs = currentGen.loc[~currentGen['locCode'].isin(usaMap['locCode']), 'locCode']
if len(mismatched_locs) > 0:
    print("Number of mismatched location codes after mapping:", len(mismatched_locs))
    print("Mismatched location codes after mapping:\n", mismatched_locs.head(20))

# Create a lookup table with unique location codes
usaMap2 = usaMap.drop_duplicates(subset='locCode').set_index('locCode')

# Set lat and long values
currentGen = currentGen.set_index('locCode')
currentGen = currentGen.join(usaMap2[['geometry']], how='left')
currentGen['long'] = currentGen['geometry'].apply(lambda geom: geom.centroid.x) + np.random.normal(0, .05,
                                                                                                   len(currentGen))
currentGen['lat'] = currentGen['geometry'].apply(lambda geom: geom.centroid.y) + np.random.normal(0, .05,
                                                                                                  len(currentGen))

# Clean up unnecessary columns
currentGen.drop(columns=['state', 'county', 'geometry'], inplace=True)

# Reset the index
currentGen = currentGen.reset_index(drop=True)


print('6. Use the skewed normal distributions of calculated ages to assign')
### 6. Use the skewed normal distributions of calculated ages to assign
###    expected retirement ages to operating plants
# -----------------------------------------

# Assign default values to missing data
default_avg_ret_age = 30
default_std_dev_ret_age = 10
default_skewness = 0

# Fill NaN values in typeChars
typeChars["AvgRetAge"] = typeChars["AvgRetAge"].fillna(default_avg_ret_age)
typeChars["StdDevRetAge"] = typeChars["StdDevRetAge"].fillna(default_std_dev_ret_age)
typeChars["skewness"] = typeChars["skewness"].fillna(default_skewness)

# Ensure that StdDevRetAge is positive and set a minimum value for the scale parameter
typeChars["StdDevRetAge"] = typeChars["StdDevRetAge"].apply(lambda x: x if x > 0 else 0.1)

# Remove rows in currentGen with NaN values for type
currentGen = currentGen.dropna(subset=['type'])

# Assign retirement age characteristics for specific plant types
typeChars.loc[["MunicipalSolidWaste", "Geothermal", "SolarThermal"], ["AvgRetAge", "StdDevRetAge", "skewness"]] = \
    typeChars.loc["Coal", ["AvgRetAge", "StdDevRetAge", "skewness"]]
typeChars.loc["NGCC", ["AvgRetAge", "StdDevRetAge", "skewness"]] = typeChars.loc[
    "NGST", ["AvgRetAge", "StdDevRetAge", "skewness"]]
typeChars.loc["WoodOtherBiomass", ["AvgRetAge", "StdDevRetAge", "skewness"]] = typeChars.loc[
    "Petroleum", ["AvgRetAge", "StdDevRetAge", "skewness"]]

# Map the retirement age characteristics to currentGen
currentGen['AvgRetAge'] = currentGen['type'].map(typeChars['AvgRetAge'])
currentGen['StdDevRetAge'] = currentGen['type'].map(typeChars['StdDevRetAge'])
currentGen['skewness'] = currentGen['type'].map(typeChars['skewness'])

# Remove rows with NaN values in critical columns after mapping
currentGen = currentGen.dropna(subset=['AvgRetAge', 'StdDevRetAge', 'skewness'])

# Generate the expRet column
try:
    currentGen["expRet"] = skewnorm.rvs(size=len(currentGen), a=currentGen["skewness"],
                                        loc=currentGen["AvgRetAge"],
                                        scale=currentGen["StdDevRetAge"])
except ValueError as e:
    print(f"Error in skewnorm.rvs: {e}")

# Remove temporary columns used for mapping
currentGen.drop(columns=['AvgRetAge', 'StdDevRetAge', 'skewness'], inplace=True)

for i in range(1, 126):
    toChange = currentGen["expRet"].isna() | (currentGen["expRet"] < currentGen["age"])
    currentGen.loc[toChange, "expRet"] = skewnorm.rvs(size=toChange.sum(),
                                                      a=typeChars.loc[currentGen.loc[toChange, "type"], "skewness"],
                                                      loc=typeChars.loc[currentGen.loc[toChange, "type"], "AvgRetAge"],
                                                      scale=typeChars.loc[
                                                          currentGen.loc[toChange, "type"], "StdDevRetAge"])

tempC = currentGen.loc[toChange, :]

if tempC["type"].eq("Nuclear").sum() > 0:
    currentGen.loc[tempC["type"].eq("Hydroelectric"), "expRet"] = 300

currentGen.loc[currentGen["type"].eq("Nuclear"), "expRet"] = np.random.binomial(1, 0.85, size=currentGen["type"].eq(
    "Nuclear").sum()) * 20 + 40

if tempC["type"].eq("OtherGas").sum() > 0:
    other_gas_indices = tempC[tempC["type"] == "OtherGas"].index
    currentGen.loc[other_gas_indices, "expRet"] = tempC.loc[other_gas_indices, "age"] + np.random.uniform(0, 10, size=other_gas_indices.size)

if tempC["type"].eq("Wind").sum() > 0:
    wind_indices = tempC[tempC["type"] == "Wind"].index
    currentGen.loc[wind_indices, "expRet"] = 50

if tempC["type"].eq("NGST").sum() > 0:
    ngst_indices = tempC[tempC["type"] == "NGST"].index
    currentGen.loc[ngst_indices, "expRet"] = 70

print('7. Capacity prediction for entire US')
### 7. Capacity prediction for entire US
### ------------------------------------

totalCapacity = pd.read_excel("data/AEOprojections.xlsx", sheet_name="Sheet2")
totalCapacity = pd.DataFrame({"year": range(2014, 2042), "capacity": totalCapacity.columns.astype(float)})
totalCapacity.loc[27, :] = np.nan
totalCapacity.dropna(inplace=True)

print('8. Energy supply prediction for the entire US')
### 8. Energy supply prediction for the entire US
### ------------------------------------

totalEnergy = pd.read_excel("data/generators_new.xlsx", sheet_name="Electricity_Demand")
totalEnergy.columns = ["year", "EnergyBillkWh"]

##########################

# Save all necessary data to the output directory
typeChars.index.name = "type"
typeChars.to_csv("out/sim_data.csv")
currentGen.to_csv("out/currentGen.csv", index=False)
totalEnergy.to_csv("out/totalEnergy.csv", index=False)
totalCapacity.to_csv("out/totalCapacity.csv", index=False)
