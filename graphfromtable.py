#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/5/22 15:07
# @Author: ZhaoKe
# @File : graphfromtable.py
# @Software: PyCharm
import pandas as pd
from inbreed_lib.procedure.xlsxreader import get_df_from_xlsx
from inbreed_lib.selector.entities import Vertex
from inbreed_lib.analyzer.LayerGraph import LayerNetworkGraph
from inbreed_lib.procedure.xlsx2graph import build_family_graph_base


def get_graph_from_csv(file_path):
    # # --------------Input Matrix--------------
    # popus, male_idxs, female_idxs = read_population_from_xlsx()
    # # print()
    # np.random.seed(42)  # 2024-04-02
    # kinship_matrix = 1 / 16 + 1 / 16 * np.random.randn(len(male_idxs), len(female_idxs))
    df = pd.read_excel(file_path, header=0, sheet_name=None)
    sheet_list = list(df.keys())
    # for item in sheet_list:
    #     if item
    vertex_list, vertex_layer, children_list, pre_name2idx = build_family_graph_base(
        file_path=file_path,
        sheet_list=sheet_list)
    N = len(vertex_list)
    # print("pre_name2idx:")
    # print(pre_name2idx)
    # ------------Poultry read and build-------------------------
    edges_df = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_list[-1],
                                cols=[7, 8, 9, 10])
    # print(edges_df.columns)
    # new_children = []
    new_vertices = []
    for idx, row in enumerate(edges_df.itertuples()):
        # if sheet_name == "19":
        # print("row:", row)
        wi = str(getattr(row, "翅号")) if "翅号" in edges_df.columns else str(getattr(row, "_1"))
        fa_i = str(getattr(row, "_2"))
        ma_i = str(getattr(row, "_3"))
        f_i = str(getattr(row, "_4"))
        vertex_list.append(Vertex(index=N + idx, name=wi, depth=0, family_id=f_i))
        new_vertices.append(Vertex(index=N + idx, name=wi, depth=0, family_id=f_i))
        # print(wi, fa_i, ma_i)
        # print(pre_name2idx[fa_i], pre_name2idx[ma_i])
        # print(children_list[pre_name2idx[fa_i]])
        children_list[pre_name2idx[fa_i]].append(N + idx)
        children_list[pre_name2idx[ma_i]].append(N + idx)
    vertex_list.extend(new_vertices)
    vertex_layer.append([ver.index for ver in new_vertices])
    # children_list =
    idx2year = {0: "16", 1: "17", 2: "18", 3: "19", 4: "20", 5: "21"}
    # for idx, item in enumerate(vertex_layer):
    #     print(idx2year[idx])
    #     print([vertex_list[j].name for j in item])
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph, vertex_layer, vertex_list, sheet_list


def get_graph_from_data(file_path):
    # # --------------Input Matrix--------------
    # popus, male_idxs, female_idxs = read_population_from_xlsx()
    # # print()
    # np.random.seed(42)  # 2024-04-02
    # kinship_matrix = 1 / 16 + 1 / 16 * np.random.randn(len(male_idxs), len(female_idxs))
    df = pd.read_excel(file_path, header=0, sheet_name=None, usecols=[1, 2, 3], engine='openpyxl')
    # print(df)
    sheet_list = list(df.keys())
    while sheet_list[-1][:5] == "Sheet":
        del sheet_list[-1]
    print("sheet list:", sheet_list)
    # for item in sheet_list:
    #     if item
    vertex_list, vertex_layer, children_list, pre_name2idx = build_family_graph_base(
        file_path=file_path,
        sheet_list=sheet_list)
    N = len(vertex_list)
    print("pre_name2idx:")
    print(pre_name2idx)
    print("-------children-0---------")
    for idx, cd in enumerate(children_list):
        print(idx, ": ", cd)
    # ------------Poultry read and build-------------------------
    edges_df = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_list[-1],
                                cols=[7, 8, 9, 10, 11])
    print("edge columns", edges_df.columns)
    print(edges_df)
    # new_children = []
    new_vertices = []
    for idx, row in enumerate(edges_df.itertuples()):
        # if sheet_name == "19":
        # print("row:", row)
        wi = str(getattr(row, "翅号")) if "翅号" in edges_df.columns else str(getattr(row, "_1"))
        fa_i = str(getattr(row, "父号"))
        ma_i = str(getattr(row, "母号"))
        f_i = str(getattr(row, "_4"))
        if "性别" in edges_df.columns:
            gd = str(getattr(row, "性别"))
        else:
            gd = -1
        vertex_list.append(Vertex(index=N + idx, name=wi, depth=0, family_id=f_i, gender=gd))
        children_list.append([])
        new_vertices.append(Vertex(index=N + idx, name=wi, depth=0, family_id=f_i, gender=gd))
        # print(wi, fa_i, ma_i)
        # print(pre_name2idx[fa_i], pre_name2idx[ma_i])
        # print(children_list[pre_name2idx[fa_i]])
        children_list[pre_name2idx[fa_i]].append(N + idx)
        children_list[pre_name2idx[ma_i]].append(N + idx)

    vertex_layer.append([ver.index for ver in new_vertices])

    print("len:", len(vertex_list))
    print([j.name for j in vertex_list])
    idx2year = {0: "2014", 1: "2015", 2: "2016", 3: "2017", 4: "2018", 5: "2019", 6: "2020"}
    for idx, item in enumerate(vertex_layer):
        print(idx2year[idx])
        print([vertex_list[j].name for j in item])

    for idx, cd in enumerate(children_list):
        print(idx, ": ", cd)
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph, vertex_layer, vertex_list, sheet_list


if __name__ == '__main__':
    lg, vl, vl2, sl = get_graph_from_data("../datasets/first330.xlsx")
    print(len(lg), lg.depth())
    print(vl[0][0], vl[0][1])
    print(vl2[0])
    print(vl2[1])
    print(sl)
