# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pm_view2.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PM_View(object):
    def setupUi(self, PM_View):
        PM_View.setObjectName("PM_View")
        PM_View.resize(793, 600)
        self.centralwidget = QtWidgets.QWidget(PM_View)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.test_label = QtWidgets.QLabel(self.centralwidget)
        self.test_label.setObjectName("test_label")
        self.verticalLayout.addWidget(self.test_label)
        self.testList = QtWidgets.QListView(self.centralwidget)
        self.testList.setObjectName("testList")
        self.verticalLayout.addWidget(self.testList)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.verticalLayout_3.addWidget(self.addButton)
        self.removeButtion = QtWidgets.QPushButton(self.centralwidget)
        self.removeButtion.setObjectName("removeButtion")
        self.verticalLayout_3.addWidget(self.removeButtion)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selected_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_label.setObjectName("selected_label")
        self.horizontalLayout_2.addWidget(self.selected_label)
        self.project_combo = QtWidgets.QComboBox(self.centralwidget)
        self.project_combo.setObjectName("project_combo")
        self.project_combo.addItem("")
        self.horizontalLayout_2.addWidget(self.project_combo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.selectedList = QtWidgets.QListView(self.centralwidget)
        self.selectedList.setObjectName("selectedList")
        self.verticalLayout_2.addWidget(self.selectedList)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(348, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        PM_View.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PM_View)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTest = QtWidgets.QMenu(self.menubar)
        self.menuTest.setObjectName("menuTest")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        PM_View.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PM_View)
        self.statusbar.setObjectName("statusbar")
        PM_View.setStatusBar(self.statusbar)
        self.actionReset = QtWidgets.QAction(PM_View)
        self.actionReset.setObjectName("actionReset")
        self.actionSave_as = QtWidgets.QAction(PM_View)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionDelete = QtWidgets.QAction(PM_View)
        self.actionDelete.setObjectName("actionDelete")
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionDelete)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTest.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(PM_View)
        QtCore.QMetaObject.connectSlotsByName(PM_View)

    def retranslateUi(self, PM_View):
        _translate = QtCore.QCoreApplication.translate
        PM_View.setWindowTitle(_translate("PM_View", "PM_View"))
        self.test_label.setText(_translate("PM_View", "Test List:"))
        self.addButton.setText(_translate("PM_View", "Add"))
        self.removeButtion.setText(_translate("PM_View", "Remove"))
        self.selected_label.setText(_translate("PM_View", "Select a project:"))
        self.project_combo.setItemText(0, _translate("PM_View", "New project"))
        self.nextButton.setText(_translate("PM_View", "Next"))
        self.deleteButton.setText(_translate("PM_View", "Delete"))
        self.cancelButton.setText(_translate("PM_View", "Cancel"))
        self.menuFile.setTitle(_translate("PM_View", "File"))
        self.menuTest.setTitle(_translate("PM_View", "Test"))
        self.menuHelp.setTitle(_translate("PM_View", "Help"))
        self.actionReset.setText(_translate("PM_View", "Reset"))
        self.actionSave_as.setText(_translate("PM_View", "Save as..."))
        self.actionDelete.setText(_translate("PM_View", "Delete"))
