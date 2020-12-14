# coding=utf-8

from pymongo import MongoClient
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from bson.objectid import ObjectId

table="morph"

client = MongoClient('mongodb://localhost:27017/')
db = client.shuron
cdict = {}
total_word = 0


# 単語のリストを作成する
for qa in db[table].find():
    for w in qa['words']:
        if w not in cdict:
            cdict[w] = 0
            
# 各単語が出て来る文書をカウント
for key in cdict:
    for qa in db[table].find():
        if key in qa['words']:
            cdict[key] = cdict[key] + 1

l = []
for c in cdict:
    l.append(cdict[c])

l.sort(reverse=True)

for c in cdict:
    if cdict[c] > 3000:
        print("{}:{}".format(c, cdict[c]))
