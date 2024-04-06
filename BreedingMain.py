#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import numpy as np
from xlsxreader import read_population_from_xlsx
from selector.GASelector import GASelector
from selector.GASelector import

def run_main():
    popus, male_idxs, female_idxs = read_population_from_xlsx()
    # print()
    np.random.seed(42)  # 2024-04-02
    kinship_matrix = 1/16 + 1/16 * np.random.randn(len(male_idxs), len(female_idxs))
    GAS = GASelector(popus=popus, male_idxs=male_idxs, female_idxs=female_idxs, kinship_matrix=kinship_matrix)
    GAS.scheduler()


if __name__ == '__main__':
    run_main()
    # print(np.random.randn(2, 10))
