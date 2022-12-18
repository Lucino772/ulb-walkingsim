import sys

# Import before everything else, this module configures the loguru logger
import walkingsim._logging

import walkingsim.ground as ground
from walkingsim.simulation import ChronoSimulation

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

    creature = sim.generator.generate_creature(creature_name)
    creature.add(sim.environment)

    sim.init()
    sim.run()

if __name__ == '__main__':
    main()
