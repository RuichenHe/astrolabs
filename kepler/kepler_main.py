from PySide2.QtWidgets import QMainWindow, QWidget, QBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from kepler_gui import KeplerLab

import sys

if __name__ == "__main__":
    app = QApplication()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    window = QMainWindow()
    lab = KeplerLab(window)
    window.setCentralWidget(lab)
    window.setWindowTitle("Kepler")
    window.setStyleSheet("background-color: black;")
    window.showMaximized()
    sys.exit(app.exec_())