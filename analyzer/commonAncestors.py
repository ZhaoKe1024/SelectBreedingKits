# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-06 23:51
from typing import List
from collections import deque
from analyzer.LayerGraph import Vertex, LayerNetworkGraph
from analyzer.data_example import get_instant_1


def find(graph: LayerNetworkGraph, v: Vertex) -> List[tuple]:
    marked = [False] * len(graph)
    que = deque()
    Li = [(v, 0)]
    marked[v.index] = True
    # 直接后继直接添加
    for child in graph.children[v.index]:
        # print("add:", graph.vertex_list[child].name)
        marked[child] = True

        que.append((graph.vertex_list[child], 1))
        # if len(graph.children[])
        Li.append((graph.vertex_list[child], 1))

    # 判断第0层的后代有没有这一层的必经点，
    # 出度等于这一层所有点的出度之和，其他点出度为0
    for child in graph.children[v.index]:
        print("name:", graph.vertex_list[child].name, sum([graph.outdegree[ind] for ind in graph.children[v.index]]))
        print("-->", graph.outdegree[child], sum([graph.outdegree[ind] for ind in graph.children[v.index]]))
        if graph.outdegree[child] == sum([graph.outdegree[ind] for ind in graph.children[v.index]]):
            return Li

    # 后续的后继就要判断是不是被当前点隔绝的了，是的话不能加，那称不上是共同祖先，
    ind = 0
    while len(que) > 0:
        t, depth = que.popleft()
        # if len(graph.vertex_layer[t.depth]) < 2:
        #     continue
        # print([ind.index for ind in que])
        ind += 1
        # print(que)
        # print(ind, t.index)
        # print("cur:", graph.vertex_list[t.index].name)
        # print("whose children: ", [graph.vertex_list[item].name for item in graph.children[t.index]])
        for child in graph.children[t.index]:
            if not marked[child]:
                marked[child] = True

                que.append((graph.vertex_list[child], depth + 1))
                # 入度是1的节点不能算共同祖先，它只是流经的一条边
                # 不行，即使跳过了该点，该点的后继也不好判断，还是得分层，割点后面的都得抛去
                # if graph.indegree[child] == 1:  # and graph.outdegree[child.index] == 1:
                #     pass
                # else:
                #     Li.append((graph.vertex_list[child], depth + 1))
                # print("add:", graph.vertex_list[child].name)
                Li.append((graph.vertex_list[child], depth + 1))
                # print(graph.vertex_list[child].name)

                # 判断该点是不是这一层的必经点，
                # 出度等于这一层所有点的出度之和，其他点出度为0
                print("name:", graph.vertex_list[child].name,
                      sum([graph.outdegree[ind] for ind in graph.children[t.index]]))
                print("-->", graph.outdegree[child], sum([graph.outdegree[ind] for ind in graph.children[t.index]]))
                if graph.outdegree[child] == sum([graph.outdegree[ind] for ind in graph.children[t.index]]):
                    break
    return Li


def find_all_ca(graph: LayerNetworkGraph, v: Vertex, w: Vertex) -> List[Vertex]:
    print("----find nearest common ancestor----")
    # 图的边全部逆转，得到新的图
    inv_graph = graph.reverse_graph()
    print([ver.name for ver in inv_graph.vertex_list])
    # print(inv_graph.vertex_layer)
    # print(inv_graph.indegree)
    # print(inv_graph.outdegree)
    print(inv_graph.children)
    # 找到两个节点的所有前驱节点及对应的节点跳数

    v.index = inv_graph.num_ver - 1 - v.index
    w.index = inv_graph.num_ver - 1 - w.index
    Lv = find(inv_graph, v)
    Lw = find(inv_graph, w)
    # print(v.name, w.name)
    print([(item.name, depth) for (item, depth) in Lv])
    print([(item.name, depth) for (item, depth) in Lw])
    return []
    # 求交集（可以优化的点，并查集，我现在是O(n2)）
    # 创建字典：节点1的节点与条数
    cnt = dict()
    for item, depth in Lv:
        cnt[item.name] = (item, depth)
    # print("init:", cnt)
    # 留下节点2也有的
    uni = [True] * len(cnt.keys())
    for j, (item, depth) in enumerate(Lw):
        if item.name in cnt.keys():
            cnt[item.name] = (item, cnt[item.name][1] + depth)
            for k, it in enumerate(Lv):
                # print(it[0].name, item.name)
                if it[0].name == item.name:
                    uni[k] = False
                    break
            # uni[j] = False
    # print("after intersection:", uni)

    # 删去节点2没有的，得到交集
    for j in range(len(uni)):
        if uni[j] is True:
            del cnt[Lv[j][0].name]
    # 根据跳数排序，
    cnt = sorted(cnt.items(), key=lambda s: s[1][1])
    for j, item in cnt:
        print(j, item[0])

    # # find nearest common ancestors:
    # for j, (item, depth) in enumerate(Lw):
    #     if item.name in cnt.keys():
    #         return Lv[j]

    # find all common ancestors:
    res = []
    for _, item in cnt:
        if item[1] > 0:
            print(item[0])
            res.append(item)
    return res


