# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\Checker\GUI\PM_GUI\new_save_dialog.ui'
#
# Created: Thu Jun 01 11:27:24 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_new_save(object):
    def setupUi(self, new_save):
        new_save.setObjectName("new_save")
        new_save.resize(298, 111)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(new_save)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_la = QtWidgets.QLabel(new_save)
        self.name_la.setObjectName("name_la")
        self.verticalLayout.addWidget(self.name_la)
        self.name_le = QtWidgets.QLineEdit(new_save)
        self.name_le.setObjectName("name_le")
        self.verticalLayout.addWidget(self.name_le)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_buttion = QtWidgets.QPushButton(new_save)
        self.save_buttion.setObjectName("save_buttion")
        self.horizontalLayout.addWidget(self.save_buttion)
        self.cancel_buttion = QtWidgets.QPushButton(new_save)
        self.cancel_buttion.setObjectName("cancel_buttion")
        self.horizontalLayout.addWidget(self.cancel_buttion)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(new_save)
        QtCore.QMetaObject.connectSlotsByName(new_save)

    def retranslateUi(self, new_save):
        new_save.setWindowTitle(QtWidgets.QApplication.translate("new_save", "Save", None, -1))
        self.name_la.setText(QtWidgets.QApplication.translate("new_save", "Enter a project name:", None, -1))
        self.save_buttion.setText(QtWidgets.QApplication.translate("new_save", "Save", None, -1))
        self.cancel_buttion.setText(QtWidgets.QApplication.translate("new_save", "Cancel", None, -1))

