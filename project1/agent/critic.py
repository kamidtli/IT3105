from agent.agent_config import *
from agent.neural_net import init_nn

import numpy as np

# The critic maps each state to values, either by using a table or a neural network
class Critic():

  def __init__(self):
    if critic_type == "neural_net":
      # Use a neural net critic
      self.value_func = init_nn()
    else:
      # Use a table critic
      self.value_func = {}
    
    self.eligibilities = {}
    self.delta = 0 # The Temporal Differencing error

  # Set all eligibilities to 0
  def reset_eligibilities(self):
    if critic_type == "table":
      for key in self.eligibilities.keys():
        self.eligibilities[key] = 0
    else:
      self.value_func.reset_eligibilities()

  # Evaluate a state
  def evaluate(self, state):
    if critic_type == "neural_net":
      return self.value_func.evaluate(state)
    else:
      return self.value_func[state]

  # Update the TD-error according to the paper
  def update_delta(self, reward, new_state, old_state):
    new_state = self.flatten_state(new_state)
    old_state = self.flatten_state(old_state)
    self.delta = reward + discount*self.evaluate(new_state) - self.evaluate(old_state)

  # Update the evaluation of states
  def update_eval(self, state):
    if critic_type == "neural_net":
      self.nn_update_eval(state)
    else:
      self.table_update_eval(state)

  # Add a state to the table, this will only 
  # be called if using the table method
  def add_state(self, state):
    state = self.flatten_state(state)
    # Add state if not already in value_func
    if state not in self.value_func:
      self.value_func[state] = 0

    # Add state if not already in eligibilities
    if state not in self.eligibilities:
      self.eligibilities[state] = 0

  # Update the eligibility is a state
  # Uses new eligibility if specified,
  # else updates according to the paper
  def update_eligibility(self, state, new_eligibility=None):
    state = self.flatten_state(state)
    if new_eligibility == None:
      new_eligibility = discount*trace_decay*self.eligibilities[state]
    if state in self.eligibilities:
      self.eligibilities[state] = new_eligibility

  # Flatten the state to a one dimensional tuple
  def flatten_state(self, state):
    flat_state = [cell for row in state for cell in row] # Flatten the 2D state list
    return tuple(flat_state) # Make state a tuple so it is hashable

  # Updates the evaluation of a state
  # using the table method
  def table_update_eval(self, state):
    state = self.flatten_state(state)
    current_eval = self.value_func[state]
    eligibility = self.eligibilities[state]
    self.value_func[state] = current_eval + critic_learning_rate*self.delta*eligibility
  
  # Evaluate the states and fit to these evaluations
  def nn_update_eval(self, states):
    features = self.get_features(states) # The states to be trained on
    targets = self.get_targets(states) # The target values for the features

    td_errors = self.value_func.fit(np.asarray(features), targets, verbose=False)

    return td_errors

  def get_features(self, states):
    features = []
    # Loop over state, action reward tuples
    for i in range(len(states)):
      # Unpack the tuples
      state, action, reward = states[i]
      features.append(self.flatten_state(state))
    return features

  def get_targets(self, states, get_evals=False):
    states_to_evaluate = []
    rewards = [] # Rewards between all states
    # Loop over the state, action reward tuples
    for i in range(len(states)):
      # Unpack the tuples
      state, action, reward = states[i]
      states_to_evaluate.append(self.flatten_state(state))

      # The rewards are for entering the state, so we
      # do not need the first reward (the reward of getting)
      # to the initial state, hence we do not append it
      if i>0:
        rewards.append(reward)

    # Evaluate all states at once, because it is faster than one by one
    evaluations = self.evaluate(states_to_evaluate)

    targets = []
    # Loop from one since we only want the successor evaluations
    for i in range(len(evaluations)-1):
      # [i+1] for successor state, and [0] for the value
      successor_state = evaluations[i+1][0]
      reward = rewards[-1] # rewards[-1] # TODO: Find out why [i] does not work
      target_val = reward + discount*successor_state
      targets.append(target_val)

    # Add a target value for the terminal state, since
    # it has no successor, the target value is the one evaluated
    targets.append(evaluations[-1][0])

    return targets