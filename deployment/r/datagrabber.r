require(openxlsx)
require(maps)


load("out/sim.rdata")

data = read.xlsx("data/generators_new.xlsx", sheet= "Operable", startRow = 2)

currentGen$Utility.Name = data$Plant.Name[as.numeric(row.names(currentGen))]

temp.data=currentGen[currentGen$type%in%c("PV", "Wind", "SolarThermal")&currentGen$age<2,]

write.csv(temp.data, "out/data/wind_solar_CSP.csv")
