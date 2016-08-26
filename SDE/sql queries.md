# ensure size shrink when drop table
PRAGMA auto_vacuum = FULL
# DELETE Certain column or alter names;
CREATE TABLE wifinew(sgtime DATETIME,mac CHAR(20),bldid CHAR(20),lastlocatedtime DATETIME,firstlocatedtime DATETIME, xcor  NUMERIC,ycor NUMERIC,status CHAR(20),out INTEGER);
INSERT INTO wifinew Select sgtime,mac, bldid,  lastlocatedtime, firstlocatedtime, xcor,ycor,status,out FROM wifi ;
DROP table wifi