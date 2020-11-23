# coding=utf-8
import sys
import csv
import numpy as np

TOPICMAX = 200
MAXYEAR = 3
line = 0
n_topics = 0
h = []
season = ["春", "夏", "秋", "冬"]
tn = np.zeros((TOPICMAX, MAXYEAR, 12)) # オリジナル
sn = np.zeros((TOPICMAX, MAXYEAR, 4))  # 季節毎の集計結果
ms = np.zeros((MAXYEAR, 12)) # 月毎の投稿数
ss = np.zeros((MAXYEAR, 4))  # 季節毎の投稿数
mr = np.zeros((TOPICMAX, MAXYEAR, 12)) # 月毎のトピック占有率
sr = np.zeros((TOPICMAX, MAXYEAR, 4))  # 季節毎のトピック占有率

if len(sys.argv) != 4:
    print("usage: topicratio.py <input> <ratio.month> <ratio.season>")
    sys.exit(0)

# ファイル読み込み
with open(sys.argv[1]) as f:
    reader  = csv.reader(f, delimiter=',')
    for r in reader:
        # 最初の行ではトピック数の決定
        if (n_topics == 0):
            n_topics = len(r) - 1
        for t in range(n_topics):
            tn[t][int(line / 12)][line % 12] = r[t + 1]
        h.append(r[0])
        line = line + 1
#print(f"tn[1][2]:{tn[1][2]}") #OK
#print(f"line={line}")

# 季節毎に集計
for t in range(n_topics):
    for i in range(line):
#        if t == 1:
#            print(f"{sn[t][int(i/12)][int((i%12)/3)]} += {tn[t][int(i/12)][i%12]}")
        sn[t][int(i/12)][int((i%12)/3)] += tn[t][int(i/12)][i%12]
#print(f"sn[1][2]:{sn[1][2]}") #OK
#print(sn)

# 月毎の投稿数合計
for i in range(line):
    for t in range(n_topics):
        ms[int(i/12)][i%12] += tn[t][int(i/12)][i%12]
#print(f"ms[1]:{ms[1]}") #OK
#print(ms)

# 季節毎の投稿数合計
for i in range(int(line/3)):
    for t in range(n_topics):
        ss[int(i/4)][int(i%4)] += sn[t][(int(i/4))][int(i%4)]
#print(f"ss[1]{ss[1]}") #OK
#print(ss)

# 数から率への変換(月毎)
for i in range(line):
    for t in range(n_topics):
        mr[t][int(i/12)][i % 12] = float(tn[t][int(i/12)][i%12]) / float(ms[int(i/12)][i % 12])
#        if i == 0:
#            print(f"mr[{t}][{int(i/12)}][{i%12}]={float(tn[t][int(i/12)][i%12])} / {float(ms[int(i/12)][i % 12])}→{mr[t][int(i/12)][i % 12]}")
#print("mr") #OK
#print(mr)

# 数から率への変換(季節毎)
for i in range(int(line/3)):
    for t in range(n_topics):
        sr[t][int(i/4)][i%4] = float(sn[t][int(i/4)][i%4]) / float(ss[int(i/4)] [i % 4] )
#print("sr")
#for t in range(20):
#    for i in range(3):
#        print(f"sr[{t}][{i}]:{sr[t][i]}")

# 月毎
with open(sys.argv[2], "w") as f:
    # ヘッダ行
    for t in range(n_topics):
        print(f",{t}", file=f, end="")
    print(file=f)
    for i in range(line):
        print(f"{h[i]}", file=f, end="")
        # 月毎トピック占有率
        for t in range(n_topics):
            print(f",{mr[t][int(i/12)][i%12]}", file=f, end="")
        print(file=f)
        

# 季節毎
with open(sys.argv[3], "w") as f:
    # ヘッダ行
    for t in range(n_topics):
        print(f",{t}", file=f, end="")
    print(file=f)
    for i in range(int(line/3)):
        print(f"{2015+int(i/4)}{season[i%4]}", file=f, end="")
        for t in range(n_topics):
            print(f",{sr[t][int(i/4)][i % 4]}", file=f, end="")
        print(file=f)