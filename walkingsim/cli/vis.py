def visualize_ga(*, date: str = None, delay: int = 0):
    from walkingsim.algorithms.ga import GeneticAlgorithm

    model = GeneticAlgorithm.load(
        date=date, visualize=True, ending_delay=delay
    )
    model.visualize()


def visualize_ppo(*, date: str, delay: int = 0):
    from walkingsim.algorithms.ppo import PPO_Algo

    model = PPO_Algo.load(date=date, visualize=True)
    model.visualize()
