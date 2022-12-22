import sys

# Import before everything else, this module configures the loguru logger
import walkingsim._logging

import walkingsim.ground as ground
from walkingsim.simulation import ChronoSimulation

# todo : for each creature generation group : parallelize the creation
#  of each creature
#  - graph pygad
#  - simulation pychrono


def main():
    environment, creature_name = 'default', 'bipede'
    if len(sys.argv) >= 2:
        environment = sys.argv[1]
    if len(sys.argv) >= 3:
        creature_name = sys.argv[2]

    environments_path = './environments'
    creatures_path = './creatures'

    sim = ChronoSimulation(environments_path, environment, creatures_path)
    sim.environment.Add(ground.Ground())
    sim.add_creature(creature_name)

    sim.render()


if __name__ == '__main__':
    main()
