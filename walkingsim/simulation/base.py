from walkingsim.envs.chrono import ChronoEnvironment
from walkingsim.fitness import fitnesses


class BaseSimulation:
    def __init__(
        self,
        env_props: dict,
        creature: str = "quadrupede",
        fitness: str = "walking-v0",
        visualize: bool = False,
        gain: float = 1,
        timestep: float = 1e-2,
        duration: float = 5,
        ending_delay: float = 0,
    ) -> None:
        self._env_props = env_props
        self._environment = ChronoEnvironment(
            visualize=visualize, creature=creature
        )
        self._render_in_step = visualize
        self._gain = gain
        self._timestep = timestep
        self._duration = duration
        self._ending_delay = ending_delay

        fitness_cls = fitnesses.get(fitness, None)
        if fitness_cls is None:
            raise RuntimeError(
                f"Fitness `{fitness}` is invalid, possible values are `{fitnesses.keys()}`"
            )
        self._fitness = fitness_cls(self._duration, self._timestep)

    @property
    def creature_shape(self):
        return self._environment.creature_shape

    @property
    def reward_props(self):
        return self._fitness.props

    @property
    def reward(self):
        return self._fitness.fitness

    def is_closed(self):
        return self._environment.closed

    # Specific to gym
    def _get_observations(self):
        return {}

    def _get_info(self):
        return {}

    # Common public methods
    def reset(self, **kwargs):
        self._environment.reset(self._env_props)
        self._fitness.reset()
        return self._get_observations(), self._get_info()

    def step(self, action):
        self._environment.step(action * self._gain, self._timestep)
        self._compute_step_reward(action * self._gain)

        if self._render_in_step:
            self.render()

        return (
            self._get_observations(),
            self._fitness.fitness,
            self.is_over(),
            self.is_over(),
            self._get_info(),
        )

    def render(self):
        self._environment.render()

    def close(self):
        self._environment.close()

    # Common private methods
    def _compute_step_reward(self, forces):
        observations = self._environment.observations
        if len(observations) == 0:
            return 0

        last_observations = observations[-1]
        self._fitness.compute(
            last_observations,
            observations,
            forces,
            self._environment.time,
        )

    def _is_time_limit_reached(self):
        return self._environment.time > self._duration

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self._fitness.done:
            is_over = True

        # Add additional delay at end of sim
        if self._ending_delay > 0:
            self._ending_delay -= self._timestep
            is_over = False

        return is_over
