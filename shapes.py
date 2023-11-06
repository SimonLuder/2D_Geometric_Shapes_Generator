import numpy as np
import cv2
import uuid
import os
import webcolors
import csv
from tqdm import tqdm

class AbstractShape:

    def __init__(self, destination: str, im_res: int, randomize=["radius", "rotation", "aspect_ratio","fill_color", "bg_color", "position"]):
        self.destination = destination
        self.im_res = im_res
        self.im_shape = (self.im_res, self.im_res, 3)
        self.randomize = randomize
        self.shape_name = None
        self.radius = None
        self.x = None
        self.y = None

    def __set_random_params(self):
        if "radius" in self.randomize:
            self.radius = np.random.randint(int(self.im_res * 0.05), int(self.im_res * 0.4))
        else: 
            self.radius = int(self.im_res * 0.25)
        if "rotation" in self.randomize:
            self.rotation = np.deg2rad(np.random.randint(-180, 180))
        else: 
            self.rotation = 0
        if "aspect_ratio" in self.randomize:
            self.aspect_ratio = np.random.randint(5, 20) / 10 # W / H ratio
        else: 
            self.aspect_ratio = 1
        if "fill_color" in self.randomize:
            self.fill_color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        else: 
            self.fill_color = (255, 255, 255)
        if "bg_color" in self.randomize:
            self.bg_color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        else: 
            self.bg_color = (0, 0, 0)
        if "position" in self.randomize:
            self.x, self.y = (
                np.random.randint(int(self.im_res * 0.1) + self.radius, 
                                int(self.im_res * 0.9) - self.radius),  # Centered x-coordinate
                np.random.randint(int(self.im_res * 0.1) + self.radius, 
                                int(self.im_res * 0.9) - self.radius),  # Centered y-coordinate
            )
        else:
            self.x, self.y = int(self.im_res * 0.5), int(self.im_res * 0.5)  # Centered x-coordinate

        
    def __save_drawing(self, image):
        filename = f"{self.__class__.__name__}_{uuid.uuid1()}.png"
        filepath = os.path.join(self.destination, filename)
        cv2.imwrite(filepath, image)
        return filename

    def __generate_prompt(self):
        prompt_parts = []

        if "fill_color" in self.randomize:
            prompt_parts.append(f"{self.get_color_name(self.fill_color)} colored")
        if self.shape_name is not None:
            prompt_parts.append(f"{self.shape_name}")
        if "radius" in self.randomize or "aspect_ratio" in self.randomize or "rotation" in self.randomize:
            prompt_parts.append("with")
        if "radius" in self.randomize:
            prompt_parts.append(f"radius {self.radius}")
        if "aspect_ratio" in self.randomize:
            prompt_parts.append(f"aspect ratio {self.aspect_ratio}")
        if "rotation" in self.randomize:
            prompt_parts.append(f"rotation {np.rad2deg(self.rotation):.0f} degrees")
        if "position" in self.randomize:
            prompt_parts.append(f"located at ({self.x}, {self.y})")
        if "bg_color" in self.randomize:
            prompt_parts.append(f"on a {self.get_color_name(self.bg_color)} background")
        prompt = ' '.join(prompt_parts)
        return prompt

    def get_fill_color(self):
        return self.fill_color
    
    def get_color_name(self, requested_colour):
        min_colours = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        closest_color = min_colours[min(min_colours.keys())]
        return closest_color
    
    def fill_background(self, canvas):
        canvas[:, :] = self.bg_color[::-1] # swapped red and blue channel in cv2!

    def generate(self):
        self.set_shape_name()
        self.__set_random_params()
        image = self.draw()
        filename = self.__save_drawing(image)
        prompt = self.__generate_prompt()
        return filename, prompt

    def rotate_shape(self, coordinates):
        r_coordinates = []
        for item in coordinates:
            r_coordinates.append(
                (
                    (item[0] - self.x) * np.cos(self.rotation) - (item[1] - self.y) * np.sin(self.rotation) + self.x,
                    (item[0] - self.x) * np.sin(self.rotation) + (item[1] - self.y) * np.cos(self.rotation) + self.y
                )
            )
        return r_coordinates
    
    def stretch_shape(self, coordinates):
        s_coordinates = []
        for item in coordinates:
            s_coordinates.append(
                (
                    (item[0] - self.x) * self.aspect_ratio + self.x,
                    item[1]
                )
            )
        return s_coordinates
        

    def draw(self):
        shape_coordinates = self.get_shape_coordinates()
        r_coordinates = []
        for coordinates in shape_coordinates:
            # strech shape
            coordinates = self.stretch_shape(coordinates)
            # rotate shape
            r_coordinates.append(self.rotate_shape(coordinates))
        canvas = np.zeros(self.im_shape, dtype=np.uint8)
        self.fill_background(canvas)
        self.paint(canvas, r_coordinates)
        return canvas

    def paint(self, canvas):
        raise NotImplementedError()
    
    def set_shape_name(self):
        raise NotImplementedError()
    

    
    

