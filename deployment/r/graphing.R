###### --------------------------------------------------------
# 
#   graphing.R 
#
#   Author: Lucas Spangher 
#   Last updated: July 10th, 2017
#   Purpose: A file by which to graph all the output
#
#   Note: many of these graphs were experimental and exploratory and are not included in the presentation 
#      To find a specific graph that is in the presentation, try searching the text by indentifying characteristics
#      in the graph such as axis labels or legend text

require(ggplot2)
require(fGarch)
require(maps)
library(e1071)

# age distributions to sample from
skewPV = skewness(currentGen$age[currentGen$type=="PV"])

df = data.frame(x=rnorm(100), y = rnorm(100), z = rnorm(100))
df2 = data.frame(x=rnorm(100), y = rnorm(100), z = rnorm(100))

ggplot()+
    geom_point(data = df, aes(x=x, y=y, color = z))+
    geom_line(data = df2, aes(x=x, y=y), color = "red")+
    ggtitle("Some Title")+ 
    xlim(-5,5)+
    theme(text= element_text(size=24))





ggplot()+
#    geom_histogram(aes(x=currentGen$age[currentGen$type=="PV"]))+
    geom_density(aes(x=rsnorm(1000,mean=typeChars["PV","AvgRetAge"],
        sd=typeChars["PV","StdDevRetAge"],skewPV), fill="blue", alpha=.4))

ggplot(retiredGen)+geom_density(aes(Retirement.Age, fill = Technology), alpha=.4)+
    facet_wrap(~Technology, scales="free_y") + #, scales="free")+
    theme(text=element_text(size = 28)) + ylab("Probability Density")+
    xlab("Age")+ggtitle("Retirement Ages of Different Types of Plants, Complete US database")

# Commented out because it has an error
# ggplot(currentGen)+geom_density(aes(Retirement.Age, fill = Technology), alpha=.4)+
#     facet_wrap(~Technology, scales="free_y") + #, scales="free")+
#     theme(text=element_text(size = 28)) + ylab("Probability Density")+
#     xlab("Age")#+ggtitle("Retirement Ages of Different Types of Plants, Complete US database")

ggplot(currentGen)+geom_density(aes(age, fill = type), alpha=.4)+
    facet_wrap(~type, scales="free")

distsUsedDF = data.frame(expand.grid(c(1:110), row.names(typeChars)))
names(distsUsedDF)=c("years", "Technology")
distsUsedDF$value = dsnorm(x = distsUsedDF$years,
    mean = typeChars[distsUsedDF$Technology, "AvgRetAge"], 
    sd = typeChars[distsUsedDF$Technology, "StdDevRetAge"],
    xi = typeChars[distsUsedDF$Technology, "skewness"])
distsUsedDF$value[distsUsedDF$Technology == "NuclearFusion"] = 0
distsUsedDF$value[distsUsedDF$Technology == "NuclearFusion" & distsUsedDF$years==60] = 1
distsUsedDF[distsUsedDF$Technology=="NuclearFusion1",]=NA
distsUsedDF=na.omit(distsUsedDF)


ggplot(retiredGen[!(retiredGen$Technology%in%c("Batteries","NuclearFusion1", "AllOther") | is.na(retiredGen$Technology)),])+geom_density(aes(Retirement.Age, fill = Technology), alpha=.4)+
    geom_line(data = distsUsedDF, aes(x= years, y = value), size = 2.5, color = "blue", alpha =1)+
    facet_wrap(~Technology, scales="free_y") + #, scales="free")+
    theme(text=element_text(size = 30)) + ylab("Probability Density")+
    xlab("Age")+ggtitle("Retirement Ages of Different Types of Plants, Complete US database")

# total Energy and Total Capacity 

ggplot(totalEnergy[totalEnergy$year%in%c(2014:2040),])+
    geom_line(aes(x=year, y= EnergyBillkWh, color = "AEO projections"), size =1)+
    geom_line(data=percent_0[percent_0$years%in%c(2014:2040),], aes(x=years, y=totalEnergyAfterAdding, color= "Simulated Energy"), size = 1)+
    geom_point(data = percent_0[percent_0$years%in%c(2014:2040),], aes(x = years, y = dearth_t_energy, color = "Simulated dearths"), size = 2)+
    scale_colour_manual("", 
        breaks=c("AEO projections", "Simulated Energy", "Simulated dearths"),
        values=c("AEO projections"="black", "Simulated Energy" = "blue", "Simulated dearths"="red"))+
    xlab("Year") + ylab("Energy (MWh)")+ #ggtitle("EIA projections for Energy Use vs. simulation")+
    theme(text= element_text(size = 36))

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(aes(x=year, y= capacity, color = "AEO projections"), size =1)+
    geom_line(data=percent_00_2030[percent_00_2030$years%in%c(2014:2040),], aes(x=years, y=totalCapacityAfterRetirement+75, color= "Simulated Capacity"), size = 1)+
    geom_point(data = percent_00_2030[percent_00_2030$years%in%c(2014:2040),], aes(x = years, y = dearth_t_cap/1000, color = "Simulated dearths"), size = 2)+
    scale_colour_manual("", 
        breaks=c("AEO projections", "Simulated Capacity", "Simulated dearths"),
        values=c("AEO projections"="black", "Simulated Capacity" = "blue", "Simulated dearths"="red"))+
    xlab("Year") + ylab("Capacity (MW)")+ #ggtitle("EIA projections for Energy Use vs. simulation")+
    theme(text= element_text(size = 36))

ggplot(totalEnergy, aes(x=year,y=EnergyBillkWh))+
    geom_point(aes(text=paste("Energy: ", EnergyBillkWh)))+
    ylim(0, max(totalEnergy$EnergyBillkWh))+
    theme(text=element_text(size=30)) + ylab("Electricity (Billion kWh)")+
    xlab("Year")

# TODO - commented because newDF not found
# ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
#     geom_line(data=newDF, aes(x=years, y=NGCCGrowth, color = "NGCCGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=WindGrowth, color = "WindGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=NuclearGrowth, color = "NuclearGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=PetroleumGrowth, color = "PetroleumGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=NGSTGrowth, color = "NGSTGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=NGCTGrowth, color = "NGCTGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=PVGrowth, color = "PVGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=HydroGrowth, color = "HydroGrowth"), size = 2, alpha = .7)+
#     geom_line(data=newDF, aes(x=years, y=CoalGrowth, color = "CoalGrowth"), size = 2, alpha = .7)+
#  #   geom_line(data=newDF, aes(x=years, y=fusionGrowth, color = "fusionGrowth"), size = 2)+
#     theme(text= element_text(size = 24))+ggtitle("Capacity change by Type of Plant")+
#     xlab("Year") + ylab("Capacity (kW)")

#     scale_colour_manual("",
#         breaks=c("NGCCGrowth", "WindGrowth", "NuclearGrowth", "PetroleumGrowth", "NGSTGrowth",
#             "NGCTGrowth", "PVGrowth", "HydroGrowth", "CoalGrowth","fusionGrowth", "Simulated dearths"),
#         values=c("NGCCGrowth"="black", "WindGrowth" = "blue", "NuclearGrowth"="cadetblue",
#             "PetroleumGrowth" = "darkorange1", "NGSTGrowth" ="deeppink", "fusionGrowth"="green4",
#             "NGCTGrowth" = "darkorchid", "PVGrowth" = "mediumpurple1","HydroGrowth" = "lightpink2",
#             "CoalGrowth"="maroon4", "Simulated dearths"="red"))+
#     ggtitle("Capacity change by Type of Plant")

