#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/5/26 11:33
# @Author: ZhaoKe
# @File : cmdexecu.py
# @Software: PyCharm
import sys
import logging
import sys
from func import NullNameException
from graphfromtable import get_graph_from_data
from procedure.kinship_on_graph import Kinship
from procedure.xlsxreader import get_df_from_xlsx
from BreedingMain import run_main


class IBCalculator(object):
    def __init__(self):
        super(IBCalculator, self).__init__()
        self.file_to_analyze = None
        self.file_to_evaluate = None
        self.kinship = None
        self.keys = ["analyse", "select", "eval", "p", "p1", "help"]
        self.describe = ["分析文件并构建族谱", "生成新一年的配种方案", "评估现有方案", "计算个体近交系数", "计算亲缘相关系数", "查看帮助"]

    def execute_all(self, kv_list):
        ind = 1
        while ind <= len(kv_list)-1:
            if kv_list[ind] == "--p1":
                assert ind+3 < len(kv_list), f"expect 4 args but get {len(kv_list)-ind}"
                self.execute(key=kv_list[ind], value=kv_list[ind+1], key2=kv_list[ind+2], value2=kv_list[ind+3])
                ind += 4
            else:
                if ind+1 == len(kv_list):
                    self.execute(key=kv_list[ind], value=None)
                    ind += 1
                else:

                    self.execute(key=kv_list[ind], value=kv_list[ind+1])
                    ind += 2

    def execute(self, key, value, key2=None, value2=None):

        if key[2:] not in self.keys:
            print(key)
            raise Exception("Unknown key.")
        print(key, "-", "value")

        if key[2:] == "help":
            for j, item in enumerate(self.keys):
                print(item, '\t', self.describe[j])
        elif key[2:] == "analyse":
            self.file_to_analyze = value
            self.analyze()
        elif key[2:] == "select":
            run_main(gene_idx=value)
        elif key[2:] == "eval":
            if self.kinship is None:
                raise Exception("please analyse file first.")
            self.file_to_evaluate = value
            self.evaluate_solution()
        elif key[2:] == "p":
            self.calc_inbrcoef(ct=value)
        elif key[2:] == "p1":
            if key2[2:] == "p2":
                self.calc_corrcoef(p1=value, p2=value2)
            else:
                raise Exception(f"Unknown key2: {key2}")
        elif key[2:] == "current_analyse":
            return self.file_to_analyze
        elif key[2:] == "current_eval":
            return self.file_to_evaluate
        else:
            raise Exception(f"Unknown key: {key}")

    # def show_text_func(self):
    #     try:
    #         self.analyze()
    #         print("已分析文件，可以进行相关计算。")
    #         print("已分析文件:", self.file_to_analyze)
    #     except Exception as e:
    #         print("有bug")
    #         logging.exception(e)
    #
    # def open_file1(self, ):
    #     """打开文件"""
    #     file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
    #     if file_path:
    #         print(file_path)
    #         self.file_to_analyze = file_path
    #         self.Label2.setText(".../" + file_path[-32:])
    #     else:
    #         self.Label2.setText("请选择有效的xlsx文件!")
    #
    # def open_file2(self, ):
    #     """打开文件"""
    #     file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
    #     if file_path:
    #         print(file_path)
    #         self.file_to_evaluate = file_path
    #         self.ExampleLabel2.setText(".../" + file_path[-32:])
    #     else:
    #         self.ExampleLabel2.setText("请选择有效的xlsx文件!")

    def analyze(self):
        if self.file_to_analyze.split(".")[-1] not in ["xlsx", "xls"]:
            raise Exception("暂时仅支持Excel文件!")
        # self.show_text_func()
        # self.kinship = Kinship(file_path=self.file_to_analyze, graph=None)
        layergraph, vertex_layer, vertex_list = get_graph_from_data(file_path=self.file_to_analyze)

        self.kinship = Kinship(graph=layergraph)

    def check_kinship(self):
        res_message = None
        if self.file_to_analyze is None:
            res_message = "请先选中待分析文件并分析。"
        if self.kinship is None:
            res_message = "请先分析文件"
        if res_message is not None:
            raise Exception(res_message)

    def calc_corrcoef(self, p1: str, p2: str):
        """计算亲缘相关系数"""
        self.check_kinship()

        p1, p2 = p1.strip(), p2.strip()
        print(p1, p2)
        try:
            res = self.kinship.calc_kinship_corr(p1=p1, p2=p2)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def calc_inbrcoef(self, ct: str):
        """计算近交系数"""
        self.check_kinship()
        ct = ct.strip()
        if '.' in ct or ct == '':
            raise Exception("请输入1个自然数编号")
        try:
            res = self.kinship.calc_inbreed_coef(p=ct)
            print(res)
            print(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            logging.exception(e)

    def evaluate_solution(self):
        self.check_kinship()
        sheet_list = ["16", "17", "18", "19", "20"]
        for sheet_name in sheet_list[1:]:
            edges_df = get_df_from_xlsx(filepath=self.file_to_evaluate, sheet_name=sheet_name,
                                        cols=[1, 2, 3])
            with open(f"./evaluate_{sheet_name}.csv", 'w', encoding="utf_8") as fout:
                fout.write("家系号,公号,母号,亲缘相关系数\n")
                for idx, row in enumerate(edges_df.itertuples()):
                    # print(row[2], row[3])
                    fout.write(f"{row[1]},{row[2]},{row[3]}," + str(
                        self.kinship.calc_kinship_corr(p1=str(row[2]), p2=str(row[3]))) + '\n')
            print(f"表格sheet{sheet_name} 评估完成！")


def run(args):
    print(args)
    # for item in args:
    #     print(type(item))
    calc = IBCalculator()
    calc.execute_all(args)
    # pass


if __name__ == '__main__':
    run(sys.argv)
