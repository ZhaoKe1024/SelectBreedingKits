#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/4/7 20:14
# @Author: ZhaoKe
# @File : xlsx2graph.py
# @Software: PyCharm
from typing import List

from analyzer.LayerGraph import LayerNetworkGraph
from selector.entities import Vertex
from procedure.xlsxreader import get_df_from_xlsx


def read_vertices_from_xlsx(file_path="./历代配种方案及出雏对照2021.xlsx", sheet_name: str = "16", id_start=0, depth=0) -> List[
    Vertex]:
    sex_table = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_name, cols=[1, 2, 3])
    # print(sex_table.head())
    # -----------------------------------------------
    # -------------Build Vertex List-----------------
    # -----------------------------------------------
    # print(sex_table.iloc[:, 1])
    male_id_len = len(set(sex_table.iloc[:, 1]))
    female_id_len = len(set(sex_table.iloc[:, 2]))
    # print("number of male poultry in " + sheet_name + ":" + str(male_id_len))
    # print("number of female poultry in " + sheet_name + ":" + str(female_id_len))
    male_name_set = set()
    name2id = dict()
    male_vertex_list = []
    female_veretx_list = []
    male_id, female_id = 0, 0
    for row in sex_table.itertuples():
        name = getattr(row, "公鸡号")
        family_id = getattr(row, "家系号")
        if not name in male_name_set:
            # name2id[name] = id_start
            male_name_set.add(name)
            male_vertex_list.append(Vertex(index=id_start + male_id,
                                           name=name,
                                           depth=depth,
                                           gender=1,
                                           family_id=family_id))
            male_id += 1
        female_veretx_list.append(Vertex(index=id_start + male_id_len + female_id,
                                         name=getattr(row, "母鸡号"),
                                         depth=depth,
                                         gender=0,
                                         family_id=family_id))
        name2id[name] = id_start
        name2id[getattr(row, "母鸡号")] = male_id_len + id_start
        female_id += 1

    # print("number of female poultry in " + sheet_name + ":" + str(len(female_veretx_list)))
    cur_vertex_list = male_vertex_list + female_veretx_list
    return cur_vertex_list

    #     if wi in male_set:
    #         sex_id = 1
    #         MaleIdxs.append(idx)
    #         popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
    #                              ma_i=ma_i, sex=1, inbreedc=0.0))
    #     elif wi in fema_set:
    #         sex_id = 0
    #         FemaIdxs.append(idx)
    #         popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
    #                              ma_i=ma_i, sex=0, inbreedc=0.0))
    #     else:
    #         UnknIdxs.append(idx)
    #         popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
    #                              ma_i=ma_i, sex=0, inbreedc=0.0))
    #
    # N = len(parent_df)
    # print(f"一共有个{N}个体, 雄性个体{len(MaleIdxs)}个,雌性个体{len(FemaIdxs)}个,未知个体{len(UnknIdxs)}个。")
    # if len(MaleIdxs) < 14:
    #     # 14-18个雄性
    #     newIdxs = random.sample(set(UnknIdxs), random.randint(14, 19) - len(MaleIdxs))
    #     MaleIdxs.extend(newIdxs)
    #     for ind in newIdxs:
    #         popus[ind].sex = 1
    #     FemaIdxs.extend(set(UnknIdxs) - set(newIdxs))
    #     # print("重新选中：", newIdxs)
    #     # print(MaleIdxs)
    # elif len(MaleIdxs) > 18:
    #     negaIdxs = random.sample(MaleIdxs, len(MaleIdxs) - random.randint(14, 19))
    #     for ind in negaIdxs:
    #         popus[ind].sex = 0
    # #     print(MaleIdxs)
    # # print("雄性个体选中：")
    # # for item in MaleIdxs:
    # #     print(item, end=', ')
    # print(f"公鸡{len(MaleIdxs)}个, 母鸡{len(FemaIdxs)}个:")
    # return popus, MaleIdxs, FemaIdxs


