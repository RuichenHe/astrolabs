import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PySide2.QtGui import QImage, QColor, QPainter
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtCore import QRect
from OpenGL.GL import *

from scene_graph1 import FullScreenImage
from galaxy import GalaxySet
from gl_utils import check_GL_error, Camera

class MyOpenGLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(MyOpenGLWidget, self).__init__(parent)
        ## Setup camera
        self.camera = Camera()
        self.top = 1.0
        self.left = 1.0
        self.near = 0.1
        self.far = 1000.0
        self.center = [0, 0, 0]
        self.eye_x = 0.0
        self.eye_y = 0.0
        self.eye = [0, 0, 1]
        self.up = [0, 1, 0]

        ## Setup background
        self.tex_unit_background = 0
        self.max_background_image_count = 6
        self.background = FullScreenImage(self.tex_unit_background, 1024, 1024, 6)

        ## Setup galaxies
        self.max_selections = 16
        self.max_galaxy_image_count = 25
        self.max_visible = 400
        self.tex_unit_galaxies = 1
        self.tex_unit_distances = 3

        self.galaxies = GalaxySet(self.max_selections, self.max_galaxy_image_count, self.max_visible, self.tex_unit_galaxies, self.tex_unit_distances)
        

        self.T_past = -15.0
        self.T_future = 2.0
        self.T_current = -12


        self.T_big_bang = -13.8 #Time of Big-Bang

        self.T_fade_i = -11.5  #Galaxies fade in
        self.T_fade_f = -11.0

        self.T_galaxy_move = -12.0
        self.T_reticule_off = -11.0

    def setEpoch(self, epoch):
        self.T_current = epoch
        self.updateTime()
        #glFlush()
        check_GL_error("ExpansionLabWidget::load_backgrounds() exit")

    def updateTime(self):
        # Normalize time values and clamp between 0.0 and 1.0
        t_galaxy = min(max((self.T_current - self.T_galaxy_move) / (self.T_future - self.T_galaxy_move), 0.0), 1.0)
        alpha_galaxy = min(max((self.T_current - self.T_fade_i) / (self.T_fade_f - self.T_fade_i), 0.0), 1.0)
        t_background = min(max((self.T_current - self.T_big_bang) / (self.T_fade_i - self.T_big_bang), 0.0), 1.0)
        background_scale = (self.T_current - self.T_big_bang) / (self.T_fade_f - self.T_big_bang)

        # # Update galaxy positions and opacity
        # self.galaxies.update_positions(t_galaxy, self.eye_x, self.eye_y)
        # self.galaxies.galaxies.global_opacity = alpha_galaxy

        # Update background properties
        self.background.alpha = 1.0 - alpha_galaxy
        self.background.time = t_background
        self.background.scale[0] = 1.0 + background_scale
        self.background.scale[1] = 1.0 + background_scale

        # # Clear and reset connectors and labels
        # self.distance_connectors.clear()
        # self.distance_labels.count = 0

        # Update positions and colors of selection boxes
        # for selection_ix in range(self.selections_count):
        #     galaxy_ix = self.selections[selection_ix].galaxy_id

        #     for i in range(3):
        #         self.selection_boxes.info[selection_ix].position[i] = \
        #             self.galaxies.info[galaxy_ix].position[i]

        #     for i in range(4):
        #         color = self.C_select_home if selection_ix == 0 else self.C_select_other
        #         self.selection_boxes.info[selection_ix].color[i] = color[i]

        #     # Additional processing for non-home galaxies
        #     if selection_ix > 0:
        #         home_ix = self.selections[0].galaxy_id
        #         # ... distance calculations and updates ...

        # # Update the count and upload changes
        # self.selection_boxes.count = self.selections_count
        # self.selection_boxes.upload_billboards()
        # self.distance_labels.upload_billboards()
        # self.distance_connectors.upload()

    def initializeGL(self):
        print("ExpansionLabWidget::initializeGL")

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        # glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        expansion_base = "../assets/backgrounds/expansion/epoch_"
        self.load_backgrounds(expansion_base, self.max_background_image_count)

        galaxies_base = "../assets/billboards/galaxies/GAL"
        self.load_galaxies(galaxies_base, self.max_galaxy_image_count)

        
    
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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        reticule_visible = self.T_current > self.T_reticule_off

        if self.T_current > self.T_fade_i:
            self.galaxies.render(self.camera)   ### need check 0110

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
        # Update the viewport when the window size changes
        glViewport(0, 0, w, h)

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