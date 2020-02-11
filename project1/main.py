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
  # print("State: {}, legal moves: {}, reward: {}, isDone: {}".format(state, legal_moves, reward, done))

  critic.add_state(state)
  action = actor.choose_action(state, legal_moves)

  step = 0
  while True:
    step += 1
    new_state, legal_moves, reward, done = env.move(action)
    critic.add_state(new_state)

    # Check if game is over
    if done != 0 or step > step_threshold:
      if i == num_of_episodes-1: # Visualize the last episode
        env.show()
      break

    new_action = actor.choose_action(new_state, legal_moves)
    actor.update_eligibility(state, action, 1)

    critic.update_delta(reward, new_state, state)
    critic.update_eligibility(state, 1)

    saps = [(state, action), (new_state, new_action)] # All state-action pairs for this step
    for sap in saps:
      s, a = sap
      critic.update_eval(s)
      critic.update_eligibility(s)
      actor.update_policy(s, a, critic.delta)
      actor.update_eligibility(s, a)

    action = new_action
    state = new_state

    print("Critic delta:", critic.delta)

  # To separate episodes in the terminal
  print()

