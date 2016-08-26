from datetime import datetime, timedelta
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine 

disk_engine = create_engine('sqlite:////Users/AAA218/Desktop/amifull_sg/new.sqlite')
conn = sqlite3.connect('new.sqlite')
cur = conn.cursor()
#cur.execute('''DROP TABLE if EXISTS wifi''')

testf = pd.read_sql_query('SELECT mac, bldid, xcor, ycor ,lastlocatedtime,firstlocatedtime,sgtime,status,out FROM wifi LIMIT 2000',disk_engine)
us_dict = dict()
interv = list()
mov = list()
distance = list()
testf = DataFrame({'mac':["ma","tec","sa","tec","ma"],'bld':["b1","b2","b3","b4","b1"],'xcor':[200,300,30,40,300],"ycor":[100,200,30,50,400],"lastlocatedtime":["2016-04-16 00:00:01","2016-04-16 02:40:01","2016-04-16 07:50:01","2016-04-16 01:35:02","2016-04-16 09:40:01"]},columns=["mac", "bld","xcor", "ycor" ,"lastlocatedtime" ])
P1 = datetime.now()
testf["lastlocatedtime"] = pd.to_datetime(testf["lastlocatedtime"])
#print testf
for i , row in enumerate(testf.values):
    #update the last row id of device
    if (us_dict.get(row[0]) == None):
        us_dict[row[0]] = i + testf.index[0] #in case subset
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
#print "mov:\n",mov[0:10],"\ndict:\n",us_dict[0:15],"distance:\n",distance[-10:],"\ninterv:\n",interv[-5:]
testf["interval"] = interv
testf["movement"] = mov
testf["distance"] = distance
P2 = datetime.now()-P1
print "total time: ",P2
testf.to_sql(name='wifinew',index=False,con=conn,if_exists='replace',dtype={ "mac": "CHAR(20)","bldid": "CHAR(20)"," xcor ":"NUMERIC","ycor":" NUMERIC","lastlocatedtime":"DATETIME","firstlocatedtime":" DATETIME", "sgtime": "DATETIME", "status":"CHAR(20)","out": "INTEGER","interval": "INTEGER","movement": "CHAR(20","distance":"NUMERIC"})







