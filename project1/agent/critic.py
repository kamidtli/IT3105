from agent.agent_config import *
from agent.neural_net import init_nn

import numpy as np

# The critic maps each state to values, either by using a table or a neural network
class Critic():

  def __init__(self):
    if critic_type == "neural_net":
      self.value_func = init_nn()
    else:
      self.value_func = {}
    
    self.eligibilities = {}
    self.delta = 0 # The Temporal Differencing error

  def reset_eligibilities(self):
    if critic_type == "table":
      for key in self.eligibilities.keys():
        self.eligibilities[key] = 0
    else:
      self.value_func.reset_eligibilities()

  def evaluate(self, state):
    if critic_type == "neural_net":
      return self.value_func.evaluate(state)
    else:
      return self.value_func[state]

  def update_delta(self, reward, new_state, old_state):
    new_state = self.flatten_state(new_state)
    old_state = self.flatten_state(old_state)
    self.delta = reward + discount*self.evaluate(new_state) - self.evaluate(old_state)

  def update_eval(self, state):
    if critic_type == "neural_net":
      self.nn_update_eval(state)
    else:
      self.table_update_eval(state)

  def add_state(self, state):
    state = self.flatten_state(state)
    # Add state if not already in value_func
    if state not in self.value_func:
      self.value_func[state] = 0

    # Add state if not already in eligibilities
    if state not in self.eligibilities:
      self.eligibilities[state] = 0

  def update_eligibility(self, state, new_eligibility=None):
    state = self.flatten_state(state)
    if new_eligibility == None:
      new_eligibility = discount*trace_decay*self.eligibilities[state]
    if state in self.eligibilities:
      self.eligibilities[state] = new_eligibility

  def flatten_state(self, state):
    flat_state = [cell for row in state for cell in row] # Flatten the 2D state list
    return tuple(flat_state) # Make state a tuple so it is hashable

  def table_update_eval(self, state):
    state = self.flatten_state(state)
    current_eval = self.value_func[state]
    eligibility = self.eligibilities[state]
    self.value_func[state] = current_eval + critic_learning_rate*self.delta*eligibility
  
  # def nn_update_eval(self, state_action_reward_pairs):
  #   states = []
  #   targets = []

  #   # for i in range(len(state_action_reward_pairs)):
  #   #   state, action, reward = state_action_reward_pairs[i]

  #   #   if i == len(state_action_reward_pairs)-1: # On the last state, i.e. there is no successor state
  #   #     targets.append(2)
  #   #     states.append(self.flatten_state(state))
  #   #   else:
  #   #     next_state = state_action_reward_pairs[i+1][0]
  #   #     target_val = reward + discount*self.evaluate(self.flatten_state(next_state))
  #   #     targets.append(target_val)
  #   #     states.append(self.flatten_state(state))

  #   non_evaluated_states = []

  #   for i in range(len(state_action_reward_pairs)):
  #     state, action, reward = state_action_reward_pairs[i]

  #     if i < len(state_action_reward_pairs)-1: # Not on the last state, i.e. there is a successor state
  #       next_state = state_action_reward_pairs[i+1][0]
  #       non_evaluated_states.append(self.flatten_state(next_state))

  #     states.append(self.flatten_state(state))

  #   evaluations = self.evaluate(non_evaluated_states)

  #   for i in range(len(evaluations)):
  #     target_val = reward + discount*evaluations[i]
  #     targets.append(target_val)

  #   # Add a target value for the terminal state, since
  #   # it has no successor 
  #   targets.append(1)

  #   # for i in range(len(states)):
  #   #   print("{} -> {}".format(states[i], targets[i]))

  #   for i in range(len(states)):
  #     td_error = self.value_func.fit([states[i]], [targets[i]], verbose=False)

  def nn_update_eval(self, states):
    features = []
    targets = []
    non_evaluated_states = []

    # Loop over state, action reward tuples
    for i in range(len(states)):
      state, action, reward = states[i]

      if i < len(states)-1: # Not on the last state, i.e. there is a successor state
        next_state = states[i+1][0]
        non_evaluated_states.append(self.flatten_state(next_state))

      features.append(self.flatten_state(state))

    evaluations = self.evaluate(non_evaluated_states)

    for evaluation in evaluations:
      target_val = reward + discount*evaluation[0]
      targets.append(target_val)

    # Add a target value for the terminal state, since
    # it has no successor
    targets.append(1)

    # print("Targets:", targets)
    # print("Features:", features)
    td_errors = self.value_func.fit(features, targets, verbose=False)

    return td_errors

    # return 0