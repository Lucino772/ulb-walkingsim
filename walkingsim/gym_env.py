from collections import defaultdict

import gymnasium as gym
import numpy as np

from walkingsim.envs.chrono import ChronoEnvironment
from walkingsim.fitness import AliveBonusFitness


class GymEnvironment(gym.Env):
    _TIME_STEP = 1e-2
    _SIM_DURATION_IN_SECS = 5
    _TIME_STEPS_TO_SECOND = 1 / _TIME_STEP
    _GENOME_DISCRETE_INTERVALS = int(
        (_TIME_STEPS_TO_SECOND * _SIM_DURATION_IN_SECS)
    )

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, properties: dict = None):
        super().__init__()
        self.__properties = properties
        self.render_mode = render_mode

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
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(8,))
        self.gain = 1000

        self.__environment = ChronoEnvironment(render_mode == "human")
        self.__fitness = AliveBonusFitness(
            self._SIM_DURATION_IN_SECS, self._TIME_STEP
        )
        self.__is_done = False
        self.__current_step = 0

        self.__reward_props = defaultdict(float)
        self.__reward = None

    @property
    def reward_props(self):
        return self.__reward_props

    @property
    def reward(self):
        return self.__reward

    def _get_obs(self):
        # FIXME: Adapt based on the selected fitness
        return {
            "forward_bonus": np.array(
                [self.__reward_props["forward_bonus"]], dtype=np.float32
            ),
            "alive_bonus": np.array(
                [self.__reward_props["alive_bonus"]], dtype=np.float32
            ),
            "speed": np.array(
                [self.__reward_props["speed"]], dtype=np.float32
            ),
            "speed_gap": np.array(
                [self.__reward_props["speed_gap"]], dtype=np.float32
            ),
            "height_diff": np.array(
                [self.__reward_props["height_diff"]], dtype=np.float32
            ),
            "walk_straight": np.array(
                [self.__reward_props["walk_straight"]], dtype=np.float32
            ),
        }

    def _get_info(self):
        return self.__reward_props.copy()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.__environment.reset(self.__properties)
        self.__is_done = False
        self.__reward = None
        self.__reward_props.clear()

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        self.__environment.step(action * self.gain, self._TIME_STEP)
        self.__reward = self._compute_step_reward(action)
        observation = self._get_obs()
        info = self._get_info()
        return observation, self.__reward, self.is_over(), self.is_over(), info

    def render(self):
        self.__environment.render()

    def close(self):
        pass

    # private methods
    def _compute_step_reward(self, forces):
        observations = self.__environment.observations
        self.__current_step += 1
        if len(observations) == 0:
            return 0

        last_observations = observations[-1]
        self.__fitness.compute(
            last_observations,
            observations,
            self.__current_step,
            forces,
            self.__environment.time,
        )
        self.__reward_props.clear()
        self.__reward_props.update(self.__fitness.props)
        self.__is_done = self.__fitness.done
        return self.__fitness.fitness

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_done:
            is_over = True

        return is_over
