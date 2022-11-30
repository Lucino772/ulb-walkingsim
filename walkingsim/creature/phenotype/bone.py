"""
3D PyChrono muscle-based walking simulator
File: bone.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for a creature bone.
"""

import pychrono as chrono


class Bone(chrono.ChBody):
    def __init__(self, dimensions):
        super().__init__()
        self.dimensions = dimensions
        self._set_collision_shape()
        self._set_box_shape()

    def _set_collision_shape(self):
        self.GetCollisionModel().ClearModel()
        material = chrono.ChMaterialSurfaceNSC()
        self.GetCollisionModel().AddBox(
            material, *self.dimensions, chrono.ChVectorD(0, 20, 0)
        )
        self.GetCollisionModel().BuildModel()
        self.SetCollide(True)

    def _set_box_shape(self):
        boxground = chrono.ChBoxShape()
        boxground.GetBoxGeometry().Size = chrono.ChVectorD(*self.dimensions)
        boxground.SetColor(chrono.ChColor(0.5, 0.7, 0.5))
        self.AddVisualShape(
            boxground, chrono.ChFrameD(chrono.ChVectorD(0, 20, 0), chrono.QUNIT)
        )
