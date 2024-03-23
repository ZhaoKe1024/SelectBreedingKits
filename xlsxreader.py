#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/15 14:12
# @Author: ZhaoKe
# @File : xlsxreader.py
# @Software: PyCharm
from typing import List
import pandas as pd


def csv_read_test(filepath="./test_xlsx_data.csv"):
    csvdf = pd.read_csv(filepath, delimiter=',', header=0, index_col=0)
    print(csvdf)


def read_xlsx(filepath="./历代配种方案及出雏对照2021.xlsx"):
    df_sheets = pd.read_excel(filepath, sheet_name=None, header=0, index_col=None,
                              usecols=[1, 2, 3, 6, 7, 8, 9, 10])  # about reading xlsx file
    for key in df_sheets.keys():
        if len(key) <= 2:
            print(f"====={key}=====")
            parent_df = df_sheets[key].iloc[:, 0:3]
            print(parent_df.shape, parent_df.dropna(axis=0).shape)  # drop rows contain NaN value


def get_df_from_xlsx(filepath="./历代配种方案及出雏对照2021.xlsx", sheet_name=None, cols: List = None):
    df_table = pd.read_excel(filepath, sheet_name=sheet_name, header=0, index_col=None,
                             usecols=cols)  # about reading xlsx file
    parent_df = df_table.dropna(axis=0).astype(int)
    return parent_df


def printArray(array):
    N = len(array)
    for i in range(N):
        if i > 0 and i % 10 == 0:
            print("\n"+str(array[i]), end=', ')
        else:
            print(array[i], end=', ')
    print()


if __name__ == '__main__':
    printArray(range(35))
