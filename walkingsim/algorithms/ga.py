import copy

import numpy as np
import pygad as pygad_
import tqdm
from loguru import logger

from walkingsim.simulation.ga import GA_Simulation
from walkingsim.utils.data_manager import DataManager
from walkingsim.utils.pygad_config import PygadConfig


class GeneticAlgorithm:
    """
    crossover_type: uniform | single_point | two_points | random
    mutation_type: adaptive | random
    """

    _dm_group = "ga"

    def __init__(
        self,
        config: PygadConfig,
        env_props: dict,
        creature: str = "quadrupede",
        visualize: bool = False,
        ending_delay: int = 0,
        best_solution=None,
    ):
        self._dm = DataManager(self._dm_group)
        config_dict = config._asdict()
        self._dm.save_log_file(
            "pygad_config.csv", list(config_dict.keys()), config_dict
        )

        self.data_log = []
        self._env_props = env_props
        self._visualize = visualize
        self._simulation = GA_Simulation(
            env_props=self._env_props,
            creature=creature,
            visualize=self._visualize,
            ending_delay=ending_delay,
        )

        self.sim_data = {
            "config": config,
            "best_fitness": 0,
            "best_solution": best_solution,
            "solutions": None,
            "creature": creature,
            "env": env_props,
        }

        self.ga = pygad_.GA(
            # Population & generations settings
            initial_population=config.initial_population,
            sol_per_pop=config.population_size,
            num_generations=config.num_generations,
            num_genes=self._simulation.creature_shape
            * self._simulation.genome_discrete_intervals,
            # Evolution settings
            num_parents_mating=config.num_parents_mating,
            mutation_percent_genes=config.mutation_percent_genes,
            parent_selection_type=config.parent_selection_type,
            crossover_type=config.crossover_type,
            mutation_type=config.mutation_type,
            keep_elitism=config.keep_elitism,
            # Execution settings
            parallel_processing=config.parallel_processing,
            save_solutions=config.save_solutions,
            # Space
            init_range_low=config.init_range_low,
            init_range_high=config.init_range_high,
            random_mutation_min_val=config.random_mutation_min_val,
            random_mutation_max_val=config.random_mutation_max_val,
            # Callbacks
            fitness_func=self.fitness_function,
            on_crossover=self.on_crossover,
            on_mutation=self.on_mutation,
            on_generation=self._on_generation,
            on_stop=self.on_stop,
        )

        self.progress_gens = tqdm.tqdm(
            total=config.num_generations,
            desc="Generations",
            leave=False,
            position=1,
        )

        self.progress_sims = tqdm.tqdm(
            total=self.ga.sol_per_pop,
            desc=f"({self.ga.generations_completed}) Fitness",
            leave=False,
            position=0,
        )

    def on_crossover(self, ga_instance, offspring_crossover):
        self.progress_sims.reset(len(offspring_crossover))
        self.progress_sims.set_description(
            f"({self.ga.generations_completed}) Crossover"
        )

    def on_mutation(self, ga_instance, offspring_mutation):
        self.progress_sims.reset(len(offspring_mutation))
        self.progress_sims.set_description(
            f"({self.ga.generations_completed}) Mutation"
        )

    def _on_generation(self, ga_instance):
        self.progress_gens.update(1)

    def on_stop(self, ga_instance, last_population_fitness):
        self.progress_sims.reset(
            len(self.ga.last_generation_offspring_mutation)
        )
        self.progress_sims.set_description(
            f"({self.ga.generations_completed}) Fitness"
        )

    def fitness_function(self, individual, solution_idx):
        """
        Calculate the fitness of an individual based on the sensor data
            and the matrix of movements represented by the individual

        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        self.progress_gens.refresh()
        logger.debug("Simulation {}".format(solution_idx))
        logger.debug("Creature genome: {}".format(individual))
        # Simulate the movement of the quadruped based on the movement matrix
        # and the sensor data

        forces_list = np.array(individual).reshape(
            (
                self._simulation.genome_discrete_intervals,
                self._simulation.creature_shape,
            )
        )

        self._simulation.reset()
        while not self._simulation.is_over():
            for forces in forces_list:
                if self._simulation.is_over():
                    break
                self._simulation.step(forces)

        fitness = self._simulation.reward
        fitness_props = self._simulation.reward_props

        logger.debug("Creature fitness: {}".format(fitness))
        self.progress_gens.refresh()
        self.progress_sims.update(1)

        # Add entry in csv log
        headers = ["generation", "specimen_id", "total_fitness"] + list(
            fitness_props.keys()
        )
        data = copy.copy(fitness_props)
        data["generation"] = self.ga.generations_completed
        data["specimen_id"] = solution_idx
        data["total_fitness"] = fitness
        self._dm.save_log_file("results.csv", headers, data)

        return fitness

    # save & load
    def save(self):
        """
        Saves the final results dictionary in a .dat file.
        Saves it as best if applicable.
        """
        self._dm.save_local_dat_file("sim_data.dat", self.sim_data)
        self._dm.save_global_dat_file("last_sim.dat", self._dm.date)

        try:
            best_sim_date = self._dm.load_global_dat_file("best_sim.dat")
            best_sim_data = DataManager(
                self._dm_group, best_sim_date, False
            ).load_local_dat_file("sim_data.dat")
            if best_sim_data["best_fitness"] < self.sim_data["best_fitness"]:
                self._dm.save_global_dat_file("best_sim.dat", self._dm.date)
        except (EOFError, FileNotFoundError):
            self._dm.save_global_dat_file("best_sim.dat", self._dm.date)

    @classmethod
    def load(
        cls, date: str = None, visualize: bool = False, ending_delay: int = 0
    ):
        dm = DataManager(cls._dm_group, date, False)
        if date is None:
            best_sim_date = dm.load_global_dat_file("best_sim.dat")
            dm = DataManager(cls._dm_group, best_sim_date, False)

        sim_data = dm.load_local_dat_file("sim_data.dat")
        return GeneticAlgorithm(
            config=sim_data["config"],
            env_props=sim_data["env"],
            creature=sim_data["creature"],
            visualize=visualize,
            ending_delay=ending_delay,
            best_solution=sim_data["best_solution"],
        )

    # train & visualize
    def train(self):
        self.ga.run()
        self._simulation.close()

        best_solution, best_fitness, _ = self.ga.best_solution()
        self.sim_data["best_fitness"] = best_fitness
        self.sim_data["best_solution"] = best_solution
        self.sim_data["solutions"] = self.ga.solutions

        logger.error("Best genome: {}".format(best_solution))
        logger.error("Best fitness: {}".format(best_fitness))

        self.progress_gens.close()
        if self.progress_sims is not None:
            self.progress_sims.close()

    def visualize(self):
        forces_list = np.array(self.sim_data["best_solution"]).reshape(
            (
                self._simulation.genome_discrete_intervals,
                self._simulation.creature_shape,
            )
        )

        self._simulation.reset()
        while not self._simulation.is_closed():
            for forces in forces_list:
                if self._simulation.is_over():
                    break
                self._simulation.step(forces)

            if self._simulation.is_over():
                self._simulation.reset()
