# -*- coding: utf-8 -*-
# @Author : ZhaoKe
# @Time : 2024-05-23 23:03
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from widgets.MainWindow import Ui_Dialog


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    sys.exit(app.exec_())
