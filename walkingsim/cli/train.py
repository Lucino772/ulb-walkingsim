def train_ga(
    *,
    creature: str,
    env: dict,
    visualize: bool = False,
    population_size: int,
    num_generations: int,
):
    # XXX DEBUG: initial pop test
    import pickle

    from walkingsim.algorithms.ga import GeneticAlgorithm
    from walkingsim.utils.pygad_config import PygadConfig

    filepath = "solutions/ga/20230320-112956/sim_data.dat"
    with open(filepath, "rb") as fp:
        test_initial_pop = pickle.load(fp)["best_solution"]
        print(f"the init pop is {test_initial_pop}")

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
        gene_space={"low": -1000, "high": 1000, "step": 0.1},
        init_range_low=-1000,
        init_range_high=1000,
        random_mutation_min_val=-1000,
        random_mutation_max_val=1000,
    )
    model = GeneticAlgorithm(
        config=config,
        env_props=env,
        creature=creature,
        visualize=visualize,
    )
    model.train()
    model.save()


def train_ppo(
    *, creature: str, env: dict, visualize: bool = False, timesteps: int
):
    from walkingsim.algorithms.ppo import PPO_Algo
    from walkingsim.utils.baselines_config import BaselinesConfig

    config = BaselinesConfig(timesteps=timesteps, show_progress=True)
    model = PPO_Algo(
        config=config, env_props=env, creature=creature, visualize=visualize
    )
    model.train()
    model.save()
