# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(825, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Banner = QtWidgets.QLabel(self.centralwidget)
        self.Banner.setGeometry(QtCore.QRect(270, 0, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Banner.setFont(font)
        self.Banner.setObjectName("Banner")

        self.list_label = QtWidgets.QLabel(self.centralwidget)
        self.list_label.setGeometry(QtCore.QRect(20, 31, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.list_label.setFont(font)
        self.list_label.setObjectName("list_label")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 80, 121, 481))
        self.listWidget.setObjectName("listWidget")

        listitem1 = QListWidgetItem()
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(20, 100, 101, 41))
        self.pushButton_1.setObjectName("pushButton_1")
        self.listWidget.insertItem(self.listWidget.count(), listitem1)
        self.listWidget.setItemWidget(listitem1, self.pushButton_1)

        listitem2 = QListWidgetItem()
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 160, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.listWidget.insertItem(self.listWidget.count(), listitem2)
        self.listWidget.setItemWidget(listitem2, self.pushButton_2)

        listitem3 = QListWidgetItem()
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 220, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWidget.insertItem(self.listWidget.count(), listitem3)
        self.listWidget.setItemWidget(listitem3, self.pushButton_3)

        listitem4 = QListWidgetItem()
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 280, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.listWidget.insertItem(self.listWidget.count(), listitem4)
        self.listWidget.setItemWidget(listitem4, self.pushButton_4)

        listitem5 = QListWidgetItem()
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 340, 101, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.listWidget.insertItem(self.listWidget.count(), listitem5)
        self.listWidget.setItemWidget(listitem5, self.pushButton_5)

        listitem6 = QListWidgetItem()
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 400, 101, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        self.listWidget.insertItem(self.listWidget.count(), listitem6)
        self.listWidget.setItemWidget(listitem6, self.pushButton_6)
        print(self.listWidget.count())

        # =============----Stack------=================
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(140, 80, 681, 481))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")

        # =====---0 分析页面---==========
        self.page_0 = QtWidgets.QWidget()
        self.page_0.setObjectName("page_0")
        self.label_9 = QtWidgets.QLabel(self.page_0)
        self.label_9.setGeometry(QtCore.QRect(40, 50, 261, 51))
        self.label_9.setObjectName("label_9")
        self.pushButton_17 = QtWidgets.QPushButton(self.page_0)
        self.pushButton_17.setGeometry(QtCore.QRect(10, 10, 150, 40))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.page_0)
        self.pushButton_18.setGeometry(QtCore.QRect(10, 110, 150, 40))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.page_0)
        self.pushButton_19.setGeometry(QtCore.QRect(410, 10, 150, 40))
        self.pushButton_19.setObjectName("pushButton_19")
        self.stackedWidget.addWidget(self.page_0)

        # =====---1 历史方案分析---==========
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.pushButton_14 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_14.setGeometry(QtCore.QRect(10, 10, 150, 40))
        self.pushButton_14.setObjectName("pushButton_14")  #
        self.label_4 = QtWidgets.QLabel(self.page_1)
        self.label_4.setGeometry(QtCore.QRect(30, 70, 231, 31))
        self.label_4.setObjectName("label_4")
        self.pushButton_15 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_15.setGeometry(QtCore.QRect(410, 10, 131, 41))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_16.setGeometry(QtCore.QRect(10, 150, 131, 41))
        self.pushButton_16.setObjectName("pushButton_16")
        self.label_17 = QtWidgets.QLabel(self.page_1)
        self.label_17.setGeometry(QtCore.QRect(40, 210, 261, 51))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.page_1)
        self.label_18.setGeometry(QtCore.QRect(30, 110, 200, 40))
        self.label_18.setObjectName("label_18")

        self.input_19 = QtWidgets.QLineEdit(self.page_1)
        self.input_19.setGeometry(QtCore.QRect(230, 110, 71, 41))
        self.input_19.setObjectName("input_8")

        self.textBrowser_eval = QtWidgets.QTextBrowser(self.page_1)
        self.textBrowser_eval.setGeometry(QtCore.QRect(40, 250, 351, 221))
        self.textBrowser_eval.setObjectName("textBrowser_3")

        self.stackedWidget.addWidget(self.page_1)
        # =====---2 亲缘相关系数计算---==========
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        self.label_11 = QtWidgets.QLabel(self.page_2)
        self.label_11.setGeometry(QtCore.QRect(40, 50, 150, 41))
        self.label_11.setObjectName("label_11")

        # 输入提示
        self.label_10 = QtWidgets.QLabel(self.page_2)
        self.label_10.setGeometry(QtCore.QRect(10, 3, 171, 80))
        self.label_10.setObjectName("label_10")

        self.input_3 = QtWidgets.QLineEdit(self.page_2)
        self.input_3.setGeometry(QtCore.QRect(200, 50, 220, 51))
        self.input_3.setObjectName("input_8")

        self.calcButton1 = QtWidgets.QPushButton(self.page_2)
        self.calcButton1.setGeometry(QtCore.QRect(40, 100, 111, 51))
        self.calcButton1.setObjectName("pushButton")

        self.textBrowser_3 = QtWidgets.QTextBrowser(self.page_2)
        self.textBrowser_3.setGeometry(QtCore.QRect(40, 170, 351, 221))
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.stackedWidget.addWidget(self.page_2)

        # =====---3 个体近交系数计算---==========
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")

        # 输入提示
        self.label = QtWidgets.QLabel(self.page_3)
        self.label.setGeometry(QtCore.QRect(10, 3, 171, 80))
        self.label.setObjectName("label")

        self.label_5 = QtWidgets.QLabel(self.page_3)
        self.label_5.setGeometry(QtCore.QRect(40, 50, 150, 41))
        self.label_5.setObjectName("label_5")

        self.input_44 = QtWidgets.QLineEdit(self.page_3)
        self.input_44.setGeometry(QtCore.QRect(200, 50, 220, 51))
        self.input_44.setObjectName("input_8")

        self.calcButton2 = QtWidgets.QPushButton(self.page_3)
        self.calcButton2.setGeometry(QtCore.QRect(40, 100, 111, 51))
        self.calcButton2.setObjectName("pushButton")

        self.textBrowser = QtWidgets.QTextBrowser(self.page_3)
        self.textBrowser.setGeometry(QtCore.QRect(40, 170, 351, 221))
        self.textBrowser.setObjectName("textBrowser")
        self.stackedWidget.addWidget(self.page_3)

        # =====---4 育种方案生成---==========
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")

        self.label_2 = QtWidgets.QLabel(self.page_4)
        self.label_2.setGeometry(QtCore.QRect(40, 45, 261, 31))
        self.label_2.setObjectName("label_2")

        self.label_12 = QtWidgets.QLabel(self.page_4)
        self.label_12.setGeometry(QtCore.QRect(40, 95, 95, 21))
        self.label_12.setObjectName("label_12")
        self.input_8 = QtWidgets.QLineEdit(self.page_4)
        self.input_8.setGeometry(QtCore.QRect(210, 85, 141, 36))
        self.input_8.setObjectName("input_8")

        self.label_13 = QtWidgets.QLabel(self.page_4)
        self.label_13.setGeometry(QtCore.QRect(40, 135, 95, 21))
        self.label_13.setObjectName("label_13")
        self.input_14 = QtWidgets.QLineEdit(self.page_4)
        self.input_14.setGeometry(QtCore.QRect(210, 125, 141, 36))
        self.input_14.setObjectName("input_14")

        self.label_15 = QtWidgets.QLabel(self.page_4)
        self.label_15.setGeometry(QtCore.QRect(40, 175, 141, 21))
        self.label_15.setObjectName("label_15")  # 输入家系个数
        self.input_16 = QtWidgets.QLineEdit(self.page_4)
        self.input_16.setGeometry(QtCore.QRect(210, 165, 141, 36))
        self.input_16.setObjectName("input_16")

        self.textBrowser_2 = QtWidgets.QTextBrowser(self.page_4)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 210, 351, 221))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.selectButton = QtWidgets.QPushButton(self.page_4)
        self.selectButton.setGeometry(QtCore.QRect(220, 45, 110, 31))
        self.selectButton.setObjectName("selectButton")

        self.pushButton = QtWidgets.QPushButton(self.page_4)
        self.pushButton.setGeometry(QtCore.QRect(20, 440, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page_4)

        self.label_7 = QtWidgets.QLabel(self.page_4)  # 导入历史配种方案
        self.label_7.setGeometry(QtCore.QRect(170, 440, 171, 41))
        self.label_7.setObjectName("label_7")

        # ====-----设置页----========
        self.page_settings = QtWidgets.QWidget()
        self.page_settings.setObjectName("page_settings")
        self.label_20 = QtWidgets.QLabel(self.page_settings)
        self.label_20.setGeometry(QtCore.QRect(240, 10, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.stackedWidget.addWidget(self.page_settings)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.listWidget, self.pushButton_1)
        MainWindow.setTabOrder(self.pushButton_1, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.pushButton_5)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Banner.setText(_translate("MainWindow", "家禽育种计算工具"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_17.setText(_translate("MainWindow", "导入配种对照文件"))
        self.pushButton_18.setText(_translate("MainWindow", "构建族谱图"))
        self.pushButton_19.setText(_translate("MainWindow", "模板下载"))

        self.pushButton_14.setText(_translate("MainWindow", "导入历史配种文件"))
        self.pushButton_15.setText(_translate("MainWindow", "模板下载"))
        self.label_4.setText(_translate("MainWindow", "待上传文件"))
        self.label_18.setText(_translate("MainWindow", "输入评估年份(需在文件中包含)"))
        self.pushButton_16.setText(_translate("MainWindow", "评估方案"))
        self.label_17.setText(_translate("MainWindow", "生成评估文件："))
        self.input_19.setText(_translate("MainWindow", ""))

        self.label_10.setText(_translate("MainWindow", "请输入两个个体的翅号(逗号或空格隔开)"))
        self.label_11.setText(_translate("MainWindow", "亲缘相关系数计算"))
        self.calcButton1.setText(_translate("MainWindow", "计算"))

        self.label.setText(_translate("MainWindow", "请输入个体的翅号"))
        self.label_5.setText(_translate("MainWindow", "个体近交系数计算"))
        # self.input_44.setText(_translate("MainWindow", "输入框"))
        self.calcButton2.setText(_translate("MainWindow", "计算"))

        self.label_2.setText(_translate("MainWindow", "文件名"))
        self.label_12.setText(_translate("MainWindow", "请输入年份："))
        self.input_8.setText(_translate("MainWindow", ""))
        self.label_13.setText(_translate("MainWindow", "请输入雌雄比："))
        self.input_14.setText(_translate("MainWindow", "10"))
        self.label_15.setText(_translate("MainWindow", "请输入所需家系个数："))
        self.input_16.setText(_translate("MainWindow", "默认等于母禽个数"))
        self.selectButton.setText(_translate("MainWindow", "生成方案"))
        self.pushButton.setText(_translate("MainWindow", "打开生成的方案"))
        self.label_7.setText(_translate("MainWindow", "filename.xlsx"))

        self.pushButton_1.setText(_translate("MainWindow", "文件分析"))
        self.pushButton_2.setText(_translate("MainWindow", "谱系分析"))
        self.pushButton_3.setText(_translate("MainWindow", "亲缘系数分析"))
        self.pushButton_4.setText(_translate("MainWindow", "近交系数分析"))
        self.pushButton_5.setText(_translate("MainWindow", "育种方案分析"))
        self.pushButton_6.setText(_translate("MainWindow", "设置页"))
        self.list_label.setText(_translate("MainWindow", "工具栏"))
        self.label_20.setText(_translate("MainWindow", "登陆设置"))


from PyQt5.QtWidgets import QApplication, QMainWindow


class MainRunningWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainRunningWindow, self).__init__()
        self.setupUi(self)  # 1


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mc = MainRunningWindow()
    mc.show()
    sys.exit(app.exec_())
