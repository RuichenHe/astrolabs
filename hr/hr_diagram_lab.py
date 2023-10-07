from PySide2.QtWidgets import QWidget, QApplication
from PySide2.QtCore import Signal, Slot
from hr_ui import Ui_HrDiagramLab
from star_image import StarData, Star
from datetime import datetime

class HrDiagramLab(QWidget):
    def __init__(self, parent=None):
        super(HrDiagramLab, self).__init__(parent)
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Initialize UI
        self.ui = Ui_HrDiagramLab()
        self.ui.setupUi(self)
        self._star_data = StarData()
        # Update build label
        self.ui.buildLabel.setText(f"Run date: {current_datetime}")

        # Hardcoded function with all of the star data
        self.add_stars()

        # Main image
        self.ui.starImage.set_star_data(self._star_data)
        self.ui.starImage.set_color_channel(0)

        # The small images B and V
        self.ui.bImage.set_star_data(self._star_data)
        self.ui.bImage.set_single_mode(True)
        # self.ui.bImage.setColorChannel(6)
        self.ui.bImage.set_color_channel(60)

        self.ui.vImage.set_star_data(self._star_data)
        self.ui.vImage.set_single_mode(True)
        # self.ui.vImage.setColorChannel(5)
        self.ui.vImage.set_color_channel(50)

        # Connect signals
        self.ui.starImage.star_selected.connect(self.on_selection_changed)
        self.ui.starImage.star_selected.connect(self.ui.bImage.on_selection_changed)
        self.ui.starImage.star_selected.connect(self.ui.vImage.on_selection_changed)
        self.ui.exitButton.clicked.connect(self.on_exitButton_clicked)

    #@Slot(bool, int)
    def on_selection_changed(self, selected, star_id):
        if not selected or star_id < 0 or star_id > self._star_data.size():
            self.ui.spinboxId.setValue(0)
            self.ui.spinboxMagnitude.setValue(0)
            self.ui.spinboxBV.setValue(0)
            self.ui.vmagSpinBox.setValue(0)
            self.ui.bmagSpinBox.setValue(0)
        else:
            star = self._star_data.get_star(star_id)
            self.ui.spinboxId.setValue(star._id)
            self.ui.spinboxMagnitude.setValue(star._mag)
            self.ui.spinboxBV.setValue(star._color)
            self.ui.vmagSpinBox.setValue(star._mag)
            self.ui.bmagSpinBox.setValue(star._mag + star._color)

    def add_stars(self):
        self._star_data.add_star(Star(3, 0.0329114, 0.560759, 20.1, 0.62))
        self._star_data.add_star(Star(44, 0.296203, 0.137975, 19.53, 0.52))
        self._star_data.add_star(Star(55, 0.382962, 0.320076, 16.3, 0.38))
        self._star_data.add_star(Star(60, 0.467089, 0.0708861, 13.7, 0.25))
        self._star_data.add_star(Star(78, 0.734076, 0.237291, 14.06, 1.15))
        self._star_data.add_star(Star(89, 0.925316, 0.921519, 21.72, 0.72))
        pass
    
    def on_exitButton_clicked(self):
        QApplication.quit()