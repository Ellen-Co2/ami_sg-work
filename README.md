### ami_sg-work
1. [Canteen] contains the series data for canteen wifi
  * canteen.csv: original combined Jun 15- July 15
  * canteen even.csv: sorting with sampling rate 5 mins
  * canteen.ipynb: sampling rate merging using notebook
  * .R : find frequency, basic ARIMAX using fourier predictors
  * .Rmd:
    - find.freq: use fft to find max power of frequency as predictors
    - find.k: find optimal K for fourier combinations
2. [SDE] contains the [plots] and codes:
  * __test1.json__: raw data entries in JSON format
  * __jsontest.ipynb__: data exploring, basic infos related to each fields;
  * __features.ipynb__: feature exploring: distribution of "stationary" "out boundary" devices, mean shift for clustering in 30 mins, snap shot plots
  * __db write.py__: to write each floor into .sqlite database(need to modify with directory and table names) plus simple preprocessing(adding "interval", "out", parsing time)
  * __identify.py__: filtering out the unusual records' mac address and store them(first records 20mins before the first located time)
  * __treat train.py__: produce train data for prediction in crowd level with predictors like "PROBING" "ASSOCIATED" "Interval" ect.. 
      
     > in "interval" use the median excluding the "lost" ones identified before
  * __visplotly.ipynb__: interactive plots for device numbers and devices movements in specific time
  * __plotting.r__: generat plots
  
  > other csv files through the process mostly related to aggregation

> Useful links related to time series models:
  1. General procedure for [ARIMA]
  2. [ARIMAX]
  3. [Plottings]

> For predicting the SDEs:
  [Panel data]


[Canteen]: https://github.com/Ellen-Co2/ami_sg-work/tree/editing/canteen
[SDE]: https://github.com/Ellen-Co2/ami_sg-work/tree/editing/SDE
[plots]: https://github.com/Ellen-Co2/ami_sg-work/tree/editing/SDE/plots
[ARIMA]: https://www.otexts.org/fpp/8/7
[ARIMAX]: http://robjhyndman.com/hyndsight/arimax/
[Plottings]: http://librestats.com/2012/06/11/autoplot-graphical-methods-with-ggplot2/
[Panel data]: http://www.princeton.edu/~otorres/Panel101R.pdf
