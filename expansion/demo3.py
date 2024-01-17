from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from OpenGL.GL import *
import sys

class MyOpenGLWidget(QOpenGLWidget):
    def initializeGL(self):
        # Initialize OpenGL state
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Set the background color to white
        #glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        # Set up the viewport and projection
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Clear the buffer with the specified clear color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Define the square's vertices
        squareVertices = [
            -0.5, -0.5, 0.0,  # Bottom left corner
             0.5, -0.5, 0.0,  # Bottom right corner
             0.5,  0.5, 0.0,  # Top right corner
            -0.5,  0.5, 0.0   # Top left corner
        ]

        squareVertices1 = [
            -0.5, 0.8, 0.0,  # Bottom left corner
             0.5, 0.8, 0.0,  # Bottom right corner
             0.5,  1, 0.0,  # Top right corner
            -0.5,  1, 0.0   # Top left corner
        ]

        # Set the drawing color to blue
        glColor3f(0.0, 0.0, 1.0)
        glLineWidth(3.0)

        # Enable and specify the vertex array
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, squareVertices)
        glDrawArrays(GL_LINE_LOOP, 0, 4)
        glVertexPointer(3, GL_FLOAT, 0, squareVertices1)

        # Draw the square as a line loop
        
        glDrawArrays(GL_LINE_LOOP, 0, 4)

        # Disable the vertex array
        glDisableClientState(GL_VERTEX_ARRAY)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.openglWidget = MyOpenGLWidget(self)
        self.setCentralWidget(self.openglWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())