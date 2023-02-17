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


class Ground(chrono.ChBodyEasyBox):
    """
    Represents an instance of the ground, the base rigid body
    where creatures can walk on.
    """

    x_size = 100
    y_size = 5
    z_size = 20
    ground_material = chrono.ChMaterialSurfaceNSC()

    def __init__(self):
        super().__init__(
            Ground.x_size,
            Ground.y_size,
            Ground.z_size,
            4000,
            True,
            True,
            Ground.ground_material,
        )
        self.SetBodyFixed(True)
        self.SetPos(chrono.ChVectorD(0, -Ground.y_size / 2, 0))
        self.GetVisualShape(0).SetColor(chrono.ChColor(0.5, 0.7, 0.3))
