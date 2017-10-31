# -*- coding: utf-8 -*-
import os
import re

try:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2 import __version__ as pyside_version
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance


def checkExternalFilePathWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check external file path']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkNgonsWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check n-gons']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkOverlappingVerticesWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check overlapping vertices']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkTransformationsWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check transformations']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkIntermediateNodeWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check intermediate node']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkPolyCountWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    verts_la = QLabel(scrollAreaWidgetContents)
    verts_la.setTextFormat(Qt.RichText)
    verts_la.setText(u'<b><span style="font-size:10pt">Verts count: &nbsp;</span></b>')
    verts_le = QLineEdit(scrollAreaWidgetContents)
    verts_le.setText(parent.data[u'details'][u'check poly count']['Verts'])
    verts_le.setValidator(QIntValidator(verts_le))
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(verts_la)
    horiLayout.addWidget(verts_le)
    vertLayout.addLayout(horiLayout)

    edges_la = QLabel(scrollAreaWidgetContents)
    edges_la.setTextFormat(Qt.RichText)
    edges_la.setText(u'<b><span style="font-size:10pt">Edges count: </span></b>')
    edges_le = QLineEdit(scrollAreaWidgetContents)
    edges_le.setText(parent.data[u'details'][u'check poly count']['Edges'])
    edges_le.setValidator(QIntValidator(edges_le))
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(edges_la)
    horiLayout.addWidget(edges_le)
    vertLayout.addLayout(horiLayout)

    faces_la = QLabel(scrollAreaWidgetContents)
    faces_la.setTextFormat(Qt.RichText)
    faces_la.setText(u'<b><span style="font-size:10pt">Faces count: &nbsp;</span></b>')
    faces_le = QLineEdit(scrollAreaWidgetContents)
    faces_le.setText(parent.data[u'details'][u'check poly count']['Faces'])
    faces_le.setValidator(QIntValidator(faces_le))
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(faces_la)
    horiLayout.addWidget(faces_le)
    vertLayout.addLayout(horiLayout)

    tris_la = QLabel(scrollAreaWidgetContents)
    tris_la.setTextFormat(Qt.RichText)
    tris_la.setText(u'<b><span style="font-size:10pt">Tris count: &nbsp;&nbsp;&nbsp;&nbsp;</span></b>')
    tris_le = QLineEdit(scrollAreaWidgetContents)
    tris_le.setText(parent.data[u'details'][u'check poly count']['Tris'])
    tris_le.setValidator(QIntValidator(tris_le))
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(tris_la)
    horiLayout.addWidget(tris_le)
    vertLayout.addLayout(horiLayout)

    UVs_la = QLabel(scrollAreaWidgetContents)
    UVs_la.setTextFormat(Qt.RichText)
    UVs_la.setText(u'<b><span style="font-size:10pt">UVs count: &nbsp;&nbsp;&nbsp;</span></b>')
    UVs_le = QLineEdit(scrollAreaWidgetContents)
    UVs_le.setText(parent.data[u'details'][u'check poly count']['UVs'])
    UVs_le.setValidator(QIntValidator(UVs_le))
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(UVs_la)
    horiLayout.addWidget(UVs_le)
    vertLayout.addLayout(horiLayout)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check poly count']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    def _getVertsCount():
        parent.data[u'details'][u'check poly count'][u'Verts'] = verts_le.text()

    def _getEdgesCount():
        parent.data[u'details'][u'check poly count'][u'Edges'] = edges_le.text()

    def _getFacesCount():
        parent.data[u'details'][u'check poly count'][u'Faces'] = faces_le.text()

    def _getTrisCount():
        parent.data[u'details'][u'check poly count'][u'Tris'] = tris_le.text()

    def _getUVsCount():
        parent.data[u'details'][u'check poly count'][u'UVs'] = UVs_le.text()

    verts_le.textChanged.connect(_getVertsCount)
    edges_le.textChanged.connect(_getEdgesCount)
    faces_le.textChanged.connect(_getFacesCount)
    tris_le.textChanged.connect(_getTrisCount)
    UVs_le.textChanged.connect(_getUVsCount)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkLaminaFacesWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check lamina faces']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)


