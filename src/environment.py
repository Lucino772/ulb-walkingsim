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
from pychrono import irrlicht as chronoirr


from ground import Ground
# from body import Body
#
# from muscle import Muscle
# from muscle import MuscleSystem
# from muscle import MuscleSystemSolver

from sphere import Sphere


class Environment(chrono.ChSystemNSC):
    """
    Represents an instance of the simulation's
    physics, as a non-smooth mechanics system.
    """

    def __init__(self):
        super().__init__()
        self.Add(Ground())
        # self.Add(Body())
        # self.Add(Sphere())

        # set sphere flying in the air at 100m height
        self.Add(Sphere())
        # self.Get_bodylist()[1].SetPos(chrono.ChVectorD(0, 100, 111110))
        # # self.Get_bodylist()[1].SetBodyFixed(False)
        # self.Get_bodylist()[1].SetMass(1111)
        # self.Get_bodylist()[1].SetInertiaXX(chrono.ChVectorD(1, 1, 1))
        # self.Get_bodylist()[1].SetPos_dt(chrono.ChVectorD(0, 0, 0))
        # self.Get_bodylist()[1].SetWvel_par(chrono.ChVectorD(0, 0, 0))
        # self.Get_bodylist()[1].SetPos_dtdt(chrono.ChVectorD(0, 0, 0))
        # self.Get_bodylist()[1].SetWacc_par(chrono.ChVectorD(0, 0, 0))
        # self.Get_bodylist()[1].SetNoSpeedNoAcceleration()
        # self.Get_bodylist()[1].SetNoForce()
        # self.Get_bodylist()[1].SetNoTorque()
        # self.Get_bodylist()[1].SetNoGravity()


        # self.Set_G_acc(chrono.ChVectorD(0, 0, 0))
        self.Set_G_acc(chrono.ChVectorD(0
                                        , -9.81
                                        , 0))
        # self.Set_G_acc(chrono.ChVectorD(0, 0, -9.81))
