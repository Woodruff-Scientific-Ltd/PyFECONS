
#########################
#
#   Simulation.r 
#
#   Author: Lucas Spangher 
#   Last Updated: July 11, 2017
#   Purpose: to run simulateFleet.r in a variety of exploratory scenarios
#        Not all of these scenaios will be included in the final paper 
# 

require(ggplot2)
require(Kmisc)
require(bayesm)
require(arm)
require(reshape)
require(nlme)
require(fGarch)

load("out/sim.rData")
source("utils.r")

START_YEAR=2014
END_YEAR=2100

source("simulateFleet.R")

### 1. initial exploratory runs 

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

### 2. Slow and steady (start early and have low penetration) or procrastinator (start late with high penetration)? 

percent_10_2025 = simulatePlants(currentGen, 2014, 2050, percent_fusion=.1, toReplace=c("all"), afterYear=2025, addCapDiffProp, totalEnergy, totalCapacity)
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

#### 3. different percent of sales, keep everything else the same

percent_10 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2020 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("all"), afterYear=2020, addCapDiffProp, totalEnergy, totalCapacity)
percent_50 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_99 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("all"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)


### 4. What if fusion only replaces renewable energy? 

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

# 4a. Does the effect still hold if only PV and Wind are selected? 

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

#### 5. Different years of entry, hold the percent the same

percent_25_2030 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2035 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2035, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2040 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2040, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2045 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2045, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2050 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2050, addCapDiffProp, totalEnergy, totalCapacity)
percent_25_2055 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear=2055, addCapDiffProp, totalEnergy, totalCapacity)

#### 6. Different market penetrations, year 2030 

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



### 6a. Different market penetrations, year 2050

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

write.csv(percent_00_2030, "out/data/BAU.csv")
write.csv(percent_10_2030, "out/data/percent_10_2030.csv")
write.csv(percent_50_2030, "out/data/percent_50_2030.csv")
write.csv(percent_99_2030, "out/data/percent_99_2030.csv")
write.csv(percent_99_2040, "out/data/percent_99_2040.csv")
write.csv(percent_10_2050, "out/data/percent_10_2050.csv")
write.csv(percent_50_2050, "out/data/percent_50_2050.csv")
write.csv(percent_10_2070, "out/data/percent_10_2070.csv")
write.csv(percent_50_2070, "out/data/percent_50_2070.csv")

#### 7. Differing amounts of CCS 

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

### 7. Try to construct contour plot: 
### generate 27 different scenarios, varrying year of entry and percent 

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

### try to construct contour plot -- unsuccessful 

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


write.csv(CP.df, "out/data/contourData.csv")

### 8. Vary runs by different lengths of S_curves 

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

# 9. Limited case of market penetation 

marketPenetration=list()

marketPenetration[[1]] = simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[2]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[3]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[4]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2050, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[5]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.25, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[6]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.75, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
marketPenetration[[7]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=0, toReplace=c("All"), afterYear = 2070, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)


# 9. Average out many runs 

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
CA2030_10[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
CA2030_50[[i]]= simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear = 2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10)
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

write.csv(CA2030_99_mean, "out/data/2030_99_mean.csv")

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

write.csv(CA2030_10_mean, "out/data/2030_10_mean.csv")
write.csv(CA2030_50_mean, "out/data/2030_50_mean.csv")
write.csv(CA2030_99_mean, "out/data/2030_99_mean.csv")
write.csv(CA2050_10_mean, "out/data/2050_10_mean.csv")
write.csv(CA2050_50_mean, "out/data/2050_50_mean.csv")
write.csv(CA2070_10_mean, "out/data/2070_10_mean.csv")
write.csv(CA2070_50_mean, "out/data/2070_50_mean.csv")



#### 9. sensitivity analysis (repeat what happened above with different combinations)


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



### 10. Vary year and market penetration for inclusion in multiple probabilities (to be published in a second, later paper)


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

write.csv(BAU, "out/data/BAU.csv")
write.csv(percent_10_10a, "out/data/percent_10_10a.csv")
write.csv(percent_50_10a, "out/data/percent_50_10a.csv")
write.csv(percent_99_10a, "out/data/percent_99_10a.csv")
write.csv(percent_10_20a, "out/data/percent_10_20a.csv")
write.csv(percent_50_20a, "out/data/percent_50_20a.csv")
write.csv(percent_99_20a, "out/data/percent_99_20a.csv")
write.csv(percent_10_30a, "out/data/percent_10_30a.csv")
write.csv(percent_50_30a, "out/data/percent_50_30a.csv")
write.csv(percent_99_30a, "out/data/percent_99_30a.csv")

