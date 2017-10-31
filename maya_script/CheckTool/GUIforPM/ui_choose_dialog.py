# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\check_scene\Qt\UI\create_checker\choose_dialog.ui'
#
# Created: Tue Oct 31 14:42:33 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_chooseDialog(object):
    def setupUi(self, chooseDialog):
        chooseDialog.setObjectName("chooseDialog")
        chooseDialog.resize(497, 149)
        self.verticalLayout = QtWidgets.QVBoxLayout(chooseDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chooseLineEdit = QtWidgets.QLineEdit(chooseDialog)
        self.chooseLineEdit.setReadOnly(True)
        self.chooseLineEdit.setObjectName("chooseLineEdit")
        self.horizontalLayout.addWidget(self.chooseLineEdit)
        self.chooseButton = QtWidgets.QPushButton(chooseDialog)
        self.chooseButton.setObjectName("chooseButton")
        self.horizontalLayout.addWidget(self.chooseButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okbutton = QtWidgets.QPushButton(chooseDialog)
        self.okbutton.setObjectName("okbutton")
        self.horizontalLayout_2.addWidget(self.okbutton)
        self.cancelButton = QtWidgets.QPushButton(chooseDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(chooseDialog)
        QtCore.QMetaObject.connectSlotsByName(chooseDialog)

    def retranslateUi(self, chooseDialog):
        chooseDialog.setWindowTitle(QtWidgets.QApplication.translate("chooseDialog", "Chose a directory to locate your suite files..", None, -1))
        self.chooseLineEdit.setPlaceholderText(QtWidgets.QApplication.translate("chooseDialog", "Choose a directory to locate your suite files...", None, -1))
        self.chooseButton.setText(QtWidgets.QApplication.translate("chooseDialog", "Choose", None, -1))
        self.okbutton.setText(QtWidgets.QApplication.translate("chooseDialog", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("chooseDialog", "Cancel", None, -1))

