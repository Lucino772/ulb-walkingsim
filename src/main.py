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
    # Ground rigid body
    ground = chrono.ChBody()
    ground.SetBodyFixed(True)
    # Ground collision shape
    ground.GetCollisionModel().ClearModel()
    ground_material = chrono.ChMaterialSurfaceNSC()
    ground.GetCollisionModel().AddBox(
        ground_material, 10, 0.5, 10, chrono.ChVectorD(0, -1, 0)
    )
    ground.GetCollisionModel().BuildModel()
    ground.SetCollide(True)

    sys.Add(ground)

    # Box shape for the ground
    boxground = chrono.ChBoxShape()
    boxground.GetBoxGeometry().Size = chrono.ChVectorD(10, 0.5, 3)
    boxground.SetColor(chrono.ChColor(0.5, 0.7, 0.5))
    ground.AddVisualShape(
        boxground, chrono.ChFrameD(chrono.ChVectorD(0, -1, 0), chrono.QUNIT)
    )

    # Simulation
    visuals = visualiser.SimVisualiser(sys)
    visuals.run()


if __name__ == "__main__":
    main()