#### 11. Use the EV as input

# TODO - need to locate this file
# EV_TWh = read.csv("/Users/lucas.spangher/Documents/ARPA-E Files/VMT_ChrisAtkinson/electricityDemandDF_TWh.csv")
#
# EV_TWh = EV_TWh[EV_TWh$year%in% c(START_YEAR:END_YEAR),]
#
# BAU = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario="fast.low")
# percent_10_10a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "fast.low")
# percent_50_10a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 10, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "fast.medium")
# percent_99_10a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT =10, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "fast.high")
# percent_10_20a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "medium.low")
# percent_50_20a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "medium.medium")
# percent_99_20a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 20, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "medium.high")
# percent_10_30a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.1, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "slow.low")
# percent_50_30a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.5, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "slow.medium")
# percent_99_30a_wEV = simulatePlants(currentGen, 2014, 2100, percent_fusion=.99, toReplace=c("All"), afterYear=2030, addCapDiffProp, totalEnergy, totalCapacity, T_ADOPT = 30, EV_Switch = TRUE, EV_addition = EV_TWh, EV_scenario = "slow.high")
#
# write.csv(BAU, "out/data/BAU.csv")
# write.csv(percent_10_10a_wEV, "out/data/percent_10_10a_wEV.csv")
# write.csv(percent_50_10a_wEV, "out/data/percent_50_10a_wEV.csv")
# write.csv(percent_99_10a_wEV, "out/data/percent_99_10a_wEV.csv")
# write.csv(percent_10_20a_wEV, "out/data/percent_10_20a_wEV.csv")
# write.csv(percent_50_20a_wEV, "out/data/percent_50_20a_wEV.csv")
# write.csv(percent_99_20a_wEV, "out/data/percent_99_20a_wEV.csv")
# write.csv(percent_10_30a_wEV, "out/data/percent_10_30a_wEV.csv")
# write.csv(percent_50_30a_wEV, "out/data/percent_50_30a_wEV.csv")
# write.csv(percent_99_30a_wEV, "out/data/percent_99_30a_wEV.csv")
#
# carbonIntensityDF = data.frame(years = START_YEAR:END_YEAR,
# 	low.slow = percent_10_30a_wEV$carbonIntensity,
# 	medium.slow=percent_50_30a_wEV$carbonIntensity,
# 	high.slow = percent_99_30a_wEV$carbonIntensity,
# 	low.medium = percent_10_20a_wEV$carbonIntensity,
# 	medium.medium = percent_50_20a_wEV$carbonIntensity,
# 	high.medium = percent_99_20a_wEV$carbonIntensity,
# 	low.fast = percent_10_10a_wEV$carbonIntensity,
# 	medium.fast = percent_50_10a_wEV$carbonIntensity,
# 	high.fast = percent_99_10a_wEV$carbonIntensity
# 	)
#
# write.csv(carbonIntensityDF, "carbonIntensityDF.csv")




##### Hackathon 

# Wind
# PV
# Nuclear
# WoodBiomass
# 

double_resource = function(df = addCapDiffProp, category = "Wind"){
		var_to_exclude = names(df)%in%category
		temp_df = df[!var_to_exclude]
		var_to_double = df[, category]
		doubled_var=pmin(1,var_to_double*2)

		temp_df = temp_df*(1-doubled_var)
		doubled_var=data.frame(a= doubled_var)
		names(doubled_var)=c(category)
		df= cbind(temp_df, doubled_var)
		df = df/rowSums(df)
		return(df)
}


### matrix construction 

# 1 
BAU = BAU
df_1000 = double_resource(addCapDiffProp, "Wind")
df_0100 = double_resource(addCapDiffProp, "PV")
df_0010 = double_resource(addCapDiffProp, "Nuclear")
df_0001 = double_resource(addCapDiffProp, "Coal")

#2 
#wind
df_1100 = double_resource(df_1000, "PV")
df_1010 = double_resource(df_1000, "Nuclear")
df_1001 = double_resource(df_1000, "Coal")
#solar
df_0110 = double_resource(df_0100, "Nuclear")
df_0101 = double_resource(df_0100, "Coal")
#Nuclear
df_0011 = double_resource(df_0010, "Coal")

#3
df_1110 = double_resource(df_1100, "Nuclear")
df_1101 = double_resource(df_1100, "Coal")
df_1011 = double_resource(df_1010, "Coal")
df_0111 = double_resource(df_0011, "PV")

