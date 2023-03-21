from typing import NamedTuple


class PygadConfig(NamedTuple):
    # Population & generations settings
    initial_population: list
    population_size: int
    num_generations: int
    # Evolution settings
    num_parents_mating: int
    mutation_percent_genes: tuple
    parent_selection_type: str
    keep_elitism: int
    crossover_type: str
    mutation_type: str
    # Execution settings
    parallel_processing: bool
    save_solutions: bool
    # Search space
    gene_space: dict
    init_range_low: int
    init_range_high: int
    random_mutation_min_val: int
    random_mutation_max_val: int
    # Creature
    num_joints: int
    # Timesteps
    timesteps: int
