# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-05-23 23:03
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QMainWindow
from widgets.MainWindow import Ui_Dialog
from func import NullNameException
from graphfromtable import get_graph_from_data
from procedure.kinship_on_graph import Kinship
from procedure.xlsxreader import get_df_from_xlsx
from BreedingMain import run_main
from widgets_tab.LoginWindow import Ui_MainWindow

class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)  # 1
        # self.text_edit.textChanged.connect(self.show_text_func)  # 2
        self.PushButton1.clicked.connect(self.open_file1)
        self.OpenButton2.clicked.connect(self.open_file2)
        self.PushButton2.clicked.connect(self.show_text_func)
        self.file_to_analyze = None
        self.file_to_evaluate = None
        self.kinship = None
        self.CalcButton1.clicked.connect(self.calc_corrcoef)
        self.CalcButton2.clicked.connect(self.calc_inbrcoef)
        self.EvalButton.clicked.connect(self.evaluate_solution)
        self.GeneButton.clicked.connect(self.generate_solution)

    def show_text_func(self):
        try:
            self.analyze()
            self.textBrowser_1.setText("已分析文件，可以进行相关计算。")
            print("已分析文件:", self.file_to_analyze)
        except Exception as e:
            print("有bug")
            logging.exception(e)

    def open_file1(self, ):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            print(file_path)
            self.file_to_analyze = file_path
            self.Label2.setText(".../" + file_path[-32:])
        else:
            self.Label2.setText("请选择有效的xlsx文件!")

    def open_file2(self, ):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            print(file_path)
            self.file_to_evaluate = file_path
            self.ExampleLabel2.setText(".../" + file_path[-32:])
        else:
            self.ExampleLabel2.setText("请选择有效的xlsx文件!")

    def analyze(self):
        if self.file_to_analyze.split(".")[-1] not in ["xlsx", "xls"]:
            QMessageBox.critical(self, "错误", "暂时仅支持Excel文件!",  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )
            return
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
            QMessageBox.critical(self, "错误", res_message,  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )

    def calc_corrcoef(self):
        """计算亲缘相关系数"""
        self.check_kinship()
        ct = self.InputBox1.text().strip()
        print(ct)
        if '.' in ct or ct == '':
            QMessageBox.critical(self, "错误", "请输入两个自然数编号（可以用逗号或空格隔开）",  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )
        if ',' in ct:
            ct_part = ct.replace(' ', '').split(',')
        elif '，' in ct:
            ct_part = ct.replace(' ', '').split('，')
        elif ' ' in ct:
            ct_part = ct.split(' ')
        else:
            QMessageBox.critical(self, "错误", "请输入自然数类型(非负，无小数点)的编号",  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )
            return
        p1, p2 = ct_part[0], ct_part[1]
        print(p1, p2)
        try:
            res = self.kinship.calc_kinship_corr(p1=p1, p2=p2)
            print(res)
            self.textBrowser_2.setText(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            QMessageBox.critical(self, "错误", e.__str__(),  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )

    def calc_inbrcoef(self):
        """计算近交系数"""
        self.check_kinship()
        ct = self.InputBox2.text().strip()
        if '.' in ct or ct == '':
            QMessageBox.critical(self, "错误", "请输入1个自然数编号",  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )
        p = ct
        try:
            res = self.kinship.calc_inbreed_coef(p=p)
            print(res)
            self.textBrowser_3.setText(self.kinship.analyzer.get_just_message())
        except NullNameException as e:
            QMessageBox.critical(self, "错误", e.__str__(),  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )

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
            self.textBrowser_4.append(f"表格sheet{sheet_name} 评估完成！")

    def generate_solution(self):
        # self.check_kinship()
        ct = self.InputBox_geneidx.text().strip()
        try:
            if int(ct) > 21:
                raise Exception("Unknown years num.")
            run_main(gene_idx=ct)
            self.textBrowser_4.setText(f"generate finished gene {ct}")
        except NullNameException as e:
            QMessageBox.critical(self, "错误", e.__str__(),  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
