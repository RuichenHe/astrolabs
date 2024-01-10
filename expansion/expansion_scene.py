from PySide2.QtWidgets import QOpenGLWidget, QWidget, QVBoxLayout
from PySide2.QtGui import QSurfaceFormat, QImage,QPainter, QColor, QPen, QFont
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QRect, QEvent
from OpenGL.GL import *
from galaxy import GalaxySet
from scene_graph import FullScreenImage, ImageAtlas, Geometry, BillboardSet
import os
from PIL import Image
import sys
import numpy as np
from gl_utils import Camera, check_GL_error
class ExpansionLabWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(ExpansionLabWidget, self).__init__(parent)

        self.max_background_image_count = 6
        self.max_selections = 16
        self.max_galaxy_image_count = 25
        self.max_visible = 400
        self.selections_count_ = 0
        self.T_past = -15.0
        self.T_future = 2.0
        self.T_current = 0
        self.tex_unit_galaxies = 1
        self.tex_unit_distances = 3
        self.tex_unit_background = 0
        

        self.T_current = 0.0
        self.T_galaxy_move = ...  # set appropriate values
        self.T_future = ...
        self.T_fade_i = ...
        self.T_fade_f = ...
        self.T_big_bang = ...





        #TODO
        # Initialize other attributes...
        self.galaxies = GalaxySet(self.max_selections, self.max_galaxy_image_count, self.max_visible, self.tex_unit_galaxies, self.tex_unit_distances)
        self.distance_labels_atlas = ImageAtlas(self.tex_unit_distances, self.label_image_w, self.label_image_h, self.max_selections)
        self.distance_labels = BillboardSet(self.max_selections)
        self.distance_connectors = Geometry(self.max_selections)
        self.selection_boxes = BillboardSet(self.max_selections)
        self.background = FullScreenImage(self.tex_unit_background, 1024, 1024, 6)

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.ClickFocus)

        # Enable Touch
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.setAttribute(Qt.WA_TouchPadAcceptSingleTouchEvents, True)

        # self.grabGesture(Qt.TapGesture)
        self.grabGesture(Qt.PanGesture)

        # Set up OpenGL surface format
        glFormat = QSurfaceFormat()
        glFormat.setVersion(3, 3)
        glFormat.setProfile(QSurfaceFormat.CoreProfile)
        self.setFormat(glFormat)
        self.camera = Camera()
        # Initialize other attributes...
        self.top = 1.0
        self.left = 1.0
        self.near = 0.1
        self.far = 1000.0
        self.center = [0, 0, 0]
        self.eye = [0, 0, 1]
        self.up = [0, 1, 0]

        #  TODO Assign custom shaders to distance_connectors_
        # self.distance_connectors_.vert_shader = "./assets/shaders/connector_lines.vert"
        # self.distance_connectors_.frag_shader = "./assets/shaders/connector_lines.frag"

        # Initialize Data
        self.selections_ = {i: 0 for i in range(self.max_selections_)}

        # Temp image for label generation
        #self.label_image_ = QImage(self.label_image_w_, self.label_image_h_, QImage.Format_RGBA8888)

        # Additional code as needed...
    def initializeGL(self):
        print("ExpansionLabWidget::initializeGL")

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        # glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Initialize galaxies
        galaxies_base = "./assets/billboards/galaxies/GAL"
        self.load_galaxies(galaxies_base, self.max_galaxy_image_count_)

        # Initialize background
        expansion_base = "./assets/backgrounds/expansion/epoch_"
        self.load_backgrounds(expansion_base, self.max_background_image_count_)

        # Selection boxes
        self.selection_boxes_.vert_shader = "./assets/shaders/billboard_set.vert"
        self.selection_boxes_.frag_shader = "./assets/shaders/selection_box.frag"
        # ... other initialization ...

        self.selection_boxes_.init_resources()
        self.selections_count_ = 0

        # Initialize distance labels
        self.distance_labels_.atlas_tex_unit_ = self.tex_unit_distances_
        self.distance_labels_.global_opacity_ = 1.0
        # ... other initialization ...

        self.distance_labels_.init_resources()
        self.distance_labels_atlas_.count_ = self.max_selections_ - 1
        self.distance_labels_atlas_.init_resources()

        

        # ... other code ...

        self.updateTime()
    def setEpoch(self, epoch):
        self.T_current_ = epoch
        self.updateTime()
    def updateTime(self):
        print("TODO")

    def load_galaxies(self, base_path, image_count):
        self.galaxies.init_resources()
        self.galaxies.galaxies_atlas.bind()

        for i in range(image_count):
            filename = os.path.join(base_path, f"{i}.png")
            try:
                img = Image.open(filename)
            except IOError as e:
                print(f"Cannot load: {filename}, {e}", file=sys.stderr)
                continue

            print(f"Loaded file {filename} ( {img.width} x {img.height} )")

            tile_image = QImage(self.galaxies_.galaxies_atlas.tile_width, self.galaxies_.galaxies_atlas.tile_height, QImage.Format_RGBA8888)
            tile_image.fill(QColor(0, 0, 0, 0))

            painter = QPainter(tile_image)
            # Uncomment for debugging: painter.fillRect(tile_image.rect(), Qt.red)
            painter.drawImage(QRect(1, 1, tile_image.width() - 2, tile_image.height() - 2), img)
            painter.end()

            # Convert QImage to byte array for OpenGL
            buffer = tile_image.bits().asarray(tile_image.width() * tile_image.height() * 4)
            self.galaxies_.galaxies_atlas.add_tile(buffer)
        self.galaxies.galaxies_atlas.save_atlas("galaxies_atlas.png")
        self.galaxies.generate_locations()
        self.galaxies.update_texture_coordinates()

    def load_backgrounds(self, base_path, image_count):
        self.background.init_resources()
        self.background.bind()

        for i in range(image_count):
            filename = f"{base_path}/{i}.png"
            img = QImage(filename)

            if img.isNull():
                print(f"Cannot load: {filename}", file=sys.stderr)
                continue

            tile_image = QImage(self.background.tex_width, self.background.tex_height, QImage.Format_RGBA8888)
            tile_image.fill(QColor(0, 0, 0, 0))

            painter = QPainter(tile_image)
            # Uncomment for debugging: painter.fillRect(tile_image.rect(), QColor('red'))
            painter.drawImage(tile_image.rect(), img)
            painter.end()

            # Convert QImage to byte array for OpenGL
            buffer = tile_image.bits().tobytes()
            self.background.upload_slice(i, buffer)

            print(f"Loaded file {i} : {filename} ( {img.width()} x {img.height()} )")

        glFlush()
        check_GL_error("ExpansionLabWidget::load_backgrounds() exit")
    
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

    def updateTime(self):
        # Normalize time values and clamp between 0.0 and 1.0
        t_galaxy = min(max((self.T_current - self.T_galaxy_move) / (self.T_future - self.T_galaxy_move), 0.0), 1.0)
        alpha_galaxy = min(max((self.T_current - self.T_fade_i) / (self.T_fade_f - self.T_fade_i), 0.0), 1.0)
        t_background = min(max((self.T_current - self.T_big_bang) / (self.T_fade_i - self.T_big_bang), 0.0), 1.0)
        background_scale = (self.T_current - self.T_big_bang) / (self.T_fade_f - self.T_big_bang)

        # Update galaxy positions and opacity
        self.galaxies.update_positions(t_galaxy, self.eye_x, self.eye_y)
        self.galaxies.global_opacity = alpha_galaxy

        # Update background properties
        self.background.alpha = 1.0 - self.galaxies.global_opacity
        self.background.time = t_background
        self.background.scale[0] = 1.0 + background_scale
        self.background.scale[1] = 1.0 + background_scale

        # Clear and reset connectors and labels
        self.distance_connectors.clear()
        self.distance_labels.count = 0

        # Update positions and colors of selection boxes
        for selection_ix in range(self.selections_count):
            galaxy_ix = self.selections[selection_ix].galaxy_id

            for i in range(3):
                self.selection_boxes.info[selection_ix].position[i] = \
                    self.galaxies.info[galaxy_ix].position[i]

            for i in range(4):
                color = self.C_select_home if selection_ix == 0 else self.C_select_other
                self.selection_boxes.info[selection_ix].color[i] = color[i]

            # Additional processing for non-home galaxies
            if selection_ix > 0:
                home_ix = self.selections[0].galaxy_id
                # ... distance calculations and updates ...

        # Update the count and upload changes
        self.selection_boxes.count = self.selections_count
        self.selection_boxes.upload_billboards()
        self.distance_labels.upload_billboards()
        self.distance_connectors.upload()
    
    def updateDistanceLabel(self, index, distance):
        # Create a label image
        label_image = QImage(self.label_image_w, self.label_image_h, QImage.Format_RGBA8888)
        label_image.fill(0)

        painter = QPainter(label_image)
        font = painter.font()
        font.setPointSize(self.label_font_size)
        font.setWeight(QFont.DemiBold)
        painter.setFont(font)

        pen = QPen(self.C_text)
        painter.setPen(pen)
        painter.fillRect(label_image.rect(), self.C_padding)
        painter.drawText(QRect(0, 0, self.label_image_w, self.label_image_h), Qt.AlignCenter | Qt.AlignBaseline, f"{distance:.2f} Mpc")

        painter.end()

        # Update the texture atlas with the new label image
        self.distance_labels_atlas.update_tile(index, label_image.bits())

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        reticule_visible = self.T_current > self.T_reticule_off

        if self.T_current > self.T_fade_i:
            # Draw galaxies
            self.galaxies.render(self.camera)

            if reticule_visible:
                self.distance_connectors.render(self.camera)

            if reticule_visible:
                # Bind texture for distance labels
                glBindTexture(GL_TEXTURE_2D, self.distance_labels_atlas.tex)
                self.distance_labels.render(self.camera)

                # Render the selection boxes
                self.selection_boxes.render(self.camera)

        # Draw the background
        if self.T_big_bang < self.T_current < self.T_fade_f:
            self.background.render(self.camera)
    def event(self, event):
        world_cs = [0.0, 0.0, 0.0, 0.0]

        if event.type() == QEvent.Gesture:
            print("Gesture event")
            return True
        elif event.type() == QEvent.TouchBegin:
            print("TouchBegin event")
            # Handle touch begin event
            return True
        elif event.type() == QEvent.MouseMove:
            e = event
            if self.mouse_down:  # Assuming self.mouse_down is defined
                dx = self.mouse_last_x - e.x()
                dy = e.y() - self.mouse_last_y
                # Handle mouse move
                return True
        elif event.type() == QEvent.MouseButtonPress:
            e = event
            # Handle mouse button press
            return True
        elif event.type() == QEvent.MouseButtonRelease:
            e = event
            # Handle mouse button release
            return True
        else:
            return super().event(event)

    



    