# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class FileDailog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        super(FileDailog, self).__init__(parent)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setNameFilter('All json files (*.json)')
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.setDirectory('D:\source\opensource\FeelUOwn\MyUtils\GUI')
