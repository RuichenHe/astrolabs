from scene_graph import Node, BillboardSet, ImageAtlas
import numpy as np
import math
import random
from OpenGL.GL import *
from gl_utils import check_GL_error


class Galaxy:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0.0
        self.selected = False
        self.name = ""
        self.tex_rect = np.array([0.0, 1.0, 1.0, 0.0], dtype=np.float32)

class GalaxySet(Node):  # Assuming Node is already defined
    def __init__(self, max_galaxy_count, max_image_count, max_visible_galaxies, galaxies_tex_unit, distance_labels_tex_unit):
        super().__init__()
        self.galaxy_size = 0.125
        self.global_scale = 1.0
        self.global_scale_min = 3.0
        self.global_scale_max = 21.0
        self.galaxy_image_w = 128
        self.galaxy_image_h = 128
        self.random_seed = 4910
        self.scale_rand_min = 0.4
        self.scale_rand_max = 1.0
        self.rand_scale_location = 0.1
        self.max_count = max_galaxy_count
        self.galaxy_info = [Galaxy() for _ in range(max_galaxy_count)]
        # Initialize galaxies_atlas and galaxies (assuming they are classes or methods)

        self.galaxies_atlas = ImageAtlas(galaxies_tex_unit, self.galaxy_image_w, self.galaxy_image_h, max_image_count)  # Assuming ImageAtlas is a class
        self.galaxies = BillboardSet(max_visible_galaxies)  # Assuming BillboardSet is a class

        # Shaders
        self.galaxies.vert_shader = "../assets/shaders/galaxy_set.vert"
        self.galaxies.frag_shader = "../assets/shaders/galaxy_set.frag"

        # Other properties
        self.galaxies.atlas_tex_unit = galaxies_tex_unit
        self.galaxies.global_opacity = 1.0

        # Quad dimensions
        self.galaxies.quad_height = self.galaxy_size
        self.galaxies.quad_width = self.galaxy_size
    def init_resources(self):
        if not self.galaxies.init_resources():
            return False
        if not self.galaxies_atlas.init_resources():
            return False
        return True
    
    def update_positions(self, t_normal, eye_x, eye_y):
        # Update global scale based on time normalization
        self.global_scale = self.global_scale_min + t_normal * self.global_scale_max

        self.galaxies.count = 0
        for i in range(self.max_count):
            print(self.galaxies.capacity)
            if self.galaxies.count >= self.galaxies.capacity:
                break

            # Example position calculation, replace with your logic
            x = self.galaxy_info[i].x - eye_x
            y = self.galaxy_info[i].y - eye_y

            # Wrap around logic (if needed)
            x = x - 1.0 if x > 0.5 else x + 1.0 if x < -0.5 else x
            y = y - 1.0 if y > 0.5 else y + 1.0 if y < -0.5 else y

            self.galaxies.info[self.galaxies.count].position = np.array([self.global_scale * x, self.global_scale * y, -1e-5 * i])
            self.galaxies.info[self.galaxies.count].scale = np.array([self.galaxy_info[i].scale_x, self.galaxy_info[i].scale_y])
            self.galaxies.info[self.galaxies.count].rotation = self.galaxy_info[i].rotation
            self.galaxies.info[self.galaxies.count].tex = self.galaxy_info[i].tex_rect

            self.galaxies.count += 1

        # Call to upload the billboard data to the GPU
        self.galaxies.upload_billboards()

    def generate_locations(self):
        rows = int(math.sqrt(self.max_count))
        cols = self.max_count // rows

        galaxy_ix = 0

        # Initialize Random Number Generator
        random.seed(self.random_seed)  # Assuming random_seed is defined in your class

        for j in range(rows):
            y = -0.5 + j / float(rows)

            for i in range(cols):
                x = -0.5 + i / float(cols)

                # Random location perturbation
                self.galaxy_info[galaxy_ix].x = x + random.uniform(-self.rand_scale_location, self.rand_scale_location)
                self.galaxy_info[galaxy_ix].y = y + random.uniform(-self.rand_scale_location, self.rand_scale_location)

                # Random scale
                scale = random.uniform(self.scale_rand_min, self.scale_rand_max)
                self.galaxy_info[galaxy_ix].scale_x = scale
                self.galaxy_info[galaxy_ix].scale_y = scale

                # Random rotation
                self.galaxy_info[galaxy_ix].rotation = random.uniform(0.0, 2 * math.pi)

                galaxy_ix += 1

    def update_texture_coordinates(self):
        random.seed(self.random_seed)  # Assuming random_seed is defined in your class

        for i in range(self.max_count):  # Assuming max_count is defined in your class
            map_ix = i

            # Generate the texture coordinates
            self.galaxy_info[i].tex_rect = self.galaxies_atlas.get_tile_coordinates(map_ix)

    def render(self, camera):
        glBindTexture(GL_TEXTURE_2D, self.galaxies_atlas.tex)

        self.galaxies.render(camera)