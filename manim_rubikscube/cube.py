from manim.constants import PI
from manim.utils.color import *
from manim.mobject.mobject import Mobject
from manim.mobject.types.vectorized_mobject import VMobject
import numpy as np
from .cubie import Cubie
from kociemba import solver as sv


class RubiksCube(VMobject):
    # Each coordinate starts at 0 and goes to (Dimensions - 1)

    # Colors are in the order Up, Right, Front, Down, Left, Back
    def __init__(self, dim=3, colors=None, cubie_size=1.0):
        if not (dim >= 2):
            raise Exception("Dimension must be >= 2")

        VMobject.__init__(self)

        if colors is None:
            colors = [WHITE, "#B90000", "#009B48", "#FFD500", "#FF5900", "#0045AD"]

        self.dimensions = dim
        self.colors = colors
        self.cubie_size = cubie_size
        self.cubies = np.ndarray((dim, dim, dim), dtype=Cubie)
        self.generate_cubies()

        # Center around the origin
        self.shift(-self.cubie_size * (self.dim - 1) / 2)

        # Rotate so that under the default camera, F is really the front etc.
        self.rotate(axis=np.array([0, 0, 1]), angle=PI / 2)
        self.rotate(axis=np.array([1, 0, 0]), angle=-PI / 2)

    def generate_cubies(self):
        for x in range(self.dimensions):
            for y in range(self.dimensions):
                for z in range(self.dimensions):
                    cubie = Cubie(
                        x, y, z, self.dimensions, self.colors, self.cubie_size
                    )
                    cubie.shift(np.array((x, y, z), dtype=float) * self.cubie_size)
                    self.add(cubie)
                    self.cubies[x, y, z] = cubie

    def set_state(self, positions):
        colors = {
            "U": self.colors[0],
            "R": self.colors[1],
            "F": self.colors[2],
            "D": self.colors[3],
            "L": self.colors[4],
            "B": self.colors[5],
        }
        positions = list(positions)
        # TODO: Try/except in case a color was not given
        # try:
        for cubie in np.rot90(self.get_face("U", False), 2).flatten():
            cubie.get_face("U").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("R", False), (0, 1)), -1).flatten():
            cubie.get_face("R").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("F", False), 0)).flatten():
            cubie.get_face("F").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("D", False), 0), 2).flatten():
            cubie.get_face("D").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("L", False), 0)).flatten():
            cubie.get_face("L").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("B", False), (0, 1)), -1).flatten():
            cubie.get_face("B").set_fill(colors[positions.pop(0)], 1)
        # except:
        #     return

    def solve_by_kociemba(self, state):
        return sv.solve(state).replace("3", "'").replace("1", "").split()

    def get_face_slice(self, face):
        """
        Return a NumPy slice object specifying which part of the array corresponds
        to which face. NumPy sli indexing a ndarray,
        e.g. a[:, 2] == a[np.s_[:, 2]]
        """
        face_slices = {
            "F": np.s_[0, :, :],
            "B": np.s_[self.dimensions - 1, :, :],
            "U": np.s_[:, :, self.dimensions - 1],
            "D": np.s_[:, :, 0],
            "L": np.s_[:, self.dimensions - 1, :],
            "R": np.s_[:, 0, :],
        }

        if face in face_slices:
            return face_slices[face]
        else:
            raise ValueError("Invalid face identifier " + face)

    def get_face(self, face, flatten=True):
        face = self.cubies[self.get_face_slice(face)]

        if flatten:
            return face.flatten()
        else:
            return face
