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

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width()/2, self.height()/2)
        painter.setPen(QPen(QBrush(Qt.darkGray), 3, Qt.SolidLine, Qt.RoundCap, Qt.BevelJoin))

        painter.drawText(0, 0, '你的名字！')
        painter.restore()
