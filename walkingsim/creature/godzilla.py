"""
3D PyChrono muscle-based walking simulator
File: godzilla.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for godzilla creature.
"""
import math
import typing as t

from walkingsim.creature.creature import Creature, _CreatureBody


class Godzilla(Creature):
    """Class for a basic godzilla."""

    _CREATURE_HEIGHT = 1.65
    _CREATURE_MOTORS = 8

    def __init__(
        self, body_cls: t.Type[_CreatureBody], root_pos: tuple = None
    ) -> None:
        super().__init__(body_cls, (0.5, 0.5, 1), root_pos)

    def create(self):
        # Body
        upper_body = self.root.branch(
            size=(0.5, 0.7, 0.7), relpos=(0, 0.6, 0)
        ).join(
            relpos=(0, -0.7 / 2, 0),
        ).branch(
            size=(0.5, 0.5, 1.5), relpos=(0, 0.6, 0)
        ).join(
            relpos=(0, 0.5 / 2, 0)
        )

        # Arms
        yoffset = (-upper_body.size[1] / 2) + 0.01
        for i, zfactor in enumerate([1, -1], start=1):
            z = upper_body.size[2] * zfactor / 2
            upper_body.branch(
                size=(0.3, 0.7, 0.15), relpos=(0, yoffset, z)
            ).join(
                relpos=(0, 0.7 / 2, 0),
                constraints_z=[-math.pi / 3, math.pi / 3],
                motor="torque"
            ).branch(
                size=(0.3, 0.7, 0.15), relpos=(0, -0.7, 0)
            ).join(
                relpos=(0, 0.7 / 2, 0),
                constraints_z=[-math.pi / 2, 0.05],
                motor="torque"
            )

        # Legs
        yoffset = (-self.root.size[1] / 2) + 0.01
        for i, zfactor in enumerate([1, -1], start=1):
            z = self.root.size[2] * zfactor / 2
            (
                self.root.branch(
                    size=(0.3, 0.7, 0.15), relpos=(0, yoffset, z)
                )  # top leg
                # .collision(family=self.root.family+i, nocollision=[self.root.family])
                .join(
                    relpos=(0, 0.7 / 2, 0),
                    constraints_z=[-math.pi / 3, math.pi / 3],
                    motor="torque",
                )
                .branch(
                    size=(0.3, 0.7, 0.15), relpos=(0, -0.7, 0)
                )  # bottom leg
                .join(
                    relpos=(0, 0.7 / 2, 0),
                    constraints_z=[-0.05, math.pi / 2],
                    motor="torque",
                )
                .branch(size=(0.4, 0.1, 0.4), relpos=(0, -0.4, 0))  # foot
                .join(relpos=(0, 0.1 / 2, 0))
            )
