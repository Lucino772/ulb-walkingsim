import pickle

import numpy as np

import walkingsim.utils._logging  # Configure logging
from walkingsim.algorithms.ga import GeneticAlgorithm
from walkingsim.utils.pygad_config import PygadConfig


def start(config):
    GA = GeneticAlgorithm(config)
    GA.run()


def main():
    iterations = 10

    initial_population_size = 100
    initial_config = PygadConfig(
        num_generations=50,
        num_parents_mating=initial_population_size // 2,
        mutation_percent_genes=(40, 10),
        parallel_processing=None,
        parent_selection_type="tournament",
        keep_elitism=int(initial_population_size * 0.1),
        crossover_type="uniform",
        mutation_type="adaptive",
        initial_population=None,
        population_size=initial_population_size,
        num_joints=8,
        save_solutions=False,
        init_range_low=-1500,
        init_range_high=1500,
        random_mutation_min_val=-1500,
        random_mutation_max_val=1500,
    )

    for i in range(iterations):
        initial_population = None
        if i != 0:
            # Load previous best solution and use as initial population
            with open("solutions/last_results.bat", "rb") as fp:
                data = pickle.load(fp)
            best_solution = data["best_solution"]

            initial_population = np.tile(
                best_solution, (initial_population_size, 1)
            )

        initial_config = initial_config._replace(
            initial_population=initial_population,
            keep_elitism=initial_config.keep_elitism
            + int(initial_population_size * 0.05),
        )
        print(f"Iteration {i}/{iterations-1}")
        print(initial_config)
        start(initial_config)


if __name__ == "__main__":
    main()
