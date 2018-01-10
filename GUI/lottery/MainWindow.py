# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui_MainWindow
import Dashboard
import Utils



class MarqueeThread(QThread):
    def __init__(self, parent):
        super(MarqueeThread, self).__init__(parent)
        self.parent = parent



class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.timer = QTimer(self)
        self.interval = 200

        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dashboard = Dashboard.Dashboard(self)
        self.setCentralWidget(self.dashboard)

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
