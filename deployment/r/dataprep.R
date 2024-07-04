############### 
#
# Dataprep.r 
# 
# Author: Lucas Spangher, ARPA-E  
# Last updated: July 11th, 2017
# Purpose: to load in and tidy up all the necessary data 

require(fGarch)
require(openxlsx)
require(maps)
require(ggplot2)

# change this directory as needed 
# setwd("/Users/lucas.spangher/Documents/ARPA-E Files/PowerPlantModel")

### 1. Assemble and tidy a data frame of important characteristics for each type of plant 
# -------------------

typeChars = read.xlsx("data/generators_new.xlsx", sheet = "CF_Operating_Retired_Data")

# tidy up the names 
names(typeChars)= gsub("[.]","", names(typeChars))
names(typeChars)= gsub("Average","Avg", names(typeChars))
names(typeChars)= gsub("Retirement","Ret", names(typeChars))
names(typeChars)= gsub("[(]","", names(typeChars))
names(typeChars)= gsub("[)]","", names(typeChars))
names(typeChars)= gsub("of","", names(typeChars))
typeChars$RowLabels = gsub(" ","",typeChars$RowLabels)
typeChars$RowLabels = gsub("-","",typeChars$RowLabels)
row.names(typeChars)=typeChars$RowLabels

# fill in any missing characteristics 

typeChars$initialCarbonPerMW = NA ## from IPCC
typeChars["Coal", "initialCarbonPerMW"] = 9.6
typeChars["Geothermal", "initialCarbonPerMW"] = 45
typeChars["MunicipalSolidWaste", "initialCarbonPerMW"] = 1.6 ## assumption
typeChars[c("NGCC","NGST","NGCT"), "initialCarbonPerMW"] = 1.6
typeChars["Nuclear", "initialCarbonPerMW"] = 18
typeChars[c("WoodOtherBiomass","OtherGas"), "initialCarbonPerMW"] = 210 # assumption 
typeChars["Petroleum", "initialCarbonPerMW"] = 9.6 # same as coal... assumption
typeChars["PV", "initialCarbonPerMW"] = 66
typeChars["SolarThermal", "initialCarbonPerMW"] = 29
typeChars["Wind", "initialCarbonPerMW"] = 15
typeChars["Hydroelectric","initialCarbonPerMW"]=19
typeChars$initialCarbonPerMW= typeChars$initialCarbonPerMW*8760*10^(-3)*10^3 # first year and in kg's and in MW
typeChars["PV","AvgRetAge"]=20
typeChars["PV","StdDevAge"]=5


# adding in characteristics for fusion --- most of these are simply translated from fission

fusionChars=typeChars["Nuclear",]
fusionChars["CapFactor"]=75
fusionChars["AvgCapacityMW"]=500
fusionChars["StdDevCapacityMW"]=150
fusionChars["RowLabels"]="NuclearFusion"
row.names(fusionChars)="NuclearFusion"
typeChars=rbind(typeChars,fusionChars)

#### 2. Load database of all retired plants.
# Goal: this will be to calculate the skewed normal distribution of the 
# age at which that power plant retired.  

retiredGen = read.xlsx("data/generators_new.xlsx", sheet="Retired and Canceled 2")
retiredGen$Technology=gsub(" ","", retiredGen$Technology)
retiredGen$Technology=gsub("-","", retiredGen$Technology)
typeChars$skewness = tapply(retiredGen$Retirement.Age,retiredGen$Technology,function(x) return(snormFit(x)$par["xi"]))[row.names(typeChars)]

# set the skewness of fusion
typeChars["NuclearFusion","skewness"]=.3 # adapted from fission

# add in corrections for geothermal and MSW 
typeChars[c("MunicipalSolidWaste","Geothermal"),"BTUFuel/kWhelec"]=10429
typeChars[is.na(typeChars$"BTUFuel/kWhelec"),"BTUFuel/kWhelec"]=0

### 4. Load database of changing US capacity over time -------------
### Goal: This will be for predicting future capacity growth in the US 
### This will then be broken up by type of plant.

