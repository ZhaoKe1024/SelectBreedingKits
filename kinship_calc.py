# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-04-07 23:12
import json
from procedure.kinship_on_graph import Kinship


def calc_and_save_as_matrix():
    kinship = Kinship()
    # print(kinship.calc_inbreed_coef(p="3916"))
    # print(kinship.calc_inbreed_coef(p="462"))
    # print(kinship.calc_inbreed_coef(p="677"))
    # kinship.print_edges()
    # kinship.print_layer()
    # kinship.print_parents()
    # kinship.print_all_poultry()
    # print(kinship.calc_kinship_corr(p1="3916", p2="3712"))
    print(kinship.calc_kinship_corr(p1="7429", p2="7433"))
    # print(kinship.calc_kinship_corr(p1="7197", p2="7194"))
    # print(kinship.calc_kinship_corr(p1="462", p2="461"))

    # json_data = dict()
    # names = kinship.name2index.keys()
    # # print(names)
    # for i, ver in enumerate(names):
    #     json_data[ver] = kinship.calc_inbreed_coef(ver)
    #
    # new_json_string = json.dumps(json_data, ensure_ascii=False)  # 正常显示中文
    # with open("./name2inbreedcoef.json", 'w') as nf:
    #     nf.write(new_json_string)


if __name__ == '__main__':
    calc_and_save_as_matrix()
