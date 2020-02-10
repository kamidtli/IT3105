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

  state, legal_moves, reward, done = env.get_current_state()
  print("State: {}, legal moves: {}, reward: {}, isDone: {}".format(state, legal_moves, reward, done))

  action = actor.choose_action(state, legal_moves)
  print("Initial action:", action)

  step = 0
  while done == 0: # Breaks when we get to a terminal state (done = 1 or -1)
    step += 1
    state, legal_moves, reward, done = env.move(action)
    print("State: {}, legal moves: {}, reward: {}, isDone: {}".format(state, legal_moves, reward, done))
    print("Chosen action:", action)

    if done != 0 or step > step_threshold:
      if i == num_of_episodes-1: # Visualize the last episode
        env.show()
      break

    action = actor.choose_action(state, legal_moves)


  # To separate episodes in the terminal
  print()

