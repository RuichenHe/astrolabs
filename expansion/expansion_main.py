from PySide2.QtWidgets import QMainWindow, QWidget, QBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from expansion_gui import ExpansionLab

import sys

if __name__ == "__main__":
    app = QApplication()
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    window = QMainWindow()
    lab = ExpansionLab(window)
    window.setCentralWidget(lab)
    window.setWindowTitle("Expansion")
    window.setStyleSheet("background-color: black;")
    window.showMaximized()
    sys.exit(app.exec_())
    