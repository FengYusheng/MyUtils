# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from ui_pm_view import Ui_PM_View

class MainWindow(QtWidgets.QMainWindow, Ui_PM_View):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
