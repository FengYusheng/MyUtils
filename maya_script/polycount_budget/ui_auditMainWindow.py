# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MindwalkToolsDevWorkspace\Draft\polycount_budget\Qt\UI\auditMainWindow.ui'
#
# Created: Wed Oct 11 10:34:16 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AuditMainWindow(object):
    def setupUi(self, AuditMainWindow):
        AuditMainWindow.setObjectName("AuditMainWindow")
        AuditMainWindow.resize(1093, 830)
        self.centralwidget = QtWidgets.QWidget(AuditMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.sceneTreeView = QtWidgets.QTreeView(self.centralwidget)
        self.sceneTreeView.setObjectName("sceneTreeView")
        self.gridLayout_3.addWidget(self.sceneTreeView, 0, 0, 1, 1)
        AuditMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AuditMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        AuditMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AuditMainWindow)
        self.statusbar.setObjectName("statusbar")
        AuditMainWindow.setStatusBar(self.statusbar)
        self.budgetDock = QtWidgets.QDockWidget(AuditMainWindow)
        self.budgetDock.setMinimumSize(QtCore.QSize(89, 111))
        self.budgetDock.setFloating(False)
        self.budgetDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.budgetDock.setObjectName("budgetDock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.budgetTabelView = QtWidgets.QTableView(self.dockWidgetContents)
        self.budgetTabelView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.budgetTabelView.setObjectName("budgetTabelView")
        self.gridLayout.addWidget(self.budgetTabelView, 0, 0, 1, 1)
        self.budgetDock.setWidget(self.dockWidgetContents)
        AuditMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.budgetDock)
        self.polyCountDock = QtWidgets.QDockWidget(AuditMainWindow)
        self.polyCountDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.polyCountDock.setObjectName("polyCountDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.polyCountTreeView = QtWidgets.QTreeView(self.dockWidgetContents_2)
        self.polyCountTreeView.setMouseTracking(False)
        self.polyCountTreeView.setAlternatingRowColors(True)
        self.polyCountTreeView.setObjectName("polyCountTreeView")
        self.gridLayout_2.addWidget(self.polyCountTreeView, 0, 0, 1, 1)
        self.polyCountDock.setWidget(self.dockWidgetContents_2)
        AuditMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.polyCountDock)
        self.resetAction = QtWidgets.QAction(AuditMainWindow)
        self.resetAction.setObjectName("resetAction")
        self.budgetAction = QtWidgets.QAction(AuditMainWindow)
        self.budgetAction.setObjectName("budgetAction")
        self.importBudgetAction = QtWidgets.QAction(AuditMainWindow)
        self.importBudgetAction.setObjectName("importBudgetAction")
        self.polyCountAction = QtWidgets.QAction(AuditMainWindow)
        self.polyCountAction.setObjectName("polyCountAction")
        self.menuEdit.addAction(self.resetAction)
        self.menuEdit.addAction(self.budgetAction)
        self.menuEdit.addAction(self.importBudgetAction)
        self.menuEdit.addAction(self.polyCountAction)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(AuditMainWindow)
        QtCore.QMetaObject.connectSlotsByName(AuditMainWindow)

    def retranslateUi(self, AuditMainWindow):
        AuditMainWindow.setWindowTitle(QtWidgets.QApplication.translate("AuditMainWindow", "Audit your asset", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("AuditMainWindow", "Edit", None, -1))
        self.menuView.setTitle(QtWidgets.QApplication.translate("AuditMainWindow", "View", None, -1))
        self.budgetDock.setWindowTitle(QtWidgets.QApplication.translate("AuditMainWindow", "Budget and LOD", None, -1))
        self.polyCountDock.setWindowTitle(QtWidgets.QApplication.translate("AuditMainWindow", "Poly Count in Current Scene", None, -1))
        self.resetAction.setText(QtWidgets.QApplication.translate("AuditMainWindow", "Reset", None, -1))
        self.budgetAction.setText(QtWidgets.QApplication.translate("AuditMainWindow", "Enter your budget", None, -1))
        self.importBudgetAction.setText(QtWidgets.QApplication.translate("AuditMainWindow", "Import Budget", None, -1))
        self.polyCountAction.setText(QtWidgets.QApplication.translate("AuditMainWindow", "Poly Count", None, -1))

