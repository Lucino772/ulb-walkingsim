"""
3D PyChrono muscle-based walking simulator
File: simulation.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Classes for the simulations
"""

import abc

from walkingsim.environment import EnvironmentLoader
from walkingsim.creature.generator import CreatureGenerator
from loguru import logger


import pychrono as chrono
import pychrono.irrlicht as chronoirr


class Simulation(abc.ABC):
    """Abstract class used to create simulations. This class is used by
    `ChronoSimulation`.

    This class initiates the `EnvironmentLoader` and the `CreatureGenerator`
    for the given engine. It also loads the given environment.

    :var environment: The environment system specific to the engine
    :var generator: The creature generator specific to the engine
    """

    def __init__(self, __engine: str, __env_datapath: str, __env: str, __creatures_datapath: str) -> None:
        self.__engine = __engine
        self.__loader = EnvironmentLoader(__env_datapath, self.__engine)
        self.__environment = self.__loader.load_environment(__env)

        self.__generator = CreatureGenerator(__creatures_datapath, self.__engine)

    @property
    def environment(self):
        return self.__environment

    @property
    def generator(self):
        return self.__generator

    def init(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class ChronoSimulation(Simulation):
    """Simulation class for `chrono`. This classes creates an irrlicht 
    visualizer and attach the `chrono` system to the visualizer.
    """

    def __init__(self, __env_datapath: str, __env: str, __creatures_datapath: str) -> None:
        super().__init__('chrono', __env_datapath, __env, __creatures_datapath)
        self.__renderer = chronoirr.ChVisualSystemIrrlicht()

    def init(self):
        logger.info('Initializing chrono simulation')
        self.__renderer.AttachSystem(self.environment)
        self.__renderer.SetWindowSize(1024, 768)
        self.__renderer.SetWindowTitle("3D muscle-based walking sim")
        # todo ? self.__renderer.SetWindowTitle("3D actuator-based
        #  walking sim")
        self.__renderer.Initialize()
        self.__renderer.AddSkyBox()
        self.__renderer.AddCamera(chrono.ChVectorD(2, 10, 3))
        #  self.__renderer.AddLight(chrono.ChVectorD(0, 10, -20), 1000)
        self.__renderer.AddTypicalLights()

    def run(self):
        logger.info('Running chrono simulation')
        while self.__renderer.Run():
            self.__renderer.BeginScene()
            self.__renderer.Render()
            self.__renderer.ShowInfoPanel(True)
            #  chronoirr.drawAllCOGs(self.__renderer, 2)  # Draw coord systems
            #  chronoirr.drawAllLinkframes(self.__renderer, 2)
            # chronoirr.drawAllLinks(self.__renderer, 2)
            # chronoirr.drawAllBoundingBoxes(self.__renderer)
            self.__renderer.EndScene()
            self.environment.DoStepDynamics(1e-3)
