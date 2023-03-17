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

        # FIXME: Adapt the observation spaces based on the selected fitness
        self.observation_space = gym.spaces.Dict(
            {
                "forward_bonus": gym.spaces.Box(low=-100, high=100),
                "alive_bonus": gym.spaces.Box(low=0, high=1000),
                "speed": gym.spaces.Box(low=-5, high=5),
                "speed_gap": gym.spaces.Box(low=-10, high=10),
                "height_diff": gym.spaces.Box(low=-50, high=50),
                "walk_straight": gym.spaces.Box(low=-50, high=50),
            }
        )
        self.action_space = gym.spaces.Box(
            low=-1, high=1, shape=(self._environment.creature_shape,)
        )

    def _get_observations(self):
        # FIXME: Adapt based on the selected fitness
        return {
            "forward_bonus": np.array(
                [self._fitness.props["forward_bonus"]], dtype=np.float32
            ),
            "alive_bonus": np.array(
                [self._fitness.props["alive_bonus"]], dtype=np.float32
            ),
            "speed": np.array(
                [self._fitness.props["speed"]], dtype=np.float32
            ),
            "speed_gap": np.array(
                [self._fitness.props["speed_gap"]], dtype=np.float32
            ),
            "height_diff": np.array(
                [self._fitness.props["height_diff"]], dtype=np.float32
            ),
            "walk_straight": np.array(
                [self._fitness.props["walk_straight"]], dtype=np.float32
            ),
        }

    def _get_info(self):
        return BaseSimulation._get_info(self)

    def reset(self, **kwargs):
        gym.Env.reset(self, **kwargs)
        return BaseSimulation.reset(self, **kwargs)
