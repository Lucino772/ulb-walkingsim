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


class SimVisualiser(chronoirr.ChVisualSystemIrrlicht):
    """
    Represents an instance of a visualiser for a given
    system/simulation.
    """

    def __init__(self, sys):
        super().__init__()
        self.sys = sys
        self.AttachSystem(self.sys)
        self.SetWindowSize(1024, 768)
        self.SetWindowTitle("3D muscle-based walking sim")
        self.Initialize()
        self.AddSkyBox()
        self.AddCamera(chrono.ChVectorD(0, 8, 12))
        self.AddTypicalLights()

    def run(self):
        """
        Runs the visuals loop for the instance's system.
        """

        while self.Run():
            self.BeginScene()
            self.Render()
            self.EndScene()
            self.sys.DoStepDynamics(1e-3)
            self.sys.GetCollisionSystem().Visualize(chrono.ChCollisionSystem.VIS_Shapes)
