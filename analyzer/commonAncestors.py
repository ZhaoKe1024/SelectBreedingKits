# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-06 23:51
import math
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

        self.num_ver = len(familyGraph)
        # inverse properties:
        self.Depth = len(familyGraph.vertex_layer)
        self.inv_vertex_layer = []
        for i in range(self.Depth):
            self.inv_vertex_layer.append(
                [self.num_ver - 1 - val for val in self.familyGraph.vertex_layer[self.Depth - 1 - i]])
        self.inv_vertex_list = familyGraph.vertex_list
        idx = 0
        for j, layer in enumerate(self.inv_vertex_layer):
            # print("depth:", j, ":", layer)
            for ver in layer:
                self.inv_vertex_list[ver].index = idx
                self.inv_vertex_list[ver].depth = j
                idx += 1
        self.inv_edge_list = []
        self.inv_indegree = [0] * self.num_ver
        self.inv_outdegree = [0] * self.num_ver
        self.parents = [[] for _ in range(self.num_ver)]  # inv_children
        for edge in familyGraph.edge_list:
            # inv graph need reverse the index of vertex
            self.__add_edge(self.num_ver - 1 - edge[1], self.num_ver - 1 - edge[0])

    def __initialize_inbreed_coef(self):
        pass

    def __invV(self, idx):
        return self.inv_vertex_list[self.num_ver - 1 - idx]

    def __invIdx(self, idx):
        return self.num_ver - 1 - idx

    def printarray(self, array):
        print([self.__invIdx(val) for val in array])

    def __add_edge(self, pre_idx, post_idx):
        self.parents[pre_idx].append(post_idx)
        self.inv_indegree[post_idx] += 1
        self.inv_outdegree[pre_idx] += 1
        self.inv_edge_list.append([pre_idx, post_idx])

    def __find(self, inv_idx: int, rev=1) -> List[tuple]:
        marked = [False] * self.num_ver
        que = deque()
        Li = [(inv_idx, [inv_idx])]
        marked[inv_idx] = True
        for p in self.parents[inv_idx][::rev]:
            marked[p] = True
            que.append((p, [inv_idx, p]))
            Li.append((p, [inv_idx, p]))
        # print("first Li:", Li)
        # 判断必经点
        # 略，先放着pass
        while len(que) > 0:
            t, pre_path = que.popleft()
            for p in self.parents[t][::rev]:
                # print("p", p, marked[p])
                if not marked[p]:
                    marked[p] = True
                    que.append((p, pre_path + [p]))
                    Li.append((p, pre_path + [p]))
        return Li

    def __intersection_path(self, ppath1, ppath2) -> List[tuple]:
        ppath1.sort(key=lambda x: x[0], reverse=1)
        ppath2.sort(key=lambda x: x[0], reverse=-1)
        # print([item[0] for item in ppath1])
        # print([item[0] for item in ppath2])
        res = []
        p1, M, p2, N = 0, len(ppath1), 0, len(ppath2)
        while p1 < M and p2 < N:
            while p1 < M and ppath1[p1][0] > ppath2[p2][0]:
                p1 += 1
            if p1 < M and ppath1[p1][0] == ppath2[p2][0]:
                res.append((ppath1[p1][0], ppath1[p1][1], ppath2[p2][1]))
            while p1 < M and ppath1[p1][0] == ppath2[p2][0]:
                p1 += 1
            p2 += 1
        # print([item[0] for item in res])
        return res

    def __dfs(self, start: int, end: int, path: List[int], allpath: List[List]) -> None:
        # print(f"start:{self.__invIdx(start)}, end:{self.__invIdx(end)}")
        if start == end:
            # print("res: ", [self.__invIdx(val) for val in path+[start]])
            allpath.append(path + [start])

        path.append(start)
        for p in self.parents[start]:
            self.__dfs(p, end, path, allpath)
            path.pop(-1)

    def find_all_path(self, start, end) -> List[List]:
        """

        :param start: forward index of start point
        :param end: forward index of end point
        :return:
        """
        # print(f"find all path from {start} to {end}")
        tmp_path = []
        paths1 = []
        self.__dfs(self.__invIdx(start), self.__invIdx(end), tmp_path, paths1)
        return paths1

    def __iloc_set(self, array2d: List[List], ind: int) -> set:
        res = set()
        for arr in array2d:
            # print("add:", arr[ind])
            res.add(arr[ind])
        return res

    def __remove_redundancy(self, ind1: int, ind2: int, parent: int) -> bool:
        """

        :param ind1: forward index
        :param ind2: forward index
        :param parent: forward index
        :return:
        """
        # print(f"remove redundancy for {ind1} and {ind2} to {parent}")
        paths1 = self.find_all_path(start=ind1, end=parent)
        paths2 = self.find_all_path(start=ind2, end=parent)
        # for path in paths1:
        #     self.printarray(path)
        # print("---")
        # for path in paths2:
        #     self.printarray(path)
        # print("set1 and set 2 and con")
        # print(self.__iloc_set(paths1, -2), self.__iloc_set(paths2, -2))
        # print(self.__iloc_set(paths1, -2) | self.__iloc_set(paths2, -2))
        # print("length:", len(self.__iloc_set(paths1, -2) | self.__iloc_set(paths2, -2)))
        if len(self.__iloc_set(paths1, -2) | self.__iloc_set(paths2, -2)) < 2:
            return False
        else:
            return True

    def find_all_common_ancestors(self, ind1: int, ind2: int) -> List[int]:
        """
        这里就不去做逆图了，直接在类里面设置反向边和反向children属性吧，方便检索
        :param ind1: reverse index of one vertex
        :param ind2:
        :return: forward index of vertices
        """
        if ind1 > ind2:
            ind1, ind2 = ind2, ind1
        L1 = self.__find(inv_idx=self.__invIdx(ind1), rev=1)
        L2 = self.__find(inv_idx=self.__invIdx(ind2), rev=-1)
        # for i in range(len(L1)):
        #     tmp_tuple = (self.__invIdx(L1[i][0]), [self.__invIdx(val) for val in L1[i][1]])
        #     L1[i] = tmp_tuple
        # for i in range(len(L2)):
        #     tmp_tuple = (self.__invIdx(L2[i][0]), [self.__invIdx(val) for val in L2[i][1]])
        #     L2[i] = tmp_tuple

        # for i in range(len(L1)):
        #     print(self.__invIdx(L1[i][0]), [self.__invIdx(val) for val in L1[i][1]])
        #     # L1[i] = tmp_tuple
        # for i in range(len(L2)):
        #     print(self.__invIdx(L2[i][0]), [self.__invIdx(val) for val in L2[i][1]])
        #     # L2[i] = tmp_tuple

        L_common = self.__intersection_path(L1, L2)
        # print("common ancestors and its path (before delete):")
        # print("[", end='')
        # for i, (idx, path1, path2) in enumerate(L_common):
        #     print(self.__invIdx(idx), end=', ')
        #     # print(self.__invIdx(idx), [self.__invIdx(item) for item in path1])
        #     # print(self.__invIdx(idx), [self.__invIdx(item) for item in path2])
        # print("]")
        # 下面需要修改
        # del_list = []
        marked = [False] * len(L_common)
        for i, (idx, _, _) in enumerate(L_common):
            # if self.__remove_redundancy(ind1=self.__invIdx(ind1), ind2=self.__invIdx(ind2), parent=self.__invIdx(idx)):
            # if self.__remove_redundancy(ind1=self.__invIdx(ind1), ind2=self.__invIdx(ind2), parent=idx):
            if self.__remove_redundancy(ind1=ind1, ind2=ind2, parent=self.__invIdx(idx)):
                marked[i] = True
        # print("del list:", del_list)
        # for i in del_list[::-1]:
        #     del L_common[i]
        res = []
        # print("[", end='')
        for i in range(len(marked)):
            if marked[i]:
                res.append(self.__invIdx(L_common[i][0]))
                # print(self.__invIdx(L_common[i][0]), end=', ')
            # print(self.__invIdx(idx), [self.__invIdx(item) for item in path1])
            # print(self.__invIdx(idx), [self.__invIdx(item) for item in path2])
        # print("]")
        return res

    def calc_path_prob(self, ind1: int, ind2: int, ancestor: int) -> float:
        """
        calculate the prob through d-value of frpth of two vertices
        :param ind1: origin index of vertex
        :param ind2:
        :param ancestor:
        :return:
        """
        gene_origin = self.inv_vertex_list[self.__invIdx(ancestor)].depth
        ind1_gene = self.inv_vertex_list[self.__invIdx(ind1)].depth
        ind2_gene = self.inv_vertex_list[self.__invIdx(ind2)].depth
        # print(gene_origin, ind1_gene, ind2_gene)
        coef_base = 1. / (1 << (abs(gene_origin - ind1_gene) + abs(gene_origin - ind2_gene)))
        if self.inv_vertex_list[ancestor].depth == self.num_ver-1:
            return coef_base
        else:
            FA = self.inv_vertex_list[ancestor].inbreed_coef
            if FA > 0.0001:
                return coef_base * (1 + FA)
            else:
                self.inv_vertex_list[ancestor].inbreed_coef = self.calc_inbreed_coef(ancestor)
                return coef_base * (1 + self.calc_inbreed_coef(ancestor))
            # print(coef_base, FA)
            # return coef_base
            # if FA > -0.9:
            #     # 如果FA非负
            #     print("======>:FA", FA)
            #     return coef_base * (1 + FA)
            # else:
            #     print("======>:FA", FA)
            #     # if self.familyGraph.vertex_list[ancestor].depth == 0:
            #     #     # 初代的近交系数就是0
            #     #     return coef_base
            #     # if FA is negative, w.r.t. it has not been calculated
            #
            #     return coef_base * (1 + self.calc_inbreed_coef(ancestor))

    def __name(self, ind: int):
        return self.inv_vertex_list[ind].name

    def calc_kinship_corr(self, ind1: int, ind2: int) -> float:
        """

        :param ind1: forward index of vertex 1
        :param ind2: forward index of vertex 2
        :return:
        """
        common_ancestors = self.find_all_common_ancestors(ind1, ind2)
        print(f"common ancestors of {self.__name(ind1)} and {self.__name(ind2)}:")
        print('\t', [self.__name(val) for val in common_ancestors])
        corr = 0.
        # return corr
        for anc in common_ancestors:
            item = self.calc_path_prob(ind1, ind2, anc)
            print(f"ind {self.__name(ind1)} and {self.__name(ind2)} to {self.__name(anc)}: item: {item}")
            corr += item
        return corr / math.sqrt((1+self.calc_inbreed_coef(ind1))*(1+self.calc_inbreed_coef(ind2)))

    def calc_inbreed_coef(self, indi: int) -> float:
        print("--------------inbreed coefficient----------------")
        # print(self.inv_vertex_list[self.__invIdx(indi)].depth)
        if self.inv_vertex_list[self.__invIdx(indi)].depth == len(self.inv_vertex_layer)-1:
            return 0.
        parent = self.get_parents(indi)
        print(f"{self.__name(indi)}的双亲:", [self.__name(val) for val in parent])
        return 0.5 * self.calc_kinship_corr(parent[0], parent[1])

    def get_parents(self, idx: int) -> List[int]:
        return [self.__invIdx(val) for val in self.parents[self.__invIdx(idx)]]


