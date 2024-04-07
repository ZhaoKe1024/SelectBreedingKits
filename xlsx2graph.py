#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/4/7 20:14
# @Author: ZhaoKe
# @File : xlsx2graph.py
# @Software: PyCharm
from typing import List
import pandas as pd
import random

from selector.entities import Poultry
from analyzer.LayerGraph import LayerNetworkGraph
from selector.entities import Vertex
from xlsxreader import get_df_from_xlsx


def read_population_from_xlsx(file_path="./历代配种方案及出雏对照2021.xlsx", sheet_name: str = "16", id_start=0):
    sex_table = get_df_from_xlsx(filepath=file_path, sheet_name=sheet_name, cols=[1, 2, 3])
    # print(sex_table.head())
    # -----------------------------------------------
    # -------------Build Vertex List-----------------
    # -----------------------------------------------
    print(sex_table.iloc[:, 1])
    male_id_len = len(set(sex_table.iloc[:, 1]))
    female_id_len = len(set(sex_table.iloc[:, 2]))
    print("number of male poultry in "+sheet_name+":"+ str(male_id_len))
    print("number of female poultry in "+sheet_name+":"+ str(female_id_len))
    male_name_set = set()
    # fema_name_set = set()
    cur_vertex_list = []
    name2id = dict()
    male_vertex_list = []
    female_veretx_list = []
    for row in sex_table.itertuples():
        name = getattr(row, "公鸡号")
        family_id = getattr(row, "家系号")
        if not name in male_name_set:
            # name2id[name] = id_start
            male_vertex_list.append(Vertex(index=id_start,
                                           name=name,
                                           gender=1,
                                           family_id=family_id))
        female_veretx_list.append(Vertex(index=male_id_len+id_start,
                                         name=getattr(row, "母鸡号"),
                                         gender=0,
                                         family_id=family_id))
        name2id[name] = id_start
        name2id[getattr(row, "母鸡号")] = male_id_len+id_start
        id_start += 1

    print("number of female poultry in "+sheet_name+":"+ str(len(female_veretx_list)))
    cur_vertex_list = male_vertex_list + female_veretx_list

    # -----------------------------------------------
    # --------------Build Edge List------------------
    # -----------------------------------------------
    
    parent_df = get_df_from_xlsx(filepath=file_path, sheet_name="16", cols=[6, 7, 8, 9, 10])

    popus = []
    MaleIdxs = []
    FemaIdxs = []
    UnknIdxs = []
    for idx, row in enumerate(parent_df.itertuples()):
        wi = getattr(row, "翅号")
        fa_i = getattr(row, "父号")
        ma_i = getattr(row, "母号")
        # print(f"({wi}<--{fa_i},{ma_i})")
        if wi in male_set:
            sex_id = 1
            MaleIdxs.append(idx)
            popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
                                 ma_i=ma_i, sex=1, inbreedc=0.0))
        elif wi in fema_set:
            sex_id = 0
            FemaIdxs.append(idx)
            popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
                                 ma_i=ma_i, sex=0, inbreedc=0.0))
        else:
            UnknIdxs.append(idx)
            popus.append(Poultry(fi=getattr(row, "_5"), wi=wi, fa_i=fa_i,
                                 ma_i=ma_i, sex=0, inbreedc=0.0))

    N = len(parent_df)
    print(f"一共有个{N}个体, 雄性个体{len(MaleIdxs)}个,雌性个体{len(FemaIdxs)}个,未知个体{len(UnknIdxs)}个。")
    if len(MaleIdxs) < 14:
        # 14-18个雄性
        newIdxs = random.sample(set(UnknIdxs), random.randint(14, 19) - len(MaleIdxs))
        MaleIdxs.extend(newIdxs)
        for ind in newIdxs:
            popus[ind].sex = 1
        FemaIdxs.extend(set(UnknIdxs) - set(newIdxs))
        # print("重新选中：", newIdxs)
        # print(MaleIdxs)
    elif len(MaleIdxs) > 18:
        negaIdxs = random.sample(MaleIdxs, len(MaleIdxs) - random.randint(14, 19))
        for ind in negaIdxs:
            popus[ind].sex = 0
    #     print(MaleIdxs)
    # print("雄性个体选中：")
    # for item in MaleIdxs:
    #     print(item, end=', ')
    print(f"公鸡{len(MaleIdxs)}个, 母鸡{len(FemaIdxs)}个:")
    return popus, MaleIdxs, FemaIdxs


def build_family_graph():
    sheet_list = ["16", "17", "18", "19", "20", "21"]
    depth = len(sheet_list)
    vertex_list = []
    vertex_layer = [[] for _ in range(depth)]
    idx = 0
    for sheet_name in sheet_list:
        read_population_from_xlsx(sheet_name=sheet_name)
    for j, num in enumerate(num_per_layer):
        for i in range(num):
            vertex_list.append(Vertex(index=idx, name=f"{j}_{i}", depth=j))
            vertex_layer[j].append(idx)
            idx += 1
    children_list = [[] for _ in range(len(vertex_list))]

    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    return layergraph
if __name__ == '__main__':
    read_population_from_xlsx()