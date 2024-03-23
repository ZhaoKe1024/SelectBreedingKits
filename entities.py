#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/15 14:51
# @Author: ZhaoKe
# @File : entities.py
# @Software: PyCharm
import random
from typing import List
from SelectBreeding.func import get_new_id, get_rand_gender


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
    def __init__(self):
        self.mate_dict = set()
        self.kinship_matrix = None

    def add_pair(self):
        pass


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
            res.append(self.items[self.cur-i-1].wing_id)
        print(res)
        # return res


def calculate_inbreed_coef(fa, ma):
    if fa.ge_idx < 2 and ma.ge_idx < 2:
        return 0
    else:
        return -1
