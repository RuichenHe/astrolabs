import math
import numpy as np

class OrbitPiece:
    def __init__(self):
        self.t = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.r = 0
        self.area = 0
        self.v_x = 0
        self.v_y = 0

    def set(self, t_in, x_in, y_in, v_x_in, v_y_in, theta_in, area_in):
        self.t = t_in
        self.x = x_in
        self.y = y_in
        self.theta = theta_in
        self.r = math.sqrt(x_in * x_in + y_in * y_in)
        self.area = area_in
        self.v_x = v_x_in
        self.v_y = v_y_in

    def __str__(self):
        return f"{self.t} {self.x} {self.y} {self.theta} {self.v_x} {self.v_y} {self.r}\n"

class Orbit:
    def __init__(self, steps_max=100000, sub_steps=10):
        self.dr_terminate_ = 0.0001
        self.R_sun_sq_ = 0.01
        self.closed_ = False
        self.collision_ = False
        self.passed_zero_ = False

        self.G_ = 4 * math.pi * math.pi
        self.velocity_scale_ = 2.0 * math.pi / 30.0
        self.dt_ = 1.0 / 365.25

        self.elements_ = [OrbitPiece() for _ in range(steps_max)]

        self.element_count_ = 0

        self.steps_max_ = steps_max
        self.sub_steps_ = sub_steps

        self.t_ = 0
        self.t_max_ = 0

    def calculate_force(self, r):
        r_ab_dist = np.sqrt(np.sum(np.power(r, 2)))

        scale = self.G_ / (r_ab_dist ** 3)

        a = -r * scale
        print(a)
        return a
    
    def test_terminate(self, element_ix):
        element = self.elements_[element_ix]
        x = element.x
        y = element.y

        # Check if we hit the earth
        dr_sq_center = x * x + y * y

        # If planet impacted
        self.collision_ = dr_sq_center < self.R_sun_sq_

        if self.passed_zero_:
            dx = self.elements_[0].x - x
            dy = self.elements_[0].y - y
            dz = 0.0  # Assuming z is always zero or not used
            dr_sq = dx * dx + dy * dy + dz * dz

            # Check if we finished the orbit
            self.closed_ = dr_sq < self.dr_terminate_
        
        terminate_type = None
        if self.collision_:
            terminate_type = "Collision"
        if self.closed_:
            terminate_type = "Closed"

        return self.collision_  or self.closed_, terminate_type
    
    def calculate_orbit(self, theta_launch_0, v_0):
        nd = 2

        # Clear state
        self.closed_ = False
        self.collision_ = False
        self.passed_zero_ = False

        a = np.array([0.0, 0.0])
        a_prev = np.array([0.0, 0.0])
        v = np.array([v_0 * self.velocity_scale_ * math.cos(theta_launch_0),
                      v_0 * self.velocity_scale_ * math.sin(theta_launch_0)])
        r = np.array([0.0, 1.0])

        self.element_count_ = 0
        self.t_ = 0

        dt_substep = self.dt_ / float(self.sub_steps_)
        a = self.calculate_force(r)
        terminate_type = None
        for step in range(self.steps_max_):
            for sub_step in range(self.sub_steps_):
                theta = math.atan2(r[1], r[0])

                # Assuming set method of OrbitPiece class
                self.elements_[self.element_count_].set(self.t_, r[0], r[1], theta, v[0], v[1], 0.0)

                # Integrate to new position
                for i in range(nd):
                    a_prev[i] = a[i]
                    r[i] += v[i] * dt_substep + 0.5 * a[i] * dt_substep ** 2

                a = self.calculate_force(r)

                for i in range(nd):
                    v[i] += 0.5 * (a[i] + a_prev[i]) * dt_substep

                self.t_ += dt_substep

            self.passed_zero_ = self.passed_zero_ or r[1] < 0.0

            terminate, terminate_type = self.test_terminate(self.element_count_)
            if terminate:
                break
            self.element_count_ += 1

        self.t_max_ = self.elements_[self.element_count_ - 1].t
        return terminate_type == "Collision"