# simualtion 

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data=percent_0, aes(x=years, y=NGCCGrowth, color = "NGCCGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=WindGrowth, color = "WindGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=NuclearGrowth, color = "NuclearGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=PetroleumGrowth, color = "PetroleumGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=NGSTGrowth, color = "NGSTGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=NGCTGrowth, color = "NGCTGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=PVGrowth, color = "PVGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=HydroGrowth, color = "HydroGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=CoalGrowth, color = "CoalGrowth"))+
    geom_line(data=percent_0, aes(x=years, y=fusionGrowth, color = "fusionGrowth"), size = 2)+
    scale_colour_manual("", 
        breaks=c("NGCCGrowth", "WindGrowth", "NuclearGrowth", "PetroleumGrowth", "NGSTGrowth",
            "NGCTGrowth", "PVGrowth", "HydroGrowth", "CoalGrowth","fusionGrowth", "Simulated dearths"),
        values=c("NGCCGrowth"="black", "WindGrowth" = "blue", "NuclearGrowth"="cadetblue",  
            "PetroleumGrowth" = "darkorange1", "NGSTGrowth" ="deeppink", "fusionGrowth"="green4",
            "NGCTGrowth" = "darkorchid", "PVGrowth" = "mediumpurple1","HydroGrowth" = "lightpink2", 
            "CoalGrowth"="maroon4", "Simulated dearths"="red"))+
    ggtitle("Capacity change by Type of Plant")


# TODO - percent_05 not found, commenting out
# ggplotly(ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
#     geom_line(data=percent_05, aes(x=years, y=NGCCGrowth, color = "NGCCGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=WindGrowth, color = "WindGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=NuclearGrowth, color = "NuclearGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=PetroleumGrowth, color = "PetroleumGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=NGSTGrowth, color = "NGSTGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=NGCTGrowth, color = "NGCTGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=PVGrowth, color = "PVGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=HydroGrowth, color = "HydroGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=CoalGrowth, color = "CoalGrowth"))+
#     geom_line(data=percent_05, aes(x=years, y=fusionGrowth, color = "fusionGrowth"), size = 2)+
#     scale_colour_manual("", 
#         breaks=c("NGCCGrowth", "WindGrowth", "NuclearGrowth", "PetroleumGrowth", "NGSTGrowth",
#             "NGCTGrowth", "PVGrowth", "HydroGrowth", "CoalGrowth","fusionGrowth", "Simulated dearths"),
#         values=c("NGCCGrowth"="black", "WindGrowth" = "blue", "NuclearGrowth"="cadetblue",  
#             "PetroleumGrowth" = "darkorange1", "NGSTGrowth" ="deeppink", "fusionGrowth"="green4",
#             "NGCTGrowth" = "darkorchid", "PVGrowth" = "mediumpurple1","HydroGrowth" = "lightpink2", 
#             "CoalGrowth"="maroon4", "Simulated dearths"="red"))+
#     ggtitle("Capacity change by Type of Plant"))


ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data=percent_50, aes(x=years, y=NGCCGrowth, color = "NGCCGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=WindGrowth, color = "WindGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=NuclearGrowth, color = "NuclearGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=PetroleumGrowth, color = "PetroleumGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=NGSTGrowth, color = "NGSTGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=NGCTGrowth, color = "NGCTGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=PVGrowth, color = "PVGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=HydroGrowth, color = "HydroGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=CoalGrowth, color = "CoalGrowth"))+
    geom_line(data=percent_50, aes(x=years, y=fusionGrowth, color = "fusionGrowth"), size = 2)+
    scale_colour_manual("", 
        breaks=c("NGCCGrowth", "WindGrowth", "NuclearGrowth", "PetroleumGrowth", "NGSTGrowth",
            "NGCTGrowth", "PVGrowth", "HydroGrowth", "CoalGrowth","fusionGrowth", "Simulated dearths"),
        values=c("NGCCGrowth"="black", "WindGrowth" = "blue", "NuclearGrowth"="cadetblue",  
            "PetroleumGrowth" = "darkorange1", "NGSTGrowth" ="deeppink", "fusionGrowth"="green4",
            "NGCTGrowth" = "darkorchid", "PVGrowth" = "mediumpurple1","HydroGrowth" = "lightpink2", 
            "CoalGrowth"="maroon4", "Simulated dearths"="red"))+
    ggtitle("Capacity change by Type of Plant")

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data=percent_99, aes(x=years, y=NGCCGrowth, color = "NGCCGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=WindGrowth, color = "WindGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=NuclearGrowth, color = "NuclearGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=PetroleumGrowth, color = "PetroleumGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=NGSTGrowth, color = "NGSTGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=NGCTGrowth, color = "NGCTGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=PVGrowth, color = "PVGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=HydroGrowth, color = "HydroGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=CoalGrowth, color = "CoalGrowth"))+
    geom_line(data=percent_99, aes(x=years, y=fusionGrowth, color = "fusionGrowth"), size = 2)+
    scale_colour_manual("", 
        breaks=c("NGCCGrowth", "WindGrowth", "NuclearGrowth", "PetroleumGrowth", "NGSTGrowth",
            "NGCTGrowth", "PVGrowth", "HydroGrowth", "CoalGrowth","fusionGrowth", "Simulated dearths"),
        values=c("NGCCGrowth"="black", "WindGrowth" = "blue", "NuclearGrowth"="cadetblue",  
            "PetroleumGrowth" = "darkorange1", "NGSTGrowth" ="deeppink", "fusionGrowth"="green4",
            "NGCTGrowth" = "darkorchid", "PVGrowth" = "mediumpurple1","HydroGrowth" = "lightpink2", 
            "CoalGrowth"="maroon4", "Simulated dearths"="red"))+
    ggtitle("Capacity change by Type of Plant")

##### total carbon output under various scenarios

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data= percent_0, aes(x=years, y=totalCarbon, color = "BAU"), size= 2, alpha=.6)+
#    geom_line(data= percent_05, aes(x=years, y=totalCarbon, color = "5%, all replaced, 2014"), size= 2, alpha=.6)+
    geom_line(data= percent_05_2030, aes(x=years, y=totalCarbon, color = "5%, all replaced, 2030"), size= 2, alpha=.6)+
    geom_line(data= percent_10, aes(x=years, y=totalCarbon, color = "10%, all replaced"), size= 2, alpha=.6)+
    geom_line(data= percent_50_WNPC_2030, aes(x=years, y=totalCarbon, color = "50%, Wind PV NGCC Coal replaced after 2030"), size= 2, alpha=.6)+
    geom_line(data= percent_50_2030, aes(x=years, y=totalCarbon, color = "50%, all replaced after 2030"), size= 2, alpha=.6)+
    geom_line(data= percent_99_2030, aes(x=years, y=totalCarbon, color = "99%, all replaced after 2030"), size= 2, alpha=.6)+
    geom_line(data= percent_99_WNPC_2030, aes(x=years, y=totalCarbon, color = "99%, WPNC replaced after 2030"), size= 2, alpha=.6)+
    ggtitle("Total Carbon Projections of Fleet under differing fusion scenarios")+
    ylab("Carbon Output, Gtons")

### 1. capacity area plots 

### 2. carbon budget, 49 Gtons for the US HAD TO INCREASE 

tempData = list(percent_00_2030, percent_10_2030, percent_50_2030, percent_99_2030, percent_99_2040)

debt = 74

debtBreakpoints = sapply(tempData, function(df){
    cum_carbon = cumsum(df$totalCarbon)
    breakPoint = which(cum_carbon>debt)[1]  ### <- carbon budget 
    return(c(df$years[breakPoint], df$totalCarbon[breakPoint]))
    })
debtBreakpoints = data.frame(year= debtBreakpoints[1,], carbonOutput = debtBreakpoints[2,])


data= lapply(tempData, function(df){
    cum_carbon = cumsum(df$totalCarbon)
    breakPoint = which(cum_carbon>debt)[1]  ### <- carbon budget 
    year = df$years[breakPoint]
    return(df[df$years<=year,])
    })