#4
df_1111 = double_resource(df_1110, "Coal")


#simulations

case_1000 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1000, totalEnergy, totalCapacity)
case_0100 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0100, totalEnergy, totalCapacity)
case_0010 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0010, totalEnergy, totalCapacity)
case_0001 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0001, totalEnergy, totalCapacity)
case_1100 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1100, totalEnergy, totalCapacity)
case_1010 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1010, totalEnergy, totalCapacity)
case_1001 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1001, totalEnergy, totalCapacity)
case_0110 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0110, totalEnergy, totalCapacity)
case_0101 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0101, totalEnergy, totalCapacity)
case_0011 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0011, totalEnergy, totalCapacity)
case_1110 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1110, totalEnergy, totalCapacity)
case_1101 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1101, totalEnergy, totalCapacity)
case_1011 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1011, totalEnergy, totalCapacity)
case_0111 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_0111, totalEnergy, totalCapacity)
case_1111 = simulatePlants(currentGen, 2014, 2100, percent_fusion=.0000000001, toReplace=c("All"), afterYear=2030, 
	df_1111, totalEnergy, totalCapacity)

write.csv(percent_0, "out/data/case_0000.csv")
write.csv(case_1000, "out/data/case_1000.csv")
write.csv(case_0100, "out/data/case_0100.csv")
write.csv(case_0010, "out/data/case_0010.csv")
write.csv(case_0001, "out/data/case_0001.csv")
write.csv(case_1100, "out/data/case_1100.csv")
write.csv(case_1010, "out/data/case_1010.csv")
write.csv(case_1001, "out/data/case_1001.csv")
write.csv(case_0110, "out/data/case_0110.csv")
write.csv(case_0011, "out/data/case_0011.csv")
write.csv(case_0101, "out/data/case_0101.csv")
write.csv(case_1110, "out/data/case_1110.csv")
write.csv(case_1101, "out/data/case_1101.csv")
write.csv(case_1011, "out/data/case_1011.csv")
write.csv(case_0111, "out/data/case_0111.csv")
write.csv(case_1111, "out/data/case_1111.csv")

temp_df_0000 = data.frame(year = percent_0$year,
	case = 0, GHG = percent_0$totalCarbon)
temp_df_0001 = data.frame(year = case_0001$year,
	case = 1, GHG = case_0001$totalCarbon)
temp_df_0010 = data.frame(year = case_0010$year,
	case = 2, GHG = case_0010$totalCarbon)
temp_df_0011 = data.frame(year = case_0011$year,
	case = 3, GHG = case_0011$totalCarbon)
temp_df_0100 = data.frame(year = case_0100$year,
	case = 4, GHG = case_0100$totalCarbon)
temp_df_0101 = data.frame(year = case_0101$year,
	case = 5, GHG = case_0101$totalCarbon)
temp_df_0110 = data.frame(year = case_0110$year,
	case = 6, GHG = case_0110$totalCarbon)
temp_df_0111 = data.frame(year = case_0111$year,
	case = 7, GHG = case_0111$totalCarbon)
temp_df_1000 = data.frame(year = case_1000$year,
	case = 8, GHG = case_1000$totalCarbon)
temp_df_1001 = data.frame(year = case_1001$year,
	case = 9, GHG = case_1001$totalCarbon)
temp_df_1010 = data.frame(year = case_1010$year,
	case = 10, GHG = case_1010$totalCarbon)
temp_df_1011 = data.frame(year = case_1011$year,
	case = 11, GHG = case_1011$totalCarbon)
temp_df_1100 = data.frame(year = case_1100$year,
	case = 12, GHG = case_1100$totalCarbon)
temp_df_1101 = data.frame(year = case_1101$year,
	case = 13, GHG = case_1101$totalCarbon)
temp_df_1110 = data.frame(year = case_1110$year,
	case = 14, GHG = case_1110$totalCarbon)
temp_df_1111 = data.frame(year = case_1111$year,
	case = 15, GHG = case_1111$totalCarbon)


total_df= rbind(temp_df_0000,
	temp_df_0001,
	temp_df_0010,
	temp_df_0011,
	temp_df_0100,
	temp_df_0101,
	temp_df_0110,
	temp_df_0111,
	temp_df_1000,
	temp_df_1001,
	temp_df_1010,
	temp_df_1011,
	temp_df_1100,
	temp_df_1101,
	temp_df_1110,
	temp_df_1111)

write.csv(total_df, "out/data/total_df.csv")



























