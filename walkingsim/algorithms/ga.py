import os
import pickle

import pygad as pygad_
from loguru import logger

from walkingsim.simulation import ChronoSimulation
from walkingsim.utils import progress

# todo from creature.genotype import Genotype


class GeneticAlgorithm:
    def __init__(
        self,
        population_size,
        num_generations,
        num_parents_mating,
        mutation_percent_genes,
        num_joints,
    ):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.mutation_percent_genes = mutation_percent_genes
        self.num_joints = num_joints
        self.num_steps = ChronoSimulation._GENOME_DISCRETE_INTERVALS

        self.ga = pygad_.GA(
            num_parents_mating=self.num_parents_mating,
            num_generations=self.num_generations,
            sol_per_pop=self.population_size,
            num_genes=self.num_joints * self.num_steps,
            mutation_percent_genes=self.mutation_percent_genes,
            fitness_func=self.fitness_function,
            on_generation=self._on_generation,
            on_start=self._on_start,
            on_mutation=self._on_mutation,
            on_stop=self._on_stop,
            parallel_processing=10,  # quantity of cores to use
        )

    @staticmethod
    def _on_start(ga_instance):
        progress.create_pb(
            "simulations",
            total=ga_instance.sol_per_pop,
            desc="Generation X",
            leave=False,
        )

    @staticmethod
    def _on_mutation(ga_instance, offspring_mutation):
        progress.reset_pb("simulations", ga_instance.sol_per_pop)
        progress.set_pb_desc(
            "simulations", f"Generation {ga_instance.generations_completed}"
        )

    @staticmethod
    def _on_generation(ga_instance):
        progress.update_pb("generations", 1)

    @staticmethod
    def _on_stop(ga_instance, last_population_fitness):
        progress.close_pb("simulations")

    @staticmethod
    def fitness_function(individual, solution_idx):
        """
        Calculate the fitness of an individual based on the sensor data
            and the matrix of movements represented by the individual

        ValueError: The fitness function must accept 2 parameters:
            1) A solution to calculate its fitness value.
            2) The solution's index within the population.

        """
        logger.debug("Simulation {}".format(solution_idx))
        logger.debug("Creature genome: {}".format(individual))
        # Simulate the movement of the quadruped based on the movement matrix
        # and the sensor data

        environment = "default"
        environments_path = "./environments"
        creatures_path = "./creatures"

        simulation = ChronoSimulation(
            environments_path,
            environment,
            creatures_path,
            False,
            individual,
        )
        # simulation.add_creature(creature_name="bipede")
        fitness = simulation.run()
        logger.debug("Creature fitness: {}".format(fitness))
        progress.update_pb("simulations", 1)
        progress.refresh_pb("generations")
        return fitness

    def save_sol(self, best_sol):
        with open("solution.dat", "wb") as fp:
            pickle.dump(best_sol, fp)

        logger.info("Best genome was successfully written in solution.dat")

    def plot(self):
        self.ga.plot_fitness()
        self.ga.plot_genes()
        self.ga.plot_new_solution_rate()

    def run(self):
        progress.create_pb(
            "generations",
            total=self.num_generations,
            desc="Generations",
            leave=False,
        )

        self.ga.run()
        best_solution, best_fitness, _ = self.ga.best_solution()
        logger.info("Genetic Algorithm ended")
        logger.info("Best genome: {}".format(best_solution))
        # print the best solution
        # for i in range(self.num_joints):
        #     print("Joint {}:", i)
        #     for j in range(self.num_steps):
        #         print(
        #             "Step", j,
        #             ":", best_solution[i * self.num_steps + j],
        #         )
        logger.info("Best fitness: {}".format(best_fitness))
        self.save_sol(best_solution)

        progress.close_all_pb()