def read_vertices_edges_from_xlsx(file_path, sheet_name, pre_sheet_name,
                                  id_start=0, depth=0, pre_name2ind: dict = None):
    cur_vertex_list = read_vertices_from_xlsx(file_path=file_path, sheet_name=sheet_name,
                                              id_start=id_start, depth=depth)
    # -----------------------------------------------
    # --------------Build Edge List------------------
    # -----------------------------------------------
    cur_name2idx = dict()
    for ver in cur_vertex_list:
        cur_name2idx[ver.name] = ver.index
        # if sheet_name == "19":
        #     print(f"name:{ver.name}_index:{ver.index}")
    # print(cur_name2idx)
    pre_children = [[] for _ in range(len(pre_name2ind))]
    edges_df = get_df_from_xlsx(filepath=file_path, sheet_name=pre_sheet_name, cols=[7, 8, 9])
    # print(edges_df.columns)
    for idx, row in enumerate(edges_df.itertuples()):
        # if sheet_name == "19":
        # print("row:", row)
        wi = str(getattr(row, "翅号")) if "翅号" in edges_df.columns else str(getattr(row, "_1"))
        # if sheet_name == "19":
        #     print("row:", row)
        #     print("wi:", wi)
        if wi in cur_name2idx:
            fa_i = str(getattr(row, "_2"))
            ma_i = str(getattr(row, "_3"))
            pre_children[pre_name2ind[fa_i]].append(cur_name2idx[wi])
            pre_children[pre_name2ind[ma_i]].append(cur_name2idx[wi])
    # for i, child_list in enumerate(pre_children):
    #     print(pre[i].name, ":", child_list)
    # if sheet_name == "19":
    #     for i, key in enumerate(pre_name2ind):
    #         print(key, ":", pre_children[i])
    return cur_vertex_list, pre_children


def build_family_graph()-> LayerNetworkGraph:
    sheet_list = ["16", "17", "18", "19", "20"]
    depth = len(sheet_list)
    vertex_list = []
    vertex_layer = [[] for _ in range(depth)]
    idx = 0
    # =============================初代点
    each_vertex_list = read_vertices_from_xlsx(sheet_name=sheet_list[0], id_start=idx, depth=depth)

    pre_name2idx = dict()
    for i, ver in enumerate(each_vertex_list):
        vertex_layer[0].append(ver.index)
        pre_name2idx[ver.name] = i
    skip_id = len(each_vertex_list)
    idx += skip_id
    vertex_list.extend(each_vertex_list)
    # ============第二代开始的点，和上一代的边-------------
    children_list = []
    for depth, sheet_name in enumerate(sheet_list):
        if depth == 0:
            continue
        print("start point and edge:", sheet_name)
        each_vertex_list, pre_children = read_vertices_edges_from_xlsx(file_path="./历代配种方案及出雏对照2021.xlsx",
                                                                       sheet_name=sheet_list[depth],
                                                                       pre_sheet_name=sheet_list[depth - 1],
                                                                       id_start=idx, depth=depth, pre_name2ind=pre_name2idx)
        pre_name2idx = dict()
        for i, ver in enumerate(each_vertex_list):
            vertex_layer[depth].append(ver.index)
            pre_name2idx[ver.name] = i
        vertex_list.extend(each_vertex_list)
        skip_id = len(each_vertex_list)
        idx += skip_id
        children_list.extend(pre_children)
    # 最后一层children全设置为[]
    for _ in range(len(vertex_layer[-1])):
        children_list.append([])

    # for i, ver in enumerate(vertex_list):
    #     print(i, ver)
    # print(sum([len(item) for item in vertex_layer]))
    # print(len(children_list))

    # for i, child_list in enumerate(children_list):
    #     print(vertex_list[i].name, ":", [vertex_list[val].name for val in child_list])
    #     if i > 100:
    #         break

    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph


if __name__ == '__main__':
    # read_population_from_xlsx()
    build_family_graph()
