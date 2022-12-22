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

    def __init__(
        self, __engine: str, __env_datapath: str, __env: str, __creatures_datapath: str
    ) -> None:
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

    def render(self):
        raise NotImplementedError


class ChronoSimulation(Simulation):
    """Simulation class for `chrono`."""

    def __init__(
        self, __env_datapath: str, __env: str, __creatures_datapath: str
    ) -> None:
        super().__init__("chrono", __env_datapath, __env, __creatures_datapath)
        self.__time_step = 1e-3
        # FIXME use ChIrrApp to have a GUI and tweak parameters within rendering
        self.__renderer = chronoirr.ChVisualSystemIrrlicht()
        self.__is_over = False
        self.__creature = None
        self.__total_reward = 0.0

    def add_creature(self, creature_name: str):
        creature = self.generator.generate_creature(creature_name)
        creature.add_to_env(self.environment)
        self.__creature = creature

    def do_step(self):
        """
        Performs one step of the current simulation.
        """
        # FIXME Pseudocode for this method:
        # 1) Get observations from creature sensors (position, angles, CoM, etc.)
        # 2) Get action from brain/controller based on sensors input
        # 3) Apply action to environment
        # 4) Compute reward and add it to total reward/fitness
        # 5) Do timestep in environment
        # 6) Evaluate if simulation is over or not
        self.environment.DoStepDynamics(self.__time_step)
        self._evaluate_status()

    @property
    def is_over(self):
        return self.__is_over

    @property
    def total_reward(self):
        return self.__total_reward

    def _evaluate_status(self):
        # FIXME list conditions for the sim to be over here and
        # change self.__is_over accordingly
        #
        # e.g. max nb of steps reached, distance target reached, body
        # fell on the ground, etc.
        self.__is_over = False

    def render(self):
        logger.info("Setting up renderer")
        self._render_setup()
        logger.info("Rendering chrono simulation")
        while self.__renderer.Run():
            self.__renderer.BeginScene()
            self.__renderer.Render()
            self.__renderer.ShowInfoPanel(True)
            #  chronoirr.drawAllCOGs(self.__renderer, 2)  # Draw coord systems
            #  chronoirr.drawAllLinkframes(self.__renderer, 2)
            # chronoirr.drawAllLinks(self.__renderer, 2)
            # chronoirr.drawAllBoundingBoxes(self.__renderer)
            self.__renderer.EndScene()
            # FIXME do_step() shouldn't be done here, the method should just
            # render one time step. Use a boolean class attribute to control rendering
            self.do_step()

    def _render_setup(self):
        logger.info("Initializing chrono simulation")
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
