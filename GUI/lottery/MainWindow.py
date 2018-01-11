# -*- coding: utf-8 -*-
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui_MainWindow
import ui_ControlPanel
import Dashboard
import Utils



class MarqueeThread(QThread):
    def __init__(self, parent):
        super(MarqueeThread, self).__init__(parent)
        self.parent = parent



class ControlPanelWidget(QWidget, ui_ControlPanel.Ui_ControlPanelWidge):
    def __init__(self, parent):
        super(ControlPanelWidget, self).__init__(parent)

        self.parent = parent

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.openButton.clicked.connect(self.setPlayerPath)


    def setPlayerPath(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setNameFilter('Text files (*.txt)')
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.setDirectory(os.path.normcase(os.path.realpath(os.path.abspath(os.path.dirname(__file__)))))
        if fileDialog.exec_():
            playerPath = fileDialog.selectedFiles()
            if len(playerPath):
                self.parent.setPlayerPath(playerPath[0])
                self.playerPathLineEdit.setText(playerPath[0])


    def deactivateWidgets(self):
        self.playerPathLineEdit.setEnabled(False)
        self.openButton.setEnabled(False)
        self.playerNumberSpinBox.setEnabled(False)
        self.startButton.setEnabled(False)


    def activateWidgets(self):
        self.playerPathLineEdit.setEnabled(True)
        self.openButton.setEnabled(True)
        self.playerNumberSpinBox.setEnabled(True)
        self.startButton.setEnabled(True)



class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer = QTimer(self)
        self.interval = 200
        self._currentPlayer = ''
        self._playerPath = ''
        self._prizewinners = set()
        self._playerNumber = 1

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dashboard = Dashboard.Dashboard(self)
        self.setCentralWidget(self.dashboard)
        self.viewMenu.addAction(self.controlPanelDock.toggleViewAction())
        self.controlPanel = ControlPanelWidget(self)
        self.controlPanelDock.setWidget(self.controlPanel)

        self.timer.timeout.connect(self.marquee)
        self.controlPanel.startButton.clicked.connect(self.startTimer)
        self.controlPanel.stopButton.clicked.connect(self.stopTimer)
        self.controlPanel.playerNumberSpinBox.valueChanged.connect(self.setPlayerNumber)


    def currentPlayer(self):
        return self._currentPlayer


    def startTimer(self):
        self._playerNumber -= 1
        self.clearPrizewinners()
        self.controlPanel.deactivateWidgets()
        self.timer.start(self.interval)


    def stopTimer(self):
        self.timer.stop()
        self._prizewinners.add(self.dashboard.currentPlayer())

        if self._playerNumber > 0:
            self.startTimer()
        else:
            self.controlPanel.activateWidgets()
            print(self._prizewinners)


    def marquee(self):
        self.dashboard.setText()
        # self.stopTimer()
        if self._playerNumber > 0:
            pass


    def setPlayerPath(self, playerPath):
        self._playerPath = playerPath

    
    def playerPath(self):
        return self._playerPath


    def prizewinners(self):
        return self._prizewinners


    def clearPrizewinners(self):
        self._playerNumber > 0 or self._prizewinners.clear()


    def playerGenerator(self):
        return Utils.playerGenerator(self._playerPath, self._prizewinners)


    def playerNumber(self):
        return self._playerNumber


    def setPlayerNumber(self, number):
        self._playerNumber = number




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
