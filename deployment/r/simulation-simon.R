######## Poisson process model ########## 
# .libPaths("\\\\doe/dfsfr/HOME_FORS3/Lucas.Spangher/My Documents/R/R-3.3.0/library")
# setwd("~/fusion_analysis_code/Code_R_Files")
require(ggplot2) 
require(Kmisc)
require(bayesm)
require(arm)
require(reshape)
require(nlme)
require(fGarch)

load("out/sim.rData")

source("utils.r")
source("simulateFleet.r")

### 1. PREDICTING energy demand -------------------------------------------------- 
# AEO does this... loaded into "totalEnergy" 

### 2. PREDICTING new proportions ------------------------------------------------
# did this, loaded into addCapDiffProp 

### 3. capacity adjustment/calculation -------------------------------------------
# to be done later 

### 4. PREPARING SIMULATION ------------------------------------------------------

# sampling retirement ages in currentGen
# setting the values of MSW and 

### 5. SIMULATION

START_YEAR=2014
END_YEAR=2050

percent_0 = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace = "NGCT", addCapDiffProp, totalEnergy, totalCapacity)
percent_05_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.05, toReplace="all", afterYear=2030,addCapDiffProp, totalEnergy, totalCapacity)
percent_10 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, addCapDiffProp, totalEnergy, totalCapacity)

percent_50_WNPC_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("Wind","NGCC","PV","Coal"), afterYear=2030, 
	addCapDiffProp, totalEnergy, totalCapacity)

percent_50_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("all"), afterYear=2030, 
	addCapDiffProp, totalEnergy, totalCapacity)
percent_99_WNPC_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.999, afterYear=2030, toReplace=c("Wind","NGCC","PV","Coal"),
	addCapDiffProp, totalEnergy, totalCapacity)
percent_99_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.999, toReplace = c("all"),
	afterYear=2030,addCapDiffProp, totalEnergy, totalCapacity)

### 3. Slow and steady (early) or procrastinator? 

percent_10_2025 = simulatePlants(currentGen, 2014, 2030, percent_fusion=.1, toReplace=c("all"), afterYear=2025, addCapDiffProp, totalEnergy, totalCapacity)
percent_15_2025 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.15, toReplace=c("all"), afterYear=2025, addCapDiffProp, totalEnergy, totalCapacity)
percent_20_2025 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.2, toReplace=c("all"), afterYear=2025, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2025 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("all"), afterYear=2025, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_2040 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("all"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("all"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_55_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.55, toReplace=c("all"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_60_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.6, toReplace=c("all"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_65_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.65, toReplace=c("all"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_90_2075 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("all"), afterYear=2075, addCapDiffProp, totalEnergy, totalCapacity)
percent_92_2075 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.92, toReplace=c("all"), afterYear=2075, addCapDiffProp, totalEnergy, totalCapacity)
percent_94_2075 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.94, toReplace=c("all"), afterYear=2075, addCapDiffProp, totalEnergy, totalCapacity)
percent_96_2075 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.98, toReplace=c("all"), afterYear=2075, addCapDiffProp, totalEnergy, totalCapacity)

#### 3a. different percent of sales 


percent_10 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2020 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("all"), afterYear=2020, addCapDiffProp, totalEnergy, totalCapacity)
percent_50 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)


### 4. Depressing case to avoid 
res = c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear")

percent_05_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.05, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_10_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_17_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.17, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_37_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.37, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_42_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.42, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_47_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.47, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_75_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)

##### 4a. what's going on 


percent_37_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.37, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_38_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.38, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_39_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.39, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_40_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.4, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_41_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.41, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_42_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.42, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2014, addCapDiffProp, totalEnergy, totalCapacity)
percent_45_ren = simulatePlants(currentGen, 2014, 2100, percent_fusion=.45, toReplace=c("Geothermal", "PV","SolarThermal","Wind","WoodOtherBiomass","Nuclear"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)

# What if you do this with all? 


percent_05_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.05, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_10_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_17_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.125, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_37_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.37, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_42_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.42, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_47_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.47, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_75_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99_ren_sub= simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("PV","Wind"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)



#### 5. Different years of entry 

percent_25_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2035 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2035, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2040 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2040, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2045 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2045, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2055 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2055, addCapDiffProp, totalEnergy, totalCapacity)

