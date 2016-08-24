dat = read.csv("p_5min.csv",header=TRUE)
attach(dat)
strptime(time,format = "%Y-%m-%d %H:%M:%S")->t1
dat$time<-t1
str(dat)
require(ggplot2)
require(scales)
library(cowplot)
min(dat[dat$bldid=='SDE1-02','mac'])
###____________plot mac numbers__________####
p =ggplot(data=dat[dat$bldid=='SDE1-02',], aes(x=sgtime, y=mac)) +geom_line(size=0.3)#+facet_wrap(~bldid,ncol=2,scales = "fixed")
a = p+ylab('count of users')+scale_x_datetime(name='periods from start(Apr.16-00:00 Sat)',date_labels ="%H",date_breaks="4 hours")
p = a+theme_bw()+ggtitle("Devices' number distribution in SDE1-02")
tiff('time mac sde1-02.tiff',width=1800,height = 1000,units = "px",res=120,compression = "lzw")
p
dev.off()
####________plot median staying________######
p =ggplot(data=dat, aes(x=dat$sgtime, y=dat$interval))+scale_x_datetime(name='periods from start(Apr.16.Sat)',date_labels ="%a-%H",date_breaks="20 hours")+xlab('periods from start(Apr.16.Sat)')+geom_line(size=0.5)+facet_wrap(~bldid,ncol=2,scales = "free_y")
b = p+ylab('median of intervals in 5 mins')
p = b+theme_bw()+ggtitle("Devices' staying time distribution")
p
tiff('time staying5.tiff',width=1800,height = 1600,units = "px",compression = "lzw",res=120)
p
dev.off()
####_________plot x,y std________________####
require(reshape2)
plodat = melt(dat[,c(1,2,5,6)],id =c("t_grp","bldid"))
str(plodat)
p =ggplot(data=plodat, aes(x=t_grp,y=value,group=variable,colour=factor(variable)))+geom_line(size=0.5)+facet_wrap(~bldid,ncol=3,scales = "free_y")+scale_x_datetime(name='periods from start(Apr.16.Sat)',date_labels ="%a-%H",date_breaks="20 hours")+xlab('periods from start(Apr.16.Sat)')
b = p+ylab('standard deviations in x/y axis within 5mins')
p = b+theme(plot.title = element_text(size = rel(1), colour = "black"),panel.grid=element_line(colour="grey"))+ggtitle("Devices' cordinates sd distribution")
p
tiff('cordinates sd 5 min.tiff',width=1800,height = 1600,units = "px",compression = "lzw",res=120)
p
dev.off()
####_______________plot mac count with variations___________####
macdat = read.csv("mac_count.csv",header=TRUE)
summary(macdat)
##________plot for interval ______________####
plodat<-macdat[!is.na(macdat$xcor)&(macdat$xcor>0)&(macdat$ycor>0)&(0<macdat$interval)&(macdat$interval<180),]
summary(plodat)
plodat1 <-macdat[!is.na(macdat$xcor)&(0<macdat$interval)&(macdat$interval<1000),]
p1 <-ggplot(data=plodat1,aes(x=interval))+geom_histogram(aes(fill = ..count..,y= ..density..),binwidth = 25)+scale_fill_gradient("Count", low = "skyblue", high = "red")+geom_density(color="darkgrey")
p1 <-p1 +scale_x_continuous(breaks=seq(0,1000,200))+xlab('interval in 0-1000sec(95.7%lower)')
p2 <-ggplot(data=plodat, aes(x=interval))+geom_histogram(aes(fill = ..count..,y= ..density..),binwidth = 1)+scale_fill_gradient("Count", low = "skyblue", high = "red")+geom_density(color="darkgrey")
p2 <- p2+scale_x_continuous(breaks=seq(0,180,15))
p3 <- ggplot(data=macdat[!is.na(macdat$xcor)&(macdat$xcor>0),], aes(x=xcor))+geom_histogram(aes(fill = ..count..,y= ..density..),binwidth = 1)+scale_fill_gradient("Count", low = "skyblue", high = "red")+geom_density()
p3 <- p3+xlab("standard deviation at x direction(above 0 subset of 52%)")
p4 <- ggplot(data=macdat[!is.na(macdat$ycor)&(macdat$ycor>0),], aes(x=ycor))+geom_histogram(aes(fill = ..count..,y= ..density..),binwidth = 1)+scale_fill_gradient("Count", low = "skyblue", high = "red")+geom_density()
p4 <- p4+xlab("standard deviation at y direction(above 0 subset of 51.85%)")
tiff('mac intervals.tiff',width=1800,height = 1000,units = "px",res=120)
plot_grid(p1, p2, p3, p4, ncol=2)
dev.off()
####_________places&appear times____________####
place <-ggplot(data=macdat, aes(x=bldid))+geom_histogram(aes(fill = ..count..),binwidth = 1)+scale_fill_gradient("Count", low = "skyblue", high = "red")+xlab("spotted building number")+scale_x_continuous(breaks=seq(0,11,1))
times <-ggplot(data=macdat[macdat$sgtime<120,], aes(x=sgtime))+geom_histogram(aes(fill = ..count..),binwidth = 1)+scale_fill_gradient("Count", low = "skyblue", high = "red")+xlab("spotted total numbers(below 95% subset)")+scale_x_continuous(breaks=seq(0,120,10))
tiff('mac spotted.tiff',width=1800,height = 500,units = "px",res=120)
plot_grid(place,times)
dev.off()
