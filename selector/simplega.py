#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/11/1 15:15
# @Author: ZhaoKe
# @File : simplega.py
# @Software: PyCharm
import math
import random
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from inbreed_lib.selector.entities import Vertex
from inbreed_lib.selector.GASelector import GASelector
from inbreed_lib.procedure.kinship_on_graph import Kinship
from inbreed_lib.func import IDGenerator


def run_main_without_graph(file_path="./kinship330.csv", gene_idx=2018, result_file=None):
    df = pd.read_csv(file_path, delimiter=',', header=0, index_col=None)
    popus_idxs = list(df.iloc[:, 0])+list(df.columns[1:])
    popus = []
    for idx, name in enumerate(popus_idxs):
        popus.append(Vertex(idx, name=name))
    kinship_matrix = np.array(df.iloc[:, 1:])
    # print(kinship_matrix.shape)
    male_num = 30
    # ===============================Algorithm==================================
    # ====================Here is vanilla Genetic Algorithm=====================
    GAS = GASelector(popus=popus, kinship_matrix=kinship_matrix, male_idxs=list(range(male_num)),
                     female_idxs=list(range(male_num, len(popus))), mode="v1")
    best_solution = GAS.scheduler()

    # ===========================找出最佳雌性，来生育最佳雄性，等数留种=====================
    female_list = []
    tmp_female_idx = 0
    tmp_female_value = 999.
    i, j = 0, 0
    tmp_male_idx = None
    cur_male_idx = best_solution.vector_male[0]
    while i < len(best_solution):
        tmp_male_idx = best_solution.vector_male[i]
        if cur_male_idx == tmp_male_idx:
            tmp_female_idx = best_solution.vector_female[i]
            if kinship_matrix[tmp_male_idx][tmp_female_idx] < tmp_female_value:
                tmp_female_value = kinship_matrix[tmp_male_idx][tmp_female_idx]
        else:
            female_list.append(tmp_female_idx)
        i += 1
    female_list.append(tmp_female_idx)
    print("best females:", len(female_list))
    # =============================================================================

    print(best_solution.vector_male)
    print(best_solution.vector_female)
    pre_pos = best_solution.vector_male[0]
    cur_female = best_solution.vector_female[0]
    # print("========----------育种方案----------==========")
    # print("(家系号，雄性个体编号, 雌性个体编号)]")
    idgenarator = IDGenerator(end_number=int(gene_idx) * 1000, year=str(int(gene_idx) + 1))

    fout = open(result_file, 'w', encoding="utf_8")
    fout.write(
        "配种方案,家系号,公鸡号,母鸡号,亲缘相关系数,出雏,批次,翅号,公鸡号,母鸡号,{}年家系号,性别\n".format(gene_idx))
    # print("配种方案", "家系号", "公鸡号", "母鸡号", "亲缘相关系数", "出雏", "批次", "翅号", "公鸡号", "母鸡号", "{}年家系号".format(gene_idx))
    year, mi, fi = "21", 0, 0
    best_idx = 0
    # print(
    #     f"{popus[pre_pos].family_id},{pre_pos}:[({popus[cur_female].family_id},{male_num + cur_female})",
    #     end=', ')

    tmp_fid = idgenarator.get_family_id(y="", m=mi)
    sex_id = "1"
    child_id = idgenarator.get_new_id()
    fout.write(","  # col 1
               + tmp_fid + ","  # col 2 家系号
               + popus[pre_pos].name + ","  # col 3 公号
               + popus[male_num + female_list[best_idx]].name + ","  # col 4 母号
               + f"{kinship_matrix[pre_pos, cur_female]:.5f},,,"  # col 5  亲缘相关系数 6 7
               + child_id + ','
               + popus[pre_pos].name + ","  # col 9 公号
               + popus[male_num + cur_female].name + ","  # col 10 母号
               + tmp_fid + ","
               + sex_id + '\n')  # 11 家系号
    best_idx += 1

    tmp_fid = idgenarator.get_family_id(y="", m=mi)
    sex_id = "0"
    child_id = idgenarator.get_new_id()
    fout.write(","  # col 1
               + tmp_fid + ","  # col 2 家系号
               + popus[pre_pos].name + ","  # col 3 公号
               + popus[male_num + cur_female].name + ","  # col 4 母号
               + f"{kinship_matrix[pre_pos, cur_female]:.5f},,,"  # col 5  亲缘相关系数 6 7
               + child_id + ','
               + popus[pre_pos].name + ","  # col 9 公号
               + popus[male_num + cur_female].name + ","  # col 10 母号
               + tmp_fid + ","
               + sex_id + '\n')  # 11 家系号
    fi += 1
    idx = 1
    # threshold = 0.5
    res_data = []
    while idx < len(best_solution):
        cur_male = best_solution.vector_male[idx]
        cur_male_name = popus[cur_male].name
        cur_female = best_solution.vector_female[idx]
        cur_female_name = popus[male_num + cur_female].name
        if cur_male != pre_pos:
            mi += 1
            tmp_fid = idgenarator.get_family_id(y="", m=mi)
            sex_id = "1"
            child_id = idgenarator.get_new_id()
            fout.write(","  # col 1
                       + tmp_fid + ","  # col 2 家系号
                       + popus[pre_pos].name + ","  # col 3 公号
                       + popus[male_num + cur_female].name + ","  # col 4 母号
                       + f"{kinship_matrix[pre_pos, cur_female]:.5f},,,"  # col 5  亲缘相关系数 6 7
                       + child_id + ','
                       + popus[pre_pos].name + ","  # col 9 公号
                       + popus[male_num + cur_female].name + ","  # col 10 母号
                       + tmp_fid + ","
                       + sex_id + '\n')  # 11 家系号
            best_idx += 1

        # <<<<<<< Updated upstream
        # fout.write(get_familyid(year, mi,
        #                         fi) + "," + cur_male_name + "," + cur_female_name + "," + f"{kinship_matrix[cur_male, cur_female]:.5f}" + '\n')
        # =======
        ibc = kinship_matrix[cur_male, cur_female]
        tmp_fid = idgenarator.get_family_id(y="", m=mi)
        sex_id = "0"
        child_id = idgenarator.get_new_id()
        fout.write(","  # col 1
                   + tmp_fid + ","  # col 2 家系号
                   + popus[pre_pos].name + ","  # col 3 公号
                   + popus[male_num + cur_female].name + ","  # col 4 母号
                   + f"{kinship_matrix[pre_pos, cur_female]:.5f},,,"  # col 5  亲缘相关系数 6 7
                   + child_id + ','
                   + popus[pre_pos].name + ","  # col 9 公号
                   + popus[male_num + cur_female].name + ","  # col 10 母号
                   + tmp_fid + ","
                   + sex_id + '\n')
        # print(tmp_fid + "," + cur_male_name + "," + cur_female_name + "," + f"{ibc:.5f}")
        res_data.append([tmp_fid, cur_male_name, cur_female_name, f"{ibc:.4f}", None, None, child_id, cur_male_name,
                         cur_female_name, tmp_fid, sex_id])
        # >>>>>>> Stashed changes
        pre_pos = cur_male
        idx += 1
        fi += 1
    # print("]")
    fout.write('\n')
    fout.close()
    print(f"generate finished gene {gene_idx}")
    # return res_data


if __name__ == '__main__':
    run_main_without_graph(file_path="../analyzer/kinship330.csv", result_file="../analyzer/output_2.csv")
