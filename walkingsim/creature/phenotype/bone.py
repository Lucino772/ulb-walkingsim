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


class Bone(chrono.ChBodyEasyBox):
    """
    Representing an instance of a creature "bone", which consists of a
    standard rigid body part, connected to other body parts with joints.
    """

    bone_material = chrono.ChMaterialSurfaceNSC()

    def __init__(self, dimensions, pos):
        super().__init__(*dimensions, 1000, True, True, Bone.bone_material)
        self.SetBodyFixed(False)
        self.SetPos(pos)
        self.dimensions = dimensions
        self.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.5))
