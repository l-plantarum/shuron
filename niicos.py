# coding=utf-8
import csv
import sys
import numpy as np
import math

# 月毎，季節毎の共通，コサイン類似度
def calccos(ar1, ar2):
    v1len = 0
    v2len = 0
    ins = 0
    for i in range(len(ar1)):
        v1len += ar1[i]*ar1[i]
        v2len += ar2[i]*ar2[i]
        ins += ar1[i] * ar2[i]
    return ins / math.sqrt(v1len) / math.sqrt(v2len)

def calceuclid(ar1, ar2):
    s = 0
    for i in range(len(ar1)):
        s += (ar1[i]-ar2[i])**2
    return math.sqrt(s)



def month(csvfile):
    # 月毎トピック占有率
    # コサイン類似度
    # ユークリッド距離
    # 正規化済ユークリッド距離
    # 一標本KS検定
    # 季節毎トピック占有率
    return

def season(csvfile):
    return

if len(sys.argv) != 3:
    print("niicos.py <month.csv> <season.csv>")
    sys.exit(0)

# ファイルの読み込み
def read_csv(csvfile, season):
    n_topics = 0
    ar = None
    line = 0
    with open(csvfile) as f:
        reader  = csv.reader(f, delimiter=',')
        for r in reader:
            # 最初の行ではトピック数の決定
            if (n_topics == 0):
                n_topics = len(r) - 1
                if season:
                    ar = np.zeros((n_topics, 3, 4)) # 3年分4シーズンで仮置き
                else:
                    ar = np.zeros((n_topics, 3, 12)) # 3年分12カ月で仮置き
            else:
                for t in range(n_topics):
                    if season:
                        ar[t][int(line / 4)][line % 4] = float(r[t + 1])
                    else:
                        ar[t][int(line / 12)][line % 12] = float(r[t + 1])
                line = line + 1
    return n_topics, line, ar

# 同じ話題の年ごとのコサイン類似度
def cosine_same_topic_other_year(ar):
    print("同じ話題の年ごとのコサイン類似度")
    sim = []
    s12 = []
    s23 = []
    print("#,15vs16,16vs17")
    for i in range(0, 20):
        sim12 = calccos(ar[i][0], ar[i][1])
        sim23 = calccos(ar[i][1], ar[i][2])
        print(f"{i}, {sim12}, {sim23}")
        s12.append(sim12)
        s23.append(sim23)
    sim.append(s12)
    sim.append(s23)
    return sim

# 同じ年の別の話題間のコサイン類似度
def cosine_same_year_other_topic(ar, year):
    print("同じ年の別の話題間のコサイン類似度")
    sim = np.zeros((20, 20)) # トピック間コサイン類似度
    mostsim = {}

    # コサイン類似度の算出
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                sim[i][j] = calccos(ar[i][year], ar[j][year])

    # 一番似ているトピック
    for i in range(0, 20):
        maxsim = 0
        maxsimtopic = -1
        for j in range(0, 20):
            if i != j:
                if maxsim < sim[i][j]:
                    maxsim = sim[i][j]
                    maxsimtopic = j
        mostsim[i] = {maxsim, maxsimtopic}
    return mostsim

# 単位ベクトルとのコサイン類似度
def similarity_between_e(ar):
    e = np.ones((12))
    print("単位ベクトルとのコサイン類似度")
    print("#,2015,2016,2017")
    for i in range(0, 20):
        sim1 = calccos(ar[i][0], e)
        sim2 = calccos(ar[i][1], e)
        sim3 = calccos(ar[i][2], e)
        print("{},{},{},{}".format(i, sim1, sim2, sim3))

# 各トピックについて，同じトピックの別の年とのユークリッド距離
def euclid_same_topic_other_year(ar):
    print("各トピックについて，同じトピックの別の年とのユークリッド距離を算出する")
    sim = []
    d12 = []
    d23 = []
    print("#,15vs16,16vs17")
    for i in range(0, 20):
        dis12 = calceuclid(ar[i][0], ar[i][1])
        dis23 = calceuclid(ar[i][1], ar[i][2])
        print(f"{i}, {dis12}, {dis23}")
        d12.append(dis12)
        d23.append(dis23)
    sim.append(d12)
    sim.append(d23)
    return sim

