# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import ui_MainWindow
import Dashboard



class MainWindow(QMainWindow, ui_MainWindow.Ui_MainWindow):
    NAMEPATH = './names.txt'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.dashboard = Dashboard.Dashboard(self)
        self.setCentralWidget(self.dashboard)


    def startMarquee(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
