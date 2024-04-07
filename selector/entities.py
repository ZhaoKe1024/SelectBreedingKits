#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/15 14:51
# @Author: ZhaoKe
# @File : entities.py
# @Software: PyCharm
import random
from typing import List
import numpy as np
from func import get_new_id, get_rand_gender


class Vertex(object):
    def __init__(self, index, name=None, depth=0, gender=0, family_id: str = ""):
        self.index = index
        self.name = name if name else str(index)
        self.depth = depth
        self.inbreed_coef = -1.0
        self.gender = gender
        self.family_id: family_id

    def __str__(self):
        return f"Vertex:({self.index}, {self.name})"


class Poultry(object):
    def __init__(self, fi, wi, sex, ma_i, fa_i, inbreedc=0.0, spouses: List = None):
        self.family_id = fi
        self.wing_id = wi
        self.sex = sex  # 0 female 1 male
        self.spouses = spouses if spouses is not None else []
        self.ancestry = Stack()
        self.ma_i = ma_i
        self.fa_i = fa_i
        self.ge_idx = 0

        self.inbreed_coef = inbreedc

    def add_spouse(self, p):
        if self.sex == 0:
            raise Exception("雌性家禽不需要分配多余1个雄性家禽。")
        if len(self.spouses) < 10:
            self.spouses.append(p)
        else:
            raise Exception("这个雄性家禽已经分配10个配种了，不能再加了。")

    def breeding_offsprings(self):
        offsprings = []
        for item in self.spouses:
            for j in range(random.randint(0, 11)):
                new_poultry = Poultry(fi=self.family_id, wi=get_new_id(), fa_i=self.wing_id, ma_i=item.wing_id,
                                      sex=get_rand_gender(), inbreedc=calculate_inbreed_coef(self, item))
                new_poultry.ancestry.push(self)
                offsprings.append(new_poultry)
        print(f"生育{len(offsprings)}个。")
        return offsprings

    def __str__(self):
        return f"family:{self.family_id}, wing_id:{self.wing_id}, father:{self.fa_i}, mother:{self.ma_i}"

    def print_spouses(self):
        for item in self.spouses:
            print(item.wing_id, end=', ')
        print()


class MateSolution(object):
    def __init__(self, male_idxs: List, female_per: int):
        """

        :param male_idxs: it must given the indices of male poultry.
        :param female_per: how many female individuals need to allocate to male poultry.
        """
        self.vector_male = [val for val in male_idxs for _ in range(female_per)]
        self.vector_female = None

        self.fitness_value = None

        # self.mate_dict = set()
        # self.kinship_matrix = None

    def get_std(self) -> float:
        male_dict = {}
        for key in self.vector_male:
            male_dict[key] = male_dict.get(key, 0) + 1
        res_arr = list(male_dict.values())
        # print("--->", res_arr)
        return np.std(res_arr)

    def add_pair(self):
        pass

    def get_pair(self, ind):
        return self.vector_male[ind], self.vector_female[ind]

    def set_pair(self, ind, male_x, female_x) -> None:
        """use to single mutation"""
        self.vector_male[ind] = male_x
        self.vector_female[ind] = female_x

    def set_female(self, ind: int, female_x) -> None:
        self.vector_female[ind] = female_x

    def set_pair_slice(self, ind_s, ind_e, male_array, female_array):
        """use to crossover"""
        self.vector_male[ind_s:ind_e + 1] = male_array
        self.vector_female[ind_s:ind_e + 1] = female_array

    def sort_vector(self, by=1):
        if by == 1:
            sort_ed = sorted(range(len(self.vector_male)), key=lambda k: self.vector_male[k], reverse=False)
        else:
            sort_ed = sorted(range(len(self.vector_female)), key=lambda k: self.vector_female[k], reverse=False)
        sorted_male = []
        sorted_female = []
        for ind in sort_ed:
            sorted_male.append(self.vector_male[ind])
            sorted_female.append(self.vector_female[ind])
        self.vector_male = sorted_male
        self.vector_female = sorted_female

    def __len__(self):
        return len(self.vector_male)


class Stack(object):
    def __init__(self):
        self.items = []
        self.cur = 0

    def get(self):
        if len(self.items) > 0:
            return self.items[-1]
        else:
            raise Exception("empty stack.")

    def push(self, item):
        self.items.append(item)
        self.cur += 1

    def backtracking(self):
        res = []
        for i in range(self.cur):
            res.append(self.items[self.cur - i - 1].wing_id)
        print(res)
        # return res


def calculate_fitness(so: MateSolution, kinship: List[List]) -> float:
    res = 0.0
    L = len(so)
    for i in range(L):
        res += kinship[so.vector_male[i]][so.vector_female[i]]
    return res


def calculate_inbreed_coef(fa, ma):
    if fa.ge_idx < 2 and ma.ge_idx < 2:
        return 0
    else:
        return -1


if __name__ == '__main__':
    so = MateSolution([], 0)
    so.vector_male = [1, 1, 1, 1, 2, 2, 2, 2, 5, 6, 7, 4, 6, 7, 5, 6]
    so.vector_female = [6, 4, 7, 6, 4, 3, 6, 8, 7, 9, 0, 7, 5, 6, 7, 8]
    for i in range(len(so)):
        print(so.vector_male[i], so.vector_female[i])
    print("==============")
    so.sort_vector()
    for i in range(len(so)):
        print(so.vector_male[i], so.vector_female[i])

    best_solution = so
    N = len(best_solution)
    print()
    pre_pos = best_solution.vector_male[0]
    print(best_solution.vector_male[0], ": [", best_solution.vector_female[0], end=', ')
    idx = 1
    while idx < N:
        if best_solution.vector_male[idx] != pre_pos:
            print(']')
            print(best_solution.vector_male[idx], ": [", end='')
        print(best_solution.vector_female[idx], end=', ')
        pre_pos = best_solution.vector_male[idx]
        idx += 1
    print("]")

    print("std:", best_solution.get_std())
