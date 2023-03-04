"""
3D PyChrono muscle-based walking simulator
File: quadrupede.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for basic quadruped creature.
"""
import math

from walkingsim.creature.creature import Creature, Vector


class Quadrupede(Creature):
    """Class for a basic quadrupede."""

    def __init__(self, pos: Vector) -> None:
        super().__init__(root_size=Vector(1.0, 0.5, 0.5), root_pos=pos)

    def create(self):
        yoffset = 0.1
        xoffset = 0.2

        for xfactor, zfactor in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x = (self.root.size.x * xfactor / 2) + (xoffset * -xfactor)
            z = self.root.size.z * zfactor / 2
            (
                self.root.branch(size=Vector(0.3, 0.7, 0.15))  # top leg
                .join(
                    relative_pos=Vector(x, yoffset, z),
                    constraints_z=[-math.pi / 3, math.pi / 3],
                    motor="torque",
                )
                .branch(size=Vector(0.3, 0.7, 0.15))  # bottom leg
                .join(constraints_z=[-0.05, math.pi / 2], motor="torque")
                .branch(size=Vector(0.4, 0.1, 0.4))  # foot
                .join()
            )
