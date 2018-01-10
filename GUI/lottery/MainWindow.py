# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui_MainWindow
import ui_ControlPanel
import Dashboard
import Utils
import Global



class MarqueeThread(QThread):
    def __init__(self, parent):
        super(MarqueeThread, self).__init__(parent)
        self.parent = parent



class ControlPanel(QWidget, ui_ControlPanel.Ui_controlPanelWidget):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)
        self.parent = parent

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.filePathLineEdit.setText(Global.PLAYERSPATH)

        self.openFileButton.clicked.connect(self.setPlayerPath)


    def setPlayerPath(self):
        pass



class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer = QTimer(self)
        self.interval = 200

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.viewMenu.addAction(self.lotteryDock.toggleViewAction())
        self.dashboard = Dashboard.Dashboard(self)
        self.setCentralWidget(self.dashboard)
        self.controlPanel = ControlPanel(self)
        self.controlDock.setWidget(self.controlPanel)

        self.startButton.clicked.connect(self.startTimer)
        self.stopButton.clicked.connect(self.stopTimer)
        self.timer.timeout.connect(self.marquee)


    def startTimer(self):
        self.timer.start(self.interval)


    def stopTimer(self):
        self.timer.stop()


    def marquee(self):
        self.dashboard.setText()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
