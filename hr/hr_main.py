from PySide2.QtWidgets import QMainWindow, QWidget, QBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QApplication
from hr_diagram_lab import HrDiagramLab

class HRMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(HRMainWindow, self).__init__(parent)

        # Creating a central widget
        widget = QWidget(self)

        # Using QVBoxLayout since QBoxLayout::TopToBottom is equivalent to a vertical layout in Qt
        layout = QVBoxLayout()

        # Assuming HrDiagramLab is another widget you've defined
        layout.addWidget(HrDiagramLab(self))

        widget.setLayout(layout)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    # Create an instance of QApplication
    app = QApplication([])
    app.setStyle("Windows")

    # Create an instance of your main window
    window = HRMainWindow()
    window.setWindowTitle("Lab H: Hertzsprung-Russell diagram")
    # Display the window
    window.show()

    # Start the Qt event loop
    app.exec_()