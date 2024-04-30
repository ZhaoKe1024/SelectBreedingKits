#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import math
import random
import numpy as np

from analyzer.LayerGraph import LayerNetworkGraph
from procedure.xlsx2graph import build_family_graph_base
from procedure.xlsxreader import read_population_from_xlsx, get_df_from_xlsx
from selector.GASelector import GASelector
from procedure.kinship_on_graph import Kinship
from selector.entities import Poultry, Vertex
from func import get_familyid

def run_main():
    # # --------------Input Matrix--------------
    # popus, male_idxs, female_idxs = read_population_from_xlsx()
    # # print()
    # np.random.seed(42)  # 2024-04-02
    # kinship_matrix = 1 / 16 + 1 / 16 * np.random.randn(len(male_idxs), len(female_idxs))
    vertex_list, vertex_layer, children_list, pre_name2idx = build_family_graph_base()
    N = len(vertex_list)
    # ------------Poultry read and build-------------------------
    edges_df = get_df_from_xlsx(sheet_name="20", cols=[7, 8, 9, 10])
    # print(edges_df.columns)
    popus = []
    new_vertices = []
    # new_children = []
    for idx, row in enumerate(edges_df.itertuples()):
        # if sheet_name == "19":
        # print("row:", row)
        wi = str(getattr(row, "翅号")) if "翅号" in edges_df.columns else str(getattr(row, "_1"))
        fa_i = str(getattr(row, "_2"))
        ma_i = str(getattr(row, "_3"))
        f_i = str(getattr(row, "_4"))
        vertex_list.append(Vertex(index=N+idx, name=wi, depth=0, family_id=f_i))
        children_list[pre_name2idx[fa_i]].append(N+idx)
        children_list[pre_name2idx[ma_i]].append(N+idx)
        popus.append(Poultry(fi=f_i, wi=wi, fa_i=fa_i, ma_i=ma_i, sex=0, inbreedc=0.))
    vertex_list.extend(new_vertices)
    vertex_layer.append([ver.index for ver in new_vertices])
    # children_list =
    layergraph = LayerNetworkGraph(vertex_list=vertex_list, vertex_layer=vertex_layer, children=children_list)
    kinship = Kinship(graph=layergraph)
    # print(kinship.calc_inbreed_coef(p="14774"))
    # kinship.print_edges()
    # kinship.print_layer()
    # kinship.print_parents()
    # kinship.print_all_poultry()
    # print(kinship.calc_kinship_corr(p1="14761", p2="14766"))
    random.shuffle(popus)
    male_rate = 1. / 11.
    male_num = math.ceil(male_rate * len(popus))
    female_num = len(popus) - male_num
    for i in range(male_num):
        vertex_list[i].gender = 1
        popus[i].sex = 1
    name2idx = dict()
    for i, p in enumerate(popus):
        name2idx[p.wing_id] = i
    # -------------Kinship read and build-------------

    kinship_matrix = np.zeros((male_num, female_num))
    for i in range(male_num):
        for j in range(female_num):
            kinship_matrix[i][j] = kinship.calc_kinship_corr(p1=popus[i].wing_id, p2=popus[male_num+j].wing_id)
    print(kinship_matrix)
    print("max min")
    print(np.max(kinship_matrix), np.min(kinship_matrix))
    print(np.sum(kinship_matrix))

    # ===============================Algorithm==================================
    # ====================Here is vanilla Genetic Algorithm=====================

    GAS = GASelector(popus=popus, kinship_matrix=kinship_matrix, male_idxs=list(range(male_num)), female_idxs=list(range(male_num, len(popus))))
    best_solution = GAS.scheduler()

    pre_pos = best_solution.vector_male[0]
    cur_female = best_solution.vector_female[0]
    print("========----------育种方案----------==========")
    print("(家系号，雄性个体编号)：[(家系号，雌性个体编号)]")
    idx = 1
    fout = open("./result_name.csv", 'w', encoding="utf_8")
    fout.write("家系号,公号,母号,亲缘相关系数\n")
    year, mi, fi = "21", 1, 1
    print(
        f"{popus[pre_pos].family_id},{pre_pos}:[({popus[cur_female].family_id},{male_num + cur_female})",
        end=', ')
    fout.write(get_familyid(year, mi, fi)+","+popus[pre_pos].wing_id+","+popus[male_num + cur_female].wing_id+","+f"{kinship_matrix[pre_pos, cur_female]}.5f"+'\n')
    fi += 1
    while idx < len(best_solution):
        cur_male = best_solution.vector_male[idx]
        cur_male_name = popus[cur_male].wing_id
        cur_female = best_solution.vector_female[idx]
        cur_female_name = popus[male_num+cur_female].wing_id
        if cur_male != pre_pos:
            mi += 1
        fi += 1
        fout.write(get_familyid(year, mi, fi) + "," + cur_male_name + "," + cur_female_name +","+f"{kinship_matrix[cur_male, cur_female]:.5f}" + '\n')
        pre_pos = cur_male
        idx += 1
    print("]")
    fout.write('\n')
    fout.close()


if __name__ == '__main__':
    run_main()
    # print(np.random.randn(2, 10))
