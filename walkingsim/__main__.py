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
    GA = GeneticAlgorithm(
        population_size=200,
        num_generations=100,
        num_parents_mating=2,
        mutation_percent_genes=10,
        num_joints=4,
    )
    GA.run()


if __name__ == "__main__":
    main()
