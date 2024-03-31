#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import random
from copy import deepcopy, copy

import numpy as np

from entities import Poultry, MateSolution
from xlsxreader import read_population_from_xlsx


class GASelector(object):
    def __init__(self, popus, male_idxs, female_idxs):
        self.num_population = 30
        self.pm, self.cm = 0.1, 0.9
        self.num_iter = 300

        self.popus = popus
        self.male_idxs, self.female_idxs = male_idxs, female_idxs
        self.num_male, self.num_female = len(male_idxs), len(female_idxs)
        self.female_per_male = self.num_female // self.num_male
        self.rest = self.num_female % self.num_male
        print(f"num sum male female: {len(self.popus)}, {self.num_male}, {self.num_female}")
        print(f"num per rest:, {self.female_per_male}, {self.rest}")
        self.male_poultries = []
        self.female_poultries = []
        for ind in self.male_idxs:
            self.male_poultries.append(popus[ind])
        for ind in self.female_idxs:
            self.female_poultries.append(popus[ind])

        self.solutions = []

    def __generate_one_solution(self):
        s = MateSolution(self.male_idxs, self.female_per_male)
        # inserting the rest individuals of the female after divide for male
        for _ in range(self.rest):
            p = random.randint(0, len(s.vector_male))
            s.vector_male.insert(p, s.vector_male[p-1])
        female_popus_copy = deepcopy(self.female_idxs)
        random.shuffle(female_popus_copy)
        s.vector_female = female_popus_copy
        return s

    def init_population(self):
        for _ in range(self.num_population):
            self.solutions.append(self.__generate_one_solution())
        for item in self.solutions:
            print(len(item.vector_male), len(item.vector_female))


def run_main():
    popus, male_idxs, female_idxs = read_population_from_xlsx()
    GASelector = GASelector(popus=popus, male_idxs=male_idxs, female_idxs=female_idxs)
    GASelector.init_population()


if __name__ == '__main__':
    run_main()
