import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtGui import QImage, QColor, QPainter
from PySide2.QtCore import QRect
from gl_utils import check_GL_error, build_program
from scene_graph import ImageAtlas
from scene_graph1 import BillboardSet
from OpenGL.GL import *
from PIL import Image

from galaxy import Galaxy
from camera import Camera


class GalaxyTex:
    def __init__(self, id, tex_cord):
        self.id = id
        self.tex_cord = tex_cord

class GalaxyInfo:
    def __init__(self, id, tex_id, x, y, width, height):
        self.id = id
        self.tex_id = tex_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.select = False
        self.scale = 1
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.bbox = None
        self.center = None
    def generate_cord(self, scale = 1):
        self.scale = scale
        self.center = np.array([self.x * scale, self.y * scale, 0], dtype=np.float32)
        self.x1 = self.x * scale - self.width/2
        self.x2 = self.x * scale + self.width/2
        self.y1 = self.y * scale - self.height/2
        self.y2 = self.y * scale + self.height/2
        result = []
        result.append(np.array([self.x1, self.y1, 0], dtype=np.float32))
        result.append(np.array([self.x2, self.y1, 0], dtype=np.float32))
        result.append(np.array([self.x2, self.y2, 0], dtype=np.float32))
        result.append(np.array([self.x1, self.y2, 0], dtype=np.float32))
        self.bbox = result
        return result
    def hit_test(self, u, v):
        if u > self.x2 or u < self.x1 or v > self.y2 or v < self.y1:
            return False
        return True



class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        #### Camera parameter
        self.near = -10.0
        self.far = 10.0
        self.top = -1.0
        self.left = -1.0
        self.center = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.eye = np.array([0.0, 0.0, 7.0])
        self.default_galaxy_size = 0.05

        self.global_scale_min = 3
        self.global_scale_max = 24
        self.global_scale = 3



        self.vert_shader = "../assets/shaders/identity.vert"
        self.frag_shader = "../assets/shaders/background.frag"

        self.galaxy_image_w = 128
        self.galaxy_image_h = 128
        self.tex_unit_galaxies = 1
        self.max_galaxy_image_count = 25
        self.max_galaxy_count = 400

        self.galaxies_atlas = ImageAtlas(self.tex_unit_galaxies, self.galaxy_image_w, self.galaxy_image_h, self.max_galaxy_image_count)  # Assuming ImageAtlas is a class
        self.galaxies = BillboardSet(1)

        self.galaxy_tex_info = []
        self.galaxy_info = []

        self.camera = Camera()

    def update_position(self, t):
        self.global_scale = self.global_scale_min + t * (self.global_scale_max - self.global_scale_min)
        self.generate_verticies()
        self.upload_vertices()


    def generate_verticies(self):
        result = None
        for current_galaxy_info in self.galaxy_info:
            current_galaxy_vert = current_galaxy_info.generate_cord(self.global_scale)
            current_galaxy_tex = self.galaxy_tex_info[current_galaxy_info.tex_id].tex_cord
            for current_vert, current_tex in zip(current_galaxy_vert, current_galaxy_tex):
                if result is None:
                    result = current_vert
                    result = np.append(result, current_tex)
                else:
                    result = np.append(result, current_vert)
                    result = np.append(result, current_tex)
        self.vertices = result

    def upload_vertices(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.galaxies.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)

    def initializeGL(self):
        self.galaxies.init_resources()
        self.galaxies_atlas.init_resources()
        self.galaxies_atlas.bind()
        base_path = "../assets/billboards/galaxies/GAL"
        galaxy_id = 0
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
            result = self.galaxies_atlas.add_tile(buffer)
            if result is not None:
                self.galaxy_tex_info.append(GalaxyTex(galaxy_id, result))
                galaxy_id = galaxy_id + 1
        self.galaxies_atlas.save_atlas("galaxies_atlas_demo2.png")
        print("self.galaxy_tex_info", len(self.galaxy_tex_info))
        self.galaxies_atlas.unbind()
        self.init_galaxy()
        self.generate_verticies()
        self.upload_vertices()

    def paintGL(self):
        print("self.galaxies.program", self.galaxies.program)
        #glUseProgram(self.galaxies.program)
        glBindTexture(GL_TEXTURE_2D, self.galaxies_atlas.tex)
        self.galaxies.render(len(self.galaxy_info))
        glBindTexture(GL_TEXTURE_2D, 0)


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        aspect = float(w) / float(h)
        print(aspect)

        top = self.top
        left = self.left

        if aspect <= 1.0:
            top /= aspect
        else:
            left *= aspect
        self.camera.init_orthographic(w, h, left, top, self.near, self.far)
        self.camera.init_model_view()
        self.camera.look_at(self.center, self.eye, self.up)

    def init_galaxy(self):
        np.random.seed(4910)
        for i in range(self.max_galaxy_count):
            x = np.random.uniform(-0.3, 0.3)
            y = np.random.uniform(-0.3, 0.3)
            tex_id = np.random.randint(0, len(self.galaxy_tex_info))
            print(i, tex_id)
            print(x, y)
            self.galaxy_info.append(GalaxyInfo(i, tex_id, x, y, self.default_galaxy_size, self.default_galaxy_size))


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
