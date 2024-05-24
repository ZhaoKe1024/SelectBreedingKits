#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/5/22 14:57
# @Author: ZhaoKe
# @File : evaluate.py
# @Software: PyCharm
from procedure.xlsxreader import get_df_from_xlsx
from graphfromtable import get_graph_from_data
from procedure.kinship_on_graph import Kinship


def evaluate_data(basefile="./历代配种方案及出雏对照2021_带性别.xlsx", evalfile="./历代配种方案及出雏对照2021_带性别.xlsx"):
    layergraph, vertex_layer, vertex_list = get_graph_from_data(file_path=basefile)
    kinship = Kinship(graph=layergraph)
    sheet_list = ["16", "17", "18", "19", "20"]
    for sheet_name in sheet_list[1:]:
        edges_df = get_df_from_xlsx(filepath=evalfile, sheet_name=sheet_name,
                                    cols=[1, 2, 3])
        with open(f"./evaluate_{sheet_name}.csv", 'w', encoding="utf_8") as fout:
            fout.write("家系号,公号,母号,亲缘相关系数\n")
            for idx, row in enumerate(edges_df.itertuples()):
                # print(row[2], row[3])
                fout.write(f"{row[1]},{row[2]},{row[3]}," + str(
                    kinship.calc_kinship_corr(p1=str(row[2]), p2=str(row[3]))) + '\n')
                # fout.write('\n')


if __name__ == '__main__':
    evaluate_data()
