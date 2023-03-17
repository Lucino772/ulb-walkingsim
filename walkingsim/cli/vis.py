import pickle
import sys

import numpy as np
from loguru import logger


class GA_Vis:
    def __init__(self, date: str, ending_delay: int) -> None:
        from walkingsim.algorithms.ga import GeneticAlgorithm

        self._model = GeneticAlgorithm.load(
            date, visualize=True, ending_delay=ending_delay
        )

    def run(self):
        self._model.visualize()


class GYM_Vis:
    def __init__(self, date: str):
        from walkingsim.algorithms.ppo import PPO_Algo

        self.algo = PPO_Algo.load(date, True)

    def run(self):
        self.algo.visualize()
