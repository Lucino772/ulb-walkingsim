def train_ga(
    *,
    creature: str,
    env: dict,
    visualize: bool = False,
    duration: int = 5,
    timestep: float = 1e-2,
    timesteps: int = 500,
    population_size: int,
    num_generations: int,
):
    from walkingsim.algorithms.ga import GeneticAlgorithm
    from walkingsim.utils.pygad_config import PygadConfig

    config = PygadConfig(
        num_generations=num_generations,
        num_parents_mating=4,  # TODO: Add argument
        mutation_percent_genes=(60, 10),  # TODO: Add argument
        parallel_processing=None,
        parent_selection_type="tournament",  # TODO: Add argument
        keep_elitism=5,  # TODO: Add argument
        crossover_type="uniform",  # TODO: Add argument
        mutation_type="adaptive",  # TODO: Add argument
        initial_population=None,  # TODO: Add argument
        population_size=population_size,
        num_joints=8,  # FIXME: Load this from the creature
        save_solutions=False,
        gene_space={"low": -1, "high": 1, "step": 0.1},
        init_range_low=-1,
        init_range_high=1,
        random_mutation_min_val=-1,
        random_mutation_max_val=1,
        timesteps=timesteps,
    )
    model = GeneticAlgorithm(
        config=config,
        env_props=env,
        creature=creature,
        visualize=visualize,
        duration=duration,
        timestep=timestep,
    )
    model.train()
    model.save()


def train_ppo(
    *,
    creature: str,
    env: dict,
    visualize: bool = False,
    duration: int = 5,
    timestep: float = 1e-2,
    timesteps: int,
):
    from walkingsim.algorithms.ppo import PPO_Algo
    from walkingsim.utils.baselines_config import BaselinesConfig

    config = BaselinesConfig(timesteps=timesteps, show_progress=True)
    model = PPO_Algo(
        config=config,
        env_props=env,
        creature=creature,
        visualize=visualize,
        duration=duration,
        timestep=timestep,
    )
    model.train()
    model.save()
