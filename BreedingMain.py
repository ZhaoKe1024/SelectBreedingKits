#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/17 18:25
# @Author: ZhaoKe
# @File : BreedingMain.py
# @Software: PyCharm
import random
from copy import deepcopy
import numpy as np
from entities import MateSolution, calculate_fitness
from xlsxreader import read_population_from_xlsx


class GASelector(object):
    def __init__(self, popus, male_idxs, female_idxs, kinship_matrix, num_iter=2):
        self.num_population = 30
        self.pm, self.pc = 0.1, 0.9
        self.num_iter = num_iter

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

        self.kinship_matrix = kinship_matrix

        self.solutions = []

    def __generate_one_solution(self):
        s = MateSolution(list(range(self.num_male)), self.female_per_male)
        # inserting the rest individuals of the female after divide for male
        for _ in range(self.rest):
            p = random.randint(0, len(s.vector_male))
            s.vector_male.insert(p, s.vector_male[p-1])
        female_popus_copy = list(range(self.num_female))
        random.shuffle(female_popus_copy)
        s.vector_female = female_popus_copy
        return s

    def init_population(self):
        for _ in range(self.num_population):
            self.solutions.append(self.__generate_one_solution())
        # for item in self.solutions:
        #     print(len(item.vector_male), len(item.vector_female))

    def crossover(self, g1, g2):
        two_pos = random.choices(range(len(g1.vector_female)), k=2)
        mi, ma = -1, -1
        if two_pos[0] > two_pos[1]:
            mi, ma = two_pos[1], two_pos[0]
        else:
            mi, ma = two_pos[0], two_pos[1]
        new_g1, new_g2 = deepcopy(g1), deepcopy(g2)
        for j in range(mi, ma+1):
            m0, f0 = g1.get_pair(two_pos[0])
            m1, f1 = g2.get_pair(two_pos[1])
            new_g1.set_pair(j, m1, f1)
            new_g2.set_pair(j, m0, f0)
        return new_g1, new_g2

    def mutation(self, g):
        new_g = deepcopy(g)
        for item in self.solutions:
            if random.random() > self.pm:
                continue
            two_pos = random.choices(range(len(item)), k=2)
            m0, f0 = item.get_pair(two_pos[0])
            m1, f1 = item.get_pair(two_pos[1])
            new_g.set_pair(two_pos[0], m1, f1)
            new_g.set_pair(two_pos[1], m0, f0)
        return new_g

    def elite_reserve(self):
        """
        reserve the best individual
        :return:
        """
        pass

    def select(self, select_prob):
        """
        select the individuals accroding to the fitness values
        :return:
        """
        L = len(select_prob)
        for i in range(L):
            if random.random() > select_prob[L-i-1]:
                self.solutions.pop(L-i-1)
        # print(self.solutions)

    def scheduler(self):
        self.init_population()
        for iter_idx in range(self.num_iter):
            for solution in self.solutions:
                # calculate population inbreed coefficient by 有效 population 含量
                # print(solution.vector_male)
                # print(solution)
                solution.fitness_value = calculate_fitness(solution, self.kinship_matrix)
            # self.elite_reserve()

            self.solutions.sort(key=lambda x: x.fitness_value)
            fitness_list = [item.fitness_value for item in self.solutions]
            # print(fitness_list)
            cumsum_fitnesses = np.cumsum(fitness_list)
            fitness_probs = [item/cumsum_fitnesses[-1] for item in cumsum_fitnesses]
            self.select(fitness_probs)
            L = len(self.solutions)

            g1_tmp, g2_tmp = -1, -1
            idx = 0
            while idx < L:
                if random.random() < self.pc:
                    if g1_tmp < 0:
                        g1_tmp = idx
                    elif g2_tmp < 0:
                        g2_tmp = idx
                    else:
                        new_g1, new_g2 = self.crossover(self.solutions[g1_tmp], self.solutions[g2_tmp])
                        self.solutions.append(new_g1)
                        self.solutions.append(new_g2)
                        g1_tmp, g2_tmp = -1, -1
                idx += 1

            # print("=============")
            # print(self.solutions)
            idx = 0
            while idx < L:
                if random.random() < self.pm:
                    new_individual = self.mutation(self.solutions[idx])
                    self.solutions.append(new_individual)
                idx += 1
            # print(self.solutions)
            # print("==============")

        best_solution = None
        best_fitness = np.inf
        for solution in self.solutions:
            # calculate population inbreed coefficient by 有效 population 含量
            fvalue = calculate_fitness(solution, self.kinship_matrix)
            if fvalue < best_fitness:
                best_fitness = fvalue
                best_solution = solution
        print("best fv:", best_fitness)


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
