#!/usr/bin/python3
# coding=utf-8

import time
import sys
from pymongo import MongoClient
import re
import datetime
import json


def datestr(arg):
	return arg[0:4]+"/"+arg[4:6]+"/"+arg[6:8]+" "+arg[8:10]+":"+arg[10:12]+":"+arg[12:]

if len(sys.argv) != 2:
	print("nii.py <nii.csv>\n")
	sys.exit(1)

path = sys.argv[1]
cl = MongoClient('mongodb://localhost:27017')
db = cl.shuron


with open(path, mode="r", encoding="utf-8") as f:
	for s in f:
		line = s.split("\t")
		# print("{}:{}:{}:{}:{}\n".format(line[0], line[1], line[2], line[3], line[4]))
		
		data = {
			'qid': line[0],
		'postdate': datestr(line[4]),
		'body': line[2] + line[3]
		}
		db.qa.insert_one(data)

cl.close()
