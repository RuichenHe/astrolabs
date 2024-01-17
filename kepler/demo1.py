import sys
import math
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtCore import QTimer
from PySide2.QtGui import QSurfaceFormat
from PySide2.QtCore import Qt
from OpenGL.GL import *
from orbit import Orbit

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.angle = 0  # Angle for rotation
        self.markers_ = 8096
        self.orbit_path_ = 8096
        self.circle_ = 256
        self.setMouseTracking(True)

        # Enable touch
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)

        self.theta_launch_ = 0.0
        self.v_launch_ = 5
        self.timer = QTimer(self)  # Timer for animation
        self.timer.timeout.connect(self.updateAnimation)  # Connect timeout signal to the update function
        self.timer.start(16)  # Approximately 60 frames per second
        self.orbit = Orbit()
        self.count = 0
        self.total_count = 0
        self.collide = False
        self.runSimulation()

        

    def initializeGL(self):
        glClearColor(0, 0, 0, 1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_circle(0.0, 0.0, 0.025, [1, 1, 0])  # Sun-like circle (yellow)

        # Calculate position for the rotating planet
        # orbit_radius = 0.35
        # x = orbit_radius * math.cos(math.radians(self.angle))
        # y = orbit_radius * math.sin(math.radians(self.angle))
        x = 0.5 * self.orbit.elements_[self.count].x
        y = 0.5 * self.orbit.elements_[self.count].y
        self.draw_circle(x, y, 0.01, [0, 0, 1])  # Planet-like circle (blue)


    def draw_circle(self, x, y, radius, color):
        sides = 32
        glBegin(GL_POLYGON)
        glColor3fv(color)
        for i in range(sides):
            cosine = radius * math.cos(i * 2 * math.pi / sides) + x
            sine = radius * math.sin(i * 2 * math.pi / sides) + y
            glVertex2f(cosine, sine)
        glEnd()

    def runSimulation(self):
        self.arrow_visible_ = False

        # Compute the orbit

        self.collide = self.orbit.calculate_orbit(self.theta_launch_, self.v_launch_)
        print("self.collide", self.collide)
        self.total_count = self.orbit.element_count_
        for i in range(self.orbit.element_count_):
            element = self.orbit.elements_[i]
            print("Element:", i, 0.5 * element.x, 0.5 * element.y)

        self.valid = True

        self.animation = True
        self.update()

    def updateAnimation(self):
        # self.angle -= 1  # Decrease the angle for counter-clockwise rotation
        # if self.angle <= -360:
        #     self.angle = 0
        self.count = self.count + 1
        if self.count >= self.orbit.element_count_:
            if self.collide:
                self.timer.stop()
            else:
                self.count = 0

        self.update()  # Trigger repaint

    def resizeGL(self, width, height):
        # Prevent a divide by zero error
        if height == 0:
            height = 1

        # Calculate the aspect ratio of the window
        aspect_ratio = width / height

        # Set the viewport to cover the new window size
        glViewport(0, 0, width, height)

        # Set up the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Adjust the projection to the new aspect ratio
        if width >= height:
            # Window is wider than tall
            glOrtho(-aspect_ratio, aspect_ratio, -1, 1, -1, 1)
        else:
            # Window is taller than wide
            glOrtho(-1, 1, -1 / aspect_ratio, 1 / aspect_ratio, -1, 1)

        glMatrixMode(GL_MODELVIEW)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.opengl_widget = OpenGLWidget(self)
        self.setCentralWidget(self.opengl_widget)
        self.setWindowTitle('OpenGL with PySide2')
        self.resize(800, 600)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
