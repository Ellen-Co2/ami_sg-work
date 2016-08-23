import sqlite3
import re
from datetime import datetime, timedelta
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import dateutil.parser as parser

conn = sqlite3.connect('new.sqlite')
from sqlalchemy import create_engine 
disk_engine = create_engine('sqlite:///new.sqlite')

import glob, os
ans = raw_input('Please enter the full directory for files:')
try:
    dirname = str(ans)
    os.chdir(dirname)
except:
    dirname = "/Users/AAA218/Desktop/ami_sg/lost/"
    print'not valid, using defaults: %s' % dirname
    os.chdir(dirname)
l = list()
for file in glob.glob("*.csv"):
    if file.startswith('SDE'):
        l.append(file)

for f in l:
    fname = '/Users/AAA218/Desktop/ami_sg/lost/' + f
    #index_start = 1
    for df in pd.read_csv(fname, header = 0,sep=',',low_memory= False,iterator=True):
        #print df.columns
        names = ["mac", "firstlocatedtime","status","sgtime"]
        df.columns = names
        #print "new_____", df.sgtime[0:10]
        try: 
            df['sgtime'] = pd.to_datetime(df["sgtime"])
            df['firstlocatedtime'] =  pd.to_datetime(df["firstlocatedtime"])
        except:
            print "skip file: %s" % fname
            continue
        #print "map the status PROBING -> 0 ASSOCIATED -> 1 UNKNOWN-> -1....."
        #df.status.replace({'PROBING','ASSOCIATED','UNKNOWN'},value= {0,1,-1},inplace=True)
        print 'write to db %s' %f
        df.to_sql(name='lost',index=False,con=conn,if_exists='append',dtype={ "mac": "CHAR(20)","sgtime": "DATETIME","status":"CHAR(20)","firstlocatedtime":" DATETIME",})
print "finish writing to database as lost!"

