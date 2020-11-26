# coding=utf-8

from minepy import MINE 
import csv
import sys
import numpy as np
import math
from scipy import stats
import numpy as numpy
from astropy import stats as asstats


# ファイルの読み込み
n_topics = 0
line = 0

if sys.argv[1] == "-s":
    ndata = 4
if sys.argv[1] == "-m":
    ndata = 12
ar = np.zeros((200, 3, ndata)) # 200トピック10年分12カ月で仮置き

with open(sys.argv[2]) as f:
    reader  = csv.reader(f, delimiter=',')
    for r in reader:
        # 最初の行ではトピック数の決定
        if (n_topics == 0):
            n_topics = len(r) - 1
            print("len={}".format(n_topics))
        else:
            for t in range(n_topics):
                ar[t][int(line / ndata)][line % ndata] = float(r[t + 1])
            line = line + 1


print("#,FY,avg, v, p-value")
for i in range(n_topics):
    for j in range(3):
        s = 0
        s2 = 0
        for k in range(ndata):
            s += ar[i][j][k]
            s2 += ar[i][j][k]**2
        # 平均
        avg = s / ndata 
        # 標準偏差
        v = math.sqrt(((s2 - avg**2 * ndata) / (ndata - 1)))
        pv = stats.kstest(ar[i][j], stats.norm(loc = avg, scale=v).cdf)
        if (pv[1] < 0.05): # 正規分布
            print("{},{},{:.6f},{:.6f},{:.6f},パラメトリック".format(i, j+2015, avg, v, pv[1]))
        else:
            print("{},{},{:.6f},{:.6f},{:.6f},ノンパラメトリック".format(i, j+2015, avg, v, pv[1]))

print("二標本KS検定")
for i in range(n_topics):
    # 2015 vs 2016
    # 2016 vs 2017
    pv1 = stats.ks_2samp(ar[i][0], ar[i][1])
    pv2 = stats.ks_2samp(ar[i][1], ar[i][2])
    print("{},{},{}".format(i, pv1[1], pv2[1]))

print("ウィルコクソンの符号順位検定")
for i in range(n_topics):
    # 2015 vs 2016
    # 2016 vs 2017
    pv1 = stats.wilcoxon(ar[i][0], ar[i][1])
    pv2 = stats.wilcoxon(ar[i][1], ar[i][2])
    print("{},{},{}".format(i, pv1[1], pv2[1]))

print("カイパー")
for i in range(n_topics):
    # 2015 vs 2016
    # 2016 vs 2017
    pv1 = asstats.kuiper_two(ar[i][0], ar[i][1])
    pv2 = asstats.kuiper_two(ar[i][1], ar[i][2])
    print("{},{},{}".format(i, pv1[1], pv2[1]))
