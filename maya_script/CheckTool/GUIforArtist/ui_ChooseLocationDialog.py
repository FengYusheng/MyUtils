# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\CheckTool/Qt/UI/GUIforArtist/ChooseLocationDialog.ui'
#
# Created: Sat Dec  9 11:51:02 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ChooseLocationDialog(object):
    def setupUi(self, ChooseLocationDialog):
        ChooseLocationDialog.setObjectName("ChooseLocationDialog")
        ChooseLocationDialog.resize(517, 195)
        self.verticalLayout = QtWidgets.QVBoxLayout(ChooseLocationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.locationLineEdit = QtWidgets.QLineEdit(ChooseLocationDialog)
        self.locationLineEdit.setObjectName("locationLineEdit")
        self.horizontalLayout.addWidget(self.locationLineEdit)
        self.chooseLocationButton = QtWidgets.QPushButton(ChooseLocationDialog)
        self.chooseLocationButton.setObjectName("chooseLocationButton")
        self.horizontalLayout.addWidget(self.chooseLocationButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.applyButton = QtWidgets.QPushButton(ChooseLocationDialog)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout_2.addWidget(self.applyButton)
        self.closeButton = QtWidgets.QPushButton(ChooseLocationDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ChooseLocationDialog)
        QtCore.QMetaObject.connectSlotsByName(ChooseLocationDialog)

    def retranslateUi(self, ChooseLocationDialog):
        ChooseLocationDialog.setWindowTitle(QtWidgets.QApplication.translate("ChooseLocationDialog", "Dialog", None, -1))
        self.locationLineEdit.setPlaceholderText(QtWidgets.QApplication.translate("ChooseLocationDialog", "Choose a location where your configuration stores.", None, -1))
        self.chooseLocationButton.setText(QtWidgets.QApplication.translate("ChooseLocationDialog", "Choose", None, -1))
        self.applyButton.setText(QtWidgets.QApplication.translate("ChooseLocationDialog", "Apply", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("ChooseLocationDialog", "Close", None, -1))

