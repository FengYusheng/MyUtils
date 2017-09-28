# -*- coding: utf-8 -*-

import sys
import os
import csv

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide import __version__
    from shiboken import wrapInstance

import pymel.core as pm

sys.path.insert(0, os.path.dirname(os.path.realpath(os.path.abspath(__file__))))
from ui_polyCountBudget2 import Ui_polyCountBudgetMainWindow
sys.path.remove(os.path.dirname(os.path.realpath(os.path.abspath(__file__))))

MAYA_VERION = pm.mel.eval('getApplicationVersionAsFloat();')



class PolyCountBudgetMainWindow(QMainWindow, Ui_polyCountBudgetMainWindow):
    '''
    TODO:
    Set budget first, then set LOD.
    '''
    def __init__(self, parent=None):
        super(PolyCountBudgetMainWindow, self).__init__(parent)
        self.budgets = None
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.extremelyHighSlider.setEnabled(False)
        self.extremelyHighSpinBox.setEnabled(False)

        self.extremleyLowSlider.valueChanged.connect(self.setExtremelyLowFromSliderToSpinBox)
        self.extremelyLowSpinBox.valueChanged.connect(self.setExtremelyLowFromSpinBoxToSlider)
        self.lowSlider.valueChanged.connect(self.setLowFromSliderToSpinBox)
        self.lowSpinBox.valueChanged.connect(self.setLowFromSpinBoxToSlider)
        self.mediumSlider.valueChanged.connect(self.setMediumFromSliderToSpinBox)
        self.mediumSpinBox.valueChanged.connect(self.setMediumFromSpinBoxToSlider)
        self.highSlider.valueChanged.connect(self.setHighFromSliderToSpinBox)
        self.highSpinBox.valueChanged.connect(self.setHighFromSpinBoxToSlider)
        self.veryHighSlider.valueChanged.connect(self.setVeryHighFromSliderToSpinBox)
        self.veryHighSpinBox.valueChanged.connect(self.setVeryHighFromSpinBoxToSlider)
        self.extremelyHighSlider.valueChanged.connect(self.setExtremelyHighFromSliderToSpinBox)
        self.extremelyHighSpinBox.valueChanged.connect(self.setExtremelyHighFromSpinBoxToSlider)
        self.budgetSlider.valueChanged.connect(self.setBudgetFromSliderToSpinBox)
        self.budgetSpinBox.valueChanged.connect(self.setBudgetFromSpinBoxToSlider)
        self.closeButton.clicked.connect(self.closeWindow)
        self.resetButton.clicked.connect(self.reset)
        self.resetAction.triggered.connect(self.reset)
        self.saveButton.clicked.connect(self.saveBudget)
        self.lodCheckBox.stateChanged.connect(self.setLODEnable)

        self.setLODEnable()


    def _setLowMinimum(self, value):
        self.lowSlider.setValue(value)
        self.lowSpinBox.setValue(value)
        self.lowSpinBox.setMinimum(value)


    def _setMediumMinimum(self, value):
        self.mediumSlider.setValue(value)
        self.mediumSpinBox.setValue(value)
        self.mediumSpinBox.setMinimum(value)


    def _setHighMinimum(self, value):
        self.highSlider.setValue(value)
        self.highSpinBox.setValue(value)
        self.highSpinBox.setMinimum(value)


    def _setVeryHighMinimum(self, value):
        self.veryHighSlider.setValue(value)
        self.veryHighSpinBox.setValue(value)
        self.veryHighSpinBox.setMinimum(value)


    def _setExtremelyHighMinimum(self, value):
        self.extremelyHighSlider.setValue(value)
        self.extremelyHighSpinBox.setValue(value)
        self.extremelyHighSpinBox.setMinimum(value)


    def _setBudgetMinimum(self, value):
        self.budgetSlider.setValue(value)
        self.budgetSpinBox.setValue(value)
        self.budgetSpinBox.setMinimum(value)


    def setExtremelyLowFromSliderToSpinBox(self):
        value = self.extremleyLowSlider.value()
        self.extremelyLowSpinBox.setValue(value)
        if value:
            self._setLowMinimum(value+1)
        else:
            self._setLowMinimum(value)


    def setExtremelyLowFromSpinBoxToSlider(self):
        value = self.extremelyLowSpinBox.value()
        self.extremleyLowSlider.setValue(value)
        if value:
            self._setLowMinimum(value+1)
        else:
            self._setLowMinimum(value)


    def setLowFromSliderToSpinBox(self):
        value = self.lowSlider.value()
        minimum = self.lowSpinBox.minimum()
        if minimum and value >= minimum:
            self.lowSpinBox.setValue(value)
            self._setMediumMinimum(value+1)
        elif not minimum and not value:
            self._setMediumMinimum(value)
        else:
            self._setLowMinimum(minimum)


    def setLowFromSpinBoxToSlider(self):
        value = self.lowSpinBox.value()
        self.lowSlider.setValue(value)
        if value:
            self._setMediumMinimum(value+1)
        else:
            self._setMediumMinimum(value)


    def setMediumFromSliderToSpinBox(self):
        value = self.mediumSlider.value()
        minimum = self.mediumSpinBox.minimum()
        if minimum and value >= minimum:
            self.mediumSpinBox.setValue(value)
            self._setHighMinimum(value+1)
        elif not minimum and not value:
            self._setHighMinimum(value)
        else:
            self._setMediumMinimum(minimum)


    def setMediumFromSpinBoxToSlider(self):
        value = self.mediumSpinBox.value()
        self.mediumSlider.setValue(value)
        if value:
            self._setHighMinimum(value+1)
        else:
            self._setHighMinimum(value)


    def setHighFromSliderToSpinBox(self):
        value = self.highSlider.value()
        minimum = self.highSpinBox.minimum()
        if minimum and value >= minimum:
            self.highSpinBox.setValue(value)
            self._setVeryHighMinimum(value+1)
        elif not minimum and not value:
            self._setVeryHighMinimum(value)
        else:
            self._setHighMinimum(minimum)


    def setHighFromSpinBoxToSlider(self):
        value = self.highSpinBox.value()
        self.highSlider.setValue(value)
        if value:
            self._setVeryHighMinimum(value+1)
        else:
            self._setVeryHighMinimum(value)


    def setVeryHighFromSliderToSpinBox(self):
        value = self.veryHighSlider.value()
        minimum = self.veryHighSpinBox.minimum()
        if minimum and value >= minimum:
            self.veryHighSpinBox.setValue(value)
            self._setExtremelyHighMinimum(value+1)
            self._setBudgetMinimum(value+2)
        elif not minimum and not value:
            self._setExtremelyHighMinimum(value)
            self._setBudgetMinimum(value)
        else:
            self._setVeryHighMinimum(minimum)


    def setVeryHighFromSpinBoxToSlider(self):
        value = self.veryHighSpinBox.value()
        self.veryHighSlider.setValue(value)
        if value:
            self._setExtremelyHighMinimum(value+1)
            self._setBudgetMinimum(value+2)
        else:
            self._setExtremelyHighMinimum(value)
            self._setBudgetMinimum(value)


    def setExtremelyHighFromSliderToSpinBox(self):
        value = self.extremelyHighSlider.value()
        self.extremelyHighSpinBox.setValue(value)


    def setExtremelyHighFromSpinBoxToSlider(self):
        value = self.extremelyHighSpinBox.value()
        self.extremelyHighSlider.setValue(value)


    def setBudgetFromSliderToSpinBox(self):
        minimum = self.budgetSpinBox.minimum()
        value = self.budgetSlider.value()
        if value >= minimum:
            self.budgetSpinBox.setValue(value)
        else:
            self.budgetSlider.setValue(minimum)


    def setBudgetFromSpinBoxToSlider(self):
        value = self.budgetSpinBox.value()
        self.budgetSlider.setValue(value)


    def setLODEnable(self):
        if self.lodCheckBox.isChecked():
            self.extremleyLowSlider.setEnabled(True)
            self.extremelyLowSpinBox.setEnabled(True)
            self.lowSlider.setEnabled(True)
            self.lowSpinBox.setEnabled(True)
            self.mediumSlider.setEnabled(True)
            self.mediumSpinBox.setEnabled(True)
            self.highSlider.setEnabled(True)
            self.highSpinBox.setEnabled(True)
            self.veryHighSlider.setEnabled(True)
            self.veryHighSpinBox.setEnabled(True)
        else:
            self.extremleyLowSlider.setValue(0)
            self.extremleyLowSlider.setEnabled(False)
            self.extremelyLowSpinBox.setEnabled(False)
            self.lowSlider.setEnabled(False)
            self.lowSpinBox.setEnabled(False)
            self.mediumSlider.setEnabled(False)
            self.mediumSpinBox.setEnabled(False)
            self.highSlider.setEnabled(False)
            self.highSpinBox.setEnabled(False)
            self.veryHighSlider.setEnabled(False)
            self.veryHighSpinBox.setEnabled(False)


    def saveBudget(self):
        def _writeDataToCSV(csvfile, data, encoding='utf-8'):
            writer = csv.writer(csvfile, dialect=csv.excel)
            for row in data:
                writer.writerow([str(s).encode(encoding) for s in row])

        current_dir = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
        desination = pm.fileDialog2(cap='Save', ds=2, fm=0, dir=current_dir, okc='Save', ff='All CSV Files (*.csv)')
        if desination is not None:
            self.budgets = [('LOD', 'From', 'TO', 'Tris/Verts')] * 7
            budget_type = 'Tris' if self.trisRadioButton.isChecked() else 'Verts'
            if self.lodCheckBox.isChecked():
                extremely_low = self.extremleyLowSlider.value()
                self.budgets[0] = ('Extremely Low', 0, extremely_low, budget_type)
                low = self.lowSlider.value()
                self.budgets[1] = ('Low', extremely_low+1, low, budget_type)
                medium = self.mediumSlider.value()
                self.budgets[2] = ('Medium', low+1, medium, budget_type)
                high = self.highSlider.value()
                self.budgets[3] = ('High', medium+1, high, budget_type)
                very_high = self.veryHighSlider.value()
                self.budgets[4] = ('Very High', high+1, very_high, budget_type)
                extremely_high = self.extremelyHighSlider.value()
                budget = self.budgetSlider.value()
                self.budgets[5] = ('Extremely High', very_high+1, budget, budget_type)
                self.budgets[6] = ('Budget', budget, budget, budget_type)
            else:
                self.budgets = [('LOD', 'From', 'TO', 'Tris/Verts')]
                budget = self.budgetSlider.value()
                self.budgets[0] = ('Budget', budget, budget, budget_type)

            type = desination[0].rpartition('.')[2]
            if 'csv' == type:
                with open(desination[0], 'wb') as csvfile:
                    _writeDataToCSV(csvfile, self.budgets)
            elif 'json' == type:
                pass
            else:
                pass


    def closeWindow(self):
        self.close()


    def reset(self):
        self.extremleyLowSlider.setValue(0)
        self.budgetSlider.setValue(0)



if __name__ == '__main__':
    window = PolyCountBudgetMainWindow()
    window.show()