plot <- ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data= data[[1]], aes(x=years, y=totalCarbon), color = "grey3", size= 2, alpha=.6)+
#    geom_line(data= data[[2]], aes(x=years, y=totalCarbon, color = "05%"), size= 2, alpha=.6)+
    geom_line(data= data[[2]], aes(x=years, y=totalCarbon), color = "grey2", size= 2, alpha=.6)+
#    geom_line(data= data[[4]], aes(x=years, y=totalCarbon, color = "25%"), size= 2, alpha=.6)+
    geom_line(data= data[[3]], aes(x=years, y=totalCarbon), color = "grey1", size= 2, alpha=.6)+
    geom_line(data= data[[5]], aes(x=years, y=totalCarbon), color = "grey1", size= 2, alpha=.6)+
#    geom_line(data= data[[6]], aes(x=years, y=totalCarbon, color = "75%"), size= 2, alpha=.6)+
    geom_line(data= data[[4]], aes(x=years, y=totalCarbon), color = "red", size= 2, alpha=.6)+
    geom_point(data= debtBreakpoints, aes(x= year, y= carbonOutput), size = 7.5, alpha = 1)+
    ylab("Carbon Output, Gtons")+theme(text=element_text(size=24))+
    annotate("text", x=c(2075, 2062.5, 2060, 2061, 2058),
        y = c(.3, .8, 1.15, 1.6, 1.75),
        label = c("99%, 2030", "50%, 2030", "99%, 2040", "10%, 2030", "BAU"),
        color = c("red","black","black","black","black"), 
        size = 6)
ggsave("out/graphs/Carbon_scenarios_5_1.pdf", plot, width = 12, height = 7.9)

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data= tempData[[1]], aes(x=years, y=totalCarbon), color = "grey3", size= 2, alpha=.6)+
#    geom_line(data= tempData[[2]], aes(x=years, y=totalCarbon, color = "05%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[2]], aes(x=years, y=totalCarbon), color = "grey2", size= 2, alpha=.6)+
#    geom_line(data= tempData[[4]], aes(x=years, y=totalCarbon, color = "25%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[3]], aes(x=years, y=totalCarbon), color = "grey1", size= 2, alpha=.6)+
#    geom_line(data= tempData[[6]], aes(x=years, y=totalCarbon, color = "75%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[4]], aes(x=years, y=totalCarbon), color = "red", size= 2, alpha=.6)+
#    geom_point(data= debtBreakpoints[c(1,3,5,7),], aes(x= year, y= carbonOutput), size = 7.5, alpha = 1)+
    ggtitle(paste("Different Market Scenarios and Respective Carbon Debt,", debt,"Gtons"))+
    ylab("Carbon Output, Gtons")+theme(text=element_text(size=24))

ggplot(totalCapacity[totalCapacity$year%in%c(2014:2040),])+
    geom_line(data= tempData[[1]], aes(x=years, y=cumsum(totalCarbon), color = "BAU"), size= 2, alpha=.6)+
    geom_line(data= tempData[[2]], aes(x=years, y=cumsum(totalCarbon), color = "05%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[3]], aes(x=years, y=cumsum(totalCarbon), color = "10%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[4]], aes(x=years, y=cumsum(totalCarbon), color = "25%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[5]], aes(x=years, y=cumsum(totalCarbon), color = "50%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[6]], aes(x=years, y=cumsum(totalCarbon), color = "75%"), size= 2, alpha=.6)+
    geom_line(data= tempData[[7]], aes(x=years, y=cumsum(totalCarbon), color = "99%"), size= 2, alpha=.6)+
    ggtitle(paste("Different Market Scenarios Cumulative Carbon (GTons)"))+
    ylab("Carbon Output, Gtons")+theme(text=element_text(size=28))

### 3. Slow and steady (early) or procrastinator? 

ggplot()+
    geom_line(data=percent_10_2025, aes(x=years, y=mav(totalCarbon), color = "a"), color = "palevioletred1", size = 2, alpha = .7)+
    geom_line(data=percent_15_2025, aes(x=years, y=mav(totalCarbon), color = "b"), color = "palevioletred2", size = 2, alpha = .7)+
    geom_line(data=percent_20_2025, aes(x=years, y=mav(totalCarbon), color = "c"), color = "palevioletred3", size = 2, alpha = .7)+
    geom_line(data=percent_25_2025, aes(x=years, y=mav(totalCarbon), color = "d"), color = "palevioletred4", size = 2, alpha = .7)+
    geom_line(data=percent_50_2050, aes(x=years, y=mav(totalCarbon), color = "e"), color = "springgreen1", size = 2, alpha = .7)+
    geom_line(data=percent_55_2050, aes(x=years, y=mav(totalCarbon), color = "f"), color = "springgreen2", size = 2, alpha = .7)+
    geom_line(data=percent_60_2050, aes(x=years, y=mav(totalCarbon), color = "g"), color = "springgreen3", size = 2, alpha = .7)+
    geom_line(data=percent_65_2050, aes(x=years, y=mav(totalCarbon), color = "h"), color = "springgreen4", size = 2, alpha = .7)+
    geom_line(data=percent_90_2075, aes(x=years, y=mav(totalCarbon), color = "i"), color = "lavenderblush1", size = 2, alpha = .7)+
    geom_line(data=percent_92_2075, aes(x=years, y=mav(totalCarbon), color = "j"), color = "lavenderblush2", size = 2, alpha = .7)+
    geom_line(data=percent_94_2075, aes(x=years, y=mav(totalCarbon), color = "k"), color = "lavenderblush3", size = 2, alpha = .7)+
    geom_line(data=percent_96_2075, aes(x=years, y=mav(totalCarbon), color = "l"), color = "lavenderblush4", size = 2, alpha = .7)+
    ggtitle("'Slow and steady' or 'College Procastination Style'?")+
    ylab("Carbon Output, Gtons")+ylim(0,2)+
    theme(text=element_text(size =28), legend.position="center")
    

### 4. Depressing case to avoid 

ggplot()+
    geom_line(data=percent_05_ren, aes(x=years, y=totalCarbon, color = "05%"), size = 2, alpha = .7)+
    geom_line(data=percent_10_ren, aes(x=years, y=totalCarbon, color = "10%"), size = 2, alpha = .7)+
    geom_line(data=percent_17_ren, aes(x=years, y=totalCarbon, color = "17%"), size = 2, alpha = .7)+
    geom_line(data=percent_25_ren, aes(x=years, y=totalCarbon, color = "25%"), size = 2, alpha = .7)+
    geom_line(data=percent_37_ren, aes(x=years, y=totalCarbon, color = "37%"), size = 2, alpha = .7)+
    geom_line(data=percent_42_ren, aes(x=years, y=totalCarbon, color = "42%"), size = 2, alpha = .7)+
    geom_line(data=percent_47_ren, aes(x=years, y=totalCarbon, color = "47%"), size = 2, alpha = .7)+
    geom_line(data=percent_50_ren, aes(x=years, y=totalCarbon, color = "50%"), size = 2, alpha = .7)+
    geom_line(data=percent_75_ren, aes(x=years, y=totalCarbon, color = "75%"), size = 2, alpha = .7)+
    geom_line(data=percent_99_ren, aes(x=years, y=totalCarbon, color = "99%"), size = 2, alpha = .7)+
    ggtitle("The Case to (maybe) Avoid: Replacing all Renewables")+
    ylab("Carbon Output, Gtons")+
    theme(text=element_text(size = 24), axis.title.y=element_text(face="bold"), axis.title.x = element_text(face="bold"))+
    ylim(0,2.7)

## ??? what's going on with renewables? 

