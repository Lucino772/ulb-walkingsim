"""
3D PyChrono muscle-based walking simulator
File: body.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Class for the body system.
"""

import pychrono.core as chrono


class Sphere(chrono.ChBody):
    """
    Represents an instance of spheric rigid body
    """

    def __init__(self):
        super().__init__()
        self.SetBodyFixed(False)
        # self.SetBodyFixed(True)
        self._set_collision_shape()
        self._set_sphere_shape()
        # set mass
        self.SetMass(111)

    def _set_collision_shape(self):
        self.GetCollisionModel().ClearModel()
        ground_material = chrono.ChMaterialSurfaceNSC()

        # self.GetCollisionModel().AddBox(ground_material
        #                                 , 1
        #                                 # , 0.5
        #                                 , 1
        #                                 , 1
        #                                 , chrono.ChVectorD(0
        #                                                    , -1
        #                                                    , 0)
        # )

        # add a sphere
        self.GetCollisionModel().AddSphere(ground_material
                                           , 0.5
                                           , chrono.ChVectorD(0
                                                              , 0
                                                              , 0)
                                           )
        #


        # self.GetCollisionModel().AddBox(ground_material
        #                                 , 10
        #                                 , 0.5
        #                                 , 10
        #                                 , chrono.ChVectorD(0
        #                                                    , -1
        #                                                    , 0
        #                                                    )
        #                                 )

        self.GetCollisionModel().BuildModel()
        #
        self.SetCollide(True)

    # set sphere shape
    def _set_sphere_shape(self):
        sphereground = chrono.ChSphereShape()
        sphereground.GetSphereGeometry().rad = 0.5
        # color rgb set dark blue
        sphereground.SetColor(chrono.ChColor(0.1
                                             , 0.1
                                             , 0.5))

        self.AddVisualShape(sphereground
                            , chrono.ChFrameD(chrono.ChVectorD(0
                                                               , 10
                                                               , 0)
                                              , chrono.QUNIT)
        )
