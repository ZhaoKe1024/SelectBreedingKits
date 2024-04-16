#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/3/23 15:00
# @Author: ZhaoKe
# @File : func.py
# @Software: PyCharm
import random

end_number = 15000


def get_new_id():
    global end_number
    end_number += 1
    return end_number


def get_familyid(y: str, m: int, f: int):
    res = y
    if m < 10:
        res += "0" + str(m)
    else:
        res += str(m)
    if f < 10:
        res += "0" + str(f)
    else:
        res += str(f)
    return res


def get_rand_gender():
    if random.random() < 0.3:
        return 1
    else:
        return 0
