# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hr_diagramZuoqZS.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from star_image import StarImage


class Ui_HrDiagramLab(object):
    def setupUi(self, HrDiagramLab):
        if not HrDiagramLab.objectName():
            HrDiagramLab.setObjectName(u"HrDiagramLab")
        HrDiagramLab.resize(1296, 680)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HrDiagramLab.sizePolicy().hasHeightForWidth())
        HrDiagramLab.setSizePolicy(sizePolicy)
        HrDiagramLab.setMinimumSize(QSize(0, 0))
        self.mainLayout = QHBoxLayout(HrDiagramLab)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(10, 30, 10, 10)
        self.starImage = StarImage(HrDiagramLab)
        self.starImage.setObjectName(u"starImage")
        sizePolicy.setHeightForWidth(self.starImage.sizePolicy().hasHeightForWidth())
        self.starImage.setSizePolicy(sizePolicy)
        self.starImage.setMinimumSize(QSize(512, 512))

        self.mainLayout.addWidget(self.starImage)

        self.sidebarWidget = QWidget(HrDiagramLab)
        self.sidebarWidget.setObjectName(u"sidebarWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sidebarWidget.sizePolicy().hasHeightForWidth())
        self.sidebarWidget.setSizePolicy(sizePolicy1)
        self.sidebarWidget.setMinimumSize(QSize(400, 0))
        self.sidebarWidget.setMaximumSize(QSize(16777215, 16777215))
        self.sidebarLayout = QVBoxLayout(self.sidebarWidget)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(10, 10, 10, 0)
        self.display_widget = QWidget(self.sidebarWidget)
        self.display_widget.setObjectName(u"display_widget")
        self.gridLayout = QGridLayout(self.display_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelMagnitude = QLabel(self.display_widget)
        self.labelMagnitude.setObjectName(u"labelMagnitude")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.labelMagnitude.setFont(font)
        self.labelMagnitude.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelMagnitude, 0, 1, 1, 1)

        self.label = QLabel(self.display_widget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.spinboxId = QSpinBox(self.display_widget)
        self.spinboxId.setObjectName(u"spinboxId")
        self.spinboxId.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spinboxId.sizePolicy().hasHeightForWidth())
        self.spinboxId.setSizePolicy(sizePolicy2)
        self.spinboxId.setStyleSheet(u"QWidget { background-color: white; \n"
"font-size: 30px\n"
"}")
        self.spinboxId.setFrame(False)
        self.spinboxId.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinboxId.setReadOnly(True)
        self.spinboxId.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinboxId.setMaximum(100)

        self.gridLayout.addWidget(self.spinboxId, 1, 0, 1, 1)

        self.spinboxMagnitude = QDoubleSpinBox(self.display_widget)
        self.spinboxMagnitude.setObjectName(u"spinboxMagnitude")
        self.spinboxMagnitude.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.spinboxMagnitude.sizePolicy().hasHeightForWidth())
        self.spinboxMagnitude.setSizePolicy(sizePolicy2)
        self.spinboxMagnitude.setMinimumSize(QSize(64, 0))
        self.spinboxMagnitude.setMaximumSize(QSize(16777215, 16777215))
        self.spinboxMagnitude.setStyleSheet(u"QWidget { background-color: white; \n"
"font-size: 30px\n"
"}")
        self.spinboxMagnitude.setFrame(False)
        self.spinboxMagnitude.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinboxMagnitude.setReadOnly(True)
        self.spinboxMagnitude.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.spinboxMagnitude, 1, 1, 1, 1)


        self.sidebarLayout.addWidget(self.display_widget)

        self.images_grid = QGridLayout()
        self.images_grid.setObjectName(u"images_grid")
        self.exitButton = QPushButton(self.sidebarWidget)
        self.exitButton.setObjectName(u"exitButton")

        self.images_grid.addWidget(self.exitButton, 10, 2, 1, 1)

        self.sdss_link_old = QLabel(self.sidebarWidget)
        self.sdss_link_old.setObjectName(u"sdss_link_old")
        font1 = QFont()
        font1.setPointSize(24)
        self.sdss_link_old.setFont(font1)
        self.sdss_link_old.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sdss_link_old.setOpenExternalLinks(True)

        self.images_grid.addWidget(self.sdss_link_old, 9, 0, 1, 3)

        self.bmagSpinBox = QDoubleSpinBox(self.sidebarWidget)
        self.bmagSpinBox.setObjectName(u"bmagSpinBox")
        self.bmagSpinBox.setEnabled(True)
        self.bmagSpinBox.setStyleSheet(u"QWidget { background-color: white;\n"
"font-size: 30px\n"
"}")
        self.bmagSpinBox.setFrame(False)
        self.bmagSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.bmagSpinBox.setReadOnly(True)
        self.bmagSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.images_grid.addWidget(self.bmagSpinBox, 1, 2, 1, 1)

        self.bImage = StarImage(self.sidebarWidget)
        self.bImage.setObjectName(u"bImage")
        self.bImage.setMinimumSize(QSize(256, 256))

        self.images_grid.addWidget(self.bImage, 6, 0, 1, 1)

        self.vImage = StarImage(self.sidebarWidget)
        self.vImage.setObjectName(u"vImage")
        self.vImage.setMinimumSize(QSize(256, 256))

        self.images_grid.addWidget(self.vImage, 6, 2, 1, 1)

        self.b_image_label = QLabel(self.sidebarWidget)
        self.b_image_label.setObjectName(u"b_image_label")
        font2 = QFont()
        font2.setPointSize(16)
        self.b_image_label.setFont(font2)
        self.b_image_label.setAlignment(Qt.AlignCenter)

        self.images_grid.addWidget(self.b_image_label, 0, 2, 1, 1)

        self.v_image_label = QLabel(self.sidebarWidget)
        self.v_image_label.setObjectName(u"v_image_label")
        self.v_image_label.setFont(font2)
        self.v_image_label.setAlignment(Qt.AlignCenter)

        self.images_grid.addWidget(self.v_image_label, 0, 0, 1, 1)

        self.vmagSpinBox = QDoubleSpinBox(self.sidebarWidget)
        self.vmagSpinBox.setObjectName(u"vmagSpinBox")
        self.vmagSpinBox.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.vmagSpinBox.sizePolicy().hasHeightForWidth())
        self.vmagSpinBox.setSizePolicy(sizePolicy3)
        self.vmagSpinBox.setStyleSheet(u"QWidget { background-color: white;\n"
"font-size: 30px\n"
"}")
        self.vmagSpinBox.setFrame(False)
        self.vmagSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.vmagSpinBox.setReadOnly(True)
        self.vmagSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.images_grid.addWidget(self.vmagSpinBox, 1, 0, 1, 1)

        self.buildLabel = QLabel(self.sidebarWidget)
        self.buildLabel.setObjectName(u"buildLabel")
        font3 = QFont()
        font3.setPointSize(9)
        self.buildLabel.setFont(font3)

        self.images_grid.addWidget(self.buildLabel, 11, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.labelBV = QLabel(self.sidebarWidget)
        self.labelBV.setObjectName(u"labelBV")
        self.labelBV.setFont(font)
        self.labelBV.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelBV)

        self.spinboxBV = QDoubleSpinBox(self.sidebarWidget)
        self.spinboxBV.setObjectName(u"spinboxBV")
        self.spinboxBV.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.spinboxBV.sizePolicy().hasHeightForWidth())
        self.spinboxBV.setSizePolicy(sizePolicy4)
        self.spinboxBV.setMinimumSize(QSize(196, 0))
        self.spinboxBV.setMaximumSize(QSize(16777215, 16777215))
        self.spinboxBV.setStyleSheet(u"QWidget { background-color: white; \n"
"font-size: 30px\n"
"}")
        self.spinboxBV.setFrame(False)
        self.spinboxBV.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinboxBV.setReadOnly(True)
        self.spinboxBV.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.horizontalLayout.addWidget(self.spinboxBV)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.images_grid.addLayout(self.horizontalLayout, 2, 0, 1, 3)


        self.sidebarLayout.addLayout(self.images_grid)


        self.mainLayout.addWidget(self.sidebarWidget)


        self.retranslateUi(HrDiagramLab)

        QMetaObject.connectSlotsByName(HrDiagramLab)
    # setupUi

    def retranslateUi(self, HrDiagramLab):
        HrDiagramLab.setWindowTitle(QCoreApplication.translate("HrDiagramLab", u"Form", None))
        self.labelMagnitude.setText(QCoreApplication.translate("HrDiagramLab", u"V-Magnitude", None))
        self.label.setText(QCoreApplication.translate("HrDiagramLab", u"ID", None))
        self.exitButton.setText(QCoreApplication.translate("HrDiagramLab", u"Exit", None))
        self.sdss_link_old.setText(QCoreApplication.translate("HrDiagramLab", u"<a href=\"http://cas.sdss.org/dr7/en/tools/chart/navi.asp?ra=88.075&dec=32.55\">Part E: Sloan Digital Sky Survey</a>", None))
        self.b_image_label.setText(QCoreApplication.translate("HrDiagramLab", u"B-Image", None))
        self.v_image_label.setText(QCoreApplication.translate("HrDiagramLab", u"V-Image", None))
        self.buildLabel.setText(QCoreApplication.translate("HrDiagramLab", u"TextLabel", None))
        self.labelBV.setText(QCoreApplication.translate("HrDiagramLab", u"B-V", None))
    # retranslateUi

