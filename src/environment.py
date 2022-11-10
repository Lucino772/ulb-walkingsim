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

from ground import Ground


class Environment(chrono.ChSystemNSC):
    """
    Represents an instance of the simulation's
    physics, as a non-smooth mechanics system.
    """

    def __init__(self):
        super().__init__()
        self.Add(Ground())
