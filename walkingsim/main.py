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

import environment
import visualiser


def main():
    print("api version : ", sys.api_version)
    # print chrono version
    # print(pychrono.version)

    env = environment.Environment()
    visuals = visualiser.Visualiser(env)
    visuals.run()


if __name__ == "__main__":
    main()
