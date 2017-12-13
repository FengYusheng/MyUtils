# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Dashboard(QWidget):
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAutoFillBackground(True)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(0, 0, self.width(), self.height(), Qt.white)
