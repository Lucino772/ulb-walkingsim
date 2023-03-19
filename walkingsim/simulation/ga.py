from walkingsim.simulation.base import BaseSimulation


class GA_Simulation(BaseSimulation):
    def __init__(
        self,
        env_props: dict,
        creature: str = "quadrupede",
        fitness: str = "walking-v0",
        visualize: bool = False,
        timestep: float = 1e-2,
        duration: float = 5,
        ending_delay: float = 0,
    ) -> None:
        super().__init__(
            env_props,
            creature,
            fitness,
            visualize,
            1,
            timestep,
            duration,
            ending_delay,
        )

    @property
    def genome_discrete_intervals(self):
        _timesteps_to_second = 1 / self._timestep
        return int(_timesteps_to_second * self._duration)
