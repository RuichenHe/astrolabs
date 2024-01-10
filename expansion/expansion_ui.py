# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'expansionzOtfOO.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from expansion_scene import ExpansionLabWidget
from demo1 import MyOpenGLWidget


class Ui_ExpansionLab(object):
    def setupUi(self, ExpansionLab):
        if not ExpansionLab.objectName():
            ExpansionLab.setObjectName(u"ExpansionLab")
        ExpansionLab.resize(1024, 600)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExpansionLab.sizePolicy().hasHeightForWidth())
        ExpansionLab.setSizePolicy(sizePolicy)
        ExpansionLab.setMinimumSize(QSize(1024, 600))
        ExpansionLab.setAutoFillBackground(False)
        ExpansionLab.setStyleSheet(u"QWidget{\n"
"  background: black;\n"
"}\n"
"\n"
"QLabel {\n"
"  color: #cfc;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: white;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: #ccc;\n"
"    font: bold 1em;\n"
"    padding: 6px;\n"
"    width: 6em;\n"
"    height: 64px;\n"
"    border-radius: 8px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"    border: 1px solid #5c5c5c;\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    height: 64px;\n"
"    margin: 1px 0;\n"
"    background: #333;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    width: 64px;\n"
"    height: 64px;\n"
"    border-radius: 32px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"    border: 1px solid #5c5c5c;\n"
"}\n"
"")
        self.gridLayout = QGridLayout(ExpansionLab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(1, 1, 1, 0)
        self.exitButton = QPushButton(ExpansionLab)
        self.exitButton.setObjectName(u"exitButton")
        font = QFont()
        font.setFamily(u"FreeSans")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.exitButton.setFont(font)

        self.gridLayout.addWidget(self.exitButton, 3, 1, 1, 1)

        self.resetButton = QPushButton(ExpansionLab)
        self.resetButton.setObjectName(u"resetButton")
        self.resetButton.setFont(font)
        self.resetButton.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icon/clear", QSize(), QIcon.Normal, QIcon.Off)
        self.resetButton.setIcon(icon)
        self.resetButton.setCheckable(False)

        self.gridLayout.addWidget(self.resetButton, 2, 1, 1, 1)

        self.sceneWidget = MyOpenGLWidget(ExpansionLab)
        self.sceneWidget.setObjectName(u"sceneWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sceneWidget.sizePolicy().hasHeightForWidth())
        self.sceneWidget.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.sceneWidget, 0, 0, 1, 3)

        self.buildLabel = QLabel(ExpansionLab)
        self.buildLabel.setObjectName(u"buildLabel")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.buildLabel.setFont(font1)
        self.buildLabel.setStyleSheet(u"QLabel#buildLabel{\n"
"	font: bold 12px;\n"
"	background: #000;\n"
"	color: #ddd;\n"
"}")

        self.gridLayout.addWidget(self.buildLabel, 4, 1, 1, 1)

        self.timeLabel = QLabel(ExpansionLab)
        self.timeLabel.setObjectName(u"timeLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy2)
        self.timeLabel.setMinimumSize(QSize(0, 64))
        font2 = QFont()
        font2.setFamily(u"MathJax_SansSerif")
        font2.setPointSize(16)
        font2.setBold(True)
        font2.setUnderline(False)
        font2.setWeight(75)
        self.timeLabel.setFont(font2)
        self.timeLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.timeLabel, 3, 0, 1, 1)

        self.directionsLabel = QLabel(ExpansionLab)
        self.directionsLabel.setObjectName(u"directionsLabel")
        sizePolicy2.setHeightForWidth(self.directionsLabel.sizePolicy().hasHeightForWidth())
        self.directionsLabel.setSizePolicy(sizePolicy2)
        font3 = QFont()
        font3.setFamily(u"FreeSans")
        font3.setPointSize(32)
        font3.setBold(True)
        font3.setWeight(75)
        self.directionsLabel.setFont(font3)
        self.directionsLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.directionsLabel, 1, 0, 1, 1)

        self.epochSlider = QSlider(ExpansionLab)
        self.epochSlider.setObjectName(u"epochSlider")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.epochSlider.sizePolicy().hasHeightForWidth())
        self.epochSlider.setSizePolicy(sizePolicy3)
        self.epochSlider.setMinimumSize(QSize(128, 64))
        self.epochSlider.setStyleSheet(u"")
        self.epochSlider.setMinimum(-100)
        self.epochSlider.setMaximum(100)
        self.epochSlider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.epochSlider, 2, 0, 1, 1)


        self.retranslateUi(ExpansionLab)

        QMetaObject.connectSlotsByName(ExpansionLab)
    # setupUi

    def retranslateUi(self, ExpansionLab):
        ExpansionLab.setWindowTitle(QCoreApplication.translate("ExpansionLab", u"Form", None))
        self.exitButton.setText(QCoreApplication.translate("ExpansionLab", u"Exit", None))
        self.resetButton.setText(QCoreApplication.translate("ExpansionLab", u"Start Over", None))
        self.buildLabel.setText(QCoreApplication.translate("ExpansionLab", u"Build: ", None))
        self.timeLabel.setText(QCoreApplication.translate("ExpansionLab", u"t = 12.0 Gyr", None))
        self.directionsLabel.setText("")
    # retranslateUi

