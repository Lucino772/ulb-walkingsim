from collections import defaultdict


class Fitness:
    def __init__(self, sim_duration: float, timestep: float) -> None:
        self._props = dict.fromkeys(self.props_range.keys(), 0.0)
        self._fitness = 0
        self._done = False
        self._timestep = timestep
        self._duration = sim_duration

    @property
    def props(self):
        return self._props

    @property
    def props_range(self):
        raise NotImplemented

    @property
    def fitness(self):
        return self._fitness

    @property
    def done(self):
        return self._done

    def reset(self):
        self._props = dict.fromkeys(self.props_range.keys(), 0.0)
        self._fitness = 0
        self._done = False

    def compute(
        self,
        last_observation: dict,
        observations: list,
        forces: list,
        time: float,
    ):
        raise NotImplementedError


class AliveBonusFitness(Fitness):
    @property
    def props_range(self):
        return {
            "alive_bonus": (0, 400),
            "speed": (-500, 500),
            "height_diff": (-100, 100),
            "forces": (-5000, 5000),
        }

    def compute(
        self,
        last_observation: dict,
        observations: list,
        forces: list,
        time: float,
    ):
        # If the trunk touches the ground, alive_bonus is negative and stops sim
        if (
            not last_observation["trunk_hit_ground"]
            and not last_observation["legs_hit_ground"]
        ):
            self._props["alive_bonus"] += 0.5
        else:
            self._props["alive_bonus"] -= 0.5
            self._done = True

        # Penalties for discouraging the joints to be stuck at their limit
        #  self._props["joints_at_limits"] += (-0.01 * last_observation["joints_at_limits"])

        # Values like the distance and speed will simply replace the one from
        # the previous observations instead of being added. The reward is then
        # calculated by adding all the values from the _props attribute.
        # Other value like the height diff and walk_straight also follow the same
        # logic.
        #  self._props["distance"] += last_observation["distance"]
        self._props["speed"] += last_observation["distance"] / time
        self._props["height_diff"] += 0.1 * (
            (last_observation["position"][1] - observations[0]["position"][1])
        )
        #  self._props["walk_straight"] = -3 * (
        #      last_observation["position"][2] ** 2
        #  )

        self._props["forces"] = -0.2 * abs((sum(forces)))
        self._fitness = sum(self._props.values())


class ForwardBonusFitness(Fitness):
    @property
    def props_range(self):
        return {
            "forward_bonus": (-100, 100),
            "alive_bonus": (0, 1000),
            "speed": (-5, 5),
            "speed_gap": (-10, 10),
            "height_diff": (-50, 50),
            "walk_straight": (-50, 50),
        }

    def compute(
        self,
        last_observation: dict,
        observations: list,
        forces: list,
        time: float,
    ):
        if len(observations) >= 2:
            if (
                last_observation["position"][0]
                > observations[-2]["position"][0]
            ):
                self._props["forward_bonus"] += 0.02
            else:
                self._props["forward_bonus"] -= 0.05 * (
                    1 - (time / self._duration)
                )

        self._props["alive_bonus"] += self._timestep / 5
        if (
            last_observation["trunk_hit_ground"]
            or last_observation["legs_hit_ground"]
        ):
            self._done = True

        target = 0.8333  # 3km/h
        distance = last_observation["distance"]
        self._props["speed"] = distance / time
        self._props["speed_gap"] = 3 * -abs(target - (distance / time))
        self._props["height_diff"] = -10 * abs(
            last_observation["position"][1] - observations[0]["position"][1]
        )
        self._props["walk_straight"] = -abs(last_observation["position"][2])
        self._fitness = sum(self._props.values())
