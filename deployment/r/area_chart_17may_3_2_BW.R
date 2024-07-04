#Load some packages
library(ggplot2)
library(reshape2)
#Plot 2030/10
fleet = read.csv('out/data/2030_10_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p1 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='a) 2030 fusion entry, 10% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#000000", "#202020","#404040", "#606060", "#808080","#A0A0A0", "#B0B0B0","#C0C0C0", "#D0D0D0","#E0E0E0")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  guides(color=FALSE, fill=guide_legend(reverse=TRUE)) +
  theme(legend.position="bottom") +
  theme(panel.background = element_blank())
#Plot 2030/50
fleet = read.csv('out/data/2030_50_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p2 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='b) 2030 fusion entry, 50% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#0F0F0F", "#787878","#7a071a", "#000d9f", "#cb435a","#f9ff00", "#0026ff","#00b1ff", "#ffb700","#ff002b")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  theme(legend.position="none")
#Plot 2050/10
fleet = read.csv('out/data/2050_10_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p3 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='c) 2050 fusion entry, 10% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#0F0F0F", "#787878","#7a071a", "#000d9f", "#cb435a","#f9ff00", "#0026ff","#00b1ff", "#ffb700","#ff002b")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  theme(legend.position="none")
#Plot 2050/50
fleet = read.csv('out/data/2050_50_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p4 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='d) 2050 fusion entry, 50% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#0F0F0F", "#787878","#7a071a", "#000d9f", "#cb435a","#f9ff00", "#0026ff","#00b1ff", "#ffb700","#ff002b")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  theme(legend.position="none")
#Plot 2070/10
fleet = read.csv('out/2070_10_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p5 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='e) 2070 fusion entry, 10% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#0F0F0F", "#787878","#7a071a", "#000d9f", "#cb435a","#f9ff00", "#0026ff","#00b1ff", "#ffb700","#ff002b")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  theme(legend.position="none")
#Plot 2070/50
fleet = read.csv('out/2070_50_mean.csv')
fleet2 = fleet[,c(2,7:16)]
fleet2 = fleet2[,c(1,10,5,2,7,6,4,9,3,8,11)]
colnames(fleet2) <- c("Years", "Coal", "Oil", "NGCC", "NGCT", "NGST", "Fission", "Hydropower", "Wind", "Solar", "Fusion")
fleet3 <- melt(fleet2, id.vars = 'Years', variable.name = 'Technology')
p6 <- ggplot(fleet3, aes(x=Years, y=value/1000)) + 
  geom_area(aes(fill = Technology), position='stack', alpha=.8) +
  geom_label(aes(2032, 1465, label='f) 2070 fusion entry, 50% ceiling'), size=2) +
  #Uncomment the below line to use color
  scale_fill_manual(values=c("#0F0F0F", "#787878","#7a071a", "#000d9f", "#cb435a","#f9ff00", "#0026ff","#00b1ff", "#ffb700","#ff002b")) +
  #Uncomment the two lines below to use greyscale
  #scale_fill_manual(values=gray(seq(0.1,0.9,length=10))) +
  #scale_colour_manual(values=c("black","black","black","black","black","black","black","black","black","black")) +
  xlab('Year') +
  ylab('Installed Capacity (GW)') +
  ylim(0,1500) +
  theme(text = element_text(size=10)) +
  theme(legend.position="none")
##Helper Function
get_legend<-function(myggplot){
  tmp <- ggplot_gtable(ggplot_build(myggplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)
}
##Save p1 legend
legend <- get_legend(p1)
#Turn Legend Off
p1 <- p1 + theme(legend.position="none")
## Plot Grid
require(grid)
library(gridExtra)

png(paste("out/graphs/mean_stacked2bw.png",sep=''), width=174, height=174, units='mm', res=300)
p7 <- grid.arrange(arrangeGrob(p1,p2,nrow=1),arrangeGrob(p3,p4,nrow=1),arrangeGrob(p5,p6,nrow=1),legend,nrow=4,heights=c(2.5,2.5,2.5,1))
dev.off()
