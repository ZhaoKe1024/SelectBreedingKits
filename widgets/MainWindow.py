# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(466, 538)
        self.Label1 = QtWidgets.QLabel(Dialog)
        self.Label1.setGeometry(QtCore.QRect(10, 10, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.Label1.setFont(font)
        self.Label1.setObjectName("Label1")
        self.PushButton1 = QtWidgets.QPushButton(Dialog)
        self.PushButton1.setGeometry(QtCore.QRect(30, 60, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.PushButton1.setFont(font)
        self.PushButton1.setObjectName("PushButton2_2")
        self.Label2 = QtWidgets.QLabel(Dialog)
        self.Label2.setGeometry(QtCore.QRect(160, 70, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.Label2.setFont(font)
        self.Label2.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.Label2.setObjectName("Label2")
        self.PushButton2 = QtWidgets.QPushButton(Dialog)
        self.PushButton2.setGeometry(QtCore.QRect(40, 110, 75, 23))
        self.PushButton2.setObjectName("PushButton2")
        self.Label4 = QtWidgets.QLabel(Dialog)
        self.Label4.setGeometry(QtCore.QRect(30, 280, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(13)
        self.Label4.setFont(font)
        self.Label4.setObjectName("Label4")
        self.Label5 = QtWidgets.QLabel(Dialog)
        self.Label5.setGeometry(QtCore.QRect(240, 280, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(13)
        self.Label5.setFont(font)
        self.Label5.setObjectName("Label5")
        self.Label6 = QtWidgets.QLabel(Dialog)
        self.Label6.setGeometry(QtCore.QRect(50, 320, 131, 21))
        self.Label6.setObjectName("Label6")
        self.Label7 = QtWidgets.QLabel(Dialog)
        self.Label7.setGeometry(QtCore.QRect(260, 310, 111, 41))
        self.Label7.setObjectName("Label7")
        self.textBrowser_1 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_1.setGeometry(QtCore.QRect(50, 150, 381, 91))
        self.textBrowser_1.setObjectName("textBrowser_1")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_2.setGeometry(QtCore.QRect(50, 370, 161, 131))
        self.textBrowser_2.setObjectName("textBrowser")
        self.textBrowser_3 = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_3.setGeometry(QtCore.QRect(250, 370, 181, 131))
        self.textBrowser_3.setObjectName("textBrowser_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Label1.setText(_translate("Dialog", "遗传族谱分析器"))
        self.PushButton1.setText(_translate("Dialog", "选中文件"))
        self.Label2.setText(_translate("Dialog", "示例：历代配种方案及出雏对照2021"))
        self.PushButton2.setText(_translate("Dialog", "分析文件"))
        self.Label4.setText(_translate("Dialog", "亲缘相关系数计算"))
        self.Label5.setText(_translate("Dialog", "个体近交系数计算"))
        self.Label6.setText(_translate("Dialog", "请输入两个个体的编号"))
        self.Label7.setText(_translate("Dialog", "请输入个体的编号"))
