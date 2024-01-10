from OpenGL.GL import *

import numpy as np
import math
from gl_utils import check_GL_error, build_program
import sys
from PIL import Image
import random


class Node:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        self.scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)

    def setPosition(self, x, y, z):
        self.position[:3] = [x, y, z]

class Billboard:
    def __init__(self):
        self.enabled = False
        self.position = np.zeros(3, dtype=np.float32)
        self.rotation = 0.0
        self.scale = np.array([1.0, 1.0], dtype=np.float32)
        self.tex = np.zeros(4, dtype=np.float32)
        self.color = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.float32)
        

class BillboardSet(Node):
    def __init__(self, max_billboards):
        super().__init__()
        self.quad_width = 0.1
        self.quad_height = 0.1
        self.global_opacity = 1.0
        self.capacity = max_billboards
        self.verts_per_board = 6
        self.attributes_per_vert = 9
        self.ix_position = 0
        self.ix_texture = 3
        self.ix_color = 5
        self.count = 0
        self.atlas_tex_unit = 0
        self.vert_shader = "../assets/shaders/billboard_set.vert"
        self.frag_shader = "../assets/shaders/billboard_set.frag"
        self.program = 0 
        self.positionHandle = 0
        self.textureHandle = 0
        self.colorHandle = 0
        self.mvpHandle = 0
        self.samplerHandle = 0 
        self.opacityHandle = 0
        self.vao = 0
        self.vbo = 0


        self.info = [Billboard() for _ in range(max_billboards)]
        self.data_size = self.attributes_per_vert * self.verts_per_board * self.capacity
        self.vertex_data = np.zeros(self.data_size, dtype=np.float32)



    def init_resources(self):
        print("BillboardSet::init_resources()")
        self.program = glCreateProgram()

        status = build_program(self.program, "BillboardSet", self.vert_shader, self.frag_shader)
        if not status:
            return False

        # Static properties
        self.positionHandle = glGetAttribLocation(self.program, "position_in_")
        self.textureHandle = glGetAttribLocation(self.program, "tex_in_")
        self.colorHandle = glGetAttribLocation(self.program, "color_in_")

        self.mvpHandle = glGetUniformLocation(self.program, "mvp_")
        self.samplerHandle = glGetUniformLocation(self.program, "atlas_")
        self.opacityHandle = glGetUniformLocation(self.program, "global_alpha_")

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        print("BillboardSet VAO", self.vao)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data_size * ctypes.sizeof(ctypes.c_float), None, GL_DYNAMIC_DRAW)

        stride = ctypes.sizeof(ctypes.c_float) * self.attributes_per_vert
        glVertexAttribPointer(self.positionHandle, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(self.ix_position * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(self.positionHandle)
        # 
        # 
        # 

        

        # if self.textureHandle > 0:
        #     glVertexAttribPointer(self.textureHandle, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(self.ix_texture * ctypes.sizeof(ctypes.c_float)))
        #     glEnableVertexAttribArray(self.textureHandle)

        # if self.colorHandle > 0:
        #     glVertexAttribPointer(self.colorHandle, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(self.ix_color * ctypes.sizeof(ctypes.c_float)))
        #     glEnableVertexAttribArray(self.colorHandle)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        error = glGetError()
        if error != GL_NO_ERROR:
            print("OpenGL error:", error)
            return False
        return check_GL_error("BillboardSet::init_resources() exit")
    
    def init_grid(self, tiles_x):
        random_scale = 0.0  # Set this to a non-zero value if randomness is needed

        tiles_y = self.count // tiles_x

        dx = 2.0 / tiles_x
        dy = 2.0 / tiles_y
        dz = -0.0001

        dx_gap = 1.0 * dx
        dy_gap = 0.0

        for i in range(self.count):
            tile_ix = i % tiles_x
            tile_iy = i // tiles_x

            x = -2.0 + (dx + dx_gap) * tile_ix
            y = -1.0 + (dy + dy_gap) * tile_iy

            self.info[i].position[0] = x + random_scale * random.uniform(-random_scale, random_scale)
            self.info[i].position[1] = y + random_scale * random.uniform(-random_scale, random_scale)
            self.info[i].position[2] = dz * i

        # Call the method to upload billboards data to GPU
        self.upload_billboards()
    
    def upload_billboards(self):

        check_GL_error("BillboardSet::upload_billboards() entry")

        offset = 0

        for i in range(len(self.info)):
            data_quad = self.info[i].color
            tex_u_0 = self.info[i].tex[0]
            tex_v_0 = self.info[i].tex[1]
            tex_u_1 = self.info[i].tex[2]
            tex_v_1 = self.info[i].tex[3]
            sin_t = math.sin(self.info[i].rotation)
            cos_t = math.cos(self.info[i].rotation)

            offset_x = self.info[i].position[0]
            x_right = 0.5 * self.quad_width * self.info[i].scale[0]
            x_left = -0.5 * self.quad_width * self.info[i].scale[0]

            offset_y = self.info[i].position[1]
            y_top = 0.5 * self.quad_width * self.info[i].scale[1]
            y_bottom = -0.5 * self.quad_width * self.info[i].scale[1]

            x_rt = cos_t * x_right - sin_t * y_top + offset_x
            y_rt = sin_t * x_right + cos_t * y_top + offset_y

            x_rb = cos_t * x_right - sin_t * y_bottom + offset_x
            y_rb = sin_t * x_right + cos_t * y_bottom + offset_y

            x_lt = cos_t * x_left - sin_t * y_top + offset_x
            y_lt = sin_t * x_left + cos_t * y_top + offset_y

            x_lb = cos_t * x_left - sin_t * y_bottom + offset_x
            y_lb = sin_t * x_left + cos_t * y_bottom + offset_y
            data_vert = np.array([
                [x_lt, y_lt, 0.0, tex_u_0, tex_v_1],
                [x_rt, y_rt, 0.0, tex_u_1, tex_v_1],
                [x_lb, y_lb, 0.0, tex_u_1, tex_v_1],
                [x_rt, y_rt, 0.0, tex_u_1, tex_v_1],
                [x_lb, y_lb, 0.0, tex_u_0, tex_v_0],
                [x_rb, y_rb, 0.0, tex_u_1, tex_v_0],
            ])

            for j in range(self.verts_per_board):
                for k in range(5):
                    self.vertex_data[offset] = data_vert[j][k]
                    offset = offset + 1
                for k in range(4):
                    self.vertex_data[offset] = data_quad[k]
                    offset = offset + 1

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        print(self.vertex_data)
        print(self.vertex_data.nbytes)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertex_data.nbytes, self.vertex_data)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        check_GL_error("BillboardSet::upload_data() exit")
    
    def render(self, camera):    ### need check 0110
        # Assuming camera is a Python object with an attribute 'mvp' which is a NumPy array
        check_GL_error("BillboardSet::render() enter")
        print("self.global_opacity", self.global_opacity)
        # Draw
        glUseProgram(self.program)
        glBindVertexArray(self.vao)

        glUniformMatrix4fv(self.mvpHandle, 1, GL_FALSE, camera.mvp)
        glUniform1i(self.samplerHandle, self.atlas_tex_unit)
        glUniform1f(self.opacityHandle, self.global_opacity)

        # Assuming count is the number of billboards to be drawn
        print("Count: ", self.count)
        glDrawArrays(GL_TRIANGLES, 0, 6 * self.count)

        glBindVertexArray(0)
        check_GL_error("BillboardSet::render() exit")

    
        
class ImageAtlas:
    def __init__(self, tex_unit, tile_width, tile_height, capacity=None, tiles_x=None, tiles_y=None):
        self.tex_unit = tex_unit
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.tex_width = 0
        self.tex_height = 0
        self.tiles_x = 0
        self.tiles_y = 0
        self.capacity = 0
        self.count = 0
        self.max_texture_width = 1024

        if capacity is not None:
            self.capacity = capacity
            # Compute maximum number of tiles we can do in the x direction
            self.tiles_x = self.max_texture_width // self.tile_width
            self.tiles_y = math.ceil(self.capacity / self.tiles_x)

            # Adjust for the capacity of 1
            if capacity == 1:
                self.tiles_x = 1
        else:
            self.tiles_x = tiles_x
            self.tiles_y = tiles_y
            self.capacity = tiles_x * tiles_y
        self.tex_width = tile_width * self.tiles_x
        self.tex_height = tile_height * self.tiles_y
        print(f"ImageAtlas::constructor:: \n"
              f"ImageAtlas:: Unit : {self.tex_unit}\n"
              f"ImageAtlas:: Tiles : {self.tiles_x} x {self.tiles_y}\n"
              f"ImageAtlas:: Capacity : {self.capacity} tiles.\n"
              f"ImageAtlas:: Size : {self.tile_width} x {self.tile_height}\n"
              f"ImageAtlas:: Texture : {self.tex_width} x {self.tex_height}")
        # Initialize the texture

    def init_resources(self):
        print("ImageAtlas::init_resources()")

        # Create a zero-filled buffer
        zero_buffer = np.zeros((self.tex_height, self.tex_width, 4), dtype=np.uint8)

        # Create the textures we need
        self.tex = glGenTextures(1)

        glActiveTexture(GL_TEXTURE0 + self.tex_unit)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glPixelStorei(GL_PACK_ALIGNMENT, 4)

        # Texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.tex_width, self.tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, zero_buffer)

        return True
    
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.tex)
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

    def cleanup(self):
        glDeleteTextures(1, [self.tex])

    def get_tile_coordinates(self, index):
        print("tiles count: ", self.count)
        if self.count <= 0:
            print("ImageAtlas::get_tile_coordinates: No tiles", file=sys.stderr)
            return None

        tex_dx = 1.0 / self.tiles_x
        tex_dy = 1.0 / self.tiles_y

        tile_index = index % self.count
        ix = tile_index % self.tiles_x
        iy = tile_index // self.tiles_x

        # Using NumPy for texture coordinate calculations
        tex_uv = np.array([
            ix * tex_dx,
            (iy + 1) * tex_dy,
            (ix + 1) * tex_dx,
            iy * tex_dy
        ], dtype=np.float32)
        print(tex_uv)

        return tex_uv
    
    def add_tile(self, buffer=None):
        if self.count >= self.capacity:
            print(f"ImageAtlas::add_tile: Can't add new tile because atlas is at capacity {self.count}/{self.capacity}", file=sys.stderr)
            raise Exception("Atlas at capacity")

        index = self.count
        self.count += 1

        if buffer is not None:
            self.update_tile(index, buffer)

        return index
        
    def update_tile(self, index, buffer):
        if index >= self.count:
            print(f"ImageAtlas::update_tile: Index {index} out of range {self.capacity}", file=sys.stderr)
            return False

        tile_x = index % self.tiles_x
        tile_y = index // self.tiles_x

        return self.upload_tile(tile_x, tile_y, buffer)

    def upload_tile(self, tile_x, tile_y, buffer):
        check_GL_error("ImageAtlas::upload_tile() entry")

        if not ((tile_x < self.tiles_x) and (tile_y < self.tiles_y)):
            print(f"col or row is out of range {tile_x} of {self.tiles_x} {tile_y} of {self.tiles_y}", file=sys.stderr)
            return False

        x = tile_x * self.tile_width
        y = tile_y * self.tile_height

        # Assuming buffer is a NumPy array
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, x, y, self.tile_width, self.tile_height, GL_RGBA, GL_UNSIGNED_BYTE, buffer)

        glFlush()
        glGenerateMipmap(GL_TEXTURE_2D)

        return check_GL_error("ImageAtlas::upload_tile() exit")
    
    def save_atlas(self, filename):
        self.save_atlas_static(self.tex, self.tex_width, self.tex_height, filename)

    def save_atlas_static(self, tex, width, height, filename):
        glBindTexture(GL_TEXTURE_2D, tex)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Create a buffer to read the texture
        buffer = np.zeros((height, width, 4), dtype=np.uint8)
        glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE, buffer)

        # PIL handles images in a different coordinate system
        buffer = np.flipud(buffer)

        print(f"ImageAtlas::save_atlas - Writing image of size {width} by {height} filename {filename}")

        image = Image.fromarray(buffer, 'RGBA')
        image.save(filename)


