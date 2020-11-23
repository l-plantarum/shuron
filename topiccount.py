#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys
import datetime

client = MongoClient('mongodb://localhost:27017')
db = client.shuron

table="morph"

beginDate = datetime.date(2015, 1, 1)

for i in (2015, 2016, 2017, 2018):
  for j in range(1, 13):
    # 2015年の3月までと2018年の4月以降はデータはないのでパス
    if (i == 2015 and j < 4) or (i == 2018 and j >= 4):
      continue
    if (j == 12):
      beginDate = datetime.date(i, j, 1)
      endDate = datetime.date(i + 1, 1, 1);
    else:
      beginDate = datetime.date(i, j, 1)
      endDate = datetime.date(i, j + 1, 1);

    bdaystr = "{0:%Y/%m/%d}".format(beginDate)
    edaystr = "{0:%Y/%m/%d}".format(endDate)
    beginTime = bdaystr + " 00:00:00"
    endTime   = edaystr + " 00:00:00"
    print("{},".format(bdaystr), end="")
    for k in range(20): 
      count = db[table].find({"postdate" : { "$gte": beginTime, "$lt": endTime}, "maxtopic": k, "nmorpy":{"$gte": 20}}).count()
      if k == 19:
        print("{}".format(count))
      else:
        print("{}".format(count), end=",")
client.close()
