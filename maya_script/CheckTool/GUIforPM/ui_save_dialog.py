# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\check_scene\Qt\UI\create_checker\save_dialog.ui'
#
# Created: Tue Oct 31 14:42:33 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

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
        save_dialog.setWindowTitle(QtWidgets.QApplication.translate("save_dialog", "Save your configuration", None, -1))
        self.enter_label.setText(QtWidgets.QApplication.translate("save_dialog", "Configurations have been modified, save them?", None, -1))
        self.yes_button.setText(QtWidgets.QApplication.translate("save_dialog", "Yes", None, -1))
        self.no_button.setText(QtWidgets.QApplication.translate("save_dialog", "No", None, -1))

