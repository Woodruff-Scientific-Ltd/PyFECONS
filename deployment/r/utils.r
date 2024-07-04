######### utils.r

#### 1. function to convert energy (TWh) to kg of carbon output

energyTWhToCarbonOutputKG= function(fleet_t, typeChars, percent_CCS){
	carbon = fleet_t$energy*typeChars[as.character(fleet_t$type),"BTUFuel/kWhelec"]*
        typeChars[as.character(fleet_t$type),"kgCO2perMMBTU"]*10^(-6)*10^9 ## 10^-6 for BTU-> MMBTU, 10^9 for TW -> kW
    carbon=carbon*(1-percent_CCS)
   	birthAdd= (fleet_t$age==1)
    carbon[birthAdd]= carbon[birthAdd]+typeChars[fleet_t$type[birthAdd], "initialCarbonPerMW"]*fleet_t$capacity[birthAdd]
    return(carbon)
    }

#### 2. function to convert capacity to energy 

capacityMWToEnergyTWh = function(fleet_t, typeChars){
	return(fleet_t$capacity*typeChars[as.character(fleet_t$type),"CapFactor"]*8760/(10^2*10^6)) # assuming percents are in (0,100)  
}

#### 3. convert kg to gigatonnes

kgToGTons = function(kgs){
	return(kgs*10^(-12))
}

#### 4. moving average function 

mav <- function(x,n=5){filter(x,rep(1/n,n), sides=2)}

#### 5. s-curve forumation

s_curve = function(T_ADOPT, k, t){
	return(k/(1+exp((log(1/19)-log(19))/T_ADOPT*(t-T_ADOPT))))
}

#### 5a. testing s-curve formulation 

ggplot()+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=5, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue")+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=10, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue")+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=20, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue1")+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=30, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue2")+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=40, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue3")+
	geom_line(aes(x=c(-25:100), y=s_curve(T_ADOPT=50, k=1, t=c(-25:100))), alpha=.7, size = 2, color = "royalblue4")+
	ggtitle("Sample S-curves")+ylab("Percent Penetration")+ylim(0,1)+xlab("Time")+
	theme(text= element_text(size=24))


