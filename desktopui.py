# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-05-23 23:03
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from widgets.MainWindow import Ui_Dialog
# from
from procedure.kinship_on_graph import Kinship


class Main(QWidget, Ui_Dialog):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)  # 1
        # self.text_edit.textChanged.connect(self.show_text_func)  # 2
        self.PushButton2.clicked.connect(self.show_text_func)

    def show_text_func(self):
        print("self.text_browser.setText(\"Test\")")
        self.textBrowser_1.setText("self.text_browser.setText(\"Test\")")
        self.textBrowser_2.append("Test")

    def open_file(self):
        "打开文件"
        pass

    def calc_corrcoef(self):
        "计算亲缘相关系数"
        pass

    def calc_inbrcoef(self):
        "计算近交系数"
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    sys.exit(app.exec_())