ggplot()+
    geom_line(data=percent_37_ren, aes(x=years, y=totalCarbon, color = "37%"), size = 2, alpha = .7)+
    geom_line(data=percent_38_ren, aes(x=years, y=totalCarbon, color = "38%"), size = 2, alpha = .7)+
    geom_line(data=percent_39_ren, aes(x=years, y=totalCarbon, color = "39%"), size = 2, alpha = .7)+
    geom_line(data=percent_40_ren, aes(x=years, y=totalCarbon, color = "40%"), size = 2, alpha = .7)+
    geom_line(data=percent_41_ren, aes(x=years, y=totalCarbon, color = "41%"), size = 2, alpha = .7)+
    geom_line(data=percent_42_ren, aes(x=years, y=totalCarbon, color = "42%"), size = 2, alpha = .7)+
    geom_line(data=percent_45_ren, aes(x=years, y=totalCarbon, color = "45%"), size = 2, alpha = .7)+
    ggtitle("Exploring the weird switch over in replacing all Renewables")+
    ylab("Carbon Output, Gtons")+
    ylim(0,2.7)

## is it if you do it with all? 

ggplot()+
    geom_line(data=percent_05, aes(x=years, y=totalCarbon, color = "05%"), size = 2, alpha = .7)+
    geom_line(data=percent_10, aes(x=years, y=totalCarbon, color = "10%"), size = 2, alpha = .7)+
    geom_line(data=percent_17, aes(x=years, y=totalCarbon, color = "17%"), size = 2, alpha = .7)+
    geom_line(data=percent_25, aes(x=years, y=totalCarbon, color = "25%"), size = 2, alpha = .7)+
    geom_line(data=percent_37, aes(x=years, y=totalCarbon, color = "37%"), size = 2, alpha = .7)+
    geom_line(data=percent_42, aes(x=years, y=totalCarbon, color = "42%"), size = 2, alpha = .7)+
    geom_line(data=percent_47, aes(x=years, y=totalCarbon, color = "47%"), size = 2, alpha = .7)+
    geom_line(data=percent_50, aes(x=years, y=totalCarbon, color = "50%"), size = 2, alpha = .7)+
    geom_line(data=percent_75, aes(x=years, y=totalCarbon, color = "75%"), size = 2, alpha = .7)+
    geom_line(data=percent_99, aes(x=years, y=totalCarbon, color = "99%"), size = 2, alpha = .7)+
    ggtitle("The Case to Avoid: Replacing all Renewables")+
    ylab("Carbon Output, Gtons")+
    ylim(0,2.7)

## is it if you do it with a subset of renewables? 

ggplot()+
    geom_line(data=percent_05_ren_sub, aes(x=years, y=totalCarbon, color = "05%"), size = 2, alpha = .7)+
    geom_line(data=percent_10_ren_sub, aes(x=years, y=totalCarbon, color = "10%"), size = 2, alpha = .7)+
    geom_line(data=percent_17_ren_sub, aes(x=years, y=totalCarbon, color = "17%"), size = 2, alpha = .7)+
    geom_line(data=percent_25_ren_sub, aes(x=years, y=totalCarbon, color = "25%"), size = 2, alpha = .7)+
    geom_line(data=percent_37_ren_sub, aes(x=years, y=totalCarbon, color = "37%"), size = 2, alpha = .7)+
    geom_line(data=percent_42_ren_sub, aes(x=years, y=totalCarbon, color = "42%"), size = 2, alpha = .7)+
    geom_line(data=percent_47_ren_sub, aes(x=years, y=totalCarbon, color = "47%"), size = 2, alpha = .7)+
    geom_line(data=percent_50_ren_sub, aes(x=years, y=totalCarbon, color = "50%"), size = 2, alpha = .7)+
    geom_line(data=percent_75_ren_sub, aes(x=years, y=totalCarbon, color = "75%"), size = 2, alpha = .7)+
    geom_line(data=percent_99_ren_sub, aes(x=years, y=totalCarbon, color = "99%"), size = 2, alpha = .7)+
    ggtitle("The Case to Avoid: Replacing all Renewables, wind+PV")+
    ylab("Carbon Output, Gtons")+
    ylim(0,2.7)



### 5. Different Years of entry

ggplot()+
    geom_line(data=percent_25_2030, aes(x=years, y=cumsum(totalCarbon), color = "2030"), size = 2, alpha = .7)+
    geom_line(data=percent_25_2035, aes(x=years, y=cumsum(totalCarbon), color = "2035"), size = 2, alpha = .7)+
    geom_line(data=percent_25_2040, aes(x=years, y=cumsum(totalCarbon), color = "2040"), size = 2, alpha = .7)+
    geom_line(data=percent_25_2045, aes(x=years, y=cumsum(totalCarbon), color = "2045"), size = 2, alpha = .7)+
    geom_line(data=percent_25_2050, aes(x=years, y=cumsum(totalCarbon), color = "2050"), size = 2, alpha = .7)+
    geom_line(data=percent_25_2055, aes(x=years, y=cumsum(totalCarbon), color = "2055"), size = 2, alpha = .7)+
    ggtitle("Different Years of Entry, 25% each")+
    ylab("Carbon Output, GTons")


####### 6. different market penetrations 

ggplot()+
    geom_line(data=percent_05_2030, aes(x=years, y=totalCarbon), color= "black", size = 2, alpha = .7)+
    ggtitle("Different Market Penetrations")+
    ylab("Carbon Output, GTons") + ylim(0,2.3)+
    theme(text=element_text(size = 24))

ggplot()+
    geom_line(data=percent_05_2030, aes(x=years, y=totalCarbon), color = "grey1", size = 2, alpha = .7)+
    geom_line(data=percent_10_2030, aes(x=years, y=totalCarbon), color = "red", size = 2, alpha = .7)+
    ggtitle("Different Market Penetrations")+
    ylab("Carbon Output, GTons") + ylim(0,2.3)+
    theme(text=element_text(size = 24))

ggplot()+
    geom_line(data=percent_05_2030, aes(x=years, y=totalCarbon), color = "grey2", size = 2, alpha = .7)+
    geom_line(data=percent_10_2030, aes(x=years, y=totalCarbon), color = "grey1", size = 2, alpha = .7)+
    geom_line(data=percent_50_2030, aes(x=years, y=totalCarbon), color = "red", size = 2, alpha = .7)+
    ggtitle("Different Market Penetrations")+
    ylab("Carbon Output, GTons") + ylim(0,2.3)+
    theme(text=element_text(size = 24))

ggplot()+
    geom_line(data=percent_05_2030, aes(x=years, y=totalCarbon), color = "grey3", size = 2, alpha = .7)+
    geom_line(data=percent_10_2030, aes(x=years, y=totalCarbon), color = "grey2", size = 2, alpha = .7)+
    geom_line(data=percent_50_2030, aes(x=years, y=totalCarbon), color = "grey1", size = 2, alpha = .7)+
    geom_line(data=percent_99_2030, aes(x=years, y=totalCarbon), color = "red", size = 2, alpha = .7)+
    ggtitle("Different Market Penetrations")+
    ylab("Carbon Output, GTons") + ylim(0,2.3)+
    theme(text=element_text(size = 24))

### 6. CCS 

ggplot()+
    geom_line(data=percent_00_CCS, aes(x=years, y=totalCarbon, color = "00% (BAU)"), size = 2, alpha = .7)+
    geom_line(data=percent_05_CCS, aes(x=years, y=totalCarbon, color = "05%"), size = 2, alpha = .7)+
    geom_line(data=percent_10_CCS, aes(x=years, y=totalCarbon, color = "10%"), size = 2, alpha = .7)+
    geom_line(data=percent_25_CCS, aes(x=years, y=totalCarbon, color = "25%"), size = 2, alpha = .7)+
    geom_line(data=percent_50_CCS, aes(x=years, y=totalCarbon, color = "50%"), size = 2, alpha = .7)+
    geom_line(data=percent_75_CCS, aes(x=years, y=totalCarbon, color = "75%"), size = 2, alpha = .7)+
    geom_line(data=percent_99_CCS, aes(x=years, y=totalCarbon, color = "99%"), size = 2, alpha = .7)+
    ggtitle("Different Amounts of CCS")+
    ylab("Carbon Output, GTons")

