import gymnasium as gym
import numpy as np

from walkingsim.simulation.base import BaseSimulation


class Gym_Simulation(BaseSimulation, gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(
        self,
        env_props: dict,
        creature: str = "quadrupede",
        visualize: bool = False,
        timestep: float = 1e-2,
        duration: float = 5,
        ending_delay: float = 0,
    ) -> None:
        BaseSimulation.__init__(
            self,
            env_props,
            creature,
            visualize,
            1000,
            timestep,
            duration,
            ending_delay,
        )
        gym.Env.__init__(self)

        self.render_mode = "human" if visualize else "rgb_array"

        obs_dict = dict()
        for key, value in self._fitness.props_range.items():
            low, high = value
            obs_dict[key] = gym.spaces.Box(low=low, high=high)

        self.observation_space = gym.spaces.Dict(obs_dict)

        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(self._environment.creature_shape,)
        )

    def _get_observations(self):
        obs_dict = dict()
        for key, value in self._fitness.props.items():
            obs_dict[key] = np.array([value], dtype=np.float32)

        return obs_dict

    def _get_info(self):
        return BaseSimulation._get_info(self)

    def reset(self, **kwargs):
        gym.Env.reset(self, **kwargs)
        return BaseSimulation.reset(self, **kwargs)
