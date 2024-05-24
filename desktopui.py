# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-05-23 23:03
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from widgets.MainWindow import Ui_Dialog
# from
from graphfromtable import get_graph_from_data
from procedure.kinship_on_graph import Kinship


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)  # 1
        # self.text_edit.textChanged.connect(self.show_text_func)  # 2
        self.PushButton1.clicked.connect(self.open_file)
        self.PushButton2.clicked.connect(self.show_text_func)
        self.file_to_analyze = None
        self.kinship = None
        self.CalcButton1.clicked.connect(self.calc_corrcoef)
        self.CalcButton2.clicked.connect(self.calc_inbrcoef)

    def show_text_func(self):
        try:
            self.analyze()
            self.textBrowser_1.setText("已分析文件，可以进行相关计算。")
        except Exception as e:
            print("有bug")
            print(e)
        print("已分析文件:", self.file_to_analyze)

    def open_file(self, ):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)")
        if file_path:
            print(file_path)
            self.file_to_analyze = file_path
            self.Label2.setText(".../" + file_path[-32:])
        else:
            self.Label2.setText("Unknown File!")

    def analyze(self):
        if self.file_to_analyze.split(".")[-1] not in ["xlsx", "xls"]:
            QMessageBox.critical(self, "错误", "暂时仅支持Excel文件!",  # 窗口提示信息
                                 QMessageBox.Cancel | QMessageBox.Close,
                                 # 窗口内添加按钮-QMessageBox.StandardButton，可重复添加使用 | 隔开；如果不写，会有个默认的QMessageBox.StandardButton
                                 QMessageBox.Cancel,  # 设置默认按钮（前提是已经设置有的按钮，若是没有设置，则无效）
                                 )
            # if api == QMessageBox.Cancel:
            #     label.setText("您选择了Cancel")
            # elif api == QMessageBox.Close:
            #     label.setText("您选择了Close")
            return
        # self.show_text_func()
        # self.kinship = Kinship(file_path=self.file_to_analyze, graph=None)
        layergraph, vertex_layer, vertex_list = get_graph_from_data()
        # year2idx = {"16": 0, "17": 1, "18": 2, "19": 3, "20": 4, "21": 5}
        # print("Load edges from", gene_idx)
        # popus = []
        # print("year idx", year2idx[gene_idx])
        # # return
        # if gene_idx == "21":
        #     # print(vertex_layer)
        #     for idx, item in enumerate(vertex_layer[year2idx[gene_idx]]):
        #         print(vertex_list[item].name)
        #         popus.append(vertex_list[item])
        # else:
        #     # print(vertex_layer)
        #     for idx, item in enumerate(vertex_layer[year2idx[gene_idx]]):
        #         # print(vertex_list[item].name)
        #         popus.append(vertex_list[item])
        #         # popus.append(Poultry(fi=f_i, wi=wi, fa_i=fa_i, ma_i=ma_i, sex=0, inbreedc=0.))
        # # return
        self.kinship = Kinship(graph=layergraph)

    def check_kinship(self):
        res_message = None
        if self.file_to_analyze is None:
            res_message = "请先选中文件"
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
        res = self.kinship.calc_kinship_corr(p1=p1, p2=p2)
        print(res)
        self.textBrowser_2.setText(str(res))

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
        res = self.kinship.calc_inbreed_coef(p=p)
        self.textBrowser_3.setText(str(res))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    sys.exit(app.exec_())
