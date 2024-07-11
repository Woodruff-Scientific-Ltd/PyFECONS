#############################
#
#   simulateFleet.r
#
#   Author: Lucas Spangher 
#   Last updated: July 11, 2017
#   Purpose: This is the main "workhorse" function of the model.
#       When run, this function will simulate the set of powerplant agents, 
#       using the sepcific scenario inputs that are listed as iput arguments to the 
#       function call. See simulation.r for use cases of this function 


simulatePlants = function(
    fleet0, # initial fleet (currentGen)
    START_YEAR=2014, 
    END_YEAR=2050,
    percent_fusion=0, # k, what the maximum percent fusion allowed is
    addCapDiffProp, # a matrix containing the differences of proportion of capacity growth per plant per year; see dataprep.r for its creation 
    totalEnergy, # a data.frame of energy per year from 2011-2040 from AEO. See dataprep.r for its creation 
    totalCapacity, # a data.frame of capacity per year from 2011-2040 from AEO. See dataprep.r for its creation 
    toReplace="all", # a char vector which energy technologies fusion will replace 
    afterYear = 2015, # when fusion is introduced
    percent_CCS = 0, # CCS component --> (future study)
    afterYearCCS=2020, # CCS component --> (future study)
    T_ADOPT=10, # width of s curve; amount of time between .05k and .95k 
    EV_Switch = FALSE, # Switch to turn on using EV 
    EV_addition = 0, # addition of EV to add electricity demand 
    EV_scenario = "BAU" # which column to use in EV scenario
    ){

source("utils.r")
       
        newYears = c(START_YEAR:END_YEAR)

        # initialize an output dataframe for which to store yearly summary variables 
        newDF=data.frame(years=newYears, 
            totalCapacityAfterRetirement=c(NA),  # numeric var explaining total fleet capacity each year after plants retire 
            totalEnergyAfterRetirement=c(NA), # numeric var explaining total fleet energy each year after plants retire 
            dearth_t_cap=c(NA), # numeric var summarizing the yearly dearth in capacity (i.e. the total required capacity - existing capacity after retirement)
            dearth_t_energy=c(NA), # numeric var summarizing the yearly dearth in energy (i.e. the total required energy - existing energy after retirement)
            NGCCGrowth=c(NA), # numeric var, sum of NGCC capacity in given year
            WindGrowth=c(NA), # numeric var, sum of wind capacity in given year
            NuclearGrowth=c(NA), # numeric var, sum of nuclear fission capacity in given year
            PetroleumGrowth=c(NA), # numeric var, sum of petroleum capacity in given year
            NGSTGrowth=c(NA), # numeric var, sum of NGST capacity in given year
            NGCTGrowth=c(NA), # numeric var, sum of NGCT capacity in given year
            PVGrowth=c(NA), # numeric var, sum of PV capacity in given year
            HydroGrowth=c(NA), # numeric var, sum of Hydro capacity in given year
            CoalGrowth=c(NA), # numeric var, sum of coal capacity in given year
            fusionGrowth=c(NA), # numeric var, sum of fusion capacity in given year
            NGCCDearth=c(NA), # numeric var, sum of NGCC capacity retiring in given year
            WindDearth=c(NA),  # numeric var, sum of Wind capacity retiring in given year
            NuclearDearth=c(NA), # numeric var, sum of Nuclear fission capacity retiring in given year
            PetroleumDearth=c(NA), # numeric var, sum of Petroleum capacity retiring in given year
            NGSTDearth=c(NA), # numeric var, sum of NGST capacity retiring in given year
            NGCTDearth=c(NA), # numeric var, sum of NGCT capacity retiring in given year
            PVDearth=c(NA), # numeric var, sum of PV capacity retiring in given year
            HydroDearth=c(NA), # numeric var, sum of Hydro capacity retiring in given year
            CoalDearth=c(NA), # numeric var, sum of Coal capacity retiring in given year
            fusionDearth=c(NA), # numeric var, sum of Nuclear fusion capacity retiring in given year
            totalEnergyAfterAdding=c(NA), # numeric var, sum of fleetwide energy after new plants are added
            carbonIntensity=c(NA), # average carbon intensity of the fleet
            totalCarbon=c(NA), # total carbon emitted in a given year
            newCap=c(NA), # new capacity added in a given year
            newFusionAdditions=c(NA), # new fusion capacity added in a given year 
            totalPlants=c(NA), # count of the total plants in the fleet in a given year
            demandGrowth=c(NA), # amount of new capacity added in a given year through growth of the capacity demand
            replacementRetirements=c(NA)) # amount of new capacity added in a given year through retirements 


        # checking to make sure percent_fusion is a decimal 0<percent_fusion<1, not 0<percent_fusion<100    
        if(percent_fusion>1) percent_fusion=percent_fusion*.01
  
        #### 1.  extend datasets beyond their ending year (2040) 
        # ------------------------------------

        # totalEnergy
        enerMod = lm(EnergyBillkWh~year, data= totalEnergy)
        newYears= c(2041:END_YEAR)
        newEner = data.frame(year=newYears, EnergyBillkWh=predict(enerMod, data.frame(year=newYears)))
        newEner$EnergyBillkWh=newEner$EnergyBillkWh+2*(totalEnergy[totalEnergy$year==2040,"EnergyBillkWh"]-newEner[newEner$year==2041,"EnergyBillkWh"])
        totalEnergy=rbind(totalEnergy,newEner)

        if(EV_Switch){
            EV_toAdd  = EV_addition[,EV_scenario]
            totalEnergy$EnergyBillkWh = totalEnergy$EnergyBillkWh + EV_toAdd
        }

        # totalCapacity
        capMod = lm(capacity~year, data= totalCapacity)
        newYears= c(2041:END_YEAR)
        newCap = data.frame(year=newYears, capacity=predict(capMod, data.frame(year=newYears)))
        totalCapacity=rbind(totalCapacity,newCap)

        # addCapDiffProp
        newACDP=addCapDiffProp["2040",]
        for (i in c(2041:END_YEAR)){
            newACDP[as.character(i),] = colMeans(addCapDiffProp[c("2038","2039","2040"),]) 
        }
        addCapDiffProp=rbind(addCapDiffProp, newACDP)
        addCapDiffProp = addCapDiffProp[rownames(addCapDiffProp)%in%c(2014:END_YEAR), ]
        addWeightedCF = addCapDiffProp

        #### 2. Set up the fusion variable and adding it into the addCapDiffProp
        # --------------------------------
        #  
        # setting up the s-curve fusion growth 
        afterYearInd = afterYear-START_YEAR
        percent_fusion = s_curve(T_ADOPT=T_ADOPT, k= percent_fusion, t=(c(1:(nrow(addCapDiffProp))-(afterYearInd)))) #rnorm(nrow(addCapDiffProp),percent_fusion,.01)

        percent_fusion[is.na(percent_fusion)] = percent_fusion[1]
        percent_fusion[percent_fusion<0] = percent_fusion[1]
        percent_fusion = c(rep(0, afterYearInd-1), percent_fusion[(afterYearInd):nrow(addCapDiffProp)])
        names(percent_fusion) = row.names(addCapDiffProp)

        # adding in fusion to addCapDiffProp by taking away from the categories that it is supposed to replace 
        if (sum(c("All","all")%in%toReplace)>0){    
            addCapDiffProp=addCapDiffProp*(1-percent_fusion)
        } else { 
            tempInds = names(addCapDiffProp)%in%toReplace
            if (length(toReplace)==1){ 
                tempSum= addCapDiffProp[,tempInds]
            } else {
                tempSum = rowSums(addCapDiffProp[,tempInds])
            }
            percent_fusion[tempSum<percent_fusion]=tempSum[tempSum<percent_fusion]
            tempMultiple = 1-percent_fusion/tempSum
            addCapDiffProp[names(tempMultiple),tempInds] = addCapDiffProp[names(tempMultiple),tempInds]*tempMultiple
        }

        addCapDiffProp$NuclearFusion=percent_fusion
        addCapDiffProp$TotalTest=NULL # this is to test that it all rows add to 1 

        addWeightedCF$TotalTest=NULL

        ### 3. Miscellaneous preparation ------------

        # tidying up some names
        CFs=typeChars[names(addWeightedCF), "CapFactor"]
        CFs[is.na(CFs)]=0

        # variable for weighted Carbon factor. Numeric vector. 
        yearlyWeightedCF=as.matrix(addWeightedCF)%*%t(t(CFs))

        # first output generation 
        newDF$demandGrowth = pmax(0, c(0, diff(totalCapacity$capacity)))

        # fleet0 is the initial fleet but is later updated in the for-loop      
        fleet_t = fleet0
        fleet_t$seqNum = c(1:nrow(fleet_t))
        fleet_t$isNew = FALSE

        # initialize graph (for making a map movie -- not included in the paper)
        p= ggplot(data=usaMap, aes(x=long,y=lat))+geom_polygon(aes(group=group))


        ### 4. Main backbone/for-loop of the simulation ------------------------------------
        # This for loop runs once per year. Its main purpose is to age all the plants
        # each year, retiring those that are aging out, and then simulating new
        # plants to replace the capacity dearth that arises from the retired plants and the 
        # overall demand/capacity growth. It also simulates new plants

        print("starting simulation")
        for(i in c(1:nrow(newDF))){
            lastPlant = fleet_t$seqNum[nrow(fleet_t)]

            ### a. age the plants and calculate energy -------------------------
            fleet_t$age = fleet_t$age+1 
            fleet_t$energy = capacityMWToEnergyTWh(fleet_t, typeChars)
            fleet_t$carbonOutput =energyTWhToCarbonOutputKG(fleet_t, typeChars, ifelse(newDF$year[i]>afterYearCCS, percent_CCS, 0))
            fleet_t$isFusion=fleet_t$type=="NuclearFusion"
         
            # b. pick which plants to retire -----------------------------------
            retiringPlants = fleet_t[fleet_t$age>fleet_t$expRet,] 

            # (record summaries in the output df called newDF)
            newDF$NGCCDearth[i]=sum(retiringPlants[retiringPlants$type=="NGCC","capacity"])
            newDF$WindDearth[i]=sum(retiringPlants[retiringPlants$type=="Wind","capacity"])
            newDF$NuclearDearth[i]=sum(retiringPlants[retiringPlants$type=="Nuclear","capacity"])
            newDF$PetroleumDearth[i]=sum(retiringPlants[retiringPlants$type=="Petroleum","capacity"])
            newDF$NGSTDearth[i]=sum(retiringPlants[retiringPlants$type=="NGST","capacity"])
            newDF$NGCTDearth[i]=sum(retiringPlants[retiringPlants$type=="NGCT","capacity"])
            newDF$PVDearth[i]=sum(retiringPlants[retiringPlants$type=="PV","capacity"])
            newDF$HydroDearth[i]=sum(retiringPlants[retiringPlants$type=="Hydroelectric","capacity"])
            newDF$CoalDearth[i]=sum(retiringPlants[retiringPlants$type=="Coal","capacity"])
            newDF$fusionDearth[i]=sum(retiringPlants[retiringPlants$type=="NuclearFusion","capacity"])
            if (i%%10==0){
                print(paste(newDF$years[i], ": ", nrow(retiringPlants), " plants retired"))
            }
            newDF$replacementRetirements[i] = sum(retiringPlants$capacity)
            fleet_t1 = fleet_t[!fleet_t$seqNum%in%retiringPlants$seqNum,]

            # c. Calculate dearth ------------------------------------------

            currentEnergy = sum(fleet_t1$energy) 
            energy_t = totalEnergy[totalEnergy$year==newDF$years[i],"EnergyBillkWh"]
            dearth_t_energy = energy_t-currentEnergy
            dearth_t_cap =(dearth_t_energy/(yearlyWeightedCF[as.character(newDF$years[i]),1]*10^-2*8760))*10^6 #### check this 
            currentCap = sum(fleet_t1$capacity)/10^3           
            
            # (record summaries in newDF)

            newDF$dearth_t_cap[i]=dearth_t_cap
            newDF$dearth_t_energy[i]=dearth_t_energy
            newDF$totalCapacityAfterRetirement[i]=currentCap
            newDF$totalEnergyAfterRetirement[i]=currentEnergy
            newDF$NGCCGrowth[i] = sum(fleet_t1[fleet_t1$type=="NGCC", "capacity"])
            newDF$WindGrowth[i] = sum(fleet_t1[fleet_t1$type=="Wind", "capacity"])
            newDF$NuclearGrowth[i] = sum(fleet_t1[fleet_t1$type=="Nuclear", "capacity"])
            newDF$PetroleumGrowth[i] = sum(fleet_t1[fleet_t1$type=="Petroleum", "capacity"])
            newDF$NGSTGrowth[i] = sum(fleet_t1[fleet_t1$type=="NGST", "capacity"])
            newDF$PVGrowth[i] = sum(fleet_t1[fleet_t1$type=="PV", "capacity"])
            newDF$HydroGrowth[i] = sum(fleet_t1[fleet_t1$type=="Hydroelectric", "capacity"])
            newDF$CoalGrowth[i] = sum(fleet_t1[fleet_t1$type=="Coal", "capacity"])
            newDF$NGCTGrowth[i] = sum(fleet_t1[fleet_t1$type=="NGCT", "capacity"])
            newDF$fusionGrowth[i] = sum(fleet_t1[fleet_t1$type=="NuclearFusion", "capacity"])
            newDF$carbonIntensity[i] = sum(fleet_t$carbonOutput)/(sum(fleet_t$energy)*10^9) # 10^9 to make this kg/kWh
            newDF$totalCarbon[i]= sum(kgToGTons(fleet_t$carbonOutput))
            newDF$newCap[i] = sum(fleet_t1$capacity[fleet_t1$isNew])/10^3
            newDF$totalPlants[i] = nrow(fleet_t)


            # d. Generate new plants based to meet the dearth proportional to AEO's additions 

            dearth_types = dearth_t_cap*addCapDiffProp[as.character(newDF$years[i]),] # TODO          
            num_plants_types = round(dearth_types/typeChars[names(dearth_types),"AvgCapacityMW"])
            num_plants_types[is.na(num_plants_types)|num_plants_types<0]=0
            
            newDF$plantsAdded[i]= sum(num_plants_types)
            newPlants=data.frame()

               if (sum(num_plants_types)>0){
                   newPlants = data.frame(type=rep(names(num_plants_types), as.numeric(num_plants_types)))
                   newPlants$capacity=pmax(rnorm(nrow(newPlants), 
                        mean = typeChars[as.character(newPlants$type),"AvgCapacityMW"],
                        sd = typeChars[as.character(newPlants$type), "StdDevCapacityMW"]), 2)
                   newPlants$locCode = sample(retiringPlants$locCode, nrow(newPlants),replace=TRUE)
                   newPlants$age =1 
                   newPlants$startYear = newDF$years[i]
                   newPlants$seqNum=c(lastPlant:(lastPlant+nrow(newPlants)-1))
                   newPlants$expRet = rsnorm(nrow(newPlants), 
                        mean = typeChars[as.character(newPlants$type),"AvgRetAge"],
                        sd = typeChars[as.character(newPlants$type),"StdDevRetAge"],
                        xi = typeChars[as.character(newPlants$type),"skewness"])
                   newPlants$energy = capacityMWToEnergyTWh(newPlants,typeChars)
                   newPlants$carbonOutput=energyTWhToCarbonOutputKG(newPlants, typeChars, ifelse(newDF$year[i]>afterYearCCS, percent_CCS, 0))
                   
                    for(j in c(1:5)){
                        toChange = is.na(newPlants$expRet) | 
                            newPlants$expRet<newPlants$age 
                        newPlants$expRet[toChange] = rsnorm(sum(toChange), 
                            mean= typeChars[as.character(newPlants$type[toChange]),"AvgRetAge"],
                            sd = typeChars[as.character(newPlants$type[toChange]),"StdDevRetAge"],
                            xi = typeChars[as.character(newPlants$type[toChange]),"skewness"])
                    }
                    newPlants[newPlants$type%in%c("Nuclear","NuclearFusion"),"expRet"] = rbinom(sum(newPlants$type%in%c("Nuclear","NuclearFusion")),1,.5)*20+40
                    newPlants$long = usaMap2[newPlants$locCode,"long"]+rnorm(nrow(newPlants),0,.05)
                    newPlants$lat = usaMap2[newPlants$locCode,"lat"]+rnorm(nrow(newPlants),0,.05)
                    newPlants$isFusion = newPlants$type=="NuclearFusion"
                    newPlants$isNew=TRUE
                } 

             # e. add new plants into existing fleet -----------------------

             newDF$newFusionAdditions[i] = sum(newPlants$capacity[newPlants$type == "NuclearFusion"])

            fleet_t=rbind(fleet_t1,newPlants)        
            newDF$totalEnergyAfterAdding[i]=sum(fleet_t$energy)

            fleet_t$isFusion = fleet_t$type=="NuclearFusion"
  

            # f. moving year by year maps of where plants are (locations are assigned randomly, just for presentation/demo purpose)
        
            if(FALSE){ #### this switch turns this computationally expensive code off

        g = ggplotGrob(ggplot(fleet_t[fleet_t$carbonOutput<1e+09,])+
                 geom_point(aes(x=capacity, y=jitter(carbonOutput, amount = 1e+07), color = typeF), size = 1.5, alpha = .2)+
                  theme(plot.background=element_rect(color="white"),
                        legend.position="none", axis.text= element_blank(), 
                        axis.ticks=element_blank())+ylab("Carbon Output")+xlab("Capacity")+
                  xlim(0,500)+ylim(0,1e+09))

        g1 = ggplotGrob(ggplot(fleet_t[fleet_t$carbonOutput<1e+09,])+
                 geom_bar(aes(x=typeF, fill = typeF))+
                  theme(plot.background=element_rect(color="white"),
                        legend.position="none", axis.text= element_blank(), 
                        axis.ticks=element_blank())+xlab("Type"))

        p+ geom_point(data=fleet_t, 
                aes(x=long, y= lat, color = typeF, size = capacity, shape = isFusion), alpha =.4)+
            annotation_custom(grob=g, xmin=-79,xmax=-65,ymin=25, ymax=32)+
            annotation_custom(grob=g1, xmin=-124,xmax=-113,ymin=25, ymax=32)+
            ggtitle(paste("Power Plants in year: ",newDF$years[i]))+
            theme(text=element_text(size = 18))#, legend.position="none")
 
       ggsave(filename = paste("outputGraphs/maps4/", newDF$years[i],".png",sep=""))
     
        fleet_t$typeF = NULL
        fleet_t$isFusion = NULL
}
            }

        print("ending simulation")
        return(newDF)
}