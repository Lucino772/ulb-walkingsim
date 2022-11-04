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

import pychrono.core as chrono
import visualiser


def main():
    # Non-smooth mechanics physics system
    sys = chrono.ChSystemNSC()
    # Simulation
    visuals = visualiser.SimVisualiser(sys)
    visuals.run()


if __name__ == "__main__":
    main()
