import sqlite3
import re
from datetime import datetime, timedelta
from pandas import DataFrame, Series
import numpy as np
import pandas as pd
from sqlalchemy import create_engine 

conn = sqlite3.connect('new.sqlite')
disk_engine = create_engine('sqlite:///new.sqlite') # Initializes database with filename new.sqlite 

### input the building names to filter
while True:
	b = raw_input("please enter the building id as 'SDEX-0X' (X as number in 1 digit) OR use enter to exit:  ")
	b = str(b)
	if len(b) <= 1 : 
		print "---Exit---" 
		break			
	
	else:
		try:
			prob_set = pd.read_sql_query("SELECT mac,sgtime,statustype,firstlocatedtime,lastlocatedtime,interval FROM wifi WHERE bldid = '{}'".format(b),disk_engine)
			print prob_set.head()
			prob_set['sgtime'] = pd.to_datetime(prob_set['sgtime'])
			prob_set['firstlocatedtime'] = pd.to_datetime(prob_set['firstlocatedtime'])
			test = prob_set.groupby('mac').agg({"sgtime": min,"firstlocatedtime":min,"statustype": min,"interval":max})
			differ = test['sgtime']-test["firstlocatedtime"]
			long_mac = differ.index[differ>"00:20:00"]
		except:
			print "bad query: %s" % query
			continue
		
		print "total devices: ",len(test.index.unique())
    	print "missing records number: ",len(long_mac)
    	print "OVER 24 h interval:" ,"\n", test[(test.interval>86400)&(test.index.isin(long_mac)) ]
    	#cs = b[1:-1] +'-lost.csv'
    	#print "write to %s" % cs
    	#test[test.index.isin(long_mac)].to_csv(cs,header=['missingtime','status','earliestsgtime'])

