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
import pychrono.irrlicht as chronoirr

def main():
    # Non-smooth mechanics
    sys = chrono.ChSystemNSC()
    mat = chrono.ChMaterialSurfaceNSC()
    ground = chrono.ChBodyEasyBox(10, 1, 10, 100, True, True, mat)
    ground.SetBodyFixed(True);
    ground.SetPos(chrono.ChVectorD(0, 0, 0))
    sys.AddBody(ground)
    

    # Create the Irrlicht visualization
    vis = chronoirr.ChVisualSystemIrrlicht()
    vis.AttachSystem(sys)
    vis.SetWindowSize(1024,768)
    vis.SetWindowTitle('3D muscle-based walking sim')
    vis.Initialize()
    vis.AddSkyBox()
    vis.AddCamera(chrono.ChVectorD(0, 8 , 6))
    vis.AddTypicalLights()

    #  Run the simulation
    while vis.Run():
        vis.BeginScene() 
        vis.Render()
        vis.EndScene()
        sys.DoStepDynamics(1e-3)
        sys.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)

if __name__ == "__main__":
    main()
