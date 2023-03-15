from gymnasium.envs.registration import register

register(
    id="quadrupede-v0",
    entry_point="walkingsim.gym_env:GymEnvironment",
    max_episode_steps=300,
)
