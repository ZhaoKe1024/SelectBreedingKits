#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import math
import random
import numpy as np
from graphfromtable import get_graph_from_data
from selector.GASelector import GASelector
from procedure.kinship_on_graph import Kinship
from func import get_familyid


def run_main(gene_idx="20"):
    layergraph, vertex_layer, vertex_list = get_graph_from_data(file_path="./历代配种方案及出雏对照2021_带性别.xlsx")
    kinship = Kinship(graph=layergraph)

    year2idx = {"16": 0, "17": 1, "18": 2, "19": 3, "20": 4, "21": 5}
    print("Load edges from", gene_idx)
    popus = []
    print("year idx", year2idx[gene_idx])
    # return
    if gene_idx == "21":
        # print(vertex_layer)
        for idx, item in enumerate(vertex_layer[year2idx[gene_idx]]):
            print(vertex_list[item].name)
            popus.append(vertex_list[item])
    else:
        # print(vertex_layer)
        for idx, item in enumerate(vertex_layer[year2idx[gene_idx]]):
            # print(vertex_list[item].name)
            popus.append(vertex_list[item])
            # popus.append(Poultry(fi=f_i, wi=wi, fa_i=fa_i, ma_i=ma_i, sex=0, inbreedc=0.))
    # return

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
        name2idx[p.name] = i
    # -------------Kinship read and build-------------

    kinship_matrix = np.zeros((male_num, female_num))
    for i in range(male_num):
        for j in range(female_num):
            kinship_matrix[i][j] = kinship.calc_kinship_corr(p1=popus[i].name, p2=popus[male_num + j].name)
    # print(kinship_matrix)
    # print("max min")
    # print(np.max(kinship_matrix), np.min(kinship_matrix))
    # print(np.sum(kinship_matrix))

    # ===============================Algorithm==================================
    # ====================Here is vanilla Genetic Algorithm=====================

    GAS = GASelector(popus=popus, kinship_matrix=kinship_matrix, male_idxs=list(range(male_num)),
                     female_idxs=list(range(male_num, len(popus))))
    best_solution = GAS.scheduler()

    pre_pos = best_solution.vector_male[0]
    cur_female = best_solution.vector_female[0]
    print("========----------育种方案----------==========")
    print("(家系号，雄性个体编号, 雌性个体编号)]")
    idx = 1
    fout = open(f"./result_name_rand_{gene_idx}.csv", 'w', encoding="utf_8")
    fout.write("家系号,公号,母号,亲缘相关系数\n")
    year, mi, fi = "21", 1, 1
    print(
        f"{popus[pre_pos].family_id},{pre_pos}:[({popus[cur_female].family_id},{male_num + cur_female})",
        end=', ')
    fout.write(get_familyid(year, mi, fi) + "," + popus[pre_pos].name + "," + popus[
        male_num + cur_female].name + "," + f"{kinship_matrix[pre_pos, cur_female]:.5f}" + '\n')
    fi += 1
    threshold = 0.2
    while idx < len(best_solution):
        cur_male = best_solution.vector_male[idx]
        cur_male_name = popus[cur_male].name
        cur_female = best_solution.vector_female[idx]
        cur_female_name = popus[male_num + cur_female].name
        if cur_male != pre_pos:
            mi += 1
        fi += 1
        # <<<<<<< Updated upstream
        # fout.write(get_familyid(year, mi,
        #                         fi) + "," + cur_male_name + "," + cur_female_name + "," + f"{kinship_matrix[cur_male, cur_female]:.5f}" + '\n')
        # =======
        ibc = kinship_matrix[cur_male, cur_female]
        if ibc < threshold:
            fout.write(get_familyid(year, mi,
                                    fi) + "," + cur_male_name + "," + cur_female_name + "," + f"{ibc:.5f}" + '\n')
            print(get_familyid(year, mi,
                               fi) + "," + cur_male_name + "," + cur_female_name + "," + f"{ibc:.5f}")
        # >>>>>>> Stashed changes
        pre_pos = cur_male
        idx += 1
    print("]")
    fout.write('\n')
    fout.close()
    print(f"generate finished gene {gene_idx}")


def run_n_generations(input_start, input_end, last_n):
    """

    :param input_start: read from sheet input_start
    :param input_end: read end at sheet input_end
    :param last_n: inbreeding last n year
    :return:
    """
    layergraph, vertex_layer, vertex_list = get_graph_from_data(file_path="./历代配种方案及出雏对照2021_带性别.xlsx")
    year2idx = {"16": 0, "17": 1, "18": 2, "19": 3, "20": 4, "21": 5}
    print("Load edges from", input_end)
    popus = []
    print("year idx", year2idx[input_end])
    # return

    # print(vertex_layer)
    for idx, item in enumerate(vertex_layer[year2idx[input_end]]):
        popus.append(vertex_list[item])
        # popus.append(Poultry(fi=f_i, wi=wi, fa_i=fa_i, ma_i=ma_i, sex=0, inbreedc=0.))

    kinship = Kinship(graph=layergraph)
    random.shuffle(popus)
    male_rate = 1. / 11.
    male_num = math.ceil(male_rate * len(popus))
    female_num = len(popus) - male_num
    for i in range(male_num):
        vertex_list[i].gender = 1
        popus[i].sex = 1
    name2idx = dict()
    for i, p in enumerate(popus):
        name2idx[p.name] = i
    # -------------Kinship read and build-------------

    kinship_matrix = np.zeros((male_num, female_num))
    for i in range(male_num):
        for j in range(female_num):
            kinship_matrix[i][j] = kinship.calc_kinship_corr(p1=popus[i].name, p2=popus[male_num + j].name)


if __name__ == '__main__':
    for i in [17, 18, 19, 20]:
        run_main(gene_idx=str(i))
    run_main(gene_idx="21")
    # print(np.random.randn(2, 10))
