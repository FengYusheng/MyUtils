# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_save_dialog(object):
    def setupUi(self, save_dialog):
        save_dialog.setObjectName("save_dialog")
        save_dialog.resize(291, 109)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(save_dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.enter_label = QtWidgets.QLabel(save_dialog)
        self.enter_label.setObjectName("enter_label")
        self.verticalLayout.addWidget(self.enter_label)
        self.name_le = QtWidgets.QLineEdit(save_dialog)
        self.name_le.setObjectName("name_le")
        self.verticalLayout.addWidget(self.name_le)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_button = QtWidgets.QPushButton(save_dialog)
        self.yes_button.setObjectName("yes_button")
        self.horizontalLayout.addWidget(self.yes_button)
        self.no_button = QtWidgets.QPushButton(save_dialog)
        self.no_button.setObjectName("no_button")
        self.horizontalLayout.addWidget(self.no_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(save_dialog)
        QtCore.QMetaObject.connectSlotsByName(save_dialog)

    def retranslateUi(self, save_dialog):
        _translate = QtCore.QCoreApplication.translate
        save_dialog.setWindowTitle(_translate("save_dialog", "Save your configuration"))
        self.enter_label.setText(_translate("save_dialog", "Configurations have been modified, save them?"))
        self.yes_button.setText(_translate("save_dialog", "Yes"))
        self.no_button.setText(_translate("save_dialog", "No"))

