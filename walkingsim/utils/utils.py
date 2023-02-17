"""
3D PyChrono muscle-based walking simulator
File: utils.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Utility functions.
"""

import math
from copy import deepcopy

import pychrono as chrono


def distance(a, b):
    return math.sqrt(
        (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2 + (a[2] + b[2]) ** 2
    )


class CustomTorqueFunction(chrono.ChFunction):
    def __init__(self, forces: list):
        super().__init__()
        self.__forces = forces

    def Clone(self):
        return deepcopy(self)

    def Get_y(self, x):
        # We want to keep x between 0 and len(self.__forces) - 1
        # => run a cycle multiple times
        x = int(x) % len(self.__forces)
        return self.__forces[x]
