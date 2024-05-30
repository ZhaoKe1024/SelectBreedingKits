# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-06 23:41
# Neural Network Layer wish Graph
# 每一层的节点之间无边，层与层之间单向连接
from typing import List


class Vertex(object):
    def __init__(self, index, name=None, depth=0):
        self.index = index
        self.name = name if name else str(index)
        self.depth = depth
        self.inbreed_coef = 0.0

    def __str__(self):
        return f"Vertex:({self.index}, {self.name})"


class LayerNetworkGraph(object):
    def __init__(self, vertex_list: List[Vertex], vertex_layer: List[List[int]], children: List[List[int]]):
        """

        :param vertex_list: List of Vertex ordered by index
        :param vertex_layer: indices of vertices for each layer
        :param children: children for each vertex
        """
        self.vertex_list = vertex_list
        self.vertex_layer = vertex_layer
        for j, layer in enumerate(vertex_layer):
            # print(j)
            for idx in layer:
                self.vertex_list[idx].depth = j
        self.children = children
        self.num_ver = len(vertex_list)
        self.indegree = [0] * self.num_ver
        self.outdegree = [0] * self.num_ver
        self.edge_list = []
        if children or len(children) > 0:
            for i, child_list in enumerate(children):
                self.outdegree[i] = len(child_list)
                # print(child_list)
                for child in child_list:
                    self.vertex_list[child].depth = i + 1
                    self.indegree[child] += 1
                    self.edge_list.append((i, child))
        else:
            self.children = [[] for _ in range(self.num_ver)]

    def add_edge(self, pre_idx, post_idx):
        # self.edge_list.append(edge)
        # insert_vertex_sorted(array=self.children[edge.pre_v], key=self.vertex_list[edge.post_v])
        self.children[pre_idx].append(post_idx)
        self.indegree[post_idx] += 1
        self.outdegree[pre_idx] += 1

    def print_edges(self) -> None:
        print(f"=======AdjList_Graph=======")
        for i in range(len(self.vertex_list)):
            print(self.vertex_list[i].name, end=': [')
            for ver in self.children[i]:
                print(self.vertex_list[ver].name, end=', ')
            print("]")

    def reverse_graph(self):
        # Depth = 0
        Depth = len(self.vertex_layer)
        new_vertex_layer = []
        for i in range(Depth):
            new_vertex_layer.append([self.num_ver - 1 - val for val in self.vertex_layer[Depth - 1 - i]])
        # print("new layers:")
        # print(new_vertex_layer)
        # new_children = [[] for _ in range(self.num_ver)]
        # for i, child_list in enumerate(self.children):
        #     for child in child_list:
        #         new_children[child].append(i)
        rev_graph = LayerNetworkGraph(vertex_list=self.vertex_list[::-1],
                                      vertex_layer=new_vertex_layer, children=[])
        for i in range(len(rev_graph)):
            # Reverse numbering for each node
            rev_graph.vertex_list[i].index = i
        for edge in self.edge_list:
            # Reverse the direction of each edge
            rev_graph.add_edge(self.num_ver - 1 - edge[1], self.num_ver - 1 - edge[0])
        # rev_graph.indegree = self.outdegree
        # rev_graph.outdegree = self.indegree

        return rev_graph

    def print_children(self):
        print("====children====")
        for ver_list in self.children:
            print([self.vertex_list[idx].name for idx in ver_list])
            # print("[", end='')
            # for ver in ver_list:
            #     print(ver.name, ":", self.children[ver.index])
            #     print(ver.name, ":", [self.vertex_list[idx].name for idx in self.children[ver.index]])  # , end=',')
            # print("]")

    def print_layers(self):
        for layer in self.vertex_layer:
            print(layer)

    def __len__(self):
        return len(self.vertex_list)

    def depth(self):
        return len(self.vertex_layer)
