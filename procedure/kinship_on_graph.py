# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-07 23:06
from analyzer.LayerGraph import LayerNetworkGraph
from analyzer.commonAncestors import FamilyAnalyzer
from procedure.xlsx2graph import build_family_graph


class Kinship(object):
    def __init__(self):
        self.family_graph = build_family_graph()
        self.analyzer = FamilyAnalyzer(familyGraph=self.family_graph)
        self.N = len(self.family_graph)
        self.name2index = dict()
        for i, ver in enumerate(self.family_graph.vertex_list):
            self.name2index[ver.name] = i
        # self.__initialize()

    # def __initialize(self):
        # self.analyzer = FamilyAnalyzer(familyGraph=)

    def calc_kinship_corr(self, p1: str, p2: str):
        return self.analyzer.calc_kinship_corr(ind1=self.name2index[p1],
                                               ind2=self.name2index[p2])

    def print_all_poultry(self):
        for i, ver in enumerate(self.family_graph.vertex_list):
            print(i, ":", ver)

    def print_layer(self):
        for layer in self.family_graph.vertex_layer:
            print([self.family_graph.vertex_list[ind].name for ind in layer])

    def print_parents(self):
        for i, par in enumerate(self.analyzer.parents):
            print(i, ":", par)

    # def print_edges(self):
        # for edge in self.family_graph.edge_list:
        #     print(edge)

        # for edge in self.family_graph.children:
        #     print(edge)