### 7. Cumulative area plots 

# 10% after 2030

cum_percent_10_2030= data.frame(apply(percent_10_2030, 2, cumsum))
cum_percent_10_2030$years=percent_10_2030$years
cum_newdata = melt(cum_percent_10_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_10_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.25)+
    ggtitle("Capacity Growth among types, 10% fusion after 2030")+
    ylab("Capacity (GW)")+ xlab("Year")+
    theme(text= element_text(size = 24))

# 50% after 2030

cum_percent_50_2030= data.frame(apply(percent_50_2030, 2, cumsum))
cum_percent_50_2030$years=percent_50_2030$years
cum_newdata = melt(cum_percent_50_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_50_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.35)+
    ggtitle("Capacity Growth among types, 50% fusion after 2030")+
    ylab("Capacity (GW)")+xlab("Year")+
    theme(text= element_text(size = 24))

# 10% after 2050

cum_percent_10_2050= data.frame(apply(percent_10_2050, 2, cumsum))
cum_percent_10_2050$years=percent_10_2050$years
cum_newdata = melt(cum_percent_10_2050, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_10_2050, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.25)+
    ggtitle("Capacity Growth among types, 10% fusion after 2050")+
    ylab("Capacity (GW)")+ xlab("Year")+
    theme(text= element_text(size = 24))

# 50% after 2050

cum_percent_50_2050= data.frame(apply(percent_50_2050, 2, cumsum))
cum_percent_50_2050$years=percent_50_2050$years
cum_newdata = melt(cum_percent_50_2050, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_50_2050, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.55)+
    ggtitle("Capacity Growth among types, 50% fusion after 2050")+
    ylab("Capacity (GW)")+xlab("Year")+
    theme(text= element_text(size = 24))+theme_bw()


# 10% after 2070

cum_percent_10_2070= data.frame(apply(percent_10_2070, 2, cumsum))
cum_percent_10_2070$years=percent_10_2070$years
cum_newdata = melt(cum_percent_10_2070, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_10_2070, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.25)+
    ggtitle("Capacity Growth among types, 10% fusion after 2070")+
    ylab("Capacity (GW)")+xlab("Year")+
    theme(text= element_text(size = 24))

# 50% after 2070

cum_percent_50_2070= data.frame(apply(percent_50_2070, 2, cumsum))
cum_percent_50_2070$years=percent_50_2070$years
cum_newdata = melt(cum_percent_50_2070, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_50_2070, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.35)+
    ggtitle("Capacity Growth among types, 50% fusion after 2070")+
    ylab("Capacity (GW)")+xlab("Year")+
    theme(text= element_text(size = 24))

# 99% 

cum_percent_99_2030= data.frame(apply(percent_99_2030, 2, cumsum))
cum_percent_99_2030$years=percent_99_2030$years
cum_newdata = melt(cum_percent_99_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_99_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata, aes(x=years, y=value/10^3))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.35)+
    ggtitle("Capacity Growth among types, 99% fusion after 2030")+
    ylab("Capacity (GW)")+
    theme(text= element_text(size = 24))


dearthPlotDF = data.frame(year = c(2014:2050), cum_dearth=cumsum(percent_10$dearth_t_cap))

ggplot(dearthPlotDF)+geom_area(aes(x=year, y=cum_dearth), fill="green", alpha=.4)

# TODO - commented because newDF not found
# ggplot(newDF)+geom_point(aes(x=dearth_t_cap,y=dearth_t_energy))

# BAU 

cum_percent_0_2030= data.frame(apply(percent_0, 2, cumsum))
cum_percent_0_2030$years=percent_0$years
cum_newdata = melt(cum_percent_0_2030, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))
newdata = melt(percent_0, id = c("years","totalCapacityAfterRetirement","totalEnergyAfterRetirement","dearth_t_cap",
    "dearth_t_energy", "totalEnergyAfterAdding","carbonIntensity","totalCarbon","plantsAdded","fusionDearth",
    "NGCCDearth","WindDearth","NuclearDearth","PetroleumDearth","NGSTDearth", "NGCTDearth", "PVDearth", "HydroDearth", "CoalDearth"))

ggplot(newdata[newdata$years%in%c(2014:2040),], aes(x=years, y=value))+
    geom_area(aes(colour=variable, fill=variable), 
        position="stack", alpha=.45)+
    ggtitle("Capacity Growth among types, BAU, 2014-2040")+
    ylab("Capacity (MW)")+
    theme(text= element_text(size = 24))

### fuel mix to add every year, using addCapDiffProp1 which needs to be initialized via the simulateFleet.r script,
# set addCapDiffProp1 = addCapDiffProp 

addCapDiffProp1$year = as.numeric(row.names(addCapDiffProp1))
addCapDiffProp1$TotalTest=NULL
new_addCap = melt(addCapDiffProp1, id = "year")

ggplot(new_addCap[new_addCap$year<3000,], aes(x=year, y = value))+
    geom_area(aes(color = variable, fill = variable), position = "stack", alpha = .6)+
    xlab("Year") + ylab("Percent")+ theme(text= element_text(size = 38))


######## BAU dearth plot 
ggplot(BAU)+
    geom_line(aes(x=years, y= NGCCDearth, color = "NGCC"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= WindDearth, color = "Wind"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= NuclearDearth, color = "Nuclear Fission"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= PetroleumDearth, color = "Petroleum"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= NGSTDearth, color = "NGST"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= NGCTDearth, color = "NGCT"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= PVDearth, color = "PV"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= HydroDearth, color = "Hyroelectric"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= CoalDearth, color = "Coal"), size = 2, alpha= .5)+
    ggtitle("Simulated Retirements by energy type (MW)")+
    xlab("Years")+ylab("Capacity (MW)")+
    theme(text=element_text(size=18))

ggplot(BAU)+
    geom_line(aes(x=years, y= mav(NGCCDearth, n=11), color = "NGCC"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(WindDearth, n=11), color = "Wind"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(NuclearDearth, n=11), color = "Nuclear Fission"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(PetroleumDearth, n=11), color = "Petroleum"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(NGSTDearth, n=11), color = "NGST"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(NGCTDearth, n=11), color = "NGCT"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(PVDearth, n=11), color = "PV"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(HydroDearth, n=11), color = "Hyroelectric"), size = 2, alpha= .5)+
    geom_line(aes(x=years, y= mav(CoalDearth, n=11), color = "Coal"), size = 2, alpha= .5)+
    ggtitle("Simulated Retirements by energy type (MW), 2 sided 11th degree Moving Average")+
    xlab("Years")+ylab("Capacity (MW)")+
    theme(text=element_text(size=18))


### different market sales 

tempData = list(percent_10, percent_25, percent_50, percent_99, BAU)

debtBreakpoints = sapply(tempData, function(df){
    cum_carbon = cumsum(df$totalCarbon)
    breakPoint = which(cum_carbon>80)[1]  ### <- carbon budget
    breakPoint=ifelse(is.na(breakPoint), nrow(df), breakPoint) 
    return(c(df$years[breakPoint], df$totalCarbon[breakPoint]))
    })
debtBreakpoints = data.frame(year= debtBreakpoints[1,], carbonOutput = debtBreakpoints[2,])


tempData2= lapply(tempData, function(df){
    cum_carbon = cumsum(df$totalCarbon)
    breakPoint = which(cum_carbon>80)[1]  ### <- carbon budget 
    breakPoint=ifelse(is.na(breakPoint), nrow(df), breakPoint) 
    year = df$years[breakPoint]
    return(df[df$years<=year,])
    })