class AbstractPolygonShape(AbstractShape):

    def paint(self, canvas, coordinates):
        points = []
        for coord in coordinates:
            p = np.array(coord, np.int32)
            p = p.reshape((-1, 1, 2))
            points.append(p)
        
        cv2.fillPoly(canvas, points, self.get_fill_color()[::-1]) # swapped red and blue channel in cv2!

    

class Triangle(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "triangle"

    def get_shape_coordinates(self):
        return [[(self.x, self.y - self.radius), (self.x - self.radius, self.y + self.radius), (self.x + self.radius, self.y + self.radius)]]

class Square(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "square"

    def get_shape_coordinates(self):
        half_side = self.radius / np.sqrt(2)
        return [[
            (self.x - half_side, self.y - half_side),
            (self.x + half_side, self.y - half_side),
            (self.x + half_side, self.y + half_side),
            (self.x - half_side, self.y + half_side)
        ]]

class Pentagon(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "pentagon"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(5):
            x = self.radius * np.cos(2 * np.pi * vertex / 5) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 5) + self.y
            coordinates.append((x, y))
        return [coordinates]

class Hexagon(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "hexagon"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(6):
            x = self.radius * np.cos(2 * np.pi * vertex / 6) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 6) + self.y
            coordinates.append((x, y))
        return [coordinates]

class Heptagon(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "heptagon"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(7):
            x = self.radius * np.cos(2 * np.pi * vertex / 7) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 7) + self.y
            coordinates.append((x, y))
        return [coordinates]

class Octagon(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "octagon"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(8):
            x = self.radius * np.cos(2 * np.pi * vertex / 8) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 8) + self.y
            coordinates.append((x, y))
        return [coordinates]

class Nonagon(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "nonagon"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(9):
            x = self.radius * np.cos(2 * np.pi * vertex / 9) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 9) + self.y
            coordinates.append((x, y))
        return [coordinates]


class Circle(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "circle"

    def get_shape_coordinates(self):
        coordinates = []
        for vertex in range(200):
            x = self.radius * np.cos(2 * np.pi * vertex / 200) + self.x
            y = self.radius * np.sin(2 * np.pi * vertex / 200) + self.y
            coordinates.append((x, y))
        return [coordinates]
    

class Star(AbstractPolygonShape):

    def set_shape_name(self):
        self.shape_name = "star"

    def get_shape_coordinates(self):
        inner_coordinates = []
        outer_coordinates = []
        for vertex in range(6):
            x1 = 0.6 * self.radius * np.cos(2 * np.pi * vertex / 5) + self.x
            y1 = 0.6 * self.radius * np.sin(2 * np.pi * vertex / 5) + self.y
            inner_coordinates.append((x1, y1))
            outer_coordinates.append((x1, y1))

            x2 = self.radius * np.cos(2 * np.pi * (vertex + 0.5) / 5) + self.x
            y2 = self.radius * np.sin(2 * np.pi * (vertex + 0.5) / 5) + self.y
            outer_coordinates.append((x2, y2))

        return [outer_coordinates, inner_coordinates]
    

class GeometricShapes:

    __GENERATORS__ = [
        Triangle, Circle, Heptagon, Octagon, Hexagon, Square,
        Nonagon, Pentagon, Star
    ]

    def __init__(self, destination: str, class_size: int, img_res: int=200, randomize=["radius", "rotation", "fill_color", "bg_color", "position"]):
        self.__size__ = class_size
        self.destination = destination
        self.__shapes = [
            generator(destination, img_res, randomize) for generator in self.__GENERATORS__
        ]
        self.prompts = list()

    def __save_csv(self):
        with open(os.path.join(self.destination, 'prompts.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerows(self.prompts)
        
    def generate(self):
        for _ in tqdm(range(self.__size__)):
            for shape in self.__shapes:
                self.prompts.append(shape.generate())

        self.__save_csv()

            