def example_all():
    p = 26
    lg = get_instant_1()
    analyzer = FamilyAnalyzer(familyGraph=lg)
    # lg.print_layers()
    # lg.print_children()
    # print("=============================")
    print("个体 index:", p)
    parent = analyzer.get_parents(p)
    print("双亲:", parent)
    common_ancs = analyzer.find_all_common_ancestors(parent[0], parent[1])
    # print("共同祖先：", common_ancs)
    print("个体 index:", p)
    print("亲缘相关系数：", analyzer.calc_kinship_corr(24, 25))
    print("个体 index:", p)
    print("个体近交系数：", 0.5*analyzer.calc_inbreed_coef(p))
    print("====================")
    p = 24
    print("个体 index:", p)
    parent = analyzer.get_parents(p)
    print("双亲:", parent)
    common_ancs = analyzer.find_all_common_ancestors(parent[0], parent[1])
    print(common_ancs)
    p1, p2 = 21, 22
    print("给定个体:", p1, p2)
    print("共同祖先：")
    common_ancs = analyzer.find_all_common_ancestors(p1, p2)
    print(common_ancs)
    print("亲缘相关系数：", analyzer.calc_kinship_corr(p1, p2))  #
    print("个体近交系数：", analyzer.calc_inbreed_coef(24), "eq?", 0.5*analyzer.calc_kinship_corr(p1, p2))


