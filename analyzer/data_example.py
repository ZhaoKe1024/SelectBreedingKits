# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-06 23:41
import random

import pandas as pd

from inbreed_lib.analyzer.LayerGraph import Vertex, LayerNetworkGraph


def get_instant_1():
    depth = 6
    num_per_layer = [9, 7, 5, 3, 2, 1]
    vertex_list = []
    vertex_layer = [[] for _ in range(depth)]
    idx = 0
    for j, num in enumerate(num_per_layer):
        for i in range(num):
            vertex_list.append(Vertex(index=idx, name=str(j) + '_' + str(i), depth=j))
            vertex_layer[j].append(idx)
            idx += 1
    children_list = [[] for _ in range(len(vertex_list))]
    children_list[0] = [9, 10]
    children_list[1] = [9]
    children_list[2] = [10]
    children_list[3] = [11, 12, 13]
    children_list[4] = [11]
    children_list[5] = [12, 13]
    children_list[6] = [14, 15]
    children_list[7] = [14]
    children_list[8] = [15]
    children_list[9] = [16]
    children_list[10] = [17, 18]
    children_list[11] = [17]
    children_list[12] = [16, 19, 20]
    children_list[13] = [18]
    children_list[14] = [19]
    children_list[15] = [20]
    children_list[16] = [21]
    children_list[17] = [21]
    children_list[18] = [22, 23]
    children_list[19] = [22, 23]
    children_list[20] = []
    children_list[21] = [24, 25]
    children_list[22] = [24]
    children_list[23] = [25]
    children_list[24] = [26]
    children_list[25] = [26]
    children_list[26] = []
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph


# ===========================生成一个30×300的种群========================
def generator_330():
    male_idxs = ["G{}M{}".format(i, i) for i in range(30)]
    female_idxs = []
    for i in range(len(male_idxs)):
        for j in range(10):
            female_idxs.append("G{}F{}".format(i, j))
    print(male_idxs)
    print(female_idxs)
    fout = open("./kinship330.csv", 'w')
    fout.write("," + ','.join(female_idxs) + '\n')
    # print((","+','.join(female_idxs)+'\n'))
    for i in range(len(male_idxs)):
        ps = []
        st = i * 10
        en = (i + 1) * 10
        for j in range(0, st):
            ps.append(0.49 + 0.4 * random.random())
        for j in range(st, en):
            ps.append(0.11 * random.random())
        for j in range(en, len(female_idxs)):
            ps.append(0.49 + 0.4 * random.random())
        fout.write(male_idxs[i] + ',' + ','.join([str(item) for item in ps]) + '\n')
        # print(male_idxs[i]+','+','.join([str(item)[:4] for item in ps])+'\n')
    fout.close()


def test_read_for_file():
    df = pd.read_csv("./kinship330.csv", delimiter=',', header=0, index_col=None)
    print(df.head(10))
    print(df.shape)


if __name__ == '__main__':
    # generator_330()
    test_read_for_file()
