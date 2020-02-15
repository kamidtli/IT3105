from game.simWorld import Environment
from agent.actor import Actor
from agent.critic import Critic
from config import *
from agent.agent_config import *
from main_plots import plot_remaining_pegs

# Initialize actor and critic
critic = Critic()
actor = Actor()

# Keep track of pegs left on board for each episode
remaining_pegs = []

# Local variable for the epsilon greedy strategy
epsilon = epsilon_greedy_value

# Run for num_of_episodes
for episode in range(num_of_episodes):
  env = Environment(viz=(episode == num_of_episodes-1))

  # Reset eligibilites in actor and critic
  critic.reset_eligibilities()
  actor.reset_eligibilities()

  state, legal_moves, reward, done = env.get_current_state()

  if critic_type == "table":
    critic.add_state(state)
    
  action = actor.choose_action(state, legal_moves, epsilon)

  saps = [(state, action)] # All state-action pairs for this episode

  step = 0
  while done == 0: # If done is -1 the game is lost, if done is 1 the game is won
    step += 1
    new_state, legal_moves, reward, done = env.move(action)

    if critic_type == "table":
      critic.add_state(new_state)

    new_action = actor.choose_action(new_state, legal_moves, epsilon)

    actor.update_eligibility(state, action, 1)

    critic.update_delta(reward, new_state, state)
    critic.update_eligibility(state, 1)


    if len(legal_moves) > 0: # The new state is not terminal, so we add it to saps
      saps.append((new_state, new_action))

    for sap in saps:
      s, a = sap
      critic.update_eval(s)
      critic.update_eligibility(s)
      actor.update_policy(s, a, critic.delta)
      actor.update_eligibility(s, a)

    action = new_action
    state = new_state

    epsilon = max(0, epsilon_greedy_value-(episode/(num_of_episodes*0.5))) # Reduces the epsilon, but never below 0

  print("Episode:", episode + 1)
  print("New delta:", critic.delta)

  remaining_pegs.append(env.get_remaining_pegs())

  if episode == num_of_episodes-1: # Visualize the last episode
    env.show()

plot_remaining_pegs(remaining_pegs)
