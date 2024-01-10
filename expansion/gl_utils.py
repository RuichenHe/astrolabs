from OpenGL.GL import *
from OpenGL.GLUT import *

from OpenGL.GL import *
import sys
import numpy as np
import math
import ctypes

def get_gl_error_description(error_code):
    error_dict = {
        GL_INVALID_ENUM: "GL_INVALID_ENUM",
        GL_INVALID_VALUE: "GL_INVALID_VALUE",
        GL_INVALID_OPERATION: "GL_INVALID_OPERATION",
        GL_INVALID_FRAMEBUFFER_OPERATION: "GL_INVALID_FRAMEBUFFER_OPERATION",
        GL_OUT_OF_MEMORY: "GL_OUT_OF_MEMORY",
        GL_STACK_UNDERFLOW: "GL_STACK_UNDERFLOW",
        GL_STACK_OVERFLOW: "GL_STACK_OVERFLOW",
    }
    return error_dict.get(error_code, "Unknown Error")

def check_GL_error(tag):
    error_code = glGetError()
    if error_code != GL_NO_ERROR:
        error_message = get_gl_error_description(error_code)
        print(f"# OpenGL Error - {tag}\t - {error_message}", file=sys.stderr)
    return error_code == GL_NO_ERROR

def load_source(filename):
    print(f"Loading {filename}")

    try:
        with open(filename, 'r') as file:
            return file.read()
    except IOError as e:
        # Handle the exception (file not found, etc.)
        print(f"Error loading file {filename}: {e}")
        return ""

def build_program(program, program_name, vert_filename, frag_filename, geo_filename=None):
    vert_src_str = load_source(vert_filename)
    frag_src_str = load_source(frag_filename)
    geo_src_str = None

    if geo_filename:
        geo_src_str = load_source(geo_filename)

    return build_program_from_source(program, program_name, vert_src_str, frag_src_str, geo_src_str)

def build_program_from_source(program, name, vert_source, frag_source, geo_source=None):
    success, vert_shader = compile_shader(GL_VERTEX_SHADER, name, vert_source)
    if not success:
        return False

    glAttachShader(program, vert_shader)

    success, frag_shader = compile_shader(GL_FRAGMENT_SHADER, name, frag_source)
    if not success:
        return False

    glAttachShader(program, frag_shader)

    geo_shader = None
    if geo_source:
        success, geo_shader = compile_shader(GL_GEOMETRY_SHADER, name, geo_source)
        if not success:
            return False
        glAttachShader(program, geo_shader)

    print("Linking")
    glLinkProgram(program)

    # Check for linking errors
    log_len = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
    if log_len > 0:
        log = glGetProgramInfoLog(program).decode()
        print(f"Linker log:\n{log}")

    # Detach and delete shaders after linking
    glDetachShader(program, vert_shader)
    glDetachShader(program, frag_shader)
    glDeleteShader(vert_shader)
    glDeleteShader(frag_shader)

    if geo_shader:
        glDetachShader(program, geo_shader)
        glDeleteShader(geo_shader)

    return True

def compile_shader(shader_type, name, source):
    print(f"Compiling {name} : ", end="")

    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    result = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if result == GL_FALSE:
        print(f"FAIL: {name}")
    else:
        print("ok")

    log_len = glGetShaderiv(shader, GL_INFO_LOG_LENGTH)
    if log_len > 10:
        log = glGetShaderInfoLog(shader).decode()
        print(f"Shader log:\n{log}")

    return result == GL_TRUE, shader


