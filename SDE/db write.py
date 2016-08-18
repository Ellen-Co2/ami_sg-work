import sqlite3
from datetime import datetime, timedelta
from pandas import DataFrame, Series
import numpy as np
import pandas as pd

### input the building dimensions
dim = {"SDE1-02":[1227.0858,1730.8369],
"SDE1-03":[275.0,394.0],
"SDE1-04":[1065.6272,1503.0952],
"SDE1-05":[1227.0858,1730.8369],
"SDE2-01":[671.634,948.0622],
"SDE2-02":[736.25146,1038.5022],
"SDE2-03":[673.7935,951.3015],
"SDE3-01" :[1214.772,1734.6945],
"SDE3-02": [2018.2332,2882.037],
"SDE3-03" :[1345.4888,1921.358],
"SDE3-04":[683.8,474.7]} #[length,width]=> [ycor,xcor]
### function to mark the out of building entries as 1
'''
def out_dim(s):
    bld = str(s["bldid"])
    if(0< s["xcor"] <= dim[bld][1] and 0< s["ycor"] <= dim[bld][0]):
            return pd.Series(dict(out=0))
    else: 
            return pd.Series(dict(out=1))
'''
### function to parse datetime and make hrfir/ hrlas/ interval
def diff(col):
    t_fun = lambda x : datetime.strptime(x[0:19],'%Y-%m-%dT%H:%M:%S')
    #secs = []
    fir_t = []
    las_t = []
    for i, row in enumerate(col.values):
        fir = t_fun(col.firstlocatedtime[i])
        las = t_fun(col.lastlocatedtime[i])
        #dif = timedelta.total_seconds(las - fir)
        #secs.append(dif)
        fir_t.append(fir)
        las_t.append(las)
    #print "interval len: %s" %len(secs)
    col['firstlocatedtime'] = fir_t
    col['lastlocatedtime'] = las_t
    #col['interval'] = secs
from sqlalchemy import create_engine 
disk_engine = create_engine('sqlite:///new.sqlite')
conn = sqlite3.connect('new.sqlite')
#cur = conn.cursor()
#cur.execute('''DROP TABLE if EXISTS wifi''')
import glob, os
ans = raw_input('Please enter the full directory for files:')
try:
    dirname = str(ans)
    os.chdir(dirname)
except:
    dirname = "/Users/AAA218/Desktop/ami_sg/SDE.csv/"
    print'not valid, using defaults: %s' % dirname
    os.chdir(dirname)
l = list()
for file in glob.glob("*.csv"):
    if file.startswith('SDE'):
        l.append(file)

for f in l:
    fname = dirname + f
    #index_start = 1
    #if f == 'SDE1_03.csv': break
    for df in pd.read_csv(fname, header = 0,sep=',',low_memory= False,iterator=True):
        #print df.columns
        names = ["sgtime", "mac","guestid","status", "bldid", "xcor", "ycor","currenttime","firstlocatedtime","lastlocatedtime"]
        df.columns = names
        #print "new_____", df.sgtime[0:10]
        try: 
            df['sgtime'] = pd.to_datetime(df["sgtime"])
            print "parse the date and make the interval"
            st1 = datetime.now()
            diff(df)
            st2 = datetime.now()
            print "used %s sec.." %timedelta.total_seconds(st2 - st1)
        except:
            print "skip file: %s" % fname
            continue
        
        print "reformat the building id...."
        bld = df["bldid"].apply(lambda x: x[-7:]).copy()
        df['bldid'] = bld
        # if out then 1
        print "create Out dim mark...0 means in-dim"
        st1 = datetime.now()
        out = []
        for i, row in enumerate(df.values):
            temp = str(df.bldid[i])
            if(0< df.xcor[i] <= dim[temp][1] and 0< df.ycor[i] <= dim[temp][0]):
                out_temp = 0
            else:
                out_temp = 1
            out.append(out_temp)
        df["out"] = out
        st2 = datetime.now()
        print "used %s sec.." %timedelta.total_seconds(st2 - st1)
        #print "map the status PROBING -> 0 ASSOCIATED -> 1 UNKNOWN-> -1....."
        #df.status.replace({'PROBING','ASSOCIATED','UNKNOWN'},value= {0,1,-1},inplace=True)
        df.drop(['guestid','currenttime'], axis=1, inplace=True)
        print df.head()
        print 'write to db %s' %f
        df.to_sql(name='wifi',index=False,con=conn,if_exists='append',dtype={"sgtime": "DATETIME", "status":"CHAR(20)", "mac": "CHAR(20)","bldid": "CHAR(20)"," xcor ":"NUMERIC","ycor":" NUMERIC","firstlocatedtime":" DATETIME","lastlocatedtime":"DATETIME", "out": "INTEGER"})
# 2650553 total


