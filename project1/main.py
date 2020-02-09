from game.simWorld import Environment
from agent.actor import Actor
from agent.critic import Critic
from config import *

# Initialize actor and critic
critic = Critic()
actor = Actor()

# Run for num_of_episodes
for i in range(num_of_episodes):
  print("Episode:", i+1)

  env = Environment()

  # Reset eligibilites in actor and critic
  critic.reset_eligibilities()
  actor.reset_eligibilities()

  s = env.get_current_state()
  action = actor.choose_action(s)
  print("Initial action:", action)

  # To separate episodes in the terminal
  print()

