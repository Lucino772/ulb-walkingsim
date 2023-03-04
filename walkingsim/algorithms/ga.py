import multiprocessing
import os
import pickle
import sys

import pygad as pygad_
import tqdm
from loguru import logger

from walkingsim.simulation import ChronoSimulation

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

        # Get the number of CPU threads
        num_threads = multiprocessing.cpu_count() * 2
        logger.debug("Number of CPU threads: {}", num_threads)
        print("Number of CPU threads: {}".format(num_threads))

        self.ga = pygad_.GA(
            num_parents_mating=self.num_parents_mating,
            num_generations=self.num_generations,
            sol_per_pop=self.population_size,
            num_genes=self.num_joints * self.num_steps,
            mutation_percent_genes=self.mutation_percent_genes,
            fitness_func=self.fitness_function,
            on_generation=self._on_generation,
            on_mutation=self._on_mutation,
            on_stop=self._on_stop,
            parallel_processing=["thread", 10],  # quantity of cores to use
            init_range_low=0,
            parent_selection_type="tournament",
            keep_elitism=10,
            crossover_type="uniform",
        )

        self.progress_sims = tqdm.tqdm(
            total=self.ga.sol_per_pop,
            desc="Generation X",
            leave=False,
        )
        self.progress_gens = tqdm.tqdm(
            total=self.num_generations,
            desc="Generations",
            leave=False,
        )

    def _on_mutation(self, ga_instance, offspring_mutation):
        self.progress_sims.reset(ga_instance.sol_per_pop)
        self.progress_sims.set_description(
            f"Generation {ga_instance.generations_completed}"
        )

    def _on_generation(self, ga_instance):
        self.progress_gens.update(1)

    def _on_stop(self, ga_instance, last_population_fitness):
        self.progress_sims.reset(ga_instance.sol_per_pop)

    def fitness_function(self, individual, solution_idx):
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
        self.progress_sims.update(1)
        self.progress_gens.refresh()
        return fitness

    def save_sol(self, best_sol, best_fitness):
        # read the previous best fitness from file fitness.dat
        with open("fitness.dat", "rb") as fp:
            if os.path.getsize("fitness.dat") > 0:
                previous_best_fitness = pickle.load(fp)
            else:
                previous_best_fitness = 0

        logger.debug("Previous best fitness: {}", previous_best_fitness)
        if previous_best_fitness < best_fitness:
            with open("solution.dat", "wb") as fp:
                pickle.dump(best_sol, fp)
            with open("fitness.dat", "wb") as fp:
                pickle.dump(best_fitness, fp)

        logger.info("Best genome was successfully written in solution.dat")

    def plot(self):
        self.ga.plot_fitness()
        self.ga.plot_genes()
        self.ga.plot_new_solution_rate()

    def run(self):
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
        self.save_sol(best_solution, best_fitness)

        self.progress_sims.close()
        self.progress_gens.close()
