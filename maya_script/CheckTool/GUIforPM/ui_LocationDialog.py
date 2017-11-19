# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\CheckTool/Qt/UI/GUIforPM/LocationDialog.ui'
#
# Created: Sun Nov 19 20:29:49 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_locationDialog(object):
    def setupUi(self, locationDialog):
        locationDialog.setObjectName("locationDialog")
        locationDialog.resize(497, 149)
        self.verticalLayout = QtWidgets.QVBoxLayout(locationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.locationLinediet = QtWidgets.QLineEdit(locationDialog)
        self.locationLinediet.setReadOnly(True)
        self.locationLinediet.setObjectName("locationLinediet")
        self.horizontalLayout.addWidget(self.locationLinediet)
        self.chooseButton = QtWidgets.QPushButton(locationDialog)
        self.chooseButton.setObjectName("chooseButton")
        self.horizontalLayout.addWidget(self.chooseButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okButton = QtWidgets.QPushButton(locationDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(locationDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(locationDialog)
        QtCore.QMetaObject.connectSlotsByName(locationDialog)

    def retranslateUi(self, locationDialog):
        locationDialog.setWindowTitle(QtWidgets.QApplication.translate("locationDialog", "Choose a directory to store your configuration.", None, -1))
        self.locationLinediet.setPlaceholderText(QtWidgets.QApplication.translate("locationDialog", "Choose a directory to store your configuration.", None, -1))
        self.chooseButton.setText(QtWidgets.QApplication.translate("locationDialog", "Choose", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("locationDialog", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("locationDialog", "Cancel", None, -1))

