from OpenGL.GL import *

import numpy as np
import math
from gl_utils import check_GL_error, build_program
from PySide2.QtGui import QImage, QPainter, QFont, QPen, QColor
from PySide2.QtCore import Qt, QRect
from OpenGL.GL import *

import sys
from PIL import Image
import random
    


class FullScreenImage:  # Assuming FlatShape is already defined
    const_ix = [0, 1, 2, 2, 3, 1]
    def __init__(self, texture_unit, tex_width, tex_height, tex_depth):
        self.position = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.vao = 0
        self.vbo = 0
        self.count = 0
        self.vert_shader = "../assets/shaders/identity.vert"
        self.frag_shader = "../assets/shaders/background.frag"
        self.program = 0
        self.positionHandle = 0
        self.backgroundHandle = 0
        self.backgroundAlpha = 0
        self.backgroundTime = 0
        self.backgroundScale = 0
        self.tex = 0
        self.tex_unit = texture_unit
        self.tex_width = tex_width
        self.tex_height = tex_height
        self.layers = tex_depth
        self.alpha = 0.0
        self.time = 0.0
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    def setPosition(self, x, y, z):
        self.position[:3] = [x, y, z]
    def cleanup(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
    def generate_quad(width, height):
        vertices = np.array([
            [-0.5 * width,  0.5 * height, 0.0], 
            [ 0.5 * width,  0.5 * height, 0.0],
            [-0.5 * width, -0.5 * height, 0.0], 
            [ 0.5 * width, -0.5 * height, 0.0]
        ], dtype=np.float32)

        # Flatten the vertices array for buffer data
        data = vertices.flatten()
        return data
    def build_quad(self, width, height):
        self.count = 6
        data = self.generate_quad(width, height)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glBindVertexArray(0)
    def build_triangle(self, radius):
        glBindVertexArray(self.vao)
        self.count = 3
        half_a = math.sqrt(3.0) * radius

        vertices = np.array([
            [-half_a, -radius, 0.0],
            [0.0, 2.0 * radius, 0.0],
            [half_a, -2 * radius, 0.0]
        ], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glFinish()
        glBindVertexArray(0)
    def setup_array(self, positionHandle):
        print(f"FlatShape::setup_array positionHandle {positionHandle}", file=sys.stderr)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexAttribPointer(positionHandle, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(positionHandle)
        glBindVertexArray(0)
    def init_resources(self):
        print("FullScreenImage::init_resources")

        # Build programs
        self.program = glCreateProgram()

        status = build_program(self.program, "FullScreenImage", self.vert_shader, self.frag_shader)
        if not status:
            return False

        self.positionHandle = glGetAttribLocation(self.program, "position_in_")
        self.backgroundHandle = glGetUniformLocation(self.program, "background_")
        self.backgroundAlpha = glGetUniformLocation(self.program, "background_alpha_")
        self.backgroundTime = glGetUniformLocation(self.program, "background_time_")
        self.backgroundScale = glGetUniformLocation(self.program, "scale_")

        # Initialize textures
        self.tex = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + self.tex_unit)
        glBindTexture(GL_TEXTURE_3D, self.tex)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        # Texture parameters
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA, self.tex_width, self.tex_height, self.layers, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.setup_array(self.positionHandle)
        self.build_triangle(2.0)

        return check_GL_error("FullScreenImage::init_resources() exit")
    
    def cleanup(self):
        glDeleteProgram(self.program)
        glDeleteTextures(1, [self.tex])

    def set_scale_from_aspect(self, aspect):
        self.scale = np.array([1.0, aspect, 1.0], dtype=np.float32)

    def upload_slice(self, layer, buffer):
        check_GL_error("FullScreenImage::upload_slice() entry")

        if layer > self.layers:
            print("FullScreenImage::upload_slice(): layer out of range", file=sys.stderr)
            return

        glBindTexture(GL_TEXTURE_3D, self.tex)
        glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, layer, self.tex_width, self.tex_height, 1, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
        glGenerateMipmap(GL_TEXTURE_3D)
        glFlush()

        check_GL_error("FullScreenImage::upload_slice() exit")
    def bind(self):
        print(self.vao)
        glBindVertexArray(self.vao)
    def unbind(self):
        glBindVertexArray(0)
    def render(self, camera):
        glUseProgram(self.program)
        
        glUniform1i(self.backgroundHandle, self.tex_unit)
        glUniform1f(self.backgroundAlpha, self.alpha)
        glUniform1f(self.backgroundTime, self.time)
        glUniform3fv(self.backgroundScale, 1, self.scale)
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, self.const_ix)

        check_GL_error("FullScreenImage::render()")


class Billboard:
    def __init__(self):
        self.enabled = False
        self.position = np.zeros(3, dtype=np.float32)
        self.rotation = 0.0
        self.scale = np.array([1.0, 1.0], dtype=np.float32)
        self.tex = np.zeros(4, dtype=np.float32)
        self.color = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.float32)


