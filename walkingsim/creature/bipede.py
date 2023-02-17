"""
3D PyChrono muscle-based walking simulator
File: quadrupede.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for basic bipede creature.
"""

from walkingsim.creature.creature import CreatureSuperClass as Creature


class Bipede(Creature):
    """
    Class for a basic bipede.

    Class attributes:
        collision_family
        trunk_dimensions
        legs_dimensions

    Attributes:
        joints
        bodies
        sensor_data
    """

    # _upper_legs_dimensions = (0.3, 0.7, 0.15)
    # _lower_legs_dimensions = (0.3, 0.7, 0.15)

    def __init__(self, pos: tuple) -> None:
        super().__init__(pos)

    def _create_legs(self):
        x_trunk = self.pos.x
        x_back_legs = x_trunk - 0.8 * (self.trunk_dim[0] / 2)

        y_trunk = self.pos.y
        y_legs = y_trunk - 1.8 * (self.trunk_dim[1] / 2)

        z_trunk = self.pos.z
        z_left_legs = z_trunk + (self.trunk_dim[2] / 2)
        z_right_legs = z_trunk - (self.trunk_dim[2] / 2)

        self._create_single_leg(x_back_legs, y_legs, z_left_legs)
        self._create_single_leg(x_back_legs, y_legs, z_right_legs)
