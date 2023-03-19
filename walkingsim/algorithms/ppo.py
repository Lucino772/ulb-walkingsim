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
    def load(cls, date: str, visualize: bool = False):
        dm = DataManager(cls._dm_group, date, fail_if_exists=False)
        params = dm.load_local_dat_file("params.dat")
        model = PPO.load(dm.get_local_path("model"))
        return PPO_Algo(
            config=params["config"],
            env_props=params["props"],
            creature=params["creature"],
            visualize=visualize,
            model=model,
        )

    # train & visualize
    def train(self):
        self._model.learn(
            self._config.timesteps, progress_bar=self._config.show_progress
        )

    def visualize(self):
        vec_env = self._model.get_env()
        obs = vec_env.reset()
        while not vec_env.env_method("is_closed")[0]:
            action, _state = self._model.predict(obs, deterministic=True)
            action = numpy.clip(action, -1, 1)
            obs, reward, done, info = vec_env.step(action)
