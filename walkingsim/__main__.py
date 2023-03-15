#  import multiprocessing
import pickle

import walkingsim.utils._logging  # Configure logging
from walkingsim.algorithms.ga import GeneticAlgorithm
from walkingsim.utils.pygad_config import PygadConfig

# The programs has 2 steps:
# 1. Training our models and get the results
# 2. Visualize those results

# Training (with PyGad)
# Each creature has a genome, in our case
# this genome defines the force to apply on a joint
# at a certain moment in time.
# For each solution proposed by PyGad, we are going to
# modify the base genome of this creature. Then this
# creature is going to be put in the simulation environment
# and the fitness of this solution will be calculated.
# Sensor data should be gathered for each step of the simulation
# giving us more possibility on how to compute the fitness value


def main():
    # threads_quantity = multiprocessing.cpu_count() * 2
    # logger.info("Number of CPU threads: {}", threads_quantity)
    # print("Number of CPU threads: {}", threads_quantity)

    population_size = 100
    config = PygadConfig(
        num_generations=50,
        num_parents_mating=4,
        mutation_percent_genes=(60, 10),
        parallel_processing=None,
        parent_selection_type="tournament",
        keep_elitism=5,
        crossover_type="uniform",
        mutation_type="adaptive",
        initial_population=None,
        population_size=population_size,
        num_joints=8,
        save_solutions=False,
        init_range_low=-1500,
        init_range_high=1500,
        random_mutation_min_val=-1500,
        random_mutation_max_val=1500,
    )

    GA = GeneticAlgorithm(config)
    GA.run()


def get_past_results():
    with open("solutions/last_results.dat", "rb") as fp:
        try:
            last_results = pickle.load(fp)
        except EOFError:
            print("last_results.dat not found")

    with open("solutions/best_results.dat", "rb") as fp:
        try:
            best_results = pickle.load(fp)
        except EOFError:
            print("best_results.dat not found")

    return best_results, last_results


if __name__ == "__main__":
    main()
