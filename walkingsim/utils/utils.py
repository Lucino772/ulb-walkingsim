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

import pychrono as chrono


def distance(a, b):
    return math.sqrt(
        (a[0] + b[0]) ** 2 + (a[1] + b[1]) ** 2 + (a[2] + b[2]) ** 2
    )


class ChCustomTorqueFunction(chrono.ChFunction_SetpointCallback):
    def __init__(self, __timestep: float, __forces: list):
        super().__init__()
        self.__timestep = __timestep
        self.__forces = __forces
        self.__lasttime = 0
        self.__steps = 0

    def SetpointCallback(self, t: float):
        dt = t - self.__lasttime
        if dt >= self.__timestep:
            self.__lasttime = t
            self.__steps = (self.__steps + 1) % len(self.__forces)

        value = self.__forces[self.__steps]
        return value
