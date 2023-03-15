"""
3D PyChrono muscle-based walking simulator
File: simulation.py
Authors:
    BECKER Robin-Gilles
    BOURGEOIS Noé
    HENRY DE FRAHAN Antoine
    PALMISANO Luca
Description:
    Classes for the simulations
"""

from collections import defaultdict

from walkingsim.envs.chrono import ChronoEnvironment


class Simulation:
    _TIME_STEP = 1e-2
    _SIM_DURATION_IN_SECS = 5
    _TIME_STEPS_TO_SECOND = 1 / _TIME_STEP
    _GENOME_DISCRETE_INTERVALS = int(
        (_TIME_STEPS_TO_SECOND * _SIM_DURATION_IN_SECS)
    )

    def __init__(self, __env_props: dict, visualize: bool = False) -> None:
        self.__environment = ChronoEnvironment(visualize)
        self.__environment.reset(__env_props)
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

    def step(self, action: list):
        self.__environment.step(action, self._TIME_STEP)
        self.__reward = self._compute_step_reward(action)

    def render(self):
        self.__environment.render()

    def _compute_step_reward(self, forces):
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
            self.__reward_props["alive_bonus"] += 0.5
        else:
            self.__reward_props["alive_bonus"] -= 0.5
            self.__is_creature_fallen = True

        # Penalties for discouraging the joints to be stuck at their limit
        #  self.__reward_props["joints_at_limits"] += (-0.01 * last_observations["joints_at_limits"])

        # Values like the distance and speed will simply replace the one from
        # the previous observations instead of being added. The reward is then
        # calculated by adding all the values from the __reward_props attribute.
        # Other value like the height diff and walk_straight also follow the same
        # logic.
        #  self.__reward_props["distance"] += last_observations["distance"]
        self.__reward_props["speed"] += (
            last_observations["distance"] / self.__environment.time
        )
        self.__reward_props["height_diff"] += 0.1 * (
            (last_observations["position"][1] - observations[0]["position"][1])
        )
        #  self.__reward_props["walk_straight"] = -3 * (
        #      last_observations["position"][2] ** 2
        #  )

        self.__reward_props["forces"] = -0.2 * abs((sum(forces)))

        return sum(self.__reward_props.values())

    def _is_time_limit_reached(self):
        return self.__environment.time > self._SIM_DURATION_IN_SECS

    def is_over(self):
        """This function returns wether or not the simulation is done"""
        is_over = False

        if self._is_time_limit_reached() or self.__is_creature_fallen:
            is_over = True

        return is_over