#### 6. Different market penetrations  

percent_00_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_05_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.05, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_10_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2033, addCapDiffProp, totalEnergy, totalCapacity)
# percent_22_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.22, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_25_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_28_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.28, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_75_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99_2040 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2040, addCapDiffProp, totalEnergy, totalCapacity)



percent_10_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
# percent_22_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.22, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_25_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_28_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.28, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_10_2070 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2070, addCapDiffProp, totalEnergy, totalCapacity)
# percent_22_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.22, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_25_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
# percent_28_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.28, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_50_2070 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2070, addCapDiffProp, totalEnergy, totalCapacity)

write.csv(percent_00_2030, "BAU.csv")
write.csv(percent_10_2030, "percent_10_2030.csv")
write.csv(percent_50_2030, "percent_50_2030.csv")
write.csv(percent_99_2030, "percent_99_2030.csv")
write.csv(percent_99_2040, "percent_99_2040.csv")
write.csv(percent_10_2050, "percent_10_2050.csv")
write.csv(percent_50_2050, "percent_50_2050.csv")
write.csv(percent_10_2070, "percent_10_2070.csv")
write.csv(percent_50_2070, "percent_50_2070.csv")

#### 6. Differing amounts of CCS 

percent_00_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=00, afterYearCCS=2020)
percent_05_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.05, afterYearCCS=2020)
percent_10_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.1, afterYearCCS=2020)
percent_25_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.25, afterYearCCS=2020)
percent_50_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.5, afterYearCCS=2020)
percent_75_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.75, afterYearCCS=2020)
percent_99_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=.99, afterYearCCS=2020)
percent_100_CCS = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=1, afterYearCCS=2020)

### BAU 

BAU = simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, percent_CCS=00, afterYearCCS=2020)

### 27 different scenarios

contourPlot = list()

