"""
3D PyChrono muscle-based walking simulator
File: main.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Program entry point. Builds the physics system
    and launches the visualiser.
"""
import sys

import pychrono
from pychrono import *

from environment import Environment
from visualiser import Visualiser


def main():
    print("api version : ", sys.api_version)
    # print chrono version
    # print(pychrono.version)

    environment = Environment()
    visuals = Visualiser(environment
                         )
    visuals.run()


if __name__ == "__main__":
    main()
