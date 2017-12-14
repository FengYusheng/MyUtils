# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\project\MayaTools\BevelTool/src/Qt/UI/SimpleOptionsWidget.ui'
#
# Created: Thu Dec 14 18:04:37 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_simpleOptionsWidget(object):
    def setupUi(self, simpleOptionsWidget):
        simpleOptionsWidget.setObjectName("simpleOptionsWidget")
        simpleOptionsWidget.resize(656, 615)
        self.verticalLayout = QtWidgets.QVBoxLayout(simpleOptionsWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bevelButton = QtWidgets.QPushButton(simpleOptionsWidget)
        self.bevelButton.setObjectName("bevelButton")
        self.verticalLayout.addWidget(self.bevelButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.optionGroupBox = QtWidgets.QGroupBox(simpleOptionsWidget)
        self.optionGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.optionGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.optionGroupBox.setFlat(False)
        self.optionGroupBox.setCheckable(False)
        self.optionGroupBox.setObjectName("optionGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.optionGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.fractionLabel = QtWidgets.QLabel(self.optionGroupBox)
        self.fractionLabel.setTextFormat(QtCore.Qt.RichText)
        self.fractionLabel.setObjectName("fractionLabel")
        self.gridLayout.addWidget(self.fractionLabel, 0, 0, 1, 1)
        self.fractionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.optionGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fractionDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.fractionDoubleSpinBox.setSizePolicy(sizePolicy)
        self.fractionDoubleSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.fractionDoubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.fractionDoubleSpinBox.setDecimals(3)
        self.fractionDoubleSpinBox.setMaximum(1.0)
        self.fractionDoubleSpinBox.setSingleStep(0.1)
        self.fractionDoubleSpinBox.setProperty("value", 0.5)
        self.fractionDoubleSpinBox.setObjectName("fractionDoubleSpinBox")
        self.gridLayout.addWidget(self.fractionDoubleSpinBox, 0, 1, 1, 1)
        self.fractionSlider = QtWidgets.QSlider(self.optionGroupBox)
        self.fractionSlider.setMaximum(10)
        self.fractionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.fractionSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.fractionSlider.setTickInterval(0)
        self.fractionSlider.setObjectName("fractionSlider")
        self.gridLayout.addWidget(self.fractionSlider, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.optionGroupBox)
        self.helpGroupBox = QtWidgets.QGroupBox(simpleOptionsWidget)
        self.helpGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.helpGroupBox.setObjectName("helpGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.helpGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.helpTextBrower = QtWidgets.QTextBrowser(self.helpGroupBox)
        self.helpTextBrower.setObjectName("helpTextBrower")
        self.gridLayout_2.addWidget(self.helpTextBrower, 0, 1, 1, 1)
        self.horizontalLayout.addWidget(self.helpGroupBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(simpleOptionsWidget)
        QtCore.QMetaObject.connectSlotsByName(simpleOptionsWidget)

    def retranslateUi(self, simpleOptionsWidget):
        simpleOptionsWidget.setWindowTitle(QtWidgets.QApplication.translate("simpleOptionsWidget", "Form", None, -1))
        self.bevelButton.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "Bevel", None, -1))
        self.optionGroupBox.setTitle(QtWidgets.QApplication.translate("simpleOptionsWidget", "Options", None, -1))
        self.fractionLabel.setText(QtWidgets.QApplication.translate("simpleOptionsWidget", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">fraction</span></p></body></html>", None, -1))
        self.helpGroupBox.setTitle(QtWidgets.QApplication.translate("simpleOptionsWidget", "Quick help", None, -1))

