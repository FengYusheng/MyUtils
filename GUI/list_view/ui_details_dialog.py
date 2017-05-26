# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'details_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_details_dialog(object):
    def setupUi(self, details_dialog):
        details_dialog.setObjectName("details_dialog")
        details_dialog.resize(596, 505)
        details_dialog.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(details_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.details_table = QtWidgets.QTableView(details_dialog)
        self.details_table.setObjectName("details_table")
        self.verticalLayout.addWidget(self.details_table)
        self.line = QtWidgets.QFrame(details_dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_button = QtWidgets.QPushButton(details_dialog)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.reset_button = QtWidgets.QPushButton(details_dialog)
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout.addWidget(self.reset_button)
        self.cancel_button = QtWidgets.QPushButton(details_dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(details_dialog)
        QtCore.QMetaObject.connectSlotsByName(details_dialog)

    def retranslateUi(self, details_dialog):
        _translate = QtCore.QCoreApplication.translate
        self.save_button.setText(_translate("details_dialog", "Save"))
        self.reset_button.setText(_translate("details_dialog", "Reset"))
        self.cancel_button.setText(_translate("details_dialog", "Cancel"))