ggplot()+
    geom_line(data=tempData2[[1]], aes(x= years, y = totalCarbon, color = "10%"), size = 2, alpha = .7)+
    geom_line(data=tempData2[[2]], aes(x= years, y = totalCarbon, color = "25%"), size = 2, alpha = .7)+
    geom_line(data=tempData2[[3]], aes(x= years, y = totalCarbon, color = "50%"), size = 2, alpha = .7)+
    geom_line(data=tempData2[[4]], aes(x= years, y = totalCarbon, color = "99%"), size = 2, alpha = .7)+
    geom_line(data=tempData2[[5]], aes(x= years, y = totalCarbon, color = "BAU"), size = 2, alpha = .7)+
    geom_point(data= debtBreakpoints, aes(x= year, y= carbonOutput), size = 7.5, alpha = .7)+
    ggtitle("Different market penetrations of fusion after year 2030")+
    xlab("Year")+ylab("Total Carbon Emissions, GtCO2")+
    theme(text=element_text(size =20))

## carbon intensity

# TODO - commented because newDF not found
# ggplotly(ggplot(newDF)+
#     geom_line(aes(x=years, y= carbonIntensity))+
#     ylim(0,550000))

## maps 

shapes= c(rep(c(15,16,3,7,18,10,8),2), 15)
names(shapes)=row.names(typeChars)

gg_color_hue <- function(n) { # ggplot default colors
  hues = seq(15, 375, length=n+1)
  hcl(h=hues, l=65, c=100)[1:n]
}

colors = gg_color_hue(nrow(typeChars))
names(colors)= names(shapes)

ggplot(data=usaMap, aes(x=long,y=lat))+geom_polygon(aes(group=group))

g = ggplotGrob(ggplot(fleet_t[fleet_t$carbonOutput<2e+09,])+
    geom_histogram(aes(x=carbonOutput, fill = type))+
    theme(plot.background=element_rect(color="white"),
        legend.position="none"))

p1= p+geom_point(data=currentGen[sample(nrow(currentGen), 
            size = round(nrow(currentGen)/16)),],
        aes(x=long, y= lat, shape = type, color = type, size = capacity), alpha =.4)+
        scale_shape_manual(values=shapes)+
        scale_colour_manual(values=colors)+
        scale_size(range=c(0,10))+
        annotation_custom(grob=g, xmin=-75,xmax=-65,ymin=25, ymax=33)

# BAU 
ggplot(data=usaMap, aes(x=long,y=lat))+geom_polygon(aes(group=group))+
    geom_point(data=currentGen, aes(x=long, y= lat, color = type, size = capacity), alpha =.3)+
    theme(text=element_text(size = 24))+
    ggtitle("US Powerplant fleet in 2014")


# try plotly        
require(plotly)
    
# FLIPPING subplots...
require(R.utils)
sourceDirectory("ggsubplot/") # need to copy over those exact files each time you need this library...

# e.g 
library(ggplot2)
library(maps)
library(plyr)

#Get world map info
US_map <- map_data("county")

#Create a base plot
p <- ggplot()  + geom_polygon(data=world_map,aes(x=long, y=lat,group=group))

# Calculate the mean longitude and latitude per region, these will be the coördinates where the plots will be placed, so you can tweak them where needed.
# Create simulation data of the age distribution per region and merge the two.

centres <- ddply(world_map,.(region),summarize,long=mean(long),lat=mean(lat))
mycat <- cut(runif(1000), c(0, 0.1, 0.3, 0.6, 1), labels=FALSE) 
mycat <- as.factor(mycat)
age <- factor(mycat,labels=c("<15","15-30","20-60",">60"))
simdat <- merge(centres ,age)
colnames(simdat) <- c( "region","long","lat","Age" )

# Select the countries where you want a subplot for and plot
simdat2 <- subset(simdat, region %in% c("USA","China","USSR","Brazil", "Australia"))



###### annotation_custom

df <- data.frame(x = (-3)*(1:10), y = 1:10)
base <- ggplot(df, aes(x, y)) +
  geom_point()
df2 <- data.frame(long = 1 , lat = 1)

g <- ggplotGrob(ggplot(df2, aes(x=long, y=lat)) +
  geom_point() +
  theme(plot.background = element_rect(colour = "black")))

base +annotation_custom(grob = g, xmin = -1, xmax = -10, ymin = 5, ymax = 1)

ggplot(data=US_map, aes(x=long,y=lat))  + geom_polygon(aes(x=long, y=lat,group=group))+
        annotation_custom(grob = g, xmin = -77, xmax = -65, ymin = 25, ymax = 33)





#  putting them all on one graph 

compiledDF = data.frame(scaleYear = outputDF.05$scaleYear+1996, 
                        gas0 = outputDF.05$scaledGasolineConsumption,
                        gas.05 = outputDF.05$scaledGasolineConsumptionWithEVs)
   
compiledDF$gas.1= outputDF.1$scaledGasolineConsumptionWithEVs  
compiledDF$gas.25 = outputDF.25$scaledGasolineConsumptionWithEVs 
compiledDF$gas.5 = outputDF.5$scaledGasolineConsumptionWithEVs
compiledDF$gas.75 = outputDF.75$scaledGasolineConsumptionWithEVs
compiledDF$gas1 = outputDF1$scaledGasolineConsumptionWithEVs
      
ggplot(compiledDF)+geom_line(aes(x=scaleYear,y=gas0, color = "No EVs"), alpha=.5, size =1)+ 
                 geom_line(aes(x=scaleYear, y= gas.05, color = "5%/year"), size =1, alpha=.5)+
                 geom_line(aes(x=scaleYear, y= gas.1, color = "10"), size =1, alpha=.5)+
                 geom_line(aes(x=scaleYear, y= gas.25, color = "25"), size =1, alpha=.5)+
                 geom_line(aes(x=scaleYear, y= gas.5, color= "50"), size =1, alpha=.5)+
                 geom_line(aes(x=scaleYear, y= gas.75, color = "75"), size =1, alpha=.5)+
                 geom_line(aes(x=scaleYear, y= gas1, color = "100"),  size =1, alpha=.5)+ 
                 labs(title="Total US Vehicle Fleet Gasoline Consumption from 1996 to 2050")+
                 xlab("Year")+ylab("Primary Energy")+
                 coord_cartesian(ylim=c(0,2e+10))+
                 scale_y_continuous(breaks=seq(0,2e+10,2.5e+9))+
                 scale_colour_manual("",
                         breaks = c("No EVs","5%/year","10","25","50","75","100"),
                         values = c("No EVs"="black","5%/year"="red",
                                                     "10"="orange", "25"="yellow", "50"="green",
                                                     "75"="blue","100"="purple"))
                 

# cash for clunkers

ccDF = outputDF.05
ccDF$gasolineConsumption.5 = outputDF.5Buying$scaledGasolineConsumption
ccDF$gasolineConsumption1.25 = outputDF1.25Buying$scaledGasolineConsumption
ccDF$gasolineConsumption1.5 = outputDF1.5Buying$scaledGasolineConsumption
ccDF$gasolineConsumption1.75 = outputDF1.75Buying$scaledGasolineConsumption
ccDF$gasolineConsumption2 = outputDF2Buying$scaledGasolineConsumption
ccDF$Year= ccDF$scaleYear+1996

ggplot(ccDF) + geom_line(aes(x= Year, y = scaledGasolineConsumption, color = "BAU"), size = 2)+
                geom_line(aes(x=Year, y= gasolineConsumption.5, color = ".5*BAU"), size = 2)+
                geom_line(aes(x=Year, y= gasolineConsumption1.25, color = "1.25*BAU"), size = 2)+
                geom_line(aes(x=Year, y= gasolineConsumption1.5, color = "1.5*BAU"), size = 2)+
                geom_line(aes(x=Year, y= gasolineConsumption1.75, color = "1.75*BAU"), size = 2)+
                geom_line(aes(x=Year, y= gasolineConsumption2, color = "2*BAU"), size = 2)+
                ggtitle("The effect of changing BAU buying and scrapping rates")+
                ylab("Scaled Gasoline Consumption")+ylim(0,2.5e+10)+
                theme(text=element_text(size=16))#+
                scale_colour_manual("", breaks = c("BAU", ".5*BAU","1.25*BAU","1.5*BAU","1.75*BAU","2*BAU"))+


