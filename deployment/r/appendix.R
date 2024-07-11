# using the combined Efficiency metric
# autoregression 
fuelDF$CombE_1= fuelDF$CombE[c(2:nrow(fuelDF),NA)]

#indicator after 2005
mod1= bayesglm(CombE~scaleYear*after2005, data=fuelDF[fuelDF$VehicleType=="Car SUV",])
display(mod1)

# sinusoidal element 
ssp <- spectrum(fuelDF$CombE)  
per <- 1/ssp$freq[ssp$spec==max(ssp$spec)]
reslm <- bayesglm(CombE ~ sin(2*pi/per*scaleYear)+cos(2*pi/per*scaleYear)+
                               sin(4*pi/per*scaleYear)+cos(4*pi/per*scaleYear)+
                               scaleYear+VehicleType, data=fuelDF)
display(reslm)



