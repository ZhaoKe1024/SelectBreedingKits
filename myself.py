#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/7/31 17:47
# @Author: ZhaoKe
# @File : myself.py
# @Software: PyCharm

from inbreed_lib.BreedingMainESR import run_main_with_graph

if __name__ == '__main__':
    # run_main_without_graph(file_path="./analyzer/kinship330.csv", result_file="./analyzer/output_{}.csv")
    # run_main_with_graph(file_path="./datasets/first330.xlsx", gene_idx="2020", result_file="./temp_files/output_{}.xlsx")
    # run_main_with_graph(file_path="./temp_files/output_2020.xlsx", gene_idx="2021", result_file="./temp_files/output_{}.xlsx")
    # run_main_with_graph(file_path="./temp_files/output_2021.xlsx", gene_idx="2022", result_file="./temp_files/output_{}.xlsx")
    # run_main_with_graph(file_path="./temp_files/output_2022.xlsx", gene_idx="2023", result_file="./temp_files/output_{}.xlsx")

    # run_main_with_graph(file_path="./datasets/simudata20241111.xlsx", gene_idx="2016", result_file="./temp_files/simudata_output_{}.xlsx")
    # run_main_with_graph(file_path="./datasets/simudata_output_2016.xlsx", gene_idx="2017", result_file="./temp_files/simudata_output_{}.xlsx")
    # run_main_with_graph(file_path="./temp_files/simudata_output_2017.xlsx", gene_idx="2018", result_file="./temp_files/simudata_output_{}.xlsx")
    # run_main_with_graph(file_path="./temp_files/simudata_output_2018.xlsx", gene_idx="2019", result_file="./temp_files/simudata_output_{}.xlsx")
    # run_main_with_graph(file_path="./datasets/250411_历代配种方案及出雏对照2021.xlsx", result_file="./temp_files/simudata_output_{}_max.xlsx", configs={"gene_idx": "2021", "mode": "max"})
    run_main_with_graph(file_path="./datasets/250414_琅琊鸡历年系谱19-24.xlsx",
                        result_file="./temp_files/langya_output_{}_max.xlsx",
                        configs={"gene_idx": "2024", "mode": "min"})