# contour plots

ggplot()+
    geom_line(data=contourPlot[[1]], aes(x= years, y = totalCarbon, color = ".1, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[2]], aes(x= years, y = totalCarbon, color = ".5, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[3]], aes(x= years, y = totalCarbon, color = ".9, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[4]], aes(x= years, y = totalCarbon, color = ".1, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[5]], aes(x= years, y = totalCarbon, color = ".5, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[6]], aes(x= years, y = totalCarbon, color = ".9, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[7]], aes(x= years, y = totalCarbon, color = ".1, 2070, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[8]], aes(x= years, y = totalCarbon, color = ".5, 2070, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[9]], aes(x= years, y = totalCarbon, color = ".9, 2070, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[10]], aes(x= years, y = totalCarbon, color = ".1, 2030, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[11]], aes(x= years, y = totalCarbon, color = ".5, 2030, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[12]], aes(x= years, y = totalCarbon, color = ".9, 2030, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[13]], aes(x= years, y = totalCarbon, color = ".1, 2050, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[14]], aes(x= years, y = totalCarbon, color = ".5, 2050, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[15]], aes(x= years, y = totalCarbon, color = ".9, 2050, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[16]], aes(x= years, y = totalCarbon, color = ".1, 2070, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[17]], aes(x= years, y = totalCarbon, color = ".5, 2070, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[18]], aes(x= years, y = totalCarbon, color = ".9, 2070, 20"), linetype = "dashed", size = 2, alpha = .7)+
    geom_line(data=contourPlot[[19]], aes(x= years, y = totalCarbon, color = ".1, 2030, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[20]], aes(x= years, y = totalCarbon, color = ".5, 2030, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[21]], aes(x= years, y = totalCarbon, color = ".9, 2030, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[22]], aes(x= years, y = totalCarbon, color = ".1, 2050, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[23]], aes(x= years, y = totalCarbon, color = ".5, 2050, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[24]], aes(x= years, y = totalCarbon, color = ".9, 2050, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[25]], aes(x= years, y = totalCarbon, color = ".1, 2070, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[26]], aes(x= years, y = totalCarbon, color = ".5, 2070, 30"), linetype="dotted", size = 2.5, alpha = .7)+
    geom_line(data=contourPlot[[27]], aes(x= years, y = totalCarbon, color = ".9, 2070, 30"), linetype="dotted", size = 2.5, alpha=.7)+
    ggtitle("Scenario exploring of three variables: year of entry, ceiling, and s-curve length")+
    theme(text=element_text(size = 24))
# contour plots

ggplot()+
    geom_line(data=contourPlot[[1]], aes(x= years, y = totalCarbon, color = ".1, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[2]], aes(x= years, y = totalCarbon, color = ".5, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[3]], aes(x= years, y = totalCarbon, color = ".9, 2030, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[4]], aes(x= years, y = totalCarbon, color = ".1, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[5]], aes(x= years, y = totalCarbon, color = ".5, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[6]], aes(x= years, y = totalCarbon, color = ".9, 2050, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[7]], aes(x= years, y = totalCarbon, color = ".1, 2070, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[8]], aes(x= years, y = totalCarbon, color = ".5, 2070, 10"), size = 1.5, alpha = .7)+
    geom_line(data=contourPlot[[9]], aes(x= years, y = totalCarbon, color = ".9, 2070, 10"), size = 1.5, alpha = .7)+
    ggtitle("Scenario exploring two variables: year of entry and market ceiling")+xlab("Year")+
    theme(text=element_text(size = 24))

# contour: Use the year of entry and the s curves 

filled.contour(x=CP.df$ceils, y=CP.df$ys, z=CP.df$yearSurpassed)

require(plot3D)

M = mesh(CP.df$ceils,CP.df$ys)
M1 = mesh(CP.df$yearSurpassed, CP.df$yearSurpassed)
surf3D(x=M$x, y=M$y, z=M1$x, colkey=FALSE, bty="b2")


### s_curve modulation


ggplot()+
    geom_line(data=SC[[1]], aes(x= years, y = totalCarbon, color = "05"), size = 2, alpha = .7)+
    geom_line(data=SC[[2]], aes(x= years, y = totalCarbon, color = "10"), size = 2, alpha = .7)+
    geom_line(data=SC[[3]], aes(x= years, y = totalCarbon, color = "15"), size = 2, alpha = .7)+
    geom_line(data=SC[[4]], aes(x= years, y = totalCarbon, color = "20"), size = 2, alpha = .7)+
    geom_line(data=SC[[5]], aes(x= years, y = totalCarbon, color = "25"), size = 2, alpha = .7)+
    geom_line(data=SC[[6]], aes(x= years, y = totalCarbon, color = "30"), size = 2, alpha = .7)+
    geom_line(data=SC[[7]], aes(x= years, y = totalCarbon, color = "35"), size = 2, alpha = .7)+
    geom_line(data=SC[[8]], aes(x= years, y = totalCarbon, color = "40"), size = 2, alpha = .7)+
    geom_line(data=SC[[9]], aes(x= years, y = totalCarbon, color = "45"), size = 2, alpha = .7)+
    geom_line(data=SC[[10]], aes(x= years, y = totalCarbon, color = "50"), size = 2, alpha = .7)+
    geom_line(data=SC[[11]], aes(x= years, y = totalCarbon, color = "55"), size = 2, alpha = .7)+
    geom_line(data=SC[[12]], aes(x= years, y = totalCarbon, color = "60"), size = 2, alpha = .7)+
    geom_line(data=SC[[13]], aes(x= years, y = totalCarbon, color = "BAU"), size = 2, alpha = .7)+
    geom_line(data=SC[[14]], aes(x= years, y = totalCarbon, color = "0"), size = 2, alpha = .7)+
    ggtitle("Effect of length of S-curves")+ 
    theme(text = element_text(size = 24))

## capacity plot 

ggplot()+
#    geom_line(data = marketPenetration[[7]], aes(x=years, y= totalCapacityAfterRetirement, color = "Total Capacity"), color = "black", size  =4, alpha = .7)+
#    geom_line(data = marketPenetration[[7]], aes(x=years, y=newCap, color = "New Capacity"), color= "grey62", size = 3, alpha= .7)+
    geom_line(data= marketPenetration[[1]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".25 ceiling, 2030 entry"), color = "springgreen1", size = 3, alpha = .7)+
    geom_line(data= marketPenetration[[2]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".75 ceiling, 2030 entry"), color = "springgreen2", size = 3, alpha = .7)+
    geom_line(data= marketPenetration[[3]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".25 ceiling, 2050 entry"), color = "peachpuff1", size = 3, alpha = .7)+
    geom_line(data= marketPenetration[[4]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".75 ceiling, 2050 entry"), color = "peachpuff2", size = 3, alpha = .7)+
    geom_line(data= marketPenetration[[5]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".25 ceiling, 2070 entry"), color = "forestgreen", size = 3, alpha = .7)+
    geom_line(data= marketPenetration[[6]], aes(x=years, y = fusionGrowth/(totalCapacityAfterRetirement*10^3), color  = ".75 ceiling, 2070 entry"), color = "darkgreen", size = 3, alpha = .7)+
    ggtitle("Total Capacity versus New Capacity")+ theme(text=element_text(size = 24))




# market penetrations 

ggplot()+
    geom_line(data = percent_00_2030, aes(x=years, y = (fusionGrowth/10^3)/totalCapacityAfterRetirement), color = "grey1", size = 2, alpha = .7)+
    geom_line(data = percent_10_2030, aes(x=years, y = (fusionGrowth/10^3)/totalCapacityAfterRetirement), color = "grey2", size = 2, alpha = .7)+
    geom_line(data = percent_50_2030, aes(x=years, y = (fusionGrowth/10^3)/totalCapacityAfterRetirement), color = "grey3", size = 2, alpha = .7)+
    geom_line(data = percent_99_2030, aes(x=years, y = (fusionGrowth/10^3)/totalCapacityAfterRetirement), color = "red", size = 2, alpha = .7)+
    ggtitle("Market Penetration of Fusion")+ theme(text=  element_text(size=24)) + ylab("Percent Penetration")+xlab("Year")

# capacity 
ggplot()+
    geom_line(data = percent_00_2030, aes(x=years, y = (fusionGrowth/10^3)), color = "grey1", size = 2, alpha = .7)+
    geom_line(data = percent_10_2030, aes(x=years, y = (fusionGrowth/10^3)), color = "grey2", size = 2, alpha = .7)+
    geom_line(data = percent_50_2030, aes(x=years, y = (fusionGrowth/10^3)), color = "grey3", size = 2, alpha = .7)+
    geom_line(data = percent_99_2030, aes(x=years, y = (fusionGrowth/10^3)), color = "red", size = 2, alpha = .7)+
    ggtitle("Capacity Growth of Fusion")+ theme(text=  element_text(size=24)) + ylab("Capacity (GW)")+
    xlab("Year")

# sensitivity analysis

ggplot()+
    geom_line(data= p50_2030df, aes(x= years, y = totalCarbon, group = element), size = .00005, alpha = .7)+
    geom_line(data = p50_2030_mean, aes(x=years, y=totalCarbon), size = 1, color = "red")+
    geom_line(data= pBAUdf, aes(x= years, y = totalCarbon, group = element), size = .00005, alpha = .7)+
    geom_line(data = pBAU_mean, aes(x=years, y=totalCarbon), size = 1, color = "red")+
    geom_line(data= p10_2030df, aes(x= years, y = totalCarbon, group = element), size = .00005, alpha = .7)+
    geom_line(data = p10_2030_mean, aes(x=years, y=totalCarbon), size = 1, color = "red")+
    geom_line(data= p99_2030df, aes(x= years, y = totalCarbon, group = element), size = .00005, alpha = .7)+
    geom_line(data = p99_2030_mean, aes(x=years, y=totalCarbon), size = 1, color = "red")+
    ylim(0,2.2)+ggtitle("Sensitivity Analysis on the four carbon scenarios")+
    theme(text= element_text(size = 24))


## sensitivity on first 10 years 

ggplot()+
    geom_line(data=CA2030_array[CA2030_array$years%in%c(2030:2040),], aes(x=years-2030, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "red4")+
    geom_line(data = CA2030_mean[CA2030_mean$years%in%c(2030:2040),], aes(x=years-2030, y = newFusionAdditions), size = 2, color = "red")+
    geom_line(data=CA2050_array[CA2050_array$years%in%c(2050:2060),], aes(x=years-2050, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "green4")+
    geom_line(data = CA2050_mean[CA2050_mean$years%in%c(2050:2060),], aes(x=years-2050, y = newFusionAdditions), size = 2, color = "green")+
    geom_line(data=CA2070_array[CA2070_array$years%in%c(2070:2080),], aes(x=years-2070, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "blue4")+
    geom_line(data = CA2070_mean[CA2070_mean$years%in%c(2070:2080),], aes(x=years-2070, y = newFusionAdditions), size = 2, color = "blue")+
    xlim(1,10)+ ylab("Fusion Addition (MW)")+ xlab("Years since fusion starts")+theme(text= element_text(size = 24))+
    annotate("text", x = 2.5, y=c(10000,7500,5000), label=c("2070 start","2050 start","2030 start"), color = c("blue", "green", "red"),size=10)+
    annotate("text", x=2.5, y= 12500, label =c("(Scaled to starting year 2030, 2050, 2070)"), color = "black", size = 10)

years2030a = CA2030_array$years%in%CA2030_array$years[which(CA2030_array$newFusionAdditions>0)[c(1:10)]]
years2050a = CA2050_array$years%in%CA2050_array$years[which(CA2050_array$newFusionAdditions>0)[c(1:10)]]
years2070a = CA2070_array$years%in%CA2070_array$years[which(CA2070_array$newFusionAdditions>0)[c(1:10)]]
years2030m = CA2030_mean$years%in%CA2030_mean$years[which(CA2030_mean$newFusionAdditions>0)[c(1:10)]]
years2050m = CA2050_mean$years%in%CA2050_mean$years[which(CA2050_mean$newFusionAdditions>0)[c(1:10)]]
years2070m = CA2070_mean$years%in%CA2070_mean$years[which(CA2070_mean$newFusionAdditions>0)[c(1:10)]]

ggplot()+
    geom_line(data=CA2030_array[years2030a,], aes(x=years-2033, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "red4")+
    geom_line(data = CA2030_mean[years2030m,], aes(x=years-2033, y = newFusionAdditions), size = 2, color = "red")+
    geom_line(data=CA2050_array[years2050a,], aes(x=years-2050, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "green4")+
    geom_line(data = CA2050_mean[years2050m,], aes(x=years-2050, y = newFusionAdditions), size = 2, color = "green")+
    geom_line(data=CA2070_array[years2070a,], aes(x=years-2070, y=newFusionAdditions, group = element), size = .00005, alpha= .7, color = "blue4")+
    geom_line(data = CA2070_mean[years2070m,], aes(x=years-2070, y = newFusionAdditions), size = 2, color = "blue")+
    ylab("Fusion Addition (MW)")+ xlab("Years since fusion starts")+theme(text= element_text(size = 24))+
    annotate("text", x = 2.5, y=c(10000,7500,5000), label=c("2070 start","2050 start","2030 start"), color = c("blue", "green", "red"),size=10)+
    annotate("text", x=2.5, y= 12500, label =c("(Scaled to first year > 0)"), color = "black", size = 10)


##### nuclear sales vs. percent retirment

ggplot()+
    geom_line(data = data.frame(Sales = sales, Saturation = marketPen2100), aes(x=Sales, y = Saturation), size = 2, color = "blue")+
    ylab("Saturation at year 2100")+xlab("Maximum sales percentage")+ theme(text=element_text(size = 30))




### testing 

testDF = data.frame(x=c(1:10), y = c(1:10)^2)

ggplot()+
    geom_line(data = testDF,aes(x=c(1:length(y)), y=c(NA,diff(y))))



##### 

ggplotly(ggplot()+
    geom_line(data= percent_10_2030, aes(x=years, y= fusionGrowth, color = "10/2030"))+
    geom_line(data= percent_50_2030, aes(x=years, y= fusionGrowth, color = "50/2030"))+
    geom_line(data= percent_99_2030, aes(x=years, y= fusionGrowth, color = "99/2030"))+
    geom_line(data= percent_10_2050, aes(x=years, y= fusionGrowth, color = "10/2050"))+
    geom_line(data= percent_50_2050, aes(x=years, y= fusionGrowth, color = "50/2050"))+
    geom_line(data= percent_10_2070, aes(x=years, y= fusionGrowth, color = "10/2070"))+
    geom_line(data= percent_50_2070, aes(x=years, y= fusionGrowth, color = "50/2070")))


# new demand growth

ggplot(percent_0)+
    geom_ribbon(aes(x = years, ymin = 0, ymax = replacementRetirements/1000,
        fill = "Replacement Retirements"))+
    geom_ribbon(aes(x = years, ymin = replacementRetirements/1000, 
        ymax = demandGrowth+replacementRetirements/1000, 
        fill = "Demand Growth"))+
    ggsave("7_11_type_of_addition.pdf")

ggplot(percent_0)+
    geom_line(aes(x = years, y = replacementRetirements/1000))+
    geom_line(aes(x = years, y = demandGrowth))

write.csv(percent_0, file = "out/percent_0_updated.csv")