addCap = read.xlsx("data/AEOprojections.xlsx", sheet="Sheet3", rowNames=TRUE, colNames = FALSE)
addCap$X29=NULL
names(addCap) = c(2014:2040)
row.names(addCap) = gsub(" ","",row.names(addCap))
addCap=data.frame(t(addCap))
names(addCap)=gsub("[.]","",names(addCap))

### group plant types 
ongs=c("NGST","Petroleum")
ctd=c("NGCT","OtherGas")
renewables=c("Geothermal", "Hydroelectric", "MunicipalSolidWaste", "PV", 
	"SolarThermal", "Wind", "WoodOtherBiomass")
ongsProps = typeChars[ongs,"TotalCapacityMW"]/sum(typeChars[ongs,"TotalCapacityMW"])
ctdProps = typeChars[ctd,"TotalCapacityMW"]/sum(typeChars[ctd,"TotalCapacityMW"])
renProps =  c(.006, .06, .015,.188, .009, .798, .06)  # comes from: typeChars[renewables, "TotalCapacityMW"]/sum(typeChars[renewables, "TotalCapacityMW"])
renProps=renProps/sum(renProps)

# get the meta category capacity changes
addCap[,ctd]= addCap$CombustionTurbineDiesel%*%t(ctdProps)
addCap[,ongs]= addCap$OilandNaturalGasSteam%*%t(ongsProps)
addCap[,renewables]= addCap$RenewableSources%*%t(renProps)

# label them appropriately 
names(addCap)[names(addCap)%in%c("CombinedCycle","NuclearPower")]=c("NGCC","Nuclear") 
addCap[,c("OilandNaturalGasSteam","CombustionTurbineDiesel","RenewableSources",
	"PumpedStorage","FuelCells","DistributedGeneration","Total")]=NULL
# could perform sanity check: row.names(typeChars)%in%names(addCap)==... TRUE! 


# Take the difference capacities to get yearly capacity change 
addCapDiff = data.frame(apply(addCap,2,diff))
addCapDiff$TotalTest= rowSums(addCapDiff) # this is to check that it all sums to 1 
addCapDiffProp= data.frame(apply(addCapDiff,1,function(row){
	row/row["TotalTest"]
	}))
names(addCapDiffProp)=gsub("X","",names(addCapDiffProp))
addCapDiffProp$"2014" = addCapDiffProp$"2015"
addCapDiffProp=data.frame(t(addCapDiffProp))
addCapDiffProp[addCapDiffProp<0]=0

# weighted capacity factors 
addWeightedCF = addCapDiffProp
addWeightedCF$TotalTest=NULL
CFs=typeChars[names(addWeightedCF), "CapFactor"]
CFs[is.na(CFs)]=0

yearlyWeightedCF=as.matrix(addWeightedCF)%*%t(t(CFs))

### 5. Tidy up and explore the database of current operating plants
### ------------------------------------------------------------

current.gen = read.xlsx("data/generators_new.xlsx", sheet= "Operable", startRow = 2)

currentGen=data.frame(state= current.gen$State, 
	county = current.gen$County,
	capacity= current.gen$"Summer.Capacity.(MW)",
	startYear = current.gen$Operating.Year,
	type = current.gen$Technology,
	age = 2014-current.gen$Operating.Year)

currentGen[currentGen$type%in%c("Batteries", "Flywheels", "Hydroelectric Pumped Storage","AllOther"),] = NA
currentGen=na.omit(currentGen)
currentGen$type = gsub(" ","",currentGen$type)
currentGen$type = gsub("-","",currentGen$type)
currentGen[currentGen$type=="AllOther",]=NA
currentGen=na.omit(currentGen)
currentGen$capacity=as.numeric(as.character(currentGen$capacity))
currentGen$capacity[is.na(currentGen$capacity)]=typeChars[currentGen$type[is.na(currentGen$capacity)],"AvgCapacityMW"]
currentGen$energy=currentGen$capacity*typeChars[as.character(currentGen$type),"CapFactor"]*8760/10^8
currentGen$carbonOutput = currentGen$energy*typeChars[as.character(currentGen$type),"BTUFuel/kWhelec"]*
								typeChars[as.character(currentGen$type),"kgCO2perMMBTU"]*10^-6*10^9