# ユークリッド距離的にいちばん近いトピックとその距離の算出
def euclid_same_year_other_topic(ar, year):
    print("ユークリッド距離的にいちばん近いトピックとその距離の算出")
    sim = np.zeros((20, 20)) # トピック間ユークリッド距離
    mostsim = {}

    # ユークリッド距離の算出
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                sim[i][j] = calceuclid(ar[i][year], ar[j][year])

    # 一番似ているトピック
    for i in range(0, 20):
        maxsim = 0
        maxsimtopic = -1
        for j in range(0, 20):
            if i != j:
                if maxsim < sim[i][j]:
                    maxsim = sim[i][j]
                    maxsimtopic = j
        mostsim[i] = (maxsim, maxsimtopic)
    return mostsim

def std_euclid(ar):
    stdar = np.zeros((len(ar), len(ar[0]), len(ar[0][0])))
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            s = 0
            s2 = 0
            for k in range(len(ar[0][0])):
                s += ar[i][j][k]
                s2 += ar[i][j][k]**2
            avg = s/len(ar[0][0])
            sdev = math.sqrt((s2 - avg**2 * len(ar[0][0])) / (len(ar[0][0]) - 1))
            if sdev == 0:
                print(f"0割り発生: トピック番号 {i} 年度 {j+2015}")
                print(ar[i][j])
            for k in range(len(ar[0][0])):
                stdar[i][j][k] = (ar[i][j][k] - avg) / sdev
    return stdar

def mostsimilar(mostsim, sim):
    for i in range(len(mostsim)):
        d, t = mostsim[i]
        if sim[i] < d: # 別の年の同じトピックより似ている同じ年のトピックがある(つまり似ていない)
            print(f"{i},{sim[i]},{d},{t},似てない")
        else:
            print(f"{i},{sim[i]},{d},{t},似ている")


m_topics, mline, mar = read_csv(sys.argv[1], False)
s_topics, sline, sar = read_csv(sys.argv[2], True)

print("月毎トピック占有率")
print("コサイン類似度")
# コサイン類似度
sim = cosine_same_topic_other_year(mar)
for i in range(2):
    print(f"FY{2015+i}")
    mostsim = cosine_same_year_other_topic (mar, i)
    mostsimilar(mostsim, sim[i])
similarity_between_e(mar)
# ユークリッド距離
print("ユークリッド距離")
sim = euclid_same_topic_other_year(mar)
for i in range(2):
    print(f"FY{2015+i}")
    mostsim = euclid_same_year_other_topic(mar, i)
    mostsimilar(mostsim, sim[i])
# 正規化済ユークリッド距離
print("正規化済みユークリッド距離")
smar = std_euclid(mar)
sim = euclid_same_topic_other_year(smar)
for i in range(2):
    print(f"FY{2015+i}")
    mostsim = euclid_same_year_other_topic(smar, i)
    mostsimilar(mostsim, sim[i])

print("季節毎トピック占有率")
print("コサイン類似度")
sim = cosine_same_topic_other_year(sar)
for i in range(2):
    print(f"FY{2015+i}")
    mostsim = cosine_same_year_other_topic(sar, i)
    mostsimilar(mostsim, sim[i])
similarity_between_e(sar)
print("ユークリッド距離")
sim = euclid_same_topic_other_year(sar)
for i in range(3):
    print(f"FY{2015+i}")
    mostsim = euclid_same_year_other_topic(sar, i)
    if i != 2:
        mostsimilar(mostsim, sim[i])
print("正規化済みユークリッド距離")
ssar = std_euclid(sar)
sim = euclid_same_topic_other_year(ssar)
for i in range(2):
    print(f"FY{2015+i}")
    mostsim = euclid_same_year_other_topic(ssar, i)
    mostsimilar(mostsim, sim[i])
