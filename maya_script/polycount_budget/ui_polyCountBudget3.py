# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\develop\MyUtils\maya_script\polycount_budget\Qt\UI\polyCountBudget3.ui'
#
# Created: Sat Oct 14 10:25:38 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_polyCountBudgetMainWindow(object):
    def setupUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setObjectName("polyCountBudgetMainWindow")
        polyCountBudgetMainWindow.resize(965, 789)
        self.centralwidget = QtGui.QWidget(polyCountBudgetMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        polyCountBudgetMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(polyCountBudgetMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 21))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtGui.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.viewMenu = QtGui.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        polyCountBudgetMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(polyCountBudgetMainWindow)
        self.statusbar.setObjectName("statusbar")
        polyCountBudgetMainWindow.setStatusBar(self.statusbar)
        self.budgetDock = QtGui.QDockWidget(polyCountBudgetMainWindow)
        self.budgetDock.setObjectName("budgetDock")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.polyCountTab = QtGui.QTabWidget(self.dockWidgetContents)
        self.polyCountTab.setObjectName("polyCountTab")
        self.setBudgetTab = QtGui.QWidget()
        self.setBudgetTab.setObjectName("setBudgetTab")
        self.gridLayout_2 = QtGui.QGridLayout(self.setBudgetTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.setBudgetTableView = QtGui.QTableView(self.setBudgetTab)
        self.setBudgetTableView.setObjectName("setBudgetTableView")
        self.gridLayout_2.addWidget(self.setBudgetTableView, 0, 0, 1, 1)
        self.polyCountTab.addTab(self.setBudgetTab, "")
        self.polycontInScene = QtGui.QWidget()
        self.polycontInScene.setObjectName("polycontInScene")
        self.gridLayout_3 = QtGui.QGridLayout(self.polycontInScene)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.polycountTreeView = QtGui.QTreeView(self.polycontInScene)
        self.polycountTreeView.setObjectName("polycountTreeView")
        self.gridLayout_3.addWidget(self.polycountTreeView, 0, 0, 1, 1)
        self.polyCountTab.addTab(self.polycontInScene, "")
        self.gridLayout.addWidget(self.polyCountTab, 0, 0, 1, 1)
        self.budgetDock.setWidget(self.dockWidgetContents)
        polyCountBudgetMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.budgetDock)
        self.resetAction = QtGui.QAction(polyCountBudgetMainWindow)
        self.resetAction.setObjectName("resetAction")
        self.editMenu.addAction(self.resetAction)
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())

        self.retranslateUi(polyCountBudgetMainWindow)
        self.polyCountTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(polyCountBudgetMainWindow)

    def retranslateUi(self, polyCountBudgetMainWindow):
        polyCountBudgetMainWindow.setWindowTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Set Your Polycount Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.editMenu.setTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.viewMenu.setTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.budgetDock.setWindowTitle(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Poly Count Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountTab.setTabText(self.polyCountTab.indexOf(self.setBudgetTab), QtGui.QApplication.translate("polyCountBudgetMainWindow", "Set Budget", None, QtGui.QApplication.UnicodeUTF8))
        self.polyCountTab.setTabText(self.polyCountTab.indexOf(self.polycontInScene), QtGui.QApplication.translate("polyCountBudgetMainWindow", "Polycont in Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.resetAction.setText(QtGui.QApplication.translate("polyCountBudgetMainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))

