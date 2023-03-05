import os
import pickle
import sys
from loguru import logger

import numpy as np

from walkingsim.simulation import ChronoSimulation


def main():
    with open("previous_run_solution.dat", "rb") as fp:
        mv_matrice = pickle.load(fp)

    with open("fitness.dat", "rb") as fp:
        if os.path.getsize("fitness.dat") > 0:
            previous_best_fitness = pickle.load(fp)
        else:
            previous_best_fitness = 0
        logger.info("Fitness: {}",
                    previous_best_fitness)

    environment, creature_name = "default", "bipede"
    if len(sys.argv) >= 2:
        environment = sys.argv[1]
    if len(sys.argv) >= 3:
        creature_name = sys.argv[2]

    environments_path = "./environments"
    creatures_path = "./creatures"

    # simulation slow motion parameter (0.1 = 10x slower)

    sim = ChronoSimulation(
        environments_path,
        environment,
        creatures_path,
        True,
        mv_matrice,
        _TIME_STEP=1e-2,
        _SIM_DURATION_IN_SECS=5,
        # _SIM_DURATION_IN_SECS=50,
        # applying the same force during set timesteps
        _FORCES_DELAY_IN_TIMESTEPS=4,
    )
    sim.run()


if __name__ == "__main__":
    main()
