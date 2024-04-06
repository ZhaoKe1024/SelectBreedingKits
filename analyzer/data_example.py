# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-06 23:41
from analyzer.LayerGraph import Vertex, LayerNetworkGraph


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
    children_list[19] = [22]
    children_list[20] = [23]
    children_list[21] = [24, 25]
    children_list[22] = [24]
    children_list[23] = [25]
    children_list[24] = [26]
    children_list[25] = [26]
    children_list[26] = []
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph
