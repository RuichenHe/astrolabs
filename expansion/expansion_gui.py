from PySide2.QtWidgets import QMainWindow, QWidget, QBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QApplication
from expansion_ui import Ui_ExpansionLab
from OpenGL.GL import *


class ExpansionLab(QWidget):
    def __init__(self, parent = None):
        super(ExpansionLab, self).__init__(parent)
        self.slider_scale = 100
        self.neighbors_required = 3

        self.ui = Ui_ExpansionLab()
        self.ui.setupUi(self)

        self.ui.epochSlider.valueChanged.connect(self.on_epochSlider_valueChanged)
        self.ui.epochSlider.setValue(0)
        self.ui.epochSlider.setMinimum(self.slider_scale * self.ui.sceneWidget.T_past)
        self.ui.epochSlider.setMaximum(self.slider_scale * self.ui.sceneWidget.T_future)
        self.ui.timeLabel.setText(f"{0:.2f} Gyr")
        self.ui.resetButton.clicked.connect(self.on_resetButton_clicked)
        self.ui.exitButton.clicked.connect(self.on_exitButton_clicked)
        self.updateSelection(0)
        self.ui.sceneWidget.countChanged.connect(self.updateSelection)

    def on_epochSlider_valueChanged(self, value):
        print(f"ExpansionLab::on_epochSlider_valueChanged {value}")
        t = value / float(self.slider_scale)
        print(t)
        self.ui.sceneWidget.setEpoch(t)
        self.ui.timeLabel.setText(f"{t:.2f} Gyr")
        self.ui.sceneWidget.paintGL()
        self.ui.sceneWidget.update()

    def updateSelection(self, selected_count):
        selections_todo = self.neighbors_required - selected_count + 1

        if selected_count == 0:
            self.ui.directionsLabel.setText("Select a Home Galaxy")
        elif selections_todo > 1:
            self.ui.directionsLabel.setText(f"Select {selections_todo} galaxies at different distances")
        elif selections_todo == 1:
            self.ui.directionsLabel.setText("Select one more galaxy")
        else:
            self.ui.directionsLabel.setText("")

    def on_resetButton_clicked(self):
        self.ui.sceneWidget.reset()
        self.updateSelection(0)
        self.ui.epochSlider.setValue(0)
        self.ui.timeLabel.setText(f"{0:.2f} Gyr")

    def on_exitButton_clicked(self):
        QApplication.quit()

    




