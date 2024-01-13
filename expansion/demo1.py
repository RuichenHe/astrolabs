import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtGui import QImage, QColor, QPainter
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtCore import QRect
from OpenGL.GL import *
import numpy as np

from scene_graph1 import FullScreenImage
from scene_graph import ImageAtlas
from scene_graph1 import BillboardSet
from galaxy import GalaxySet
from gl_utils import check_GL_error
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
    def generate_cord(self, scale = 1):
        self.scale = scale
        self.x1 = self.x * scale - self.width/2
        self.x2 = self.x * scale + self.width/2
        self.y1 = self.y * scale - self.height/2
        self.y2 = self.y * scale + self.height/2
        result = []
        result.append(np.array([self.x1, self.y1, 0], dtype=np.float32) )
        result.append(np.array([self.x2, self.y1, 0], dtype=np.float32))
        result.append(np.array([self.x2, self.y2, 0], dtype=np.float32))
        result.append(np.array([self.x1, self.y2, 0], dtype=np.float32))
        return result
    def hit_test(self, u, v):
        if u > self.x2 or u < self.x1 or v > self.y2 or v < self.y1:
            return False
        return True


class MyOpenGLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(MyOpenGLWidget, self).__init__(parent)
        ## Setup camera
        self.camera = Camera()
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

        ## Setup background
        self.tex_unit_background = 0
        self.max_background_image_count = 6
        self.background = FullScreenImage(self.tex_unit_background, 1024, 1024, 6)
        
        self.T_past = -15.0
        self.T_future = 2.0
        self.T_current = 0


        self.T_big_bang = -13.8 #Time of Big-Bang

        self.T_fade_i = -11.5  #Galaxies fade in
        self.T_fade_f = -11.0

        self.T_galaxy_move = -12.0
        self.T_reticule_off = -11.0

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

    def setEpoch(self, epoch):
        self.T_current = epoch
        self.updateTime()
        #glFlush()
        check_GL_error("ExpansionLabWidget::load_backgrounds() exit")

    def updateTime(self):
        # Normalize time values and clamp between 0.0 and 1.0
        t_galaxy = min(max((self.T_current - self.T_galaxy_move) / (self.T_future - self.T_galaxy_move), 0.0), 1.0)

        print("t_galaxy", t_galaxy)
        alpha_galaxy = min(max((self.T_current - self.T_fade_i) / (self.T_fade_f - self.T_fade_i), 0.0), 1.0)
        t_background = min(max((self.T_current - self.T_big_bang) / (self.T_fade_i - self.T_big_bang), 0.0), 1.0)
        background_scale = (self.T_current - self.T_big_bang) / (self.T_fade_f - self.T_big_bang)

        # # Update galaxy positions and opacity
        self.update_position(t_galaxy)
        self.galaxies.global_opacity = alpha_galaxy

        # Update background properties
        self.background.alpha = 1.0 - alpha_galaxy
        self.background.time = t_background
        self.background.scale[0] = 1.0 + background_scale
        self.background.scale[1] = 1.0 + background_scale


    def initializeGL(self):
        print("ExpansionLabWidget::initializeGL")

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        # glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        expansion_base = "../assets/backgrounds/expansion/epoch_"
        self.load_backgrounds(expansion_base, self.max_background_image_count)


        #### For galaxies
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
        self.updateTime()


        
    
    def load_backgrounds(self, base_path, image_count):
        self.background.init_resources()
        self.background.bind()
        for i in range(image_count):
            filename = f"{base_path}{i}.png"
            print(filename)
            img = QImage(filename)
            if img.isNull():
                print(f"Cannot load: {filename}", file=sys.stderr)
                continue
            tile_image = QImage(self.background.tex_width, self.background.tex_height, QImage.Format_RGBA8888)
            tile_image.fill(QColor(0, 0, 0, 0))
            painter = QPainter(tile_image)
        #     # Uncomment for debugging: painter.fillRect(tile_image.rect(), QColor('red'))
            painter.drawImage(tile_image.rect(), img)
            painter.end()

        #     # Convert QImage to byte array for OpenGL
            buffer = tile_image.bits().tobytes()
            self.background.upload_slice(i, buffer)
            print(f"Loaded file {i} : {filename} ( {img.width()} x {img.height()} )")
        glFlush()
        self.background.unbind()
        check_GL_error("ExpansionLabWidget::load_backgrounds() exit")

    def load_galaxies(self, base_path, image_count):
        self.galaxies.init_resources()
        self.galaxies.galaxies_atlas.bind()

        for i in range(image_count):
            filename = f"{base_path}{i+1}.png"
            img = QImage(filename)
            if img.isNull():
                print(f"Cannot load: {filename}", file=sys.stderr)
                continue

            tile_image = QImage(self.galaxies.galaxies_atlas.tile_width, self.galaxies.galaxies_atlas.tile_height, QImage.Format_RGBA8888)
            tile_image.fill(QColor(0, 0, 0, 0))
            painter = QPainter(tile_image)
            # Uncomment for debugging: painter.fillRect(tile_image.rect(), Qt.red)
            painter.drawImage(QRect(1, 1, tile_image.width() - 2, tile_image.height() - 2), img)
            painter.end()

            # Convert QImage to byte array for OpenGL
            buffer = tile_image.bits().tobytes()
            self.galaxies.galaxies_atlas.add_tile(buffer)
        self.galaxies.galaxies_atlas.save_atlas("galaxies_atlas.png")
        self.galaxies.generate_locations()
        self.galaxies.update_texture_coordinates()

    def init_galaxy(self):
        np.random.seed(4910)
        for i in range(self.max_galaxy_count):
            x = np.random.uniform(-0.3, 0.3)
            y = np.random.uniform(-0.3, 0.3)
            tex_id = np.random.randint(0, len(self.galaxy_tex_info))
            print(i, tex_id)
            print(x, y)
            self.galaxy_info.append(GalaxyInfo(i, tex_id, x, y, self.default_galaxy_size, self.default_galaxy_size))

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        reticule_visible = self.T_current > self.T_reticule_off

        if self.T_current > self.T_fade_i:
            glBindTexture(GL_TEXTURE_2D, self.galaxies_atlas.tex)
            self.galaxies.render(len(self.galaxy_info))
            glBindTexture(GL_TEXTURE_2D, 0)

        #     # if reticule_visible:
        #     #     self.distance_connectors.render(self.camera)

        #     # if reticule_visible:
        #     #     # Bind texture for distance labels
        #     #     glBindTexture(GL_TEXTURE_2D, self.distance_labels_atlas.tex)
        #     #     self.distance_labels.render(self.camera)

        #     #     # Render the selection boxes
        #     #     self.selection_boxes.render(self.camera)

        # # Draw the background

        if self.T_big_bang < self.T_current < self.T_fade_f:
            #glBindVertexArray(self.background.vao)
            self.background.bind()
            self.background.render(self.camera)
            self.background.unbind()
    def resizeGL(self, w, h):
        aspect = float(w) / float(h)

        top = self.top
        left = self.left

        if aspect <= 1.0:
            top /= aspect
        else:
            left *= aspect

        self.camera.init_orthographic(w, h, left, top, self.near, self.far)
        self.camera.init_model_view()
        self.camera.look_at(self.center, self.eye, self.up)
        glViewport(0, 0, w, h)
    def hit_test(self, u, v):
        for current_galaxy_info in self.galaxy_info:
            if current_galaxy_info.hit_test(u, v) == True:
                return current_galaxy_info.id
        return -1
    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        u = 2 * x/self.size().width() - 1
        v = 1 - 2 * y/self.size().height()
        print("u, v:", u, v)
        print(self.hit_test(u,v))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)  # Set window size
        self.setCentralWidget(MyOpenGLWidget(self))
        self.setWindowTitle("PySide2 + OpenGL Example")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())