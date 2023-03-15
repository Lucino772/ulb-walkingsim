import gymnasium as gym
from stable_baselines3 import PPO

import walkingsim

env = gym.make(
    "quadrupede-v0", render_mode="human", properties={"gravity": [0, -9.81, 0]}
)
model = PPO("MultiInputPolicy", env, verbose=1)
model.learn(total_timesteps=2e5, progress_bar=True)

# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(100_000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = vec_env.step(action)
#     vec_env.render()
