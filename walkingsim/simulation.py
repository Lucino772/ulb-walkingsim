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
    :var creature: The creature in the simulation
    :var genome: The genome of the creature
    """

    def __init__(
        self, __engine: str, __env_datapath: str, __env: str, __creatures_datapath: str, __visualize: bool = False
    ) -> None:
        self.__engine = __engine
        self.__loader = EnvironmentLoader(__env_datapath, self.__engine)
        self._visualize = __visualize
        self.__environment = self.__loader.load_environment(__env)

        self.__generator = CreatureGenerator(__creatures_datapath, self.__engine)

        self.__creature = None
        self.__genome = None

    def add_creature(self, creature_name: str, genome: dict = None):
        # FIXME: This function can be removed and done in the __init__ method
        if self.__creature is not None:
            logger.error("Cannot add a new creature to the simulation, one already exists !")
            raise RuntimeError("Creature already exists in simulation")

        # FIXME: Pass the genome when creating the creature
        creature = self.generator.generate_creature(creature_name)
        creature.add_to_env(self.environment)
        self.__creature = creature
        self.__genome = genome
        logger.debug(f"Creature '{creature}' added to the simulation")

    @property
    def environment(self):
        return self.__environment

    @property
    def generator(self):
        return self.__generator

    @property
    def creature(self):
        return self.__creature

    @property
    def genome(self):
        return self.__genome

    def run(self):
        raise NotImplementedError


class ChronoSimulation(Simulation):
    """Simulation class for `chrono`."""

    def __init__(
        self, __env_datapath: str, __env: str, __creatures_datapath: str, __visualize: bool = False
    ) -> None:
        super().__init__("chrono", __env_datapath, __env, __creatures_datapath, __visualize)
        self.__time_step = 1e-2
        self.__renderer = None
        if self._visualize == True:
            # FIXME use ChIrrApp to have a GUI and tweak parameters within rendering
            self.__renderer = chronoirr.ChVisualSystemIrrlicht()

    # Visualize
    def _render_setup(self):
        logger.info("Initializing chrono simulation renderer")
        self.__renderer.AttachSystem(self.environment)
        self.__renderer.SetWindowSize(1024, 768)
        self.__renderer.SetWindowTitle("3D muscle-based walking sim")
        self.__renderer.Initialize()
        self.__renderer.AddSkyBox()
        self.__renderer.AddCamera(chrono.ChVectorD(2, 10, 3))
        #  self.__renderer.AddLight(chrono.ChVectorD(0, 10, -20), 1000)
        self.__renderer.AddTypicalLights()

    def _render_step(self):
        logger.debug("Rendering step in chrono simulation")
        self.__renderer.BeginScene()
        self.__renderer.Render()
        self.__renderer.ShowInfoPanel(True)
        #  chronoirr.drawAllCOGs(self.__renderer, 2)  # Draw coord systems
        #  chronoirr.drawAllLinkframes(self.__renderer, 2)
        # chronoirr.drawAllLinks(self.__renderer, 2)
        # chronoirr.drawAllBoundingBoxes(self.__renderer)
        self.__renderer.EndScene()

    # Run Simulation
    def _evaluate(self):
        """This function returns wether or not the simulation is done, and the
        result (fitness) of this simulation.
        """
        # FIXME Pseudocode for this method:
        # 1) Get observations from creature sensors (position, angles, CoM, etc.)
        # 2) Get action from brain/controller based on sensors input
        # 3) Apply action to environment
        # 4) Compute reward and add it to total reward/fitness
        # 5) Do timestep in environment
        # 6) Evaluate if simulation is over or not
        sensor_data = self.creature.sensor_data
        if len(sensor_data) > 0:
            print(sensor_data[-1]['position'], sensor_data[-1]['distance'], sensor_data[-1]['total_distance'])

        # TODO: Using those sensor data, we could calculate som fitness value
        return False, 0

    def do_run(self):
        is_over = self._evaluate()[0]
        if self._visualize:
            return self.__renderer.Run()

        return is_over

    def run(self):
        logger.info("Starting simulation")
        if self._visualize:
            self._render_setup()

        try:
            while self.do_run():
                if self._visualize:
                    self._render_step()

                self.creature.capture_sensor_data()
                self.environment.DoStepDynamics(self.__time_step)
        except KeyboardInterrupt:
            logger.info("Simulation was stopped by user")

        return self._evaluate()[1]