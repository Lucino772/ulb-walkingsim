import copy
import pickle

import numpy as np
import pygad as pygad_
import tqdm
from loguru import logger

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation
from walkingsim.utils.data_manager import DataManager


class GeneticAlgorithm:
    """
    crossover_type: uniform | single_point | two_points | random
    mutation_type: adaptive | random
    """

    def __init__(self, config):

        self.__data_manager = DataManager()
        self.__data_manager.save_local_dat_file("pygad_config.dat", config)
        config_dict = config._asdict()
        self.__data_manager.save_log_file(
            "pygad_config.csv", list(config_dict.keys()), config_dict
        )
        self.data_log = []

        self.final_results = {
            "best_fitness": 0,
            "best_solution": None,
            "solutions": None,
        }

        self.ga = pygad_.GA(
            # Population & generations settings
            initial_population=config.initial_population,
            sol_per_pop=config.population_size,
            num_generations=config.num_generations,
            num_genes=config.num_joints
            * Simulation._GENOME_DISCRETE_INTERVALS,
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
                Simulation._GENOME_DISCRETE_INTERVALS,
                self.ga.num_genes // Simulation._GENOME_DISCRETE_INTERVALS,
            )
        )

        env_props = EnvironmentProps("./environments").load("default")
        simulation = Simulation(env_props)

        while not simulation.is_over():
            for forces in forces_list:
                if simulation.is_over():
                    break
                simulation.step(forces)

        fitness = simulation.reward
        fitness_props = simulation.reward_props

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
        self.__data_manager.save_log_file("results.csv", headers, data)

        return fitness

    def save_results(self):
        """
        Saves the final results dictionary in a .dat file.
        Saves it as best if applicable.
        """
        # In dedicated folder
        self.__data_manager.save_local_dat_file(
            "results.bat", self.final_results
        )

        # In solutions folder
        self.__data_manager.save_global_dat_file(
            "last_results.bat", self.final_results
        )
        if self._is_best_result():
            self.__data_manager.save_global_dat_file(
                "best_results.bat", self.final_results
            )

    def _is_best_result(self):
        res = False
        try:
            with open(
                self.__data_manager.root_dir + "best_results.dat", "rb"
            ) as fp:
                best_results = pickle.load(fp)
                if (
                    best_results["best_fitness"]
                    < self.final_results["best_fitness"]
                ):
                    res = True

        except (EOFError, FileNotFoundError):
            res = True

        return res

    def plot(self):
        logger.info("Plotting results")
        print("Plotting results")
        self.ga.plot_fitness()
        # self.ga.plot_genes()
        # self.ga.plot_new_solution_rate()    # Plot the new solution
        # rate. The new solution rate is the number of new solutions
        # created in the current generation divided by the population size.

    def run(self):
        logger.info("run()")
        logger.info("Genetic Algorithm started")
        self.ga.run()
        logger.info("Genetic Algorithm ended")

        solutions = self.ga.solutions  #
        best_solution, best_fitness, _ = self.ga.best_solution()
        self.final_results["best_fitness"] = best_fitness
        self.final_results["best_solution"] = best_solution
        self.final_results["solutions"] = solutions

        logger.info("Best genome: {}".format(best_solution))
        logger.error("Best genome: {}".format(best_solution))
        logger.info("Best fitness: {}".format(best_fitness))
        logger.error("Best fitness: {}".format(best_fitness))

        self.save_results()

        # self.plot()

        self.progress_gens.close()
        if self.progress_sims is not None:
            self.progress_sims.close()