class FamilyAnalyzer(object):
    def __init__(self, familyGraph: LayerNetworkGraph):
        self.familyGraph = familyGraph
        # initialize the inbreed coefficients of origin generation

        # inverse properties:
        self.Depth = len(familyGraph.vertex_layer)
        self.inv_vertex_layer = []
        for i in range(self.Depth):
            self.inv_vertex_layer.append([self.num_ver - 1 - val for val in self.familyGraph.vertex_layer[self.Depth - 1 - i]])
        self.inv_vertex_list = familyGraph.vertex_list
        for i in range(self.num_ver):
            self.inv_vertex_list[i].index = i
        self.num_ver = len(familyGraph)
        self.inv_edge_list = []
        self.inv_indegree = [0] * self.num_ver
        self.inv_outdegree = [0] * self.num_ver
        self.parents = [[] for _ in range(self.num_ver)]  # inv_children
        for edge in familyGraph.edge_list:
            self.__add_edge(self.num_ver-1-edge[1], self.num_ver-1-edge[0])

    def __add_edge(self, pre_idx, post_idx):
        self.parents[pre_idx].append(post_idx)
        self.inv_indegree[post_idx] += 1
        self.inv_outdegree[pre_idx] += 1
        self.inv_edge_list.append([post_idx, pre_idx])

    def __find(self, ver: Vertex) -> List[tuple]:

        marked = [False] * self.num_ver
        que = deque()
        Li = [(ver, 0)]
        marked[ver.index] = True
        return []

    def find_all_common_ancestors(self, ind1: int, ind2: int) -> List[int]:
        """
        这里就不去做逆图了，直接在类里面设置反向边和反向children属性吧，方便检索
        :param ind1:
        :param ind2:
        :return:
        """
        res = []
        return res

    def __calc_path_prob(self, ind1: int, ind2: int, ancestor: int) -> float:
        gene_origin = self.familyGraph.vertex_list[ancestor].depth
        ind1_gene = self.familyGraph.vertex_list[ind1].depth
        ind2_gene = self.familyGraph.vertex_list[ind2].depth
        coef_base = 1. / (1 << (abs(gene_origin - ind1_gene) + abs(gene_origin - ind2_gene)))
        FA = self.familyGraph.vertex_list[ind2].inbreed_coef
        if FA > -0.9:
            # 如果FA非负
            return coef_base * (1 + FA)
        else:
            # if self.familyGraph.vertex_list[ancestor].depth == 0:
            #     # 初代的近交系数就是0
            #     return coef_base
            # if FA is negative, w.r.t. it has not been calculated
            return coef_base * (1 + self.calc_inbreed_coef(ancestor))

    def calc_kinship_corr(self, ind1: int, ind2: int) -> float:
        common_ancestors = self.find_all_common_ancestors(ind1, ind2)
        corr = 0.
        for anc in common_ancestors:
            corr += self.__calc_path_prob(ind1, ind2, anc)
        return corr

    def calc_inbreed_coef(self, ind: int) -> float:
        parent = self.familyGraph.children[ind]
        return 0.5 * self.calc_kinship_corr(parent[0], parent[1])


if __name__ == "__main__":
    lg = get_instant_1()

    find_all_ca(graph=lg, v=Vertex(index=6, name="K"), w=Vertex(index=7, name="L"))
