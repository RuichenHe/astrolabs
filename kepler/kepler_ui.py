# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'keplerZryNeR.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from demo1 import OpenGLWidget as KeplerScene
# from kepler.kepler_scene_graph import KeplerScene


class Ui_KeplerLab(object):
    def setupUi(self, KeplerLab):
        if not KeplerLab.objectName():
            KeplerLab.setObjectName(u"KeplerLab")
        KeplerLab.resize(1024, 858)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeplerLab.sizePolicy().hasHeightForWidth())
        KeplerLab.setSizePolicy(sizePolicy)
        KeplerLab.setMinimumSize(QSize(0, 0))
        KeplerLab.setStyleSheet(u"QWidget{\n"
"  background: #000;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 3.0em;\n"
"    padding: 6px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
"/*    border: 1px solid #5c5c5c; */\n"
"   border: 2px solid #000;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QPushButton#velocityMinusButton, QPushButton#velocityPlusButton,\n"
"QPushButton#angleMinusButton, QPushButton#anglePlusButton{\n"
"  color: #f00;\n"
"  background: #000;\n"
"  border: 0px;\n"
"}\n"
"\n"
"QPushButton::checked{\n"
"  border: 2px  solid #5c5c5c;\n"
"  background: #8f8f8f;\n"
"}\n"
"\n"
"QLabel, QDoubleSpinBox{\n"
" color: #f00;\n"
"}\n"
"\n"
"QPushButton::disabled{\n"
"  border: 0px;\n"
"}\n"
"\n"
"\n"
"QPushButton#velocityMinusButton::disabled, \n"
"QPushButton#velocityPlusButton::disabled,\n"
"QPushButton#angleMinusButton::disabled, \n"
"QPushButton#anglePlusButton::dis"
                        "abled{\n"
"  color: #000;\n"
"  background: #000;\n"
"  border: 0px;\n"
"}\n"
"\n"
"\n"
"")
        self.horizontalLayout = QHBoxLayout(KeplerLab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.sceneWidget = KeplerScene(KeplerLab)
        self.sceneWidget.setObjectName(u"sceneWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sceneWidget.sizePolicy().hasHeightForWidth())
        self.sceneWidget.setSizePolicy(sizePolicy1)
        self.sceneWidget.setMinimumSize(QSize(640, 480))

        self.horizontalLayout.addWidget(self.sceneWidget)

        self.widget = QWidget(KeplerLab)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.widget.setMinimumSize(QSize(256, 0))
        self.widget.setMaximumSize(QSize(256, 16777215))
        self.widget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.angleLayout = QHBoxLayout()
        self.angleLayout.setSpacing(4)
        self.angleLayout.setObjectName(u"angleLayout")
        self.angleLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.angleLabel = QLabel(self.widget)
        self.angleLabel.setObjectName(u"angleLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.angleLabel.sizePolicy().hasHeightForWidth())
        self.angleLabel.setSizePolicy(sizePolicy3)
        self.angleLabel.setMinimumSize(QSize(32, 128))
        font = QFont()
        font.setFamily(u"MathJax_SansSerif")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.angleLabel.setFont(font)
        self.angleLabel.setAlignment(Qt.AlignCenter)
        self.angleLabel.setWordWrap(True)

        self.angleLayout.addWidget(self.angleLabel)

        self.angleSpinBox = QDoubleSpinBox(self.widget)
        self.angleSpinBox.setObjectName(u"angleSpinBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.angleSpinBox.sizePolicy().hasHeightForWidth())
        self.angleSpinBox.setSizePolicy(sizePolicy4)
        self.angleSpinBox.setMinimumSize(QSize(64, 128))
        self.angleSpinBox.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setFamily(u"MathJax_SansSerif")
        font1.setPointSize(16)
        font1.setBold(True)
        font1.setWeight(75)
        self.angleSpinBox.setFont(font1)
        self.angleSpinBox.setStyleSheet(u"")
        self.angleSpinBox.setFrame(False)
        self.angleSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.angleSpinBox.setReadOnly(False)
        self.angleSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.angleSpinBox.setMaximum(359.990000000000009)
        self.angleSpinBox.setSingleStep(1.000000000000000)

        self.angleLayout.addWidget(self.angleSpinBox)

        self.angleFineButtons = QVBoxLayout()
        self.angleFineButtons.setObjectName(u"angleFineButtons")
        self.angleFineButtons.setSizeConstraint(QLayout.SetMinimumSize)
        self.anglePlusButton = QPushButton(self.widget)
        self.anglePlusButton.setObjectName(u"anglePlusButton")
        self.anglePlusButton.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.anglePlusButton.sizePolicy().hasHeightForWidth())
        self.anglePlusButton.setSizePolicy(sizePolicy5)
        self.anglePlusButton.setMinimumSize(QSize(64, 0))
        self.anglePlusButton.setMaximumSize(QSize(64, 16777215))
        self.anglePlusButton.setAutoRepeat(True)

        self.angleFineButtons.addWidget(self.anglePlusButton)

        self.angleMinusButton = QPushButton(self.widget)
        self.angleMinusButton.setObjectName(u"angleMinusButton")
        self.angleMinusButton.setMinimumSize(QSize(64, 0))
        self.angleMinusButton.setMaximumSize(QSize(64, 16777215))
        self.angleMinusButton.setAutoRepeat(True)

        self.angleFineButtons.addWidget(self.angleMinusButton)


        self.angleLayout.addLayout(self.angleFineButtons)

        self.angleUnitsLabel = QLabel(self.widget)
        self.angleUnitsLabel.setObjectName(u"angleUnitsLabel")
        sizePolicy3.setHeightForWidth(self.angleUnitsLabel.sizePolicy().hasHeightForWidth())
        self.angleUnitsLabel.setSizePolicy(sizePolicy3)
        self.angleUnitsLabel.setMinimumSize(QSize(64, 128))
        self.angleUnitsLabel.setMaximumSize(QSize(32, 16777215))
        self.angleUnitsLabel.setFont(font)
        self.angleUnitsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.angleUnitsLabel.setWordWrap(True)

        self.angleLayout.addWidget(self.angleUnitsLabel)


        self.verticalLayout.addLayout(self.angleLayout)

        self.velocityLayout = QHBoxLayout()
        self.velocityLayout.setSpacing(4)
        self.velocityLayout.setObjectName(u"velocityLayout")
        self.velocityLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.velocityLabel = QLabel(self.widget)
        self.velocityLabel.setObjectName(u"velocityLabel")
        sizePolicy3.setHeightForWidth(self.velocityLabel.sizePolicy().hasHeightForWidth())
        self.velocityLabel.setSizePolicy(sizePolicy3)
        self.velocityLabel.setMinimumSize(QSize(32, 128))
        self.velocityLabel.setFont(font)
        self.velocityLabel.setAlignment(Qt.AlignCenter)

        self.velocityLayout.addWidget(self.velocityLabel)

        self.velocitySpinBox = QDoubleSpinBox(self.widget)
        self.velocitySpinBox.setObjectName(u"velocitySpinBox")
        sizePolicy4.setHeightForWidth(self.velocitySpinBox.sizePolicy().hasHeightForWidth())
        self.velocitySpinBox.setSizePolicy(sizePolicy4)
        self.velocitySpinBox.setMinimumSize(QSize(64, 128))
        self.velocitySpinBox.setMaximumSize(QSize(16777215, 16777215))
        self.velocitySpinBox.setFont(font)
        self.velocitySpinBox.setStyleSheet(u"")
        self.velocitySpinBox.setFrame(False)
        self.velocitySpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.velocitySpinBox.setReadOnly(False)
        self.velocitySpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.velocitySpinBox.setDecimals(2)
        self.velocitySpinBox.setMaximum(300.000000000000000)
        self.velocitySpinBox.setSingleStep(0.100000000000000)
        self.velocitySpinBox.setValue(0.000000000000000)

        self.velocityLayout.addWidget(self.velocitySpinBox)

        self.velocityFineButtons = QVBoxLayout()
        self.velocityFineButtons.setObjectName(u"velocityFineButtons")
        self.velocityFineButtons.setSizeConstraint(QLayout.SetMinimumSize)
        self.velocityPlusButton = QPushButton(self.widget)
        self.velocityPlusButton.setObjectName(u"velocityPlusButton")
        sizePolicy5.setHeightForWidth(self.velocityPlusButton.sizePolicy().hasHeightForWidth())
        self.velocityPlusButton.setSizePolicy(sizePolicy5)
        self.velocityPlusButton.setMinimumSize(QSize(64, 0))
        self.velocityPlusButton.setMaximumSize(QSize(64, 16777215))
        self.velocityPlusButton.setAutoRepeat(True)

        self.velocityFineButtons.addWidget(self.velocityPlusButton)

        self.velocityMinusButton = QPushButton(self.widget)
        self.velocityMinusButton.setObjectName(u"velocityMinusButton")
        self.velocityMinusButton.setMinimumSize(QSize(64, 0))
        self.velocityMinusButton.setMaximumSize(QSize(64, 16777215))
        self.velocityMinusButton.setAutoRepeat(True)

        self.velocityFineButtons.addWidget(self.velocityMinusButton)


        self.velocityLayout.addLayout(self.velocityFineButtons)

        self.velocityUnitsLabel = QLabel(self.widget)
        self.velocityUnitsLabel.setObjectName(u"velocityUnitsLabel")
        sizePolicy3.setHeightForWidth(self.velocityUnitsLabel.sizePolicy().hasHeightForWidth())
        self.velocityUnitsLabel.setSizePolicy(sizePolicy3)
        self.velocityUnitsLabel.setMinimumSize(QSize(64, 128))
        self.velocityUnitsLabel.setMaximumSize(QSize(64, 16777215))
        self.velocityUnitsLabel.setFont(font)
        self.velocityUnitsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.velocityLayout.addWidget(self.velocityUnitsLabel)


        self.verticalLayout.addLayout(self.velocityLayout)

        self.runClearButton = QPushButton(self.widget)
        self.runClearButton.setObjectName(u"runClearButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.runClearButton.sizePolicy().hasHeightForWidth())
        self.runClearButton.setSizePolicy(sizePolicy6)
        self.runClearButton.setMinimumSize(QSize(0, 0))
        self.runClearButton.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(16)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.runClearButton.setFont(font2)
        self.runClearButton.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u":/icon/play", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/icon/stop", QSize(), QIcon.Normal, QIcon.On)
        self.runClearButton.setIcon(icon)
        self.runClearButton.setCheckable(False)

        self.verticalLayout.addWidget(self.runClearButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.circleButton = QPushButton(self.widget)
        self.circleButton.setObjectName(u"circleButton")
        sizePolicy6.setHeightForWidth(self.circleButton.sizePolicy().hasHeightForWidth())
        self.circleButton.setSizePolicy(sizePolicy6)
        self.circleButton.setMinimumSize(QSize(0, 0))
        self.circleButton.setFont(font2)
        self.circleButton.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icon/circle", QSize(), QIcon.Normal, QIcon.Off)
        self.circleButton.setIcon(icon1)
        self.circleButton.setCheckable(True)
        self.circleButton.setChecked(False)

        self.verticalLayout.addWidget(self.circleButton)

        self.rulerButton = QPushButton(self.widget)
        self.rulerButton.setObjectName(u"rulerButton")
        sizePolicy6.setHeightForWidth(self.rulerButton.sizePolicy().hasHeightForWidth())
        self.rulerButton.setSizePolicy(sizePolicy6)
        self.rulerButton.setMinimumSize(QSize(0, 0))
        self.rulerButton.setFont(font2)
        icon2 = QIcon()
        icon2.addFile(u":/icon/ruler", QSize(), QIcon.Normal, QIcon.Off)
        self.rulerButton.setIcon(icon2)
        self.rulerButton.setCheckable(True)
        self.rulerButton.setChecked(False)

        self.verticalLayout.addWidget(self.rulerButton)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.sweepButton = QPushButton(self.widget)
        self.sweepButton.setObjectName(u"sweepButton")
        self.sweepButton.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.sweepButton.sizePolicy().hasHeightForWidth())
        self.sweepButton.setSizePolicy(sizePolicy6)
        self.sweepButton.setMinimumSize(QSize(0, 0))
        self.sweepButton.setFont(font2)
        icon3 = QIcon()
        icon3.addFile(u":/icon/sweep", QSize(), QIcon.Normal, QIcon.Off)
        self.sweepButton.setIcon(icon3)
        self.sweepButton.setCheckable(True)
        self.sweepButton.setChecked(False)

        self.verticalLayout.addWidget(self.sweepButton)

        self.clearSweepsButton = QPushButton(self.widget)
        self.clearSweepsButton.setObjectName(u"clearSweepsButton")
        sizePolicy6.setHeightForWidth(self.clearSweepsButton.sizePolicy().hasHeightForWidth())
        self.clearSweepsButton.setSizePolicy(sizePolicy6)
        self.clearSweepsButton.setMinimumSize(QSize(0, 0))
        self.clearSweepsButton.setFont(font2)
        icon4 = QIcon()
        icon4.addFile(u":/icon/clear", QSize(), QIcon.Normal, QIcon.Off)
        self.clearSweepsButton.setIcon(icon4)

        self.verticalLayout.addWidget(self.clearSweepsButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.exitButton = QPushButton(self.widget)
        self.exitButton.setObjectName(u"exitButton")
        sizePolicy6.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy6)
        self.exitButton.setFont(font2)
        icon5 = QIcon()
        icon5.addFile(u":/icon/exit", QSize(), QIcon.Normal, QIcon.Off)
        self.exitButton.setIcon(icon5)

        self.verticalLayout.addWidget(self.exitButton)

        self.buildLabel = QLabel(self.widget)
        self.buildLabel.setObjectName(u"buildLabel")
        sizePolicy3.setHeightForWidth(self.buildLabel.sizePolicy().hasHeightForWidth())
        self.buildLabel.setSizePolicy(sizePolicy3)
        self.buildLabel.setStyleSheet(u"QLabel#buildLabel{\n"
"          font: bold 12px;\n"
"          background: #000;\n"
"          color: white;\n"
"          }")
        self.buildLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.buildLabel)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(KeplerLab)
        self.velocityMinusButton.clicked.connect(self.velocitySpinBox.stepDown)
        self.velocityPlusButton.clicked.connect(self.velocitySpinBox.stepUp)

        QMetaObject.connectSlotsByName(KeplerLab)
    # setupUi

    def retranslateUi(self, KeplerLab):
        KeplerLab.setWindowTitle(QCoreApplication.translate("KeplerLab", u"Form", None))
        self.angleLabel.setText(QCoreApplication.translate("KeplerLab", u"\u2220", None))
        self.anglePlusButton.setText(QCoreApplication.translate("KeplerLab", u"+", None))
        self.angleMinusButton.setText(QCoreApplication.translate("KeplerLab", u"-", None))
        self.angleUnitsLabel.setText(QCoreApplication.translate("KeplerLab", u"deg", None))
        self.velocityLabel.setText(QCoreApplication.translate("KeplerLab", u"V", None))
        self.velocityPlusButton.setText(QCoreApplication.translate("KeplerLab", u"+", None))
        self.velocityMinusButton.setText(QCoreApplication.translate("KeplerLab", u"-", None))
        self.velocityUnitsLabel.setText(QCoreApplication.translate("KeplerLab", u"km/s", None))
        self.runClearButton.setText(QCoreApplication.translate("KeplerLab", u"Launch", None))
        self.circleButton.setText(QCoreApplication.translate("KeplerLab", u"Reference Circle", None))
        self.rulerButton.setText(QCoreApplication.translate("KeplerLab", u"On-Screen Ruler", None))
        self.sweepButton.setText(QCoreApplication.translate("KeplerLab", u"Start Sweep", None))
        self.clearSweepsButton.setText(QCoreApplication.translate("KeplerLab", u"Clear Sweeps", None))
        self.exitButton.setText(QCoreApplication.translate("KeplerLab", u"Exit", None))
        self.buildLabel.setText(QCoreApplication.translate("KeplerLab", u"Build: ", None))
    # retranslateUi

