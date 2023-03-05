import multiprocessing
import os
import pickle


# from loguru import logger

from walkingsim.algorithms.ga import GeneticAlgorithm

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
    population_size = 500

    _TIME_STEP = 1e-2
    # _SIM_DURATION_IN_SECS = 50   # ValueError: cannot reshape array of
    # size 299948 into shape (4,7498)

    _SIM_DURATION_IN_SECS = 5
    # applying the same force during set timesteps
    _FORCES_DELAY_IN_TIMESTEPS = 4

    _TIME_STEPS_TO_SECOND = 60 // _TIME_STEP
    _GENOME_DISCRETE_INTERVALS = int(
        (
            _TIME_STEPS_TO_SECOND
            * _SIM_DURATION_IN_SECS
            // _FORCES_DELAY_IN_TIMESTEPS
        )
    )
    threads_quantity = multiprocessing.cpu_count() * 2
    # logger.info("Number of CPU threads: {}", threads_quantity)
    print("Number of CPU threads: {}", threads_quantity)

    with open("solution.dat", "rb") as fp:
        if os.path.getsize("solution.dat") > 0:
            previous_solution = pickle.load(fp)
        else:
            previous_solution = None

    GA = GeneticAlgorithm(
        initial_population=[previous_solution]*population_size,
        population_size=population_size,
        sol_per_pop=population_size,
        num_steps=_GENOME_DISCRETE_INTERVALS,

        num_generations=2,
        num_parents_mating=4,
        num_joints=8,
        # parallel_processing=None,
        parallel_processing=24,
        init_range_low=-1000,
        init_range_high=1000,

        parent_selection_type="tournament",
        # K_tournament=population_size // 100,
        keep_elitism=population_size // 100,

        crossover_type="uniform",
        # crossover_type="single_point",
        # crossover_type="two_points",
        # crossover_type="random",

        # UserWarning: Use the 'save_solutions' parameter with caution
        # as it may cause memory overflow when either the number of
        # generations, number of
        # genes, or number of
        # solutions in population is large.
        save_solutions=False,

        mutation_type="adaptive",
        mutation_percent_genes=(40,10),

        # mutation_type="random",
        # mutation_by_replacement=True,
        # random_mutation_min_val=-1000,
        # random_mutation_max_val=1000,
    )
    GA.run()


if __name__ == "__main__":
    main()
