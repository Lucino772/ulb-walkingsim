"""
3D PyChrono muscle-based walking simulator
File: visualiser.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for the simulation visualisation.
"""
import pychrono.core as chrono
import pychrono.irrlicht as chronoirr


class Visualiser(chronoirr.ChVisualSystemIrrlicht):
    """
    Represents an instance of a visualiser for a given
    system/simulation.
    """

    def __init__(self, sys):
        super().__init__()
        self._sys = sys
        self.AttachSystem(self._sys)
        self.SetWindowSize(1024, 768)
        self.SetWindowTitle("3D muscle-based walking sim")
        self.Initialize()
        self.AddSkyBox()
        self.AddCamera(chrono.ChVectorD(0, 20, -80))
        self.AddLight(chrono.ChVectorD(0, 10, -20), 1000)

    def run(self):
        """
        Runs the visuals loop for the instance's system.
        """

        while self.Run():
            self.BeginScene()
            self.Render()
            self.EndScene()
            self._sys.DoStepDynamics(1e-3)
            self._sys.GetCollisionSystem().Visualize(
                chrono.ChCollisionSystem.VIS_Shapes
            )
