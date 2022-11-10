"""
3D PyChrono muscle-based walking simulator
File: ground.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for the ground rigid body.
"""

import pychrono.core as chrono


class Ground(chrono.ChBody):
    """
    Represents an instance of the ground, the base rigid body
    where creatures can walk on.
    """

    def __init__(self):
        super().__init__()
        self.SetBodyFixed(True)
        self._set_collision_shape()
        self._set_box_shape()

    def _set_collision_shape(self):
        self.GetCollisionModel().ClearModel()
        ground_material = chrono.ChMaterialSurfaceNSC()
        self.GetCollisionModel().AddBox(
            ground_material, 10, 0.5, 10, chrono.ChVectorD(0, -1, 0)
        )
        self.GetCollisionModel().BuildModel()
        self.SetCollide(True)

    def _set_box_shape(self):
        boxground = chrono.ChBoxShape()
        boxground.GetBoxGeometry().Size = chrono.ChVectorD(10, 0.5, 3)
        boxground.SetColor(chrono.ChColor(0.5, 0.7, 0.5))
        self.AddVisualShape(
            boxground, chrono.ChFrameD(chrono.ChVectorD(0, -1, 0), chrono.QUNIT)
        )
