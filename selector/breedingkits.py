#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/23 15:42
# @Author: ZhaoKe
# @File : breedingkits.py
# @Software: PyCharm
import numpy as np


def calculate_kinship_matrix(population):
    male_list = []
    female_list = []
    male_cnt, female_cnt = 0, 0
    for item in population:
        if item.sex == 1:
            male_cnt += 1
            male_list.append(item)
        else:
            female_cnt += 1
            female_list.append(item)
    kinship_matrix = np.zeros((male_cnt, female_cnt))
    for i, item_m in enumerate(male_list):
        for j, item_f in enumerate(female_list):
            kinship_matrix[i, j] = calculate_kin_correlation_coef(item_m, item_f)


def calculate_kin_correlation_coef(fa, ma):
    if fa.ge_idx < 1 and ma.ge_idx < 1:
        return 0
    else:
        return -1
