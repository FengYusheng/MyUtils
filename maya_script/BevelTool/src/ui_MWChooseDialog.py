# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/MWChooseDialog.ui'
#
# Created: Mon Mar 12 17:26:29 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MWChooseDialog(object):
    def setupUi(self, MWChooseDialog):
        MWChooseDialog.setObjectName("MWChooseDialog")
        MWChooseDialog.resize(501, 232)
        self.verticalLayout = QtWidgets.QVBoxLayout(MWChooseDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(MWChooseDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.remeberCheckBox = QtWidgets.QCheckBox(MWChooseDialog)
        self.remeberCheckBox.setObjectName("remeberCheckBox")
        self.horizontalLayout.addWidget(self.remeberCheckBox)
        self.yesButton = QtWidgets.QPushButton(MWChooseDialog)
        self.yesButton.setAutoDefault(False)
        self.yesButton.setDefault(True)
        self.yesButton.setFlat(False)
        self.yesButton.setObjectName("yesButton")
        self.horizontalLayout.addWidget(self.yesButton)
        self.noButton = QtWidgets.QPushButton(MWChooseDialog)
        self.noButton.setObjectName("noButton")
        self.horizontalLayout.addWidget(self.noButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MWChooseDialog)
        QtCore.QMetaObject.connectSlotsByName(MWChooseDialog)

    def retranslateUi(self, MWChooseDialog):
        MWChooseDialog.setWindowTitle(QtWidgets.QApplication.translate("MWChooseDialog", "Dialog", None, -1))
        self.textEdit.setHtml(QtWidgets.QApplication.translate("MWChooseDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">is already in</span></p></body></html>", None, -1))
        self.remeberCheckBox.setText(QtWidgets.QApplication.translate("MWChooseDialog", "Remeber this.", None, -1))
        self.yesButton.setText(QtWidgets.QApplication.translate("MWChooseDialog", "Yes", None, -1))
        self.noButton.setText(QtWidgets.QApplication.translate("MWChooseDialog", "No", None, -1))

