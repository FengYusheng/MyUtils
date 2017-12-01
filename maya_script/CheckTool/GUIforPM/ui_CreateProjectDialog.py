# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\MindwalkTools\MayaTools\MWCheckTool/Qt/UI/GUIforPM/CreateProjectDialog.ui'
#
# Created: Fri Dec 01 17:29:29 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        CreateProjectDialog.setObjectName("CreateProjectDialog")
        CreateProjectDialog.resize(445, 170)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateProjectDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectNameLabel = QtWidgets.QLabel(CreateProjectDialog)
        self.projectNameLabel.setTextFormat(QtCore.Qt.RichText)
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.horizontalLayout.addWidget(self.projectNameLabel)
        self.projectNameLineEdit = QtWidgets.QLineEdit(CreateProjectDialog)
        self.projectNameLineEdit.setObjectName("projectNameLineEdit")
        self.horizontalLayout.addWidget(self.projectNameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.okButton = QtWidgets.QPushButton(CreateProjectDialog)
        self.okButton.setDefault(True)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_2.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(CreateProjectDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CreateProjectDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateProjectDialog)

    def retranslateUi(self, CreateProjectDialog):
        CreateProjectDialog.setWindowTitle(QtWidgets.QApplication.translate("CreateProjectDialog", "Enter your project\'s name", None, -1))
        self.projectNameLabel.setText(QtWidgets.QApplication.translate("CreateProjectDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Project name:</span></p></body></html>", None, -1))
        self.projectNameLineEdit.setPlaceholderText(QtWidgets.QApplication.translate("CreateProjectDialog", "Enter your project\'s name.", None, -1))
        self.okButton.setText(QtWidgets.QApplication.translate("CreateProjectDialog", "OK", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("CreateProjectDialog", "Cancel", None, -1))

