# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


from myLittleTimer import Ui_myLitteTimer

class Worker(QThread):
    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)


    def run(self):
        print('{0} starts to work.'.format(self.currentThread()))
        self.sleep(3)


class MyTimer(QMainWindow, Ui_myLitteTimer):
    def __init__(self, parent=None):
        super(MyTimer, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.timer = QTimer(self)
        self.worker = Worker()
        self.tray = None
        self.interval = 2000 # 1 min
        self.progressBar.setMaximum(60)
        self.createTray()

        self.timer.timeout.connect(self.updateDateTime)
        self.worker.finished.connect(self.finishWork)


    def createAction(self):
        pass


    def createTray(self):
        menu = QMenu(self)
        restoreAction = QAction(self)
        menu.addAction(restoreAction)
        self.tray = QSystemTrayIcon(self)
        self.tray.setContextMenu(menu)
        self.tray.show()


    def updateDateTime(self):
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        value = self.progressBar.value() + 2
        self.progressBar.setValue(value)

        if value > 60:
            self.timer.stop()
            self.startWork()


    def finishWork(self):
        if self.worker.isFinished():
            # deleteLater is helpful.
            # self.worker.deleteLater()
            self.progressBar.setMaximum(60)
            self.timer.start(self.interval)


    def startWork(self):
        self.worker.start()
        self.progressBar.setValue(0)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = MyTimer()
    timer.show()
    timer.startWork()
    sys.exit(app.exec_())
