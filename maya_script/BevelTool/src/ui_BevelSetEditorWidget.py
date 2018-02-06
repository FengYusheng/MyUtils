# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/BevelSetEditorWidget.ui'
#
# Created: Tue Feb 06 14:20:12 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_bevelSetEditorWidget(object):
    def setupUi(self, bevelSetEditorWidget):
        bevelSetEditorWidget.setObjectName("bevelSetEditorWidget")
        bevelSetEditorWidget.resize(620, 538)
        self.verticalLayout = QtWidgets.QVBoxLayout(bevelSetEditorWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newSetButton = QtWidgets.QPushButton(bevelSetEditorWidget)
        self.newSetButton.setObjectName("newSetButton")
        self.horizontalLayout.addWidget(self.newSetButton)
        self.addMemberButton = QtWidgets.QPushButton(bevelSetEditorWidget)
        self.addMemberButton.setObjectName("addMemberButton")
        self.horizontalLayout.addWidget(self.addMemberButton)
        self.removeMemberButton = QtWidgets.QPushButton(bevelSetEditorWidget)
        self.removeMemberButton.setObjectName("removeMemberButton")
        self.horizontalLayout.addWidget(self.removeMemberButton)
        self.selectMemberButton = QtWidgets.QPushButton(bevelSetEditorWidget)
        self.selectMemberButton.setObjectName("selectMemberButton")
        self.horizontalLayout.addWidget(self.selectMemberButton)
        self.deleteSetButton = QtWidgets.QPushButton(bevelSetEditorWidget)
        self.deleteSetButton.setObjectName("deleteSetButton")
        self.horizontalLayout.addWidget(self.deleteSetButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(bevelSetEditorWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.bevelSetTreeView = QtWidgets.QTreeView(self.splitter)
        self.bevelSetTreeView.setObjectName("bevelSetTreeView")
        self.optionGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.optionGroupBox.setTitle("")
        self.optionGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.optionGroupBox.setFlat(True)
        self.optionGroupBox.setCheckable(False)
        self.optionGroupBox.setObjectName("optionGroupBox")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(bevelSetEditorWidget)
        QtCore.QMetaObject.connectSlotsByName(bevelSetEditorWidget)

    def retranslateUi(self, bevelSetEditorWidget):
        bevelSetEditorWidget.setWindowTitle(QtWidgets.QApplication.translate("bevelSetEditorWidget", "Form", None, -1))
        self.newSetButton.setText(QtWidgets.QApplication.translate("bevelSetEditorWidget", "New", None, -1))
        self.addMemberButton.setText(QtWidgets.QApplication.translate("bevelSetEditorWidget", "Add", None, -1))
        self.removeMemberButton.setText(QtWidgets.QApplication.translate("bevelSetEditorWidget", "Remove", None, -1))
        self.selectMemberButton.setText(QtWidgets.QApplication.translate("bevelSetEditorWidget", "Select", None, -1))
        self.deleteSetButton.setText(QtWidgets.QApplication.translate("bevelSetEditorWidget", "Delete", None, -1))

