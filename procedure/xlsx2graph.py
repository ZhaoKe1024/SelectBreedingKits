#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/4/7 20:14
# @Author: ZhaoKe
# @File : xlsx2graph.py
# @Software: PyCharm
from typing import List

from inbreed_lib.analyzer.LayerGraph import LayerNetworkGraph
from inbreed_lib.selector.entities import Vertex
from inbreed_lib.procedure.xlsxreader import get_df_from_xlsx


def read_init_vertices_from_xlsx(file_path="./历代配种方案及出雏对照2021.xlsx", sheet_name: str = "16", id_start=0,
                                 depth=0) -> List[Vertex]:
    sex_table = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_name, cols=[1, 2, 3],
                                 types={"家系号": str, "公鸡号": str, "母鸡号": str})
    sex_table.dropna(how="all", inplace=True)
    print(sex_table.head())
    # -----------------------------------------------
    # -------------Build Vertex List-----------------
    # -----------------------------------------------
    # print(sex_table.iloc[:, 1])
    male_id_len = len(set(sex_table.iloc[:, 1]))
    female_id_len = len(set(sex_table.iloc[:, 2]))
    print("number of male poultry in " + sheet_name + ":" + str(male_id_len))
    print("number of female poultry in " + sheet_name + ":" + str(female_id_len))
    male_name_set = set()
    female_name_set = set()
    name2id = dict()
    male_vertex_list = []
    female_veretx_list = []
    male_id, female_id = 0, 0
    for row in sex_table.itertuples():
        name = getattr(row, "公鸡号")
        # if name
        name = name.split('.')[0]
        family_id = getattr(row, "家系号").split('.')[0]
        fname = getattr(row, "母鸡号").split('.')[0]
        if name not in male_name_set:
            # name2id[name] = id_start
            male_name_set.add(name)
            male_vertex_list.append(Vertex(index=id_start + male_id,
                                           name=name,
                                           depth=depth,
                                           gender=1,
                                           family_id=family_id))
            male_id += 1
            name2id[name] = id_start
        if fname not in female_name_set:
            female_name_set.add(fname)
            female_veretx_list.append(Vertex(index=id_start + male_id_len + female_id,
                                             name=fname,
                                             depth=depth,
                                             gender=0,
                                             family_id=family_id))
            female_id += 1
            name2id[fname] = male_id_len + id_start

    # print("number of female poultry in " + sheet_name + ":" + str(len(female_veretx_list)))
    cur_vertex_list = male_vertex_list + female_veretx_list
    print("len of cur vertex list:")
    print(len(male_vertex_list), len(female_veretx_list))
    print(len(cur_vertex_list))
    return cur_vertex_list


# def read_vertices_from_xlsx(file_path="./历代配种方案及出雏对照2021.xlsx", sheet_name: str = "16", id_start=0,
#                             depth=0) -> List[Vertex]:
#     sex_table = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_name, cols=[7, 8, 9, 10, 11])
#     print(sex_table.head(10))
#     # -----------------------------------------------
#     # -------------Build Vertex List-----------------
#     # -----------------------------------------------
#     # print(sex_table.iloc[:, 1])
#     male_name_set = set()
#     male_vertex_list = []
#     male_id, female_id = 0, 0
#     for row in sex_table.itertuples():
#         name = row[2]  # getattr(row, "公鸡号")
#         family_id = row[4]  # getattr(row, "家系号")
#         if not name in male_name_set:
#             # name2id[name] = id_start
#             male_name_set.add(name)
#             male_vertex_list.append(Vertex(index=id_start + male_id,
#                                            name=name,
#                                            depth=depth,
#                                            gender=1,
#                                            family_id=family_id))
#             male_id += 1
#         female_veretx_list.append(Vertex(index=id_start + male_id_len + female_id,
#                                          name=row[3],  # getattr(row, "母鸡号"),
#                                          depth=depth,
#                                          gender=0,
#                                          family_id=family_id))
#         name2id[name] = id_start
#         name2id[row[3]] = male_id_len + id_start
#         female_id += 1
#
#     male_id_len = len(set(sex_table.iloc[:, 1]))
#     female_id_len = len(set(sex_table.iloc[:, 2]))
#     # print("number of male poultry in " + sheet_name + ":" + str(male_id_len))
#     # print("number of female poultry in " + sheet_name + ":" + str(female_id_len))
#     name2id = dict()
#     female_veretx_list = []
#     for row in sex_table.itertuples():
#         name = row[2]  # getattr(row, "公鸡号")
#         family_id = row[4]  # getattr(row, "家系号")
#         if not name in male_name_set:
#             # name2id[name] = id_start
#             male_name_set.add(name)
#             male_vertex_list.append(Vertex(index=id_start + male_id,
#                                            name=name,
#                                            depth=depth,
#                                            gender=1,
#                                            family_id=family_id))
#             male_id += 1
#         female_veretx_list.append(Vertex(index=id_start + male_id_len + female_id,
#                                          name=row[3],  # getattr(row, "母鸡号"),
#                                          depth=depth,
#                                          gender=0,
#                                          family_id=family_id))
#         name2id[name] = id_start
#         name2id[row[3]] = male_id_len + id_start
#         female_id += 1
#
#     # print("number of female poultry in " + sheet_name + ":" + str(len(female_veretx_list)))
#     cur_vertex_list = male_vertex_list + female_veretx_list
#     return cur_vertex_list