class Camera:
    def __init__(self):
        self.fov = None
        self.near = None
        self.far = None
        self.width = None
        self.height = None
        self.aspect = None

        self.focal_length = 0.0
        
        

        # Matrices
        self.p = np.zeros(16)  # Projection matrix
        self.mv = np.zeros(16)  # ModelView matrix
        self.mvp = np.zeros(16)  # ModelViewProjection matrix
        self.inv_p = np.zeros(16)  # Inverse Projection matrix
        self.inv_mv = np.zeros(16)  # Inverse ModelView matrix
        self.inv_mvp = np.zeros(16)  # Inverse ModelViewProjection matrix

        # Eye position and orientation
        self.eye = np.array([0.0, 0.0, -1.0, 0.0])
        self.eye_world = np.zeros(4)
        self.right_world = np.zeros(4)
        self.up_world = np.zeros(4)
        self.eye_dist = 0.0
        self.eye_orientation = np.zeros(3)

        # Default coordinate system
        self.eye_default = np.array([0.0, 0.0, -1.0, 0.0])
        self.up_default = np.array([0.0, 1.0, 0.0, 0.0])
        self.right_default = np.array([1.0, 0.0, 0.0, 0.0])

        self.width = 0
        self.height = 0
        self.orthographic = False

    def init_orthographic(self, width, height, left, top, near, far):
        self.aspect = float(width) / float(height)
        self.width = width
        self.height = height
        self.near = near
        self.far = far
        self.fov = None  # fov is not used in orthographic projection

        self.p = Camera.calculate_orthographic(left, -left, top, -top, near, far)
        self.orthographic = True

    @staticmethod
    def calculate_orthographic(l, r, b, t, n, f):
        inv_rml = 1.0 / (r - l)
        inv_tmb = 1.0 / (t - b)
        inv_fmn = 1.0 / (f - n)

        p = np.zeros(16)

        p[0] = 2.0 * inv_rml
        p[5] = 2.0 * inv_tmb
        p[10] = 2.0 * inv_fmn
        p[12] = -(r + l) * inv_rml
        p[13] = -(t + b) * inv_tmb
        p[14] = -(f + n) * inv_fmn
        p[15] = 1.0

        return p
    
    def init_perspective(self, width, height, fov, near, far):
        self.aspect = float(width) / float(height)
        self.width = width
        self.height = height
        self.fov = fov
        self.near = near
        self.far = far

        self.focal_length = self.calculate_perspective(fov, self.aspect, near, far, self.p)
        self.inv_p = np.linalg.inv(self.p)
        self.orthographic = False

    def calculate_perspective(fov, aspect, near, far, p):
        focal_length = 1.0 / math.tan(fov * math.pi / 360.0)
        fpn = near + far
        inv_fmn = 1.0 / (near - far)

        # Zero out the matrix first
        p.fill(0)

        p[0] = focal_length / aspect
        p[5] = focal_length
        p[10] = fpn * inv_fmn
        p[11] = -1.0
        p[14] = 2.0 * near * far * inv_fmn

        return focal_length
    def init_model_view(self):
        self.mv = np.zeros(16)  # Zero out MV

        # Rotation
        self.mv[0] = self.mv[5] = self.mv[10] = 1.0

        # Translation
        self.mv[14] = -2.5
        self.mv[15] = 1.0

        self.inv_mv = np.linalg.inv(self.mv.reshape(4, 4)).flatten()

    def look_at(self, center, eye, up):
        # Clear model-view matrix
        self.mv = np.zeros(16)

        fwd = np.array(center, dtype=np.float64) - np.array(eye, dtype=np.float64)
        eye_dist_sq = np.dot(fwd, fwd)
        self.eye_dist = np.sqrt(eye_dist_sq)
        eye_dist_inv = 1.0 / self.eye_dist
        print(eye_dist_inv)
        print(fwd)
        fwd *= eye_dist_inv
        self.eye_orientation = fwd

        side = np.cross(fwd, up)
        up = np.cross(side, fwd)

        for i in range(3):
            self.mv[4 * i] = side[i]
            self.mv[1 + 4 * i] = up[i]
            self.mv[2 + 4 * i] = -fwd[i]

        for i in range(4):
            self.mv[12 + i] = -(self.mv[i] * eye[0] + self.mv[4 + i] * eye[1] + self.mv[8 + i] * eye[2])
        self.mv[15] = 1.0

        self.inv_mv = np.linalg.inv(self.mv.reshape(4, 4)).flatten()
        self.generate_transform()  # Assuming generate_transform is another method to be implemented
    
    def init_from_quaternion(self, q, r):
        # Clear model-view matrix
        self.mv = np.zeros(16)

        q_sq = np.square(q[1:4])  # Square of quaternion components

        # Diagonal
        self.mv[0] = 1 - 2 * (q_sq[1] + q_sq[2])
        self.mv[5] = 1 - 2 * (q_sq[0] + q_sq[2])
        self.mv[10] = 1 - 2 * (q_sq[0] + q_sq[1])

        # Lower left triangle
        self.mv[1] = 2 * (q[1] * q[2] + q[0] * q[3])
        self.mv[2] = 2 * (q[1] * q[3] - q[0] * q[2])
        self.mv[6] = 2 * (q[2] * q[3] + q[0] * q[1])

        # Upper right triangle
        self.mv[4] = 2 * (q[1] * q[2] - q[0] * q[3])
        self.mv[8] = 2 * (q[1] * q[3] + q[0] * q[2])
        self.mv[9] = 2 * (q[2] * q[3] - q[0] * q[1])

        # Translation
        for i in range(3):
            self.mv[12 + i] = r[i]
        self.mv[15] = 1.0

        self.inv_mv = np.linalg.inv(self.mv.reshape(4, 4)).flatten()
        self.generate_transform()  # Assuming generate_transform is implemented

    def generate_transform(self):
        self.mvp = np.dot(self.p.reshape(4, 4), self.mv.reshape(4, 4)).flatten()
        self.inv_mvp = np.linalg.inv(self.mvp.reshape(4, 4)).flatten()

        # Transform default vectors to world coordinates
        self.eye_world = np.dot(self.inv_mv.reshape(4, 4), self.eye_default)
        self.right_world = np.dot(self.inv_mv.reshape(4, 4), self.right_default)
        self.up_world = np.dot(self.inv_mv.reshape(4, 4), self.up_default)

    @staticmethod
    def calculate_mvp(p, mv):
        # Assuming p and mv are flat NumPy arrays representing matrices
        p1, p2, p3, p4, p5 = p[0], p[5], p[10], p[14], p[11]
        
        mvp = np.zeros(16)

        offset = 0
        for i in range(3):
            mvp[offset + 0] = p1 * mv[offset]
            mvp[offset + 1] = p2 * mv[offset + 1]
            mvp[offset + 2] = p3 * mv[offset + 2] + p4 * mv[offset + 3]
            mvp[offset + 3] = p5 * mv[offset + 2]
            offset += 4

        for i in range(3):
            mvp[offset] = p[5 * i] * mv[offset] + p[12 + i]
            offset += 1

        mvp[offset] = p[11] * mv[14] + p[15]
        return mvp
