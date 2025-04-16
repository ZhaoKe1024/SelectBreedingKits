#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/8/1 18:06
# @Author: ZhaoKe
# @File : relationplot.py
# @Software: PyCharm
import random
# from pyecharts import options as opts
# from pyecharts.charts import Graph
# from pyecharts.render import make_snapshot
# from snapshot_selenium import snapshot as driver

# vertices = list(range(27))
# graph = [[10, 0], [10, 2], [12, 3], [12, 5], [18, 10], [18, 13], [13, 3], [13, 5], [19, 12], [19, 14], [14, 6], [14, 7],
#          [21, 16], [21, 17], [16, 9], [16, 12], [9, 0], [9, 1], [17, 10], [17, 11], [11, 3], [11, 4], [24, 21],
#          [24, 22], [22, 18], [22, 19], [25, 21], [25, 23], [23, 18], [23, 19]]
# depths = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5]

def tuple_contrain(tList, t2):
    if len(tList) == 0:
        return False
    for item in tList:
        if item[0] == t2[0] and item[1] == t2[1]:
            return True
    return False


def generate_relation_plot(vertices_depth_edges, save_path="graph_with_edge_options.html"):
    vertices = []
    # xy = []
    layers = set()
    # print("------1---------")
    for obj_item in vertices_depth_edges:
        if not tuple_contrain(vertices, (obj_item[0][0], obj_item[0][1])):
            vertices.append((obj_item[0][0], obj_item[0][1]))
            # xy.append((obj_item[0][1] * h_margin))
        if not tuple_contrain(vertices, (obj_item[1][0], obj_item[1][1])):
            vertices.append((obj_item[1][0], obj_item[1][1]))
        if obj_item[0][1] not in layers:
            layers.add(obj_item[0][1])
        if obj_item[1][1] not in layers:
            layers.add(obj_item[1][1])
            # xy.append((obj_item[1][1] * h_margin))
    # print("点集:", len(vertices), vertices)
    # print("层数：", layers)
    # edges = [[]] * len(layers)
    # print("------2---------")
    layers_tmp = [set() for _ in range(max(layers) + 1)]  # 不可以[set()]*(max(layers)+1)
    # print("------3---------")
    # print(layers_tmp)
    # max_num_layer = 0
    for obj_item in vertices_depth_edges:
        if obj_item[0] not in layers_tmp[obj_item[0][1]]:
            layers_tmp[obj_item[0][1]].add(obj_item[0])
        if obj_item[1] not in layers_tmp[obj_item[1][1]]:
            layers_tmp[obj_item[1][1]].add(obj_item[1])
    # print("------4---------")
    # print("统计：")
    # for item in layers_tmp:
    #     print(item)

    graph_v = []
    xy = []
    h_margin = 4
    v_margin = 8
    # print("------5---------")
    for j, obj_item in enumerate(layers_tmp):
        nlist = sorted(list(obj_item), key=lambda x: x[0])
        # print(nlist)
        top_m = 4
        for i, node in enumerate(nlist):
            graph_v.append(node[0])
            xy.append([j * h_margin, top_m + i * v_margin])
    # print("------6---------")
    graph_e = []
    for obj_item in vertices_depth_edges:
        graph_e.append([obj_item[0][0], obj_item[1][0]])
    print(graph_v)
    print(xy)
    print(graph_e)
    return graph_v, graph_e, xy
    # # vertices = [1, 2, 3, 4, 5, 6]
    # # graph = [[1, 4], [2, 4], [2, 5], [3, 5], [4, 6], [5, 6]]
    #
    # # xy = [[0, 5], [0, 8], [0, 11], [2, 7], [2, 9], [4, 8]]
    # # x left margin,  y: top margin
    # nodes_data = [opts.GraphNode(x=xy[j][0] * h_margin, y=xy[j][1], name="{}".format(graph_v[j]), symbol_size=20) for j
    #               in
    #               range(len(graph_v))]
    # links_data = []
    # for item in graph_e:
    #     links_data.append(opts.GraphLink(source="{}".format(item[0]), target="{}".format(item[1]), value=2))
    # # print(nodes_data)
    # # print(xy)
    # # print(links_data)
    # c = (
    #     Graph()
    #     .add(
    #         "Poultry Relation",
    #         nodes_data,
    #         links_data,
    #         repulsion=4000,
    #         edge_label=opts.LabelOpts(
    #             is_show=True, position="middle", formatter="{b}:{c}"
    #         ),
    #         edge_symbol=["none", "arrow"],
    #         layout="none"
    #     )
    #     .set_global_opts(
    #         title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink-WithEdgeLabel")
    #     )
    #     .render(save_path)
    # )
    # make_snapshot(driver, c, "test.png")


if __name__ == '__main__':
    obj_list = [((10, 4), (0, 5)), ((10, 4), (2, 5)), ((12, 4), (3, 5)), ((12, 4), (5, 5)), ((18, 3), (10, 4)),
                ((18, 3), (13, 4)),
                ((13, 4), (3, 5)), ((13, 4), (5, 5)), ((19, 3), (12, 4)), ((19, 3), (14, 4)), ((14, 4), (6, 5)),
                ((14, 4), (7, 5)),
                ((21, 2), (16, 3)), ((21, 2), (17, 3)), ((16, 3), (9, 4)), ((16, 3), (12, 4)), ((9, 4), (0, 5)),
                ((9, 4), (1, 5)),
                ((17, 3), (10, 4)), ((17, 3), (11, 4)), ((11, 4), (3, 5)), ((11, 4), (4, 5)), ((24, 1), (21, 2)),
                ((24, 1), (22, 2)), ((22, 2), (18, 3)), ((22, 2), (19, 3)), ((25, 1), (21, 2)), ((25, 1), (23, 2)),
                ((23, 2), (18, 3)), ((23, 2), (19, 3))]
    generate_relation_plot(obj_list)