def read_vertices_edges_from_xlsx(file_path, sheet_name, pre_sheet_name,
                                  id_start=0, depth=0, pre_name2ind: dict = None, pre_children=None):
    print("read points from:{}.".format(sheet_name))
    cur_vertex_list = read_init_vertices_from_xlsx(file_path=file_path, sheet_name=sheet_name,
                                                   id_start=id_start, depth=depth)

    # -----------------------------------------------
    # --------------Build Edge List------------------
    # -----------------------------------------------
    cur_name2idx = dict()
    for ver in cur_vertex_list:
        cur_name2idx[ver.name] = ver.index
        # if sheet_name in ["17", "18"]:
        #     print(f"name:{ver.name}_index:{ver.index}")
    print("pre_name2idx")
    print(pre_name2ind)
    print("cur_name2idx:")
    print(cur_name2idx)
    #
    print("pre number", len(pre_name2ind))
    print("children list length:{}.".format(len(pre_children)))
    print("read edges from {}.".format(pre_sheet_name))
    edges_df = get_df_from_xlsx(filepath=file_path, sheet_name=pre_sheet_name, cols=[7, 8, 9, 11],
                                types={"翅号": str, "父号": str, "母号": str})
    edges_df.dropna(how="all", inplace=True)
    print(edges_df.columns)
    for idx, row in enumerate(edges_df.itertuples()):
        # if sheet_name == "19":
        # print("row:", row, row[1], row[2], row[3])
        wi = str(getattr(row, "翅号")) if "翅号" in edges_df.columns else str(getattr(row, "_1"))
        wi = wi.split('.')[0]
        # if sheet_name in ["17", "18"]:
        # print("row:", row)
        # print("wi:", wi)
        if wi in cur_name2idx:
            fa_i = str(getattr(row, "父号")).split('.')[0]
            ma_i = str(getattr(row, "母号")).split('.')[0]
            print("fa mi:", fa_i, ma_i, cur_name2idx[wi])
            print("pre_name2ind:", pre_name2ind[fa_i], pre_name2ind[ma_i])
            print(pre_children[pre_name2ind[fa_i]])
            print(pre_name2ind[ma_i])
            print(pre_children[pre_name2ind[ma_i]])
            print(cur_name2idx[wi])
            pre_children[pre_name2ind[fa_i]].append(cur_name2idx[wi])
            pre_children[pre_name2ind[ma_i]].append(cur_name2idx[wi])
    # for i, child_list in enumerate(pre_children):
    #     print(pre[i].name, ":", child_list)
    # if sheet_name in ["17", "18"]:
    #     for i, key in enumerate(pre_name2ind):
    #         print(key, ":", pre_children[i])
    return cur_vertex_list, pre_children


def build_family_graph_base(file_path="./历代配种方案及出雏对照2021_带性别.xlsx", sheet_list=None):
    sheet_list = sheet_list
    depth = len(sheet_list)
    vertex_list = []
    vertex_layer = [[] for _ in range(depth)]
    idx = 0
    # =============================初代点
    each_vertex_list = read_init_vertices_from_xlsx(file_path=file_path, sheet_name=sheet_list[0], id_start=idx,
                                                    depth=depth)

    pre_name2idx = dict()
    for i, ver in enumerate(each_vertex_list):
        vertex_layer[0].append(ver.index)
        pre_name2idx[ver.name] = i
    map_len = len(pre_name2idx)
    # print("pre_name2idx:")
    # print(pre_name2idx)
    skip_id = len(each_vertex_list)
    idx += skip_id
    vertex_list.extend(each_vertex_list)
    # ============第二代开始的点，和上一代的边-------------
    children_list = []
    for _ in vertex_list:
        children_list.append([])
    for depth, sheet_name in enumerate(sheet_list):
        if depth == 0:
            continue
        print("build start point and edge for sheet:", sheet_name)
        if sheet_name[:5] == "Sheet":
            continue
        each_vertex_list, children_list = read_vertices_edges_from_xlsx(file_path=file_path,
                                                                        sheet_name=sheet_list[depth],
                                                                        pre_sheet_name=sheet_list[depth - 1],
                                                                        id_start=idx, depth=depth,
                                                                        pre_name2ind=pre_name2idx,
                                                                        pre_children=children_list)
        # pre_name2idx = dict()
        # print("pre_children---------------")
        # print(pre_children)

        for _ in each_vertex_list:
            children_list.append([])
        for i, ver in enumerate(each_vertex_list):
            vertex_layer[depth].append(ver.index)
            pre_name2idx[ver.name] = map_len + i
        map_len = len(pre_name2idx)
        vertex_list.extend(each_vertex_list)
        skip_id = len(each_vertex_list)
        idx += skip_id
        # children_list.extend(pre_children)

    # # 最后一层children全设置为[]
    # for _ in range(len(vertex_layer[-1])):
    #     children_list.append([])

    for i, ver in enumerate(vertex_list):
        print(i, ver)
    print(sum([len(item) for item in vertex_layer]))
    print(len(children_list))

    for i, child_list in enumerate(children_list):
        print(vertex_list[i].name, ":", [vertex_list[val].name for val in child_list])
        if i > 100:
            break
    return vertex_list, vertex_layer, children_list, pre_name2idx


def build_family_graph(file_path="./历代配种方案及出雏对照2021_带性别.xlsx") -> LayerNetworkGraph:
    vertex_list, vertex_layer, children_list, _ = build_family_graph_base(
        file_path=file_path,
        sheet_list=["16", "17", "18", "19", "20"])
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph


if __name__ == '__main__':
    # read_population_from_xlsx()
    vertex_list, vertex_layer, children_list, pre_name2idx = build_family_graph_base(
        "../历代配种方案及出雏对照2021.xlsx")
    parents = [[] for _ in range(len(vertex_list))]
    for i, childs in enumerate(children_list):
        for ver in childs:
            parents[ver].append(i)
    for i, child_list in enumerate(parents):
        print(vertex_list[i].name, ":", [vertex_list[val].name for val in child_list])
    # build_family_graph()
