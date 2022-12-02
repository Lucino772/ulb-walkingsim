"""
3D PyChrono muscle-based walking simulator
File: environment.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for the complete physics system.
"""

import pychrono.core as chrono

import walkingsim.ground as ground


class Environment(chrono.ChSystemNSC):
    """
    Represents an instance of the simulation's
    physics, as a non-smooth mechanics system.
    """

    def __init__(self):
        super().__init__()
        self.Add(ground.Ground())
        self.Set_G_acc(chrono.ChVectorD(0, -9.81, 0))
        # TODO These params make an object fall..
        #  chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        #  chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)