currentGen$StateName = tolower(state.name[match(currentGen$state,state.abb)]) 
currentGen$locCode = paste(tolower(currentGen$StateName),",",tolower(currentGen$county), sep="")

usaMap=map_data("county")
usaMap$locCode=paste(usaMap$region,",",usaMap$subregion,sep="")

usaMap2 = usaMap[!duplicated(usaMap$locCode),]
row.names(usaMap2)=usaMap2$locCode
currentGen$long = usaMap2[currentGen$locCode,"long"]+rnorm(nrow(currentGen),0,.05)
currentGen$lat = usaMap2[currentGen$locCode,"lat"]+rnorm(nrow(currentGen),0,.05)

currentGen$state=NULL
currentGen$county=NULL
currentGen$StateName=NULL


### 6. Use the skewed normal distributions of calculated ages to assign
###    expected retirement ages to operating plants
# ----------------------------------------- 


typeChars[c("MunicipalSolidWaste","Geothermal","SolarThermal"),c("AvgRetAge",
		"StdDevRetAge", "skewness")]=typeChars["Coal",c("AvgRetAge","StdDevRetAge", "skewness")]
typeChars["NGCC",c("AvgRetAge","StdDevRetAge", "skewness")]=typeChars["NGST",c("AvgRetAge","StdDevRetAge", "skewness")]
typeChars["WoodOtherBiomass",c("AvgRetAge","StdDevRetAge", "skewness")]=typeChars["Petroleum",c("AvgRetAge","StdDevRetAge", "skewness")]

currentGen$expRet = rsnorm(nrow(currentGen), 
		mean = typeChars[currentGen$type,"AvgRetAge"],
        sd = typeChars[currentGen$type,"StdDevRetAge"],
        xi = typeChars[currentGen$type,"skewness"])

for(i in c(1:125)){
	toChange = is.na(currentGen$expRet) | 
		currentGen$expRet<currentGen$age 
	print(sum(toChange, na.rm=TRUE))
	currentGen$expRet[toChange] = rsnorm(sum(toChange), 
		mean= typeChars[currentGen$type[toChange],"AvgRetAge"],
		sd = typeChars[currentGen$type[toChange],"StdDevRetAge"],
        xi = typeChars[currentGen$type[toChange],"skewness"])
}
tempC= currentGen[toChange,]

tempC[tempC$type=="Nuclear",]

if(sum(tempC$type=="Hydroelectric")>0){
	currentGen[row.names(tempC[tempC$type=="Hydroelectric",]), "expRet"]=300
}

currentGen[currentGen$type=="Nuclear", "expRet"]=rbinom(nrow(currentGen[currentGen$type=="Nuclear",]),1,.85)*20+40

if(sum(tempC$type=="OtherGas")>0){
	currentGen[row.names(tempC[tempC$type=="OtherGas",]), "expRet"]=tempC[tempC$type=="OtherGas","age"]+
		runif(sum(tempC$type=="OtherGas"),0,10)
}
if(sum(tempC$type=="Wind")>0){
	currentGen[row.names(tempC[tempC$type=="Wind",]), "expRet"]=50
}
if(sum(tempC$type=="NGST")>0){currentGen[row.names(tempC[tempC$type=="NGST",]), "expRet"]=70}


### 7. Capacity prediction for entire US
### ------------------------------------

totalCapacity = read.xlsx("data/AEOprojections.xlsx", sheet = "Sheet2")
totalCapacity=data.frame(year = c(2014:2041),capacity= as.numeric(names(totalCapacity)))
totalCapacity[28,]=NA
totalCapacity=na.omit(totalCapacity)

### 8. Energy supply prediction for the entire US 
### ------------------------------------

totalEnergy = read.xlsx("data/generators_new.xlsx", sheet="Electricity_Demand")
names(totalEnergy) = c("year","EnergyBillkWh")

##########################

save.image("out/sim.rData")

