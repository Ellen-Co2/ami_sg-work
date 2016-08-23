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
try:
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
    dirname = "/Users/AAA218/Desktop/amifull_sg/SDE.csv/"
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
testf = pd.read_sql_query('SELECT mac, bldid, xcor, ycor ,lastlocatedtime,firstlocatedtime,sgtime,status,out FROM wifi ',disk_engine)
us_dict = dict()
interv = list()
mov = list()
distance = list()
#testf = DataFrame({'mac':["ma","tec","sa","tec","ma"],'bld':["b1","b2","b3","b4","b1"],'xcor':[200,300,30,40,300],"ycor":[100,200,30,50,400],"lastlocatedtime":["2016-04-16 00:00:01","2016-04-16 02:40:01","2016-04-16 07:50:01","2016-04-16 09:35:02","2016-04-16 09:40:01"]},columns=["mac", "bld","xcor", "ycor" ,"lastlocatedtime" ])

testf["lastlocatedtime"] = pd.to_datetime(testf["lastlocatedtime"])
#print testf
for i , row in enumerate(testf.values):
    #update the last row id of device
    if (us_dict.get(row[0]) == None):
        us_dict[row[0]] = i 
        interv.append(0)
        mov.append('first')
        distance.append(float('NaN'))
        #print mov,"\ndistance:\n",distance
        continue
    else:
        # For the mac with prev record, first store and update the record
        prev_ind = us_dict.get(row[0])
        us_dict[row[0]] = i 
        prev_bld = testf.iloc[prev_ind,1]
        prev_t = testf.iloc[prev_ind,4]
        prev_x = testf.iloc[prev_ind,2]
        prev_y = testf.iloc[prev_ind,3]
        dif = timedelta.total_seconds(row[4] - prev_t)
        #print prev_ind,prev_t,prev_x,prev_y,prev_bld
        interv.append(dif)
        #print interv
        if (prev_bld != row[1]): 
            mov.append(prev_bld)
            distance.append(float('NaN'))
        else:
            dista = round(np.sqrt((prev_x-row[2])**2 + (prev_y-row[3])**2),2)
            distance.append(dista)
            if ((dista <= 1800)&(dif <= 3600)): #not moving exceeding 30*30 feet and disappear 1 hrs
                mov.append('stay')
            else:
                mov.append('left')
print "mov:\n",mov[0:10],"\ndict:\n",us_dict[0:15],"distance:\n",distance[-10:],"\ninterv:\n",interv[-5:]
testf["interv"] = interv
testf["movement"] = mov
testf["distance"] = distance
testf.to_sql(name='Adding',index=False,con=conn,if_exists='DROP',dtype={ "mac": "CHAR(20)","bldid": "CHAR(20)"," xcor ":"NUMERIC","ycor":" NUMERIC","lastlocatedtime":"DATETIME","firstlocatedtime":" DATETIME", "sgtime": "DATETIME", "status":"CHAR(20)","out": "INTEGER","interval": "INTEGER","movement": "CHAR(20","Distance":"NUMERIC"})