def checkShaderNameWidget(parent):
    scrollAreaWidgetContents = QWidget()
    scrollAreaWidgetContents.setGeometry(0, 0, 378, 472)
    scrollAreaWidgetContents.setAttribute(Qt.WA_DeleteOnClose, True)
    vertLayout = QVBoxLayout(scrollAreaWidgetContents)

    tipLabel = QLabel(scrollAreaWidgetContents)
    tipLabel.setTextFormat(Qt.RichText)
    tipLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
    tipLabel.setText(u'<b><span style="font-size:10pt">whatsThis</span></b>')
    tipTextEdit = QTextEdit(scrollAreaWidgetContents)

    tipTextEdit.setHtml(u"""<b>
            <span style="font-size:8pt">
            {0}
            </span>
            </b>"""\
            .format(parent.template[u'whatsThis'][u'check shader names']))

    tipTextEdit.setReadOnly(True)

    vertLayout.addWidget(tipLabel)
    vertLayout.addWidget(tipTextEdit)

    easyRadioButton = QRadioButton(u'Easy', scrollAreaWidgetContents)
    easyRadioButton.setObjectName(u'easyRadioButton')
    easyRadioButton.setChecked(True)
    reRadioButton = QRadioButton(u'Regular expression', scrollAreaWidgetContents)
    reRadioButton.setObjectName(u'reRadioButton')
    buttonGroup = QButtonGroup(scrollAreaWidgetContents)
    buttonGroup.addButton(easyRadioButton)
    buttonGroup.addButton(reRadioButton)
    horiLayout = QHBoxLayout(parent)
    horiLayout.addWidget(easyRadioButton)
    horiLayout.addWidget(reRadioButton)
    vertLayout.addLayout(horiLayout)

    prefix_le = QLineEdit(scrollAreaWidgetContents)
    prefix_la = QLabel(scrollAreaWidgetContents)
    prefix_la.setText(u'<b><span style="font-size:8pt">prefix:  </span></b>')
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(prefix_la)
    horiLayout.addWidget(prefix_le)

    postfix_la = QLabel(scrollAreaWidgetContents)
    postfix_la.setText(u'<b><span style="font-size:8pt">postfix: </span></b>')
    postfix_le = QLineEdit(scrollAreaWidgetContents)
    horiLayout.addWidget(postfix_la)
    horiLayout.addWidget(postfix_le)
    vertLayout.addLayout(horiLayout)

    addButton = QPushButton(scrollAreaWidgetContents)
    addButton.setText(u'Add Prefix And Postfix')
    resetButton = QPushButton(scrollAreaWidgetContents)
    resetButton.setText(u'Reset')
    horiLayout = QHBoxLayout(scrollAreaWidgetContents)
    horiLayout.addWidget(addButton)
    horiLayout.addWidget(resetButton)
    vertLayout.addLayout(horiLayout)

    preview_la = QLabel(scrollAreaWidgetContents)
    preview_la.setTextFormat(Qt.RichText)
    preview_la.setFrameStyle(QFrame.StyledPanel|QFrame.Plain)
    preview_la.setText(u'<b><span style="font-size:10pt">Preview</span></b>')
    vertLayout.addWidget(preview_la)

    formatTextEdit = QTextEdit(scrollAreaWidgetContents)
    data = parent.data[u'details'][u'check shader names']
    not len(data) or formatTextEdit.setPlainText(u'\n'.join(data)+u'\n')
    formatTextEdit.setReadOnly(True)
    vertLayout.addWidget(formatTextEdit)

    def _addPrefixPostfix():
        prefix = prefix_le.text()
        postfix = postfix_le.text()
        if prefix != '' or postfix != '':
            preview = formatTextEdit.toPlainText()
            another = prefix + u'<SHADER>' + postfix + u'\n'
            another in preview or formatTextEdit.setPlainText(preview + another)

    addButton.clicked.connect(_addPrefixPostfix)

    def _reset():
        prefix_le.clear()
        postfix_le.clear()
        formatTextEdit.clear()
        preview_la.setText(u'<b><span style="font-size:10pt">Preview</span></b>')

    resetButton.clicked.connect(_reset)

    def _switchMode():
        if reRadioButton.isChecked():
            prefix_le.setEnabled(False)
            postfix_le.setEnabled(False)
            addButton.setEnabled(False)
            resetButton.setEnabled(False)
            preview_la.setText(u'<b><span style="font-size:10pt">Enter your regular expression:</span></b>')
            formatTextEdit.clear()
            formatTextEdit.setReadOnly(False)
        else:
            prefix_le.setEnabled(True)
            postfix_le.setEnabled(True)
            addButton.setEnabled(True)
            resetButton.setEnabled(True)
            preview_la.setText(u'<b><span style="font-size:10pt">Preview</span></b>')
            formatTextEdit.clear()
            formatTextEdit.setReadOnly(True)

    buttonGroup.buttonClicked.connect(_switchMode)

    def _getNamePrototype():
        fmt = formatTextEdit.toPlainText()
        parent.data[u'details'][u'check shader names'] = fmt.split(u'\n')[0:-1]\
                                                    if easyRadioButton.isChecked() \
                                                    else [fmt]

    formatTextEdit.textChanged.connect(_getNamePrototype)

    def _previewNamePrototype():
        text = u'Preview: ' + prefix_le.text() + u'&#60;SHADER&#62;' + postfix_le.text()
        preview_la.setText(u'<b><span style="font-size:10pt">{0}</span></b>'.format(text))

    prefix_le.textEdited.connect(_previewNamePrototype)
    postfix_le.textEdited.connect(_previewNamePrototype)

    parent.scrollArea.setWidget(scrollAreaWidgetContents)
