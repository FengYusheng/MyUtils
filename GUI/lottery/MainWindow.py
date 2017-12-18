# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui_MainWindow
import Dashboard



class MarqueeThread(QThread):
    NAMEPATH = './names.txt'

    def __init__(self, parent):
        super(MarqueeThread, self).__init__(parent)
        self.parent = parent


    def run(self):
        while True:
            with open(MarqueeThread.NAMEPATH, 'r', encoding='utf-8') as f:
                for _ in f:
                    print(_)



class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    NAMEPATH = './names.txt'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dashboard = Dashboard.Dashboard(self)
        self.setCentralWidget(self.dashboard)

        self.startButton.clicked.connect(self.startMarquee)
        self.stopButton.clicked.connect(self.stopMarquee)


    def startMarquee(self):
        self.dashboard.startTimer()


    def stopMarquee(self):
        self.dashboard.stopTimer()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
