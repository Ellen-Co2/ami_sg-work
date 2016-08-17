dat = read.csv("can_even.csv.txt",header = T)

require("tseries")
require("forecast")
#tr = dat[c(1:(12*24*24)),]
#tst = dat[c((12*24*25):nrow(dat)),]
#ts(tr[,2],frequency = nrow(tr)/24)->tr.ts
####---------identify cycles using FFT-----------####
find.freq <- function(f.ts){
  abs(fft(f.ts)/sqrt(length(f.ts)))^2-> I
  Pow = I[1:as.integer(length(f.ts)/2)]
  FREQ =(0:as.integer((length(Pow)-1)))/length(Pow)
  plot(FREQ,Pow,type="l")
  T1 <- data.frame(array(c(Pow,FREQ),dim=c(length(Pow),2)))
  colnames(T1)<- c("Power","Frequency")
  
  return (T1)
}
t1<-find.freq(dat[,2]) ## power 2nd has T=144/72
t2<- find.freq(diff(dat[,2]))
pow <- order(t2$Power,decreasing = T) # power highest T=28.79/24
ff1 <- 1/t2$Frequency[pow[1]]
#Using diff the highest around 28

ms.tr <- msts(dat[,2],c(12,(12*24*7)))
plot.ts(x = ms.tr)
acf(ms.tr,lag.max = 7*24*12,main= "ACF for Jun 15-Jul 15") # approximately following 1 day cycle and one week
## using fourier terms to model cycles##
# define multiple cycles as hourly and weekly, freq= c(12, (12*24*7))
#find optimal fourier K value

aicc.tmp <- NULL
aicc.val <- NULL
for (i in 1:6) {
  for (j in 1:3) {
    #f.day <- fourier(ms.tr, i )
    #f.wk <- fourier(ms.tr, j )
    x.fourier <- fourier(ms.tr,c(i,j))
    fitmd <- auto.arima(ms.tr, D = 0, max.P = 0, max.Q = 0, xreg = x.fourier,max.d=2, ic="bic", allowdrift=TRUE)
    aicc.tmp <- cbind(i, j , fitmd$aicc)
    aicc.val <- rbind(aicc.val,aicc.tmp)
  }
}
colnames(aicc.val) <- c("Fourier_hr_terms","Fourier_wk_terms","bic")
aicc.val <- data.frame(aicc.val)
min.bic <- min(aicc.val$bic)
min.f <-aicc.val[which(aicc.val$bic == min.bic),]
min.f
# the best K for Fourier is hr=6 wk=1
#### forecast with the best model
x.f = fourier(ms.tr,c(6,1))
x.fh = fourier(ms.tr,c(6,1), h = 12*24) #forecasting 24 hrs
best_md = auto.arima(ms.tr, D = 0, max.P = 0, max.Q = 0, xreg = x.f, max.d=3, ic="bic", allowdrift=TRUE)
b_fcast = forecast(best_md, xreg = x.fh, h = 12*24)


#### fit with daily and wkly cycles ####
ms.tr1 <- msts(dat[,2],c((12*24),(12*24*7)))
bic.tmp <- NULL
bic.val <- NULL
for (i in 1:6) {# cycle total 31 
  for (j in 1:3) {
    #f.day <- fourier(ms.tr, i )
    #f.wk <- fourier(ms.tr, j )
    x.dayf <- fourier(ms.tr1,c(i,j))
    d.md <- auto.arima(ms.tr1, D = 0, max.P = 0, max.Q = 0, xreg = x.dayf, max.d = 3, ic="bic", allowdrift=TRUE)
    bic.tmp <- cbind(i, j , d.md$bic)
    bic.val <- rbind(bic.val,bic.tmp)
  }
}
colnames(bic.val) <- c("Fourier_day_terms","Fourier_wk_terms","bic")
bic.val <- data.frame(bic.val)
min.bicd <- min(bic.val$bic)
min.fd <-bic.val[which(bic.val$bic == min.bicd),]
min.fd
# the best K for Fourier is hr=6 wk=1
#### forecast with the best model
x.fd = fourier(ms.tr1,c(6,1))
x.fdh = fourier(ms.tr1,c(6,1), h = 12*24) #forecasting 24 hrs
best_md.day = auto.arima(ms.tr1, D = 0, max.P = 0, max.Q = 0, xreg = x.fd, max.d=3, ic="bic", allowdrift=TRUE)
b_dfcast = forecast(best_md.day, xreg = x.fdh, h = 12*24)
Acf(best_md.day$residuals)