class FlatShape(Node):  # Assuming Node is a base class already defined
    const_ix = [0, 1, 2, 2, 3, 1]

    def __init__(self):
        super().__init__()
        self.vao = 0
        self.vbo = 0
        self.count = 0

    def init_resources(self):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        return True

    def cleanup(self):
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])

    @staticmethod
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

    def bind(self):
        glBindVertexArray(self.vao)

    def render(self, camera):
        glDrawElements(GL_TRIANGLES, self.count, GL_UNSIGNED_INT, self.const_ix)

    

class FullScreenImage(FlatShape):  # Assuming FlatShape is already defined
    def __init__(self, texture_unit, tex_width, tex_height, tex_depth):
        super().__init__()
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

        # Create geometry
        super().init_resources()
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

    def render(self, camera):
        glUseProgram(self.program)
        
        glUniform1i(self.backgroundHandle, self.tex_unit)
        glUniform1f(self.backgroundAlpha, self.alpha)
        glUniform1f(self.backgroundTime, self.time)
        glUniform3fv(self.backgroundScale, 1, self.scale)
        
        super().bind()  ####  need check 0110
        super().render(camera)

        check_GL_error("FullScreenImage::render()")

class Geometry:
    def __init__(self, line_count):
        self.vert_shader_path = "./assets/shaders/default.vert"
        self.frag_shader_path = "./assets/shaders/default.frag"
        self.mode = GL_LINES
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.program = None  # To be set up later
        self.positionHandle = None  # To be set up later
        self.colorHandle = None  # To be set up later
        self.mvpHandle = None  # To be set up later
        self.solidColorHandle = None  # To be set up later
        self.defaultColor = [1.0, 0.0, 1.0, 1.0]

        self.count = 0
        self.capacity = 2 * line_count
        self.size = 2 * 7 * line_count  # 7 is stride (3 for position + 4 for color)
        self.verts = np.zeros(self.size, dtype=np.float32)

    def __del__(self):
        # Clean up resources if necessary
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])

    def init_resources(self):
        print("Geometry::init_resources")

        self.program, status = build_program(self.vert_shader_path, self.frag_shader_path)
        if not status:
            return False

        self.positionHandle = glGetAttribLocation(self.program, "position_in_")
        self.colorHandle = glGetAttribLocation(self.program, "color_in_")

        self.mvpHandle = glGetUniformLocation(self.program, "mvp_")
        self.solidColorHandle = glGetUniformLocation(self.program, "solid_color_")

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.size * self.verts.itemsize, self.verts, GL_STATIC_DRAW)

        glVertexAttribPointer(self.positionHandle, 3, GL_FLOAT, GL_FALSE, self.stride * self.verts.itemsize, None)
        glEnableVertexAttribArray(self.positionHandle)

        if self.colorHandle > 0:
            glVertexAttribPointer(self.colorHandle, 4, GL_FLOAT, GL_FALSE, self.stride * self.verts.itemsize, ctypes.c_void_p(3 * self.verts.itemsize))
            glEnableVertexAttribArray(self.colorHandle)

        glBindVertexArray(0)

        return self.check_GL_error("Geometry::init_resources - exit")

    def clear(self):
        self.count = 0

    def cleanup(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])

    def addPoint(self, v, c):
        offset = self.stride * self.count

        # Add position data
        self.verts[offset:offset + 3] = v
        offset += 3

        # Add color data
        self.verts[offset:offset + 4] = c
        self.count += 1

    def upload(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.stride * self.count * self.verts.itemsize, self.verts)

        # Check for OpenGL errors
        # self.check_GL_error("Geometry::upload exit")  # Implement if needed

    def render(self, camera):
        glUseProgram(self.program)
        glUniformMatrix4fv(self.mvpHandle, 1, GL_FALSE, camera.mvp)
        glUniform4fv(self.solidColorHandle, 1, self.defaultColor)

        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, self.count)