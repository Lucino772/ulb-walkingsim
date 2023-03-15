from collections import defaultdict

import gymnasium as gym
import numpy as np

from walkingsim.envs.chrono import ChronoEnvironment


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

        self.observation_space = gym.spaces.Dict(
            {"distance": gym.spaces.Box(low=-1000, high=1000)}
        )
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(8,))
        self.gain = 1000

        self.__environment = ChronoEnvironment(render_mode == "human")
        self.__is_creature_fallen = False
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
        return {
            "distance": np.array(
                [self.__environment.observations[-1]["distance"]],
                dtype=np.float32,
            )
        }

    def _get_info(self):
        return self.__reward_props.copy()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.__environment.reset(self.__properties)
        self.__is_creature_fallen = False
        self.__reward = None
        self.__reward_props.clear()

        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def step(self, action):
        self.__environment.step(action * self.gain, self._TIME_STEP)
        self.__reward = self._compute_step_reward()
        observation = self._get_obs()
        info = self._get_info()
        self.render()
        return observation, self.__reward, self.is_over(), self.is_over(), info

    def render(self):
        self.__environment.render()

    def close(self):
        pass

    # private methods
    def _compute_step_reward(self):
        observations = self.__environment.observations
        self.__current_step += 1
        if len(observations) == 0:
            return 0

        last_observations = observations[-1]

        # If the trunk touches the ground, alive_bonus is negative and stops sim
        if (
            not last_observations["trunk_hit_ground"]
            and not last_observations["legs_hit_ground"]
        ):
            self.__reward_props["alive_bonus"] += 1
        else:
            self.__reward_props["alive_bonus"] -= 1
            self.__is_creature_fallen = True

        # Penalties for discouraging the joints to be stuck at their limit
        self.__reward_props["joints_at_limits"] += (
            -0.01 * last_observations["joints_at_limits"]
        )

        # Values like the distance and speed will simply replace the one from
        # the previous observations instead of being added. The reward is then
        # calculated by adding all the values from the __reward_props attribute.
        # Other value like the height diff and walk_straight also follow the same
        # logic.
        self.__reward_props["distance"] = last_observations["distance"] * 100
        self.__reward_props["speed"] = (
            self.__reward_props["distance"] / self.__environment.time
        )
        self.__reward_props["height_diff"] = (
            -50
            * (
                last_observations["position"][1]
                - observations[0]["position"][1]
            )
            ** 2
        )
        self.__reward_props["walk_straight"] = -3 * (
            last_observations["position"][2] ** 2
        )

        return sum(self.__reward_props.values())

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_creature_fallen:
            is_over = True

        return is_over
