from manim.mobject.types.vectorized_mobject import VGroup
from manim.constants import *
from manim.utils.color import *
from manim.utils.space_ops import z_to_vector
from manim.mobject.geometry import Square
from .cube_utils import get_faces_of_cubie

import numpy as np


class Cubie(VGroup):
    position = np.array

    def __init__(self, x, y, z, dim, colors, size):
        self.dimensions = dim
        self.colors = colors
        self.position = np.array([x, y, z])
        self.faces = {}
        self.size = size

        # TODO: Be able to pass args from RubiksCube to Cubie that apply to the Squares, such as stroke_width
        super().__init__()

    def get_position(self):
        return self.position

    def get_rounded_center(self):
        return tuple(
            [round(self.get_x(), 3), round(self.get_y(), 3), round(self.get_z(), 3)]
        )

    def generate_points(self):
        faces = np.array(
            get_faces_of_cubie(
                self.dimensions, (self.position[0], self.position[1], self.position[2])
            )
        ).tolist()
        i = 0
        for vect in OUT, DOWN, LEFT, IN, UP, RIGHT:
            face = Square(
                side_length=self.size, shade_in_3d=True, stroke_width=3
            )
            if vect.tolist() in faces:
                face.set_fill(self.colors[i], 1)
            else:
                face.set_fill(BLACK, 1)

            face.flip()
            face.shift(OUT * self.size / 2)
            face.apply_matrix(z_to_vector(vect))

            self.faces[tuple(vect)] = face
            self.add(face)
            i += 1

    def get_face(self, face):
        if face == "F":
            return self.faces[tuple(LEFT)]
        elif face == "B":
            return self.faces[tuple(RIGHT)]
        elif face == "R":
            return self.faces[tuple(DOWN)]
        elif face == "L":
            return self.faces[tuple(UP)]
        elif face == "U":
            return self.faces[tuple(OUT)]
        elif face == "D":
            return self.faces[tuple(IN)]

    def init_colors(self):
        self.set_fill(
            color=self.fill_color or self.color, opacity=self.fill_opacity, family=False
        )
        self.set_stroke(
            color=self.stroke_color or self.color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
            family=False,
        )
        self.set_background_stroke(
            color=self.background_stroke_color,
            width=self.background_stroke_width,
            opacity=self.background_stroke_opacity,
            family=False,
        )

    def __repr__(self):
        return "Cubie({})".format(self.get_rounded_center())