contourPlot[[1]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[2]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[3]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[4]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[5]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[6]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[7]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[8]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[9]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
contourPlot[[10]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[11]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[12]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[13]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[14]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[15]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[16]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[17]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[18]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
contourPlot[[19]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[20]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[21]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[22]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[23]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[24]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[25]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[26]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
contourPlot[[27]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)



ceils = c(.1,.3,.5,.7,.9)
ys= c(2030,2040,2050,2060,2070)
num = length(ceils)*length(ys)
CP.df = data.frame(ceils=rep(NA,num), ys = rep(NA,num), yearSurpassed= rep(NA,num))

k=1
for(i in c(1:length(ceils))){
	for(j in c(1:length(ys))){
		CP.df$ceils[k] = ceils[j]
		CP.df$ys[k] = ys[i]
		carbon  = cumsum(contourPlot[[k]]$totalCarbon)
		CP.df$yearSurpassed[k] = which(carbon>65)[1]
		k=k+1 
	}
}


write.csv(CP.df, "contourData.csv")

### S_curves 

SC = list()

SC[[1]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 5)
SC[[2]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
SC[[3]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 15)
SC[[4]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
SC[[5]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 25)
SC[[6]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
SC[[7]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 35)
SC[[8]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 40)
SC[[9]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 45)
SC[[10]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 50)
SC[[11]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 55)
SC[[12]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 60)
SC[[13]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 60)
SC[[14]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.9, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 0.0001)

# market penetation 

marketPenetration=list()

marketPenetration[[1]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[2]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[3]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[4]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[5]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[6]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[7]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)


# Annual fusion capacity additions 

CA2030_10 = list()
CA2030_50 = list()
CA2030_99 = list()
CA2050_10 = list()
CA2050_50 = list()
CA2070_10 = list()
CA2070_50 = list()


iter = 100 

# 2030 

for (i in c(1:iter)){
#	CA2030_10[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
#	CA2030_50[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
	CA2030_99[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
}

elements = expand.grid(c(1:nrow(CA2030_10[[1]])), c(1:iter))$Var2
CA2030_10_array = do.call(rbind, CA2030_10)
CA2030_50_array = do.call(rbind, CA2030_50)
CA2030_99_array = do.call(rbind, CA2030_99)
CA2030_10_array$element = elements
CA2030_50_array$element = elements
CA2030_99_array$element = elements
CA2030_10_3D = array(unlist(CA2030_10), c(dim(CA2030_10[[1]]), length(CA2030_10)))
CA2030_50_3D = array(unlist(CA2030_50), c(dim(CA2030_50[[1]]), length(CA2030_50)))
CA2030_99_3D = array(unlist(CA2030_99), c(dim(CA2030_99[[1]]), length(CA2030_99)))
CA2030_10_mean = data.frame(apply(CA2030_10_3D, 1:2, mean))
CA2030_50_mean = data.frame(apply(CA2030_50_3D, 1:2, mean))
CA2030_99_mean = data.frame(apply(CA2030_99_3D, 1:2, mean))
names(CA2030_10_mean)=names(CA2030_10_array)[!names(CA2030_10_array) %in% c("element")]
names(CA2030_50_mean)=names(CA2030_50_array)[!names(CA2030_50_array) %in% c("element")]
names(CA2030_99_mean)=names(CA2030_99_array)[!names(CA2030_99_array) %in% c("element")]

write.csv(CA2030_99_mean, "2030_99_mean.csv")

# 2050

for (i in c(1:iter)){
	CA2050_10[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
	CA2050_50[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
}

elements = expand.grid(c(1:nrow(CA2050_10[[1]])), c(1:iter))$Var2
CA2050_10_array = do.call(rbind, CA2050_10)
CA2050_50_array = do.call(rbind, CA2050_50)
CA2050_10_array$element = elements
CA2050_50_array$element = elements
CA2050_10_3D = array(unlist(CA2050_10), c(dim(CA2050_10[[1]]), length(CA2050_10)))
CA2050_50_3D = array(unlist(CA2050_50), c(dim(CA2050_50[[1]]), length(CA2050_50)))
CA2050_10_mean = data.frame(apply(CA2050_10_3D, 1:2, mean))
CA2050_50_mean = data.frame(apply(CA2050_50_3D, 1:2, mean))
names(CA2050_10_mean)=names(CA2050_10_array)[!names(CA2050_10_array) %in% c("element")]
names(CA2050_50_mean)=names(CA2050_50_array)[!names(CA2050_50_array) %in% c("element")]

# 2070

for (i in c(1:iter)){
	CA2070_10[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
	CA2070_50[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
}

elements = expand.grid(c(1:nrow(CA2070_10[[1]])), c(1:iter))$Var2
CA2070_10_array = do.call(rbind, CA2070_10)
CA2070_50_array = do.call(rbind, CA2070_50)
CA2070_10_array$element = elements
CA2070_50_array$element = elements
CA2070_10_3D = array(unlist(CA2070_10), c(dim(CA2070_10[[1]]), length(CA2070_10)))
CA2070_50_3D = array(unlist(CA2070_50), c(dim(CA2070_50[[1]]), length(CA2070_50)))
CA2070_10_mean = data.frame(apply(CA2070_10_3D, 1:2, mean))
CA2070_50_mean = data.frame(apply(CA2070_50_3D, 1:2, mean))
names(CA2070_10_mean)=names(CA2070_10_array)[!names(CA2070_10_array) %in% c("element")]
names(CA2070_50_mean)=names(CA2070_50_array)[!names(CA2070_50_array) %in% c("element")]


# writing csvs 

write.csv(CA2030_10_mean, "2030_10_mean.csv")
write.csv(CA2030_50_mean, "2030_50_mean.csv")
write.csv(CA2030_99_mean, "2030_99_mean.csv")
write.csv(CA2050_10_mean, "2050_10_mean.csv")
write.csv(CA2050_50_mean, "2050_50_mean.csv")
write.csv(CA2070_10_mean, "2070_10_mean.csv")
write.csv(CA2070_50_mean, "2070_50_mean.csv")



#### sensitivity analysis 


# 50%
p50_2030=list()
p50_2030df= NULL
for(i in c(1:50)){
	p50_2030[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
	p50_2030[[i]]$element=i
	p50_2030df = rbind(p50_2030df, p50_2030[[i]])
}


p50_2030_array = do.call(rbind, p50_2030)
p50_2030_3D = array(unlist(p50_2030), c(dim(p50_2030[[1]]), length(p50_2030)))
p50_2030_mean = data.frame(apply(p50_2030_3D, 1:2, mean))
names(p50_2030_mean)=names(p50_2030_array)

## BAU
pBAU=list()
pBAUdf= NULL
for(i in c(1:25)){
	pBAU[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
	pBAU[[i]]$element=i
	pBAUdf = rbind(pBAUdf, pBAU[[i]])
}

pBAU_array = do.call(rbind, pBAU)
pBAU_3D = array(unlist(pBAU), c(dim(pBAU[[1]]), length(pBAU)))
pBAU_mean = data.frame(apply(pBAU_3D, 1:2, mean))
names(pBAU_mean)=names(pBAU_array)


## 10% 
p10_2030=list()
p10_2030df= NULL
for(i in c(1:25)){
	p10_2030[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
	p10_2030[[i]]$element=i
	p10_2030df = rbind(p10_2030df, p10_2030[[i]])
}

p10_2030_array = do.call(rbind, p10_2030)
p10_2030_3D = array(unlist(p10_2030), c(dim(p10_2030[[1]]), length(p10_2030)))
p10_2030_mean = data.frame(apply(p10_2030_3D, 1:2, mean))
names(p10_2030_mean)=names(p10_2030_array)

## 99%
p99_2030=list()
p99_2030df= NULL
for(i in c(1:25)){
	p99_2030[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
	p99_2030[[i]]$element=i
	p99_2030df = rbind(p99_2030df, p99_2030[[i]])
}

p99_2030_array = do.call(rbind, p99_2030)
p99_2030_3D = array(unlist(p99_2030), c(dim(p99_2030[[1]]), length(p99_2030)))
p99_2030_mean = data.frame(apply(p99_2030_3D, 1:2, mean))
names(p99_2030_mean)=names(p99_2030_array)



save.image("out/results.rdata")
save.image("out/sim.rdata")


##### capacity graph 

iter =20
sales = c(0:iter)/iter

marketPen2100 = numeric()

for (i in c(1:length(sales))){
	CG= simulatePlants(currentGen, 2014, 2100, percent_fusion=sales[i], toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
	stats2100 =CG[CG$years==2100,]
	marketPen2100[i] = stats2100$fusionGrowth/(stats2100$totalCapacityAfterRetirement*1000)
}



### probabilities 


BAU = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_10_10a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
percent_50_10a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
percent_99_10a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT =10)
percent_10_20a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
percent_50_20a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
percent_99_20a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20)
percent_10_30a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
percent_50_30a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)
percent_99_30a = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30)

write.csv(BAU, "BAU.csv")
write.csv(percent_10_10a, "percent_10_10a.csv")
write.csv(percent_50_10a, "percent_50_10a.csv")
write.csv(percent_99_10a, "percent_99_10a.csv")
write.csv(percent_10_20a, "percent_10_20a.csv")
write.csv(percent_50_20a, "percent_50_20a.csv")
write.csv(percent_99_20a, "percent_99_20a.csv")
write.csv(percent_10_30a, "percent_10_30a.csv")
write.csv(percent_50_30a, "percent_50_30a.csv")
write.csv(percent_99_30a, "percent_99_30a.csv")



