# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\private_work\p4KuaiSync\MyUtils\maya_script\BevelTool/src/Qt/UI/SimpleOptionsWidget.ui'
#
# Created: Thu Feb 08 13:23:10 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_simpleOptionsWidget(object):
    def setupUi(self, simpleOptionsWidget):
        simpleOptionsWidget.setObjectName("simpleOptionsWidget")
        simpleOptionsWidget.resize(656, 615)
        self.gridLayout_3 = QtWidgets.QGridLayout(simpleOptionsWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.bevelButton = QtWidgets.QPushButton(simpleOptionsWidget)
        self.bevelButton.setObjectName("bevelButton")
        self.gridLayout_3.addWidget(self.bevelButton, 0, 0, 1, 1)
        self.optionGroupBox = QtWidgets.QGroupBox(simpleOptionsWidget)
        self.optionGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.optionGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.optionGroupBox.setFlat(False)
        self.optionGroupBox.setCheckable(False)
        self.optionGroupBox.setObjectName("optionGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.optionGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.segmentsSpinBox = QtWidgets.QSpinBox(self.optionGroupBox)
        self.segmentsSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.segmentsSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.segmentsSpinBox.setMinimum(1)
        self.segmentsSpinBox.setMaximum(12)
        self.segmentsSpinBox.setProperty("value", 1)
        self.segmentsSpinBox.setObjectName("segmentsSpinBox")
        self.gridLayout.addWidget(self.segmentsSpinBox, 1, 1, 1, 2)
        self.segmentsLabel = QtWidgets.QLabel(self.optionGroupBox)
        self.segmentsLabel.setObjectName("segmentsLabel")
        self.gridLayout.addWidget(self.segmentsLabel, 1, 0, 1, 1)
        self.segmentsSlider = QtWidgets.QSlider(self.optionGroupBox)
        self.segmentsSlider.setMinimum(1)
        self.segmentsSlider.setMaximum(12)
        self.segmentsSlider.setOrientation(QtCore.Qt.Horizontal)
        self.segmentsSlider.setObjectName("segmentsSlider")
        self.gridLayout.addWidget(self.segmentsSlider, 1, 3, 1, 1)
        self.miteringLabel = QtWidgets.QLabel(self.optionGroupBox)
        self.miteringLabel.setObjectName("miteringLabel")
        self.gridLayout.addWidget(self.miteringLabel, 2, 0, 1, 1)
        self.fractionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.optionGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fractionDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.fractionDoubleSpinBox.setSizePolicy(sizePolicy)
        self.fractionDoubleSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.fractionDoubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.fractionDoubleSpinBox.setDecimals(3)
        self.fractionDoubleSpinBox.setMinimum(0.001)
        self.fractionDoubleSpinBox.setMaximum(1.0)
        self.fractionDoubleSpinBox.setSingleStep(0.001)
        self.fractionDoubleSpinBox.setProperty("value", 0.5)
        self.fractionDoubleSpinBox.setObjectName("fractionDoubleSpinBox")
        self.gridLayout.addWidget(self.fractionDoubleSpinBox, 0, 1, 1, 2)
        self.fractionSlider = QtWidgets.QSlider(self.optionGroupBox)
        self.fractionSlider.setMinimum(1)
        self.fractionSlider.setMaximum(1000)
        self.fractionSlider.setProperty("value", 500)
        self.fractionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fractionSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.fractionSlider.setTickInterval(0)
        self.fractionSlider.setObjectName("fractionSlider")
        self.gridLayout.addWidget(self.fractionSlider, 0, 3, 1, 1)
        self.fractionLabel = QtWidgets.QLabel(self.optionGroupBox)
        self.fractionLabel.setTextFormat(QtCore.Qt.RichText)
        self.fractionLabel.setObjectName("fractionLabel")
        self.gridLayout.addWidget(self.fractionLabel, 0, 0, 1, 1)
        self.miterAlongLabel = QtWidgets.QLabel(self.optionGroupBox)
        self.miterAlongLabel.setObjectName("miterAlongLabel")
        self.gridLayout.addWidget(self.miterAlongLabel, 3, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(227, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(227, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.miterAlongComboBox = QtWidgets.QComboBox(self.optionGroupBox)
        self.miterAlongComboBox.setObjectName("miterAlongComboBox")
        self.miterAlongComboBox.addItem("")
        self.miterAlongComboBox.addItem("")
        self.miterAlongComboBox.addItem("")
        self.miterAlongComboBox.addItem("")
        self.gridLayout.addWidget(self.miterAlongComboBox, 3, 2, 1, 1)
        self.miteringComboBox = QtWidgets.QComboBox(self.optionGroupBox)
        self.miteringComboBox.setObjectName("miteringComboBox")
        self.miteringComboBox.addItem("")
        self.miteringComboBox.addItem("")
        self.miteringComboBox.addItem("")
        self.miteringComboBox.addItem("")
        self.miteringComboBox.addItem("")
        self.gridLayout.addWidget(self.miteringComboBox, 2, 2, 1, 1)
        self.bevelMemberEdgesButton = QtWidgets.QPushButton(self.optionGroupBox)
        self.bevelMemberEdgesButton.setObjectName("bevelMemberEdgesButton")
        self.gridLayout.addWidget(self.bevelMemberEdgesButton, 4, 0, 1, 4)
        self.gridLayout_3.addWidget(self.optionGroupBox, 1, 0, 1, 1)
        self.helpTabWidget = QtWidgets.QTabWidget(simpleOptionsWidget)
        self.helpTabWidget.setObjectName("helpTabWidget")
        self.helpTab = QtWidgets.QWidget()
        self.helpTab.setObjectName("helpTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.helpTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.helpTextBrower = QtWidgets.QTextBrowser(self.helpTab)
        self.helpTextBrower.setObjectName("helpTextBrower")
        self.gridLayout_2.addWidget(self.helpTextBrower, 0, 0, 1, 1)
        self.helpTabWidget.addTab(self.helpTab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.helpTabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.helpTabWidget, 1, 1, 1, 1)

        self.retranslateUi(simpleOptionsWidget)
        self.helpTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(simpleOptionsWidget)

    def retranslateUi(self, simpleOptionsWidget):
        simpleOptionsWidget.setWindowTitle(QtWidgets.QApplication.translate("simpleOptionsWidget", "Form", None, -1))
        self.bevelButton.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "Bevel", None, -1))
        self.optionGroupBox.setTitle(QtWidgets.QApplication.translate("simpleOptionsWidget", "Options", None, -1))
        self.segmentsLabel.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Segments</span></p></body></html>", None, -1))
        self.miteringLabel.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Mitering</span></p></body></html>", None, -1))
        self.fractionLabel.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Fraction</span></p></body></html>", None, -1))
        self.miterAlongLabel.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Miter Along</span></p></body></html>", None, -1))
        self.miterAlongComboBox.setItemText(0, QtWidgets.QApplication.translate("simpleOptionsWidget", "Auto", None, -1))
        self.miterAlongComboBox.setItemText(1, QtWidgets.QApplication.translate("simpleOptionsWidget", "Center", None, -1))
        self.miterAlongComboBox.setItemText(2, QtWidgets.QApplication.translate("simpleOptionsWidget", "Edge", None, -1))
        self.miterAlongComboBox.setItemText(3, QtWidgets.QApplication.translate("simpleOptionsWidget", "Hard edge", None, -1))
        self.miteringComboBox.setItemText(0, QtWidgets.QApplication.translate("simpleOptionsWidget", "Auto", None, -1))
        self.miteringComboBox.setItemText(1, QtWidgets.QApplication.translate("simpleOptionsWidget", "Uniform", None, -1))
        self.miteringComboBox.setItemText(2, QtWidgets.QApplication.translate("simpleOptionsWidget", "Patch", None, -1))
        self.miteringComboBox.setItemText(3, QtWidgets.QApplication.translate("simpleOptionsWidget", "Radial", None, -1))
        self.miteringComboBox.setItemText(4, QtWidgets.QApplication.translate("simpleOptionsWidget", "None", None, -1))
        self.bevelMemberEdgesButton.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "Bevel member edges", None, -1))
        self.helpTabWidget.setTabText(self.helpTabWidget.indexOf(self.helpTab), QtWidgets.QApplication.translate("simpleOptionsWidget", "Quick help", None, -1))
        self.helpTabWidget.setTabText(self.helpTabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("simpleOptionsWidget", "Tab 2", None, -1))