class BillboardSet:
    def __init__(self, max_billboards):
        self.capacity = max_billboards
        self.vert_shader = "../assets/shaders/billboard_set.vert"
        self.frag_shader = "../assets/shaders/billboard_set.frag"
        self.program = None 
        self.vao = None
        self.vbo = None
        self.info = [Billboard() for _ in range(self.capacity)]
        self.count = 0
        self.global_opacity = 0

    def init_resources(self):
        glUseProgram(0)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        # glEnable(GL_DEPTH_TEST)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        #glUseProgram(self.program)
        #self.opacityHandle = glGetUniformLocation(self.program, "global_alpha_")

        self.vbo = glGenBuffers(1)
        self.vbo_line = glGenBuffers(1)
        self.text_label_vbo = glGenBuffers(1)
        self.text_label_vao = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.text_label_vao)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_2D, 0)

    def generate_label_texture(self, text):
        width, height = 256, 128
        font_size = 40
        text_color = QColor(0, 255, 0)  # White color
        background_color = QColor(0, 255, 0, 32)  # Transparent background

        # Create a QImage and a QPainter
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(background_color)

        painter = QPainter(image)
        painter.setPen(QPen(text_color))
        painter.setFont(QFont("Arial", font_size))
        painter.drawText(QRect(0, 0, width, height), Qt.AlignCenter, text)
        painter.end()
        buffer = image.bits().tobytes()
        return buffer
    
    def render(self, obj_count, bbox_vertices, line_vertices, text_label_info):
        glUseProgram(0)

        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 20, None)
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12))
        glDrawArrays(GL_QUADS, 0, 4 * obj_count)

        if bbox_vertices is not None:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_line)
            glBindTexture(GL_TEXTURE_2D, 0)  #### Need to reset the texture before drawing
            glBufferData(GL_ARRAY_BUFFER, bbox_vertices.nbytes, bbox_vertices, GL_DYNAMIC_DRAW)
            glColor4f(1.0, 1.0, 0.0, 1)
            glLineWidth(3.0)
            glVertexPointer(3, GL_FLOAT, 0, None)
            for i in range(int(bbox_vertices.shape[0]/12)):
                glDrawArrays(GL_LINE_LOOP, int(i * 4), 4)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        if line_vertices is not None:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_line)
            glBindTexture(GL_TEXTURE_2D, 0)  #### Need to reset the texture before drawing
            glBufferData(GL_ARRAY_BUFFER, line_vertices.nbytes, line_vertices, GL_DYNAMIC_DRAW)
            glColor4f(1.0, 0.0, 1.0, 1)
            glLineWidth(3.0)
            glVertexPointer(3, GL_FLOAT, 0, None)
            glDrawArrays(GL_LINES, 0, line_vertices.shape[0])
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)


            #### Draw the text label
            glColor4f(1.0, 1.0, 1.0, 1.0)
            for text_info in text_label_info:
                text = "%.2f Mpc"%(text_info[0])
                buffer = self.generate_label_texture(text)


                glBindTexture(GL_TEXTURE_2D, self.text_label_vao)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 256, 128, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer)
                glGenerateMipmap(GL_TEXTURE_2D)
                
                x = text_info[1]
                y = text_info[2]
                z = text_info[3]
                squareVertices = np.array([
                x-0.05, y-0.05, z, 0, 1, 
                x+0.05, y-0.05, z, 1, 1,  
                x+0.05,  y+0.05, z, 1, 0, 
                x-0.05,  y+0.05, z , 0, 0,
                ], dtype=np.float32)

                glBindBuffer(GL_ARRAY_BUFFER, self.text_label_vbo)
                glBufferData(GL_ARRAY_BUFFER, squareVertices.nbytes, squareVertices, GL_DYNAMIC_DRAW)
                glVertexPointer(3, GL_FLOAT, 20, None)
                glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12))
                glDrawArrays(GL_QUADS, 0, 4)



                glBindTexture(GL_TEXTURE_2D, 0)


            
            




