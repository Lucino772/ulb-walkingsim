import pickle
import sys

import numpy as np

from walkingsim.simulation import ChronoSimulation


def main():
    with open("solution.dat", "rb") as fp:
        mv_matrice = pickle.load(fp)

    environment, creature_name = "default", "bipede"
    if len(sys.argv) >= 2:
        environment = sys.argv[1]
    if len(sys.argv) >= 3:
        creature_name = sys.argv[2]

    environments_path = "./environments"
    creatures_path = "./creatures"

    sim = ChronoSimulation(
        environments_path,
        environment,
        creatures_path,
        True,
        mv_matrice,
    )
    sim.run()


if __name__ == "__main__":
    main()
