# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\teamtaticscript.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_JustAScript(object):
    def setupUi(self, JustAScript):
        JustAScript.setObjectName("JustAScript")
        JustAScript.resize(800, 600)
        JustAScript.setStyleSheet("QPushButton {\n"
"    color: rgb(255,255,255);\n"
"    background-color: #353B45\n"
"}\n"
"QLabel{\n"
"    color: rgb(255,255,255);\n"
"}\n"
"QCheckBox{\n"
"    color: rgb(255,255,255);\n"
"}\n"
"QTextBrowser{\n"
"    color: rgb(255,255,255);\n"
"    background-color: rgb(40, 44, 52);\n"
"    border-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QMainWindow{\n"
"background-color: rgb(40, 44, 52);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(JustAScript)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(11, 11, 781, 85))
        self.textBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 110, 781, 481))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setStyleSheet("font: 18pt \"Agency FB\";")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sur_time = QtWidgets.QSpinBox(self.widget)
        self.sur_time.setStyleSheet("font: 18pt \"Agency FB\";")
        self.sur_time.setObjectName("sur_time")
        self.horizontalLayout.addWidget(self.sur_time)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("font: 18pt \"Agency FB\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.loop_time = QtWidgets.QSpinBox(self.widget)
        self.loop_time.setStyleSheet("font: 18pt \"Agency FB\";")
        self.loop_time.setObjectName("loop_time")
        self.horizontalLayout_2.addWidget(self.loop_time)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet("font: 18pt \"Agency FB\";")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.wandering = QtWidgets.QCheckBox(self.widget)
        self.wandering.setStyleSheet("font: 18pt \"Agency FB\";")
        self.wandering.setObjectName("wandering")
        self.verticalLayout_2.addWidget(self.wandering)
        self.d_card = QtWidgets.QCheckBox(self.widget)
        self.d_card.setStyleSheet("font: 18pt \"Agency FB\";")
        self.d_card.setObjectName("d_card")
        self.verticalLayout_2.addWidget(self.d_card)
        self.exp = QtWidgets.QCheckBox(self.widget)
        self.exp.setStyleSheet("font: 18pt \"Agency FB\";")
        self.exp.setObjectName("exp")
        self.verticalLayout_2.addWidget(self.exp)
        self.shop = QtWidgets.QCheckBox(self.widget)
        self.shop.setStyleSheet("font: 18pt \"Agency FB\";")
        self.shop.setObjectName("shop")
        self.verticalLayout_2.addWidget(self.shop)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 5)
        self.verticalLayout_2.setStretch(3, 5)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(2, 3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.start = QtWidgets.QPushButton(self.widget)
        self.start.setStyleSheet("font: 18pt \"Agency FB\";")
        self.start.setObjectName("start")
        self.verticalLayout_3.addWidget(self.start)
        self.stop = QtWidgets.QPushButton(self.widget)
        self.stop.setStyleSheet("font: 18pt \"Agency FB\";\n"
"color: rgb(255, 255, 255);")
        self.stop.setObjectName("stop")
        self.verticalLayout_3.addWidget(self.stop)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(2, 1)
        JustAScript.setCentralWidget(self.centralwidget)

        self.retranslateUi(JustAScript)
        QtCore.QMetaObject.connectSlotsByName(JustAScript)

    def retranslateUi(self, JustAScript):
        _translate = QtCore.QCoreApplication.translate
        JustAScript.setWindowTitle(_translate("JustAScript", "JustAScript"))
        self.textBrowser.setHtml(_translate("JustAScript", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'PMingLiU\'; font-size:18pt;\">本程式僅使用於聯盟戰旗掛機</span></p></body></html>"))
        self.label.setText(_translate("JustAScript", "投降時間"))
        self.label_2.setText(_translate("JustAScript", "掛機次數"))
        self.label_3.setText(_translate("JustAScript", "動作選擇"))
        self.wandering.setText(_translate("JustAScript", "是否遊走"))
        self.d_card.setText(_translate("JustAScript", "是否D牌"))
        self.exp.setText(_translate("JustAScript", "是否升級"))
        self.shop.setText(_translate("JustAScript", "是否買棋"))
        self.start.setText(_translate("JustAScript", "開始"))
        self.stop.setText(_translate("JustAScript", "停止"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    JustAScript = QtWidgets.QMainWindow()
    ui = Ui_JustAScript()
    ui.setupUi(JustAScript)
    JustAScript.show()
    sys.exit(app.exec_())
