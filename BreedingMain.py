#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import random
import numpy as np

from entities import Poultry, MateSolution
from xlsxreader import get_df_from_xlsx


if __name__ == '__main__':
    file_path = "./历代配种方案及出雏对照2021.xlsx"
    sex_table = get_df_from_xlsx(filepath=file_path, sheet_name="17", cols=[1, 2, 3])
    # print(sex_table.head())
    male_set = set(sex_table.iloc[:, 1].tolist())
    fema_set = set(sex_table.iloc[:, 2].tolist())
    # print(f"公鸡{len(male_set)}个, 母鸡{len(fema_set)}个:")
    # print(male_set)
    # print(fema_set)
    parent_df = get_df_from_xlsx(filepath=file_path, sheet_name="16", cols=[6, 7, 8, 9, 10])
    # print(parent_df.head())
    # print(parent_df.shape, parent_df.dropna(axis=0).shape)  # drop rows contain NaN value
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
    # print(f"一共有个{N}个体, 雄性个体{len(MaleIdxs)}个,雌性个体{len(FemaIdxs)}个,未知个体{len(UnknIdxs)}个。")
    if len(MaleIdxs) < 14:
        # 14-18个雄性
        newIdxs = random.sample(set(UnknIdxs), random.randint(14, 19) - len(MaleIdxs))
        MaleIdxs.extend(newIdxs)
        for ind in newIdxs:
            popus[ind].sex = 1
        FemaIdxs.extend(set(UnknIdxs)-set(newIdxs))
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

    cur_iter, max_iter = 0, 10  # 先迭代10代看看
    lb, ub = 0, 11  # 每一对父母生出孩子数目的随机值：(0, 11)
    # 第0 代，近交系数均为0，亲缘关系矩阵均为0
    # FN = len(FemaIdxs)
    family_matrix = np.zeros((len(MaleIdxs), len(FemaIdxs)))
    # 初代都是独立的，所以可以随机选育即可
    next_popus = []
    Female_num = len(MaleIdxs) * 10
    if Female_num > len(FemaIdxs):
        Female_num = len(FemaIdxs)
    Allo_Indices = list(range(Female_num))
    random.shuffle(Allo_Indices)
    # print(Allo_Indices)
    Fema_popus = [popus[Allo_Indices[i]] for i in Allo_Indices]
    # for item in Fema_popus:
    #     print(item)

    # 第0代均匀交配，每个雄性分配同等数目的雌性
    male_num = len(MaleIdxs)
    for i, item in enumerate(Fema_popus):
        popus[MaleIdxs[i % male_num]].add_spouse(Fema_popus[i])
    for i in MaleIdxs:
        popus[i].print_spouses()

    # 第1 代，近交系数均为0，亲缘关系开始初始化为非0
    new_popus = []
    for i in range(male_num):
        new_popus.extend(popus[MaleIdxs[i]].breeding_offsprings())
    ind = 0
    for item in new_popus:
        print(item)
        item.ancestry.backtracking()
        ind += 1
        if ind > 10:
            break

    # 第2 代开始，近交系数开始不为0，需要根据保留的系谱来计算
