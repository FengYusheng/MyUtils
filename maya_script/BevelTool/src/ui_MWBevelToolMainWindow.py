# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/MWBevelToolMainWindow_io.ui'
#
# Created: Wed Mar 21 15:22:34 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MWBevelToolMainWindow(object):
    def setupUi(self, MWBevelToolMainWindow):
        MWBevelToolMainWindow.setObjectName("MWBevelToolMainWindow")
        MWBevelToolMainWindow.resize(935, 817)
        self.centralwidget = QtWidgets.QWidget(MWBevelToolMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.bevelSetTreeView = QtWidgets.QTreeView(self.splitter)
        self.bevelSetTreeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.bevelSetTreeView.setTextElideMode(QtCore.Qt.ElideNone)
        self.bevelSetTreeView.setIndentation(0)
        self.bevelSetTreeView.setWordWrap(False)
        self.bevelSetTreeView.setObjectName("bevelSetTreeView")
        self.bevelSetTreeView.header().setMinimumSectionSize(50)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        MWBevelToolMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MWBevelToolMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 21))
        self.menubar.setObjectName("menubar")
        self.editMenu = QtWidgets.QMenu(self.menubar)
        self.editMenu.setObjectName("editMenu")
        self.viewMenu = QtWidgets.QMenu(self.menubar)
        self.viewMenu.setObjectName("viewMenu")
        MWBevelToolMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MWBevelToolMainWindow)
        self.statusbar.setObjectName("statusbar")
        MWBevelToolMainWindow.setStatusBar(self.statusbar)
        self.bevelSetDock = QtWidgets.QDockWidget(MWBevelToolMainWindow)
        self.bevelSetDock.setMinimumSize(QtCore.QSize(280, 256))
        self.bevelSetDock.setObjectName("bevelSetDock")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bevelSetLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.bevelSetLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bevelSetLabel.setObjectName("bevelSetLabel")
        self.verticalLayout_2.addWidget(self.bevelSetLabel)
        self.bevelSetGroupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.bevelSetGroupBox.setTitle("")
        self.bevelSetGroupBox.setFlat(True)
        self.bevelSetGroupBox.setObjectName("bevelSetGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.bevelSetGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.createBevelSetButton = QtWidgets.QPushButton(self.bevelSetGroupBox)
        self.createBevelSetButton.setEnabled(False)
        self.createBevelSetButton.setObjectName("createBevelSetButton")
        self.verticalLayout.addWidget(self.createBevelSetButton)
        self.addButton = QtWidgets.QPushButton(self.bevelSetGroupBox)
        self.addButton.setEnabled(False)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtWidgets.QPushButton(self.bevelSetGroupBox)
        self.removeButton.setEnabled(False)
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout.addWidget(self.removeButton)
        self.deleteButton = QtWidgets.QPushButton(self.bevelSetGroupBox)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.verticalLayout_2.addWidget(self.bevelSetGroupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 542, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.bevelSetDock.setWidget(self.dockWidgetContents)
        MWBevelToolMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.bevelSetDock)
        self.selectionConstraintDock = QtWidgets.QDockWidget(MWBevelToolMainWindow)
        self.selectionConstraintDock.setMinimumSize(QtCore.QSize(280, 508))
        self.selectionConstraintDock.setObjectName("selectionConstraintDock")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.selectionLabel = QtWidgets.QLabel(self.dockWidgetContents_2)
        self.selectionLabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.selectionLabel.setObjectName("selectionLabel")
        self.verticalLayout_4.addWidget(self.selectionLabel)
        self.selectionConstraintGroupBox = QtWidgets.QGroupBox(self.dockWidgetContents_2)
        self.selectionConstraintGroupBox.setTitle("")
        self.selectionConstraintGroupBox.setFlat(True)
        self.selectionConstraintGroupBox.setObjectName("selectionConstraintGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.selectionConstraintGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.selectHardEdgesButton = QtWidgets.QPushButton(self.selectionConstraintGroupBox)
        self.selectHardEdgesButton.setObjectName("selectHardEdgesButton")
        self.verticalLayout_3.addWidget(self.selectHardEdgesButton)
        self.selectSoftEdgesButton = QtWidgets.QPushButton(self.selectionConstraintGroupBox)
        self.selectSoftEdgesButton.setObjectName("selectSoftEdgesButton")
        self.verticalLayout_3.addWidget(self.selectSoftEdgesButton)
        self.smoothingAngleCheckBox = QtWidgets.QCheckBox(self.selectionConstraintGroupBox)
        self.smoothingAngleCheckBox.setObjectName("smoothingAngleCheckBox")
        self.verticalLayout_3.addWidget(self.smoothingAngleCheckBox)
        self.smoothingAngleSlider = QtWidgets.QSlider(self.selectionConstraintGroupBox)
        self.smoothingAngleSlider.setEnabled(False)
        self.smoothingAngleSlider.setMaximum(1800000)
        self.smoothingAngleSlider.setProperty("value", 300000)
        self.smoothingAngleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.smoothingAngleSlider.setObjectName("smoothingAngleSlider")
        self.verticalLayout_3.addWidget(self.smoothingAngleSlider)
        self.smoothingAngleSpinBox = QtWidgets.QDoubleSpinBox(self.selectionConstraintGroupBox)
        self.smoothingAngleSpinBox.setEnabled(False)
        self.smoothingAngleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.smoothingAngleSpinBox.setDecimals(4)
        self.smoothingAngleSpinBox.setMaximum(180.0)
        self.smoothingAngleSpinBox.setProperty("value", 30.0)
        self.smoothingAngleSpinBox.setObjectName("smoothingAngleSpinBox")
        self.verticalLayout_3.addWidget(self.smoothingAngleSpinBox)
        self.verticalLayout_4.addWidget(self.selectionConstraintGroupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 289, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.selectionConstraintDock.setWidget(self.dockWidgetContents_2)
        MWBevelToolMainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.selectionConstraintDock)
        self.finishBevelAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.finishBevelAction.setObjectName("finishBevelAction")
        self.displayDrawOverrideAttrAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.displayDrawOverrideAttrAction.setObjectName("displayDrawOverrideAttrAction")
        self.actionCreate_a_Bevel_Set = QtWidgets.QAction(MWBevelToolMainWindow)
        self.actionCreate_a_Bevel_Set.setObjectName("actionCreate_a_Bevel_Set")
        self.actionMove_Edges_into_New_Bevel_Set = QtWidgets.QAction(MWBevelToolMainWindow)
        self.actionMove_Edges_into_New_Bevel_Set.setObjectName("actionMove_Edges_into_New_Bevel_Set")
        self.actionCreate = QtWidgets.QAction(MWBevelToolMainWindow)
        self.actionCreate.setObjectName("actionCreate")
        self.moveAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.moveAction.setCheckable(True)
        self.moveAction.setObjectName("moveAction")
        self.maintainAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.maintainAction.setCheckable(True)
        self.maintainAction.setObjectName("maintainAction")
        self.chooseAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.chooseAction.setCheckable(True)
        self.chooseAction.setChecked(True)
        self.chooseAction.setObjectName("chooseAction")
        self.displayOverrideAction = QtWidgets.QAction(MWBevelToolMainWindow)
        self.displayOverrideAction.setObjectName("displayOverrideAction")
        self.editMenu.addAction(self.displayOverrideAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.moveAction)
        self.editMenu.addAction(self.maintainAction)
        self.editMenu.addAction(self.chooseAction)
        self.menubar.addAction(self.editMenu.menuAction())
        self.menubar.addAction(self.viewMenu.menuAction())

        self.retranslateUi(MWBevelToolMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MWBevelToolMainWindow)

    def retranslateUi(self, MWBevelToolMainWindow):
        MWBevelToolMainWindow.setWindowTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Mindwalk Bevel Tool", None, -1))
        self.editMenu.setTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Edit", None, -1))
        self.viewMenu.setTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "View", None, -1))
        self.bevelSetDock.setWindowTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Bevel Set Box", None, -1))
        self.bevelSetLabel.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Bevel Set</span></p></body></html>", None, -1))
        self.createBevelSetButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "New", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Add", None, -1))
        self.removeButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Remove", None, -1))
        self.deleteButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Delete", None, -1))
        self.selectionConstraintDock.setWindowTitle(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Selection Constraint Box", None, -1))
        self.selectionLabel.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Select Soft/Hard Edge</span></p></body></html>", None, -1))
        self.selectHardEdgesButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Select Hard Edges", None, -1))
        self.selectSoftEdgesButton.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Select Soft Edges", None, -1))
        self.smoothingAngleCheckBox.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Smoothing angle", None, -1))
        self.finishBevelAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Finish Bevel", None, -1))
        self.displayDrawOverrideAttrAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Display DrawOverrideAttributes", None, -1))
        self.actionCreate_a_Bevel_Set.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Create a Bevel Set", None, -1))
        self.actionMove_Edges_into_New_Bevel_Set.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Move Edges into New Bevel Set", None, -1))
        self.actionCreate.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Create", None, -1))
        self.moveAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Move Edges into Target Bevel Set", None, -1))
        self.maintainAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Maintain Present Status", None, -1))
        self.chooseAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Let User Choose", None, -1))
        self.displayOverrideAction.setText(QtWidgets.QApplication.translate("MWBevelToolMainWindow", "Draw Override", None, -1))

