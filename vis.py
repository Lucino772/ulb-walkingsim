import pickle

import numpy as np

from walkingsim.loader import EnvironmentProps
from walkingsim.simulation import Simulation


def main():
    with open("solutions/last_results.bat", "rb") as fp:
        results = pickle.load(fp)

    forces_list = np.array(results["best_solution"]).reshape(
        (Simulation._GENOME_DISCRETE_INTERVALS, 8)
    )

    env_props = EnvironmentProps("./environments").load("default")
    simulation = Simulation(env_props, True)

    while not simulation.is_over():
        for forces in forces_list:
            if simulation.is_over():
                break
            simulation.step(forces)
            simulation.render()

    print(simulation.reward)
    print(simulation.reward_props)


if __name__ == "__main__":
    main()
