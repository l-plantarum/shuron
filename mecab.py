# coding=utf-8

import  MeCab
import sys
from pymongo import MongoClient
import re
import datetime

def get_stopwords(filename):
    stopwords = []
    with open(filename) as f:
        stopwords = [s.strip() for s in f.readlines()]
    return stopwords

# URLの正規表現
urlpattern = r"^http[s]?://.*$"
reurl = re.compile(urlpattern)

#tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
tagger = MeCab.Tagger()

client = MongoClient('mongodb://localhost:27017/')
db = client.shuron

now = datetime.datetime.now()
today = "{0:%Y%m%d}".format(now)

longq = 0
shortq = 0

indb = "qa"
outdb = "morph"
if len(sys.argv) == 1:
    stopwords = []
else:
    stopwords = get_stopwords(sys.argv[1])

print(outdb)
if (db[indb].count() == 0):
	print("no database {}".format(indb))
	sys.exit(1)

i = 0
ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))
convtbl = str.maketrans(ZEN, HAN)
# とりあえずちょっとだけとってみる
#for qa in db[indb].find({"qid":"14146177619"}):
for qa in db[indb].find():
    lines = qa['body'].split()
    results = []
    nmorph = 0
    clist = []
    for line in lines:
        if (reurl.match(line)):
            continue

        # 〇判定
        line = re.sub('([A-Ea-e])<>判定', '\\1判定', line)
        # 高〇
        line = re.sub("高校?[1１一]年?生?",  "高一", line)
        line = re.sub("高校?[2２二]年?生?",  "高二", line)
        line = re.sub("高校?[3３三]年?生?",  "高三", line)
        # &gt;, &lt;の置換
        line = line.replace("&gt;", "<").replace("&lt;", ">")

        # 全角→半角変換，mecab処理
        wordinfo = tagger.parse(line.translate(convtbl))

        doc = wordinfo.split('\n')
        nmorph += len(doc)
        for i  in range(len(doc)):
            d = doc[i]
        # for d in doc:
            if (d in ['','EOS']):
                continue
            dic = d.split('\t')
            if (dic[0] in [ '/', '[', ']', '(', ')', '「', '」', '?']):
                continue
            defs = dic[1].split(',')
            if dic[0] in ["次", "位", "期", "年", "冊", "校","月"] and len(results) != 0: # 直前のアイテムに付加する
                results[-1] = results[-1] + dic[0]
                continue
            if (defs[0] in ["連体詞", "副詞", "接続詞", "助動詞", "接頭詞", "感動詞", "助詞", "記号", "フィラー", "BOS/EOS"]):
                if dic[0] not in ["高"]: #「高3」の高がはじかれる
                    continue
            if defs[0] == "名詞" and defs[1] in ["引用文字列", "動詞非自立的","副詞可能","接続詞的","接尾","代名詞","特殊"]:
                continue
            if (defs[1] in ["非自立"]):
                continue
            if defs[6] in stopwords:
                continue
#            if (defs[6] in ["ない", "する", "やる", "なる", "できる", "れる"]):
#                continue
#            if (defs[6] in ["大学", "ある", "コロナ", "思う", "今", "受験", "学校", "影響", "勉強"]):
#                continue
#            if (defs[6] in ["私", "志望", "高校", "志望", "合格"]):
#                continue
# 高[一二三]
            if dic[0] in ["高", "新高"] :
                clist = [dic[0]]
            elif defs[1] == "数" or dic[0] in ['.', '%']: 
                # 次がなければここまでの結果を出力
                if i == len(doc) - 1:
                    results.append("".join(clist) + dic[0])
                    clist.clear()
                    break
                d2 = doc[i + 1]
                dic2 = d2.split('\t')
                if len(dic2) == 1:
                    results.append("".join(clist) + dic[0])
                    clist.clear()
                    break
                defs2 = dic2[1].split(',')
                # 次が数ならclistに追加，数でなければclistを結合してclistに追加
                if defs2[1] == "数" or dic2[0] in ['.', '%']: 
                    clist.append(dic[0])
                else:
                    results.append("".join(clist)+ dic[0])
                    clist.clear()
            elif defs[6] == '*':
                results.append(dic[0])
            else:
                results.append(defs[6])
    # 数値等

    if indb == "niiqa":
	    qa['url'] = qa['qid']


    if nmorph >= 20:
        data = {
    	    '_id': qa['_id'],
            'qid': qa['qid'],
	        'postdate': qa['postdate'],
	        'words': results,
	        'nmorpy': nmorph,
	        'nwords': len(results)
        }
        db[outdb].insert_one(data)
        longq += 1
    else:
        shortq += 1

print(f"インポートした質問:{longq}")
print(f"インポートしなかった質問:{shortq}")
