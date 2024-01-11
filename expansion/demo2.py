import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtGui import QImage, QColor, QPainter
from PySide2.QtCore import QRect
from gl_utils import check_GL_error, build_program
from scene_graph import ImageAtlas
from OpenGL.GL import *
from PIL import Image

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.vert_shader = "../assets/shaders/identity.vert"
        self.frag_shader = "../assets/shaders/background.frag"

        self.galaxy_image_w = 128
        self.galaxy_image_h = 128
        self.tex_unit_galaxies = 1
        self.max_galaxy_image_count = 25

        self.galaxies_atlas = ImageAtlas(self.tex_unit_galaxies, self.galaxy_image_w, self.galaxy_image_h, self.max_galaxy_image_count)  # Assuming ImageAtlas is a class
        

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        # glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.program = glCreateProgram()

        status = build_program(self.program, "FullScreenImage", self.vert_shader, self.frag_shader)
        if not status:
            return False
        
        self.galaxies_atlas.init_resources()
        self.galaxies_atlas.bind()
        base_path = "../assets/billboards/galaxies/GAL"
        for i in range(self.max_galaxy_image_count):
            filename = f"{base_path}{i+1}.png"
            img = QImage(filename)
            if img.isNull():
                print(f"Cannot load: {filename}", file=sys.stderr)
                continue

            tile_image = QImage(self.galaxies_atlas.tile_width, self.galaxies_atlas.tile_height, QImage.Format_RGBA8888)
            tile_image.fill(QColor(0, 0, 0, 0))
            painter = QPainter(tile_image)
            # Uncomment for debugging: painter.fillRect(tile_image.rect(), Qt.red)
            painter.drawImage(QRect(1, 1, tile_image.width() - 2, tile_image.height() - 2), img)
            painter.end()

            # Convert QImage to byte array for OpenGL
            buffer = tile_image.bits().tobytes()
            self.galaxies_atlas.add_tile(buffer)
        self.galaxies_atlas.save_atlas("galaxies_atlas_demo2.png")
        self.galaxies_atlas.unbind()

        #self.tex = self.loadTexture("galaxies_atlas_demo2.png")
        self.tex = self.galaxies_atlas.tex

        # Quad vertices and texture coordinates      
        self.vertices = np.array([
            -1, -1, 0,  0, 1,
             1, -1, 0,  1, 1,
             1,  1, 0,  1, 0,
            -1,  1, 0,  0, 0,
        ], dtype=np.float32)

        self.vertices2 = np.array([
            # First Triangle (x, y, z, u, v)
            -1.0, -1.0, 0.0, 0.0, 0.0,
             1.0, -1.0, 0.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 0.0, 1.0,
            
            # Second Triangle (x, y, z, u, v)
            -1.0,  1.0, 0.0, 0.0, 1.0,
             1.0, -1.0, 0.0, 1.0, 0.0,
             1.0,  1.0, 0.0, 1.0, 1.0
        ], dtype=np.float32)


        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 20, None)
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12))

        glDrawArrays(GL_QUADS, 0, 4)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glBindTexture(GL_TEXTURE_2D, 0)

    def loadTexture(self, imagePath):
        img = QImage(imagePath)
        tile_image = QImage(1200, 800, QImage.Format_RGBA8888)
        tile_image.fill(QColor(0, 0, 0, 0))
        painter = QPainter(tile_image)
    #     # Uncomment for debugging: painter.fillRect(tile_image.rect(), QColor('red'))
        painter.drawImage(tile_image.rect(), img)
        painter.end()

    #     # Convert QImage to byte array for OpenGL
        buffer = tile_image.bits().tobytes()

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1200, 800, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer)

        return texture

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.openglWidget = GLWidget(self)
        self.setCentralWidget(self.openglWidget)
        self.resize(1200, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
