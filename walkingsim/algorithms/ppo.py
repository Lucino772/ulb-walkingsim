import copy
import gymnasium as gym
import numpy
from gymnasium.envs.registration import EnvSpec
from stable_baselines3 import PPO

from walkingsim.utils.baselines_config import BaselinesConfig
from walkingsim.utils.data_manager import DataManager


class PPO_Algo:
    _dm_group = "ppo"

    def __init__(
        self,
        config: BaselinesConfig,
        env_props: dict,
        creature: str = "quadrupede",
        fitness: str = "walking-v0",
        visualize: bool = False,
        timestep: float = 1e-2,
        duration: int = 5,
        model: PPO = None,
    ) -> None:
        self._dm = DataManager(self._dm_group)
        self._config = config
        self._env_props = env_props
        self._creature = creature

        self._spec = EnvSpec(
            "gym_simulation-v0",
            entry_point="walkingsim.simulation.gym:Gym_Simulation",
            max_episode_steps=300,
        )
        self._env = gym.make(
            self._spec,
            max_episode_steps=300,
            env_props=env_props,
            creature=creature,
            visualize=visualize,
            fitness=fitness,
            timestep=timestep,
            duration=duration,
        )
        if model is None:
            self._model = PPO("MultiInputPolicy", self._env, verbose=1)
        else:
            self._model = model
            self._model.set_env(self._env)

    # save & load
    def save(self):
        self._dm.save_local_dat_file(
            "params.dat",
            {
                "config": self._config,
                "props": self._env_props,
                "creature": self._creature,
            },
        )
        self._model.save(self._dm.get_local_path("model"))

    @classmethod
    def load(cls, date: str, visualize: bool = False, timestep: float = 1e-2):
        dm = DataManager(cls._dm_group, date, fail_if_exists=False)
        params = dm.load_local_dat_file("params.dat")
        model = PPO.load(dm.get_local_path("model"))
        return PPO_Algo(
            config=params["config"],
            env_props=params["props"],
            creature=params["creature"],
            visualize=visualize,
            timestep=timestep,
            model=model,
        )

    # train & visualize
    def callback(self, *args):
        fitness = args[0]['rewards'][0]
        fitness_props = {
            key: value[0][0]
            for key, value in args[0]['new_obs'].items()
        }

        # Add entry in csv log
        headers = ["total_fitness"] + list(
            fitness_props.keys()
        )
        data = copy.copy(fitness_props)
        data["total_fitness"] = fitness
        self._dm.save_log_file("results.csv", headers, data)

    def train(self):
        self._model.learn(
            self._config.timesteps, progress_bar=self._config.show_progress, callback=self.callback
        )

    def visualize(self):
        vec_env = self._model.get_env()
        obs = vec_env.reset()
        while not vec_env.env_method("is_closed")[0]:
            action, _state = self._model.predict(obs, deterministic=True)
            action = numpy.clip(action, -1, 1)
            obs, reward, done, info = vec_env.step(action)
