#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/5/22 15:07
# @Author: ZhaoKe
# @File : graphfromtable.py
# @Software: PyCharm
from procedure.xlsxreader import get_df_from_xlsx
from selector.entities import Vertex
from analyzer.LayerGraph import LayerNetworkGraph
from procedure.xlsx2graph import build_family_graph_base


def get_graph_from_data(file_path):
    # # --------------Input Matrix--------------
    # popus, male_idxs, female_idxs = read_population_from_xlsx()
    # # print()
    # np.random.seed(42)  # 2024-04-02
    # kinship_matrix = 1 / 16 + 1 / 16 * np.random.randn(len(male_idxs), len(female_idxs))
    sheet_list = ["16", "17", "18", "19", "20"]
    vertex_list, vertex_layer, children_list, pre_name2idx = build_family_graph_base(
        file_path=file_path,
        sheet_list=sheet_list)
    N = len(vertex_list)
    # print("pre_name2idx:")
    # print(pre_name2idx)
    # ------------Poultry read and build-------------------------
    edges_df = get_df_from_xlsx(filepath=file_path, sheet_name="20",
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
    idx2year = {0: "16", 1: "17", 2: "18", 3: "19", 4: "20", 5:"21"}
    # for idx, item in enumerate(vertex_layer):
    #     print(idx2year[idx])
    #     print([vertex_list[j].name for j in item])
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph, vertex_layer, vertex_list
