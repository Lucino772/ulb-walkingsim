class GA_Train:
    def __init__(
        self,
        creature: str,
        env: dict,
        population_size: int = None,
        num_generations: int = None,
        workers: int = None,
        use_multiprocessing: bool = False,
        visualize: bool = False,
    ) -> None:
        from walkingsim.algorithms.ga import GeneticAlgorithm
        from walkingsim.utils.pygad_config import PygadConfig

        # FIXME: target (walking, running, etc.)

        parallel_processing = workers
        if use_multiprocessing:
            parallel_processing = ("process", workers)

        config = PygadConfig(
            num_generations=num_generations,
            num_parents_mating=4,  # TODO: Add argument
            mutation_percent_genes=(60, 10),  # TODO: Add argument
            parallel_processing=parallel_processing,
            parent_selection_type="tournament",  # TODO: Add argument
            keep_elitism=5,  # TODO: Add argument
            crossover_type="uniform",  # TODO: Add argument
            mutation_type="adaptive",  # TODO: Add argument
            initial_population=None,  # TODO: Add argument
            population_size=population_size,
            num_joints=8,  # FIXME: Load this from the creature
            save_solutions=False,
            init_range_low=-1500,
            init_range_high=1500,
            random_mutation_min_val=-1500,
            random_mutation_max_val=1500,
        )

        self.algo = GeneticAlgorithm(config, env, creature, visualize)

    def run(self):
        self.algo.train()
        self.algo.save()


class GYM_Train:
    def __init__(
        self,
        creature: str,
        env: dict,
        timesteps: int,
        algo: str = "PPO",
        show_progress: bool = False,
        visualize: bool = False,
    ) -> None:
        from walkingsim.algorithms.ppo import PPO_Algo
        from walkingsim.utils.baselines_config import BaselinesConfig

        # FIXME: target (walking, running, etc.)
        # FIXME: Use different algorithms
        self.config = BaselinesConfig(timesteps, show_progress)
        self.algo = PPO_Algo(self.config, env, creature, visualize)

    def run(self):
        self.algo.train()
        self.algo.save()