if __name__ == "__main__":
    # example_all()

    lg = get_instant_1()
    analyzer = FamilyAnalyzer(familyGraph=lg)
    # analyzer.calc_path_prob(16, 17, 0)
    # print(analyzer.calc_inbreed_coef(2))
    # print(analyzer.calc_inbreed_coef(9))
    print(analyzer.calc_inbreed_coef(26))
    print(analyzer.calc_inbreed_coef(24))
    # print(analyzer.find_all_common_ancestors(21, 22))
    # print(analyzer.find_all_common_ancestors(24, 25))

    # p1, p2 = 21, 22
    # lg = get_instant_1()
    # analyzer = FamilyAnalyzer(familyGraph=lg)
    # paths = analyzer.find_all_path(21, 3)
    # for path in paths:
    #     analyzer.printarray(path)
    #
    # paths = analyzer.find_all_path(22, 3)
    # for path in paths:
    #     analyzer.printarray(path)
    # common_ancs = analyzer.find_all_common_ancestors(24, 25)
    # print(common_ancs)
    # common_ancs = analyzer.find_all_common_ancestors(16, 17)
    # print(common_ancs)
    # print(analyzer.calc_inbreed_coef(26))
    # print(analyzer.calc_path_prob(24, 25, ancestor=10))
    # print(analyzer.calc_kinship_corr(24, 25))
    # print(analyzer.inv_indegree)
    # print(analyzer.inv_outdegree)
    # print(analyzer.inv_edge_list)
    # for layer in analyzer.inv_vertex_layer:
    #     print(layer)
    # find_all_ca(graph=lg, v=Vertex(index=6, name="K"), w=Vertex(index=7, name="L"))
