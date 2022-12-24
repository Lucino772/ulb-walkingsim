import sys

import networkx as nx
import numpy as np
import pygad
from _logging import logger
from creature.genotype import Genotype

from walkingsim.auto_indent import AutoIndent

logger.debug("Starting genetic_algorithm.py")
sys.stdout = AutoIndent(sys.stdout)


class GeneticAlgorithm:
    # pygad.set_seed(42)
    def __init__(
        self,
        population_size,
        num_generations,
        num_parents_mating,
        fitness_func,
        num_genes,
        gene_type,
        gene_space,
        init_range_low,
        init_range_high,
        mutation_percent_genes,
        mutation_type,
        mutation_num_genes,
        mutation_by_replacement,
        mutation_range_low,
        mutation_range_high,
        crossover_type,
        crossover_percent_parents,
        on_generation,
        keep_parents,
    ):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.fitness_func = fitness_func
        self.num_genes = num_genes
        self.gene_type = gene_type
        self.gene_space = gene_space
        self.init_range_low = init_range_low
        self.init_range_high = init_range_high
        self.mutation_percent_genes = mutation_percent_genes
        self.mutation_type = mutation_type
        self.mutation_num_genes = mutation_num_genes
        self.mutation_percent_genes = mutation_percent_genes
        self.mutation_by_replacement = mutation_by_replacement
        self.mutation_range_low = mutation_range_low
        self.mutation_range_high = mutation_range_high
        self.crossover_type = crossover_type
        self.crossover_percent_parents = crossover_percent_parents
        self.on_generation = on_generation
        self.keep_parents = keep_parents
