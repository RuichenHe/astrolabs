import numpy as np


class Camera:
    def __init__(self):
        self.fov = None
        self.near = None
        self.far = None
        self.width = None
        self.height = None
        self.aspect = None
        self.eye_orientation = None
        self.eye = np.zeros(3)


        self.focal_length = 0.0
        # Matrices
        self.p = np.zeros((4, 4))
        self.mv = np.zeros((4, 4))
        self.mvp = np.zeros((4, 4))  # ModelViewProjection matrix
        self.inv_p = np.zeros((4, 4))  # Inverse Projection matrix
        self.inv_mv = np.zeros((4, 4))  # Inverse ModelView matrix
        self.inv_mvp = np.zeros((4, 4))  # Inverse ModelViewProjection matrix


        self.eye_default = np.array([0.0, 0.0, -1.0, 0.0])
        self.up_default = np.array([0.0, 1.0, 0.0, 0.0])
        self.right_default = np.array([1.0, 0.0, 0.0, 0.0])

        self.eye_world = np.zeros(4)
        self.up_world = np.zeros(4)
        self.right_world = np.zeros(4)


    def init_orthographic(self, l, r, t, b, n, f):
        inv_r_m_l = 1.0/ (r - l)
        inv_t_m_b = 1.0 / (t - b)
        inv_n_m_f = 1.0 / (n - f)
        self.p[0][0] = 2 * inv_r_m_l
        self.p[0][3] = (r + l) * inv_r_m_l

        self.p[1][1] = 2 * inv_t_m_b
        self.p[1][3] = (t + b) * inv_r_m_l

        self.p[2][2] = 2 * inv_n_m_f
        self.p[2][3] = (f + n) * inv_n_m_f

        self.p[3][3] = 1
    def init_model_view(self):
        self.mv = np.zeros((4, 4))
        self.mv[0][0] = 1.0
        self.mv[1][1] = 1.0
        self.mv[2][2] = 1.0
        self.mv[3][3] = 1.0
        self.mv[2][3] = -2.5
        self.inv_mv = np.linalg.inv(self.mv)
    def look_at(self, center, eye, up):
        self.mv = np.zeros((4, 4), dtype=np.float32)
        self.eye = eye
        fwd = center - eye
        eye_dist = np.sqrt(np.dot(fwd, fwd))
        eye_dist_inv = 1.0 / eye_dist
        fwd = fwd * eye_dist_inv
        self.eye_orientation = fwd

        side = np.array([fwd[1] * up[2] -  up[1] * fwd[2], fwd[2] * up[0] - fwd[0] *  up[2], fwd[0] * up[1] -  up[0] * fwd[1]])
        up = np.array([side[1] * fwd[2] - side[2] * fwd[1], fwd[0] * side[2] - side[0] * fwd[2], side[0] * fwd[1] - side[1] * fwd[0]])

        self.mv[0][0:3] = side
        self.mv[1][0:3] = up
        self.mv[2][0:3] = -fwd

        for i in range(3):
            self.mv[i][3] = -np.dot(self.mv[i][0:3], eye)

        self.mv[3][3] = 1
        self.inv_mv = np.linalg.inv(self.mv)
        self.generate_transform()

    def generate_transform(self):
        self.mvp = np.zeros((4, 4))
        for i in range(3):
            self.mvp[i][:] = self.p[i][i] * self.mv[i][:]
        self.mvp[3][:] = self.p[3][2] * self.mv[2][:]
        self.mvp[:][3] = self.mvp[:][3] + self.p[:][3]
        print(self.mvp)
        self.inv_mvp = np.linalg.inv(self.mvp)
        print(self.inv_mvp)

        self.eye_world = self.inv_mv @ self.eye_default
        self.right_world = self.inv_mv @ self.right_default
        self.up_world = self.inv_mv @ self.up_default




