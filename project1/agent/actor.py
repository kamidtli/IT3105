import random
from agent.agent_config import *

# The actor uses a policy to map state-action pairs (s, a), to the corresponding desireability
class Actor():

  def __init__(self):
    self.policy = {}
    self.eligibilities = {}

  # Sets the eligibilities to 0
  def reset_eligibilities(self):
    for key in self.eligibilities.keys():
      self.eligibilities[key] = 0

  # Adds states to policy and eligibilities and chooses the best action
  def choose_action(self, state, legal_actions, epsilon):
    if (len(legal_actions) == 0):
      return (0, 0, 0, 0) # No action

    state = self.flatten_state(state)
    self.add_state_action_pairs_to_policy(state, legal_actions)
    self.add_state_action_pairs_to_eligibilities(state, legal_actions)
    action = self.get_optimal_action(state, legal_actions, epsilon)
    return action

  # Flattens state to one a dimensional tuple
  def flatten_state(self, state):
    flat_state = [cell for row in state for cell in row] # Flatten the 2D state list
    return tuple(flat_state) # Make state a tuple so it is hashable

  # Adds Saps to policy
  def add_state_action_pairs_to_policy(self, state, legal_actions):
    for action in legal_actions:
      if (state, action) not in self.policy:
        self.policy[(state, action)] = 0

  # Add saps to eligibilities
  def add_state_action_pairs_to_eligibilities(self, state, legal_actions):
    for action in legal_actions:
      if (state, action) not in self.eligibilities:
        self.eligibilities[(state, action)] = 0

  # Returns the optimal action for a given state
  def get_optimal_action(self, state, actions, epsilon=0):
    if (random.uniform(0, 1) < epsilon):
      return random.choice(actions)

    max_value = float('-inf')
    best_actions = []
    for action in actions:
      value = self.policy[(state, action)]
      if value > max_value:
        # Optimal action found, best_actions should only contain this action now
        max_value = value 
        best_actions = [action] # Resets best_actions to only the current action
      elif value == max_value:
        # Append action to best_actions since it's equally good
        best_actions.append(action)
    
    # Should never enter this part, only for debugging (if we get Nan)
    if len(best_actions) == 0:
      print("Did not find optimal action. Returned a random one")
      saps = ["{} -> {}".format((state, action), self.policy[(state, action)]) for action in actions]
      print(saps)
      return random.choice(actions)

    return random.choice(best_actions)

  # Update the eligibility of a state action pair
  def update_eligibility(self, state, action, new_eligibility=None):
    state = self.flatten_state(state)
    sap = (state, action)

    if sap in self.eligibilities:
      if new_eligibility == None:
        new_eligibility = discount*trace_decay*self.eligibilities[sap]
      
      if sap in self.eligibilities:
        self.eligibilities[sap] = new_eligibility

  # Update the policy for a state action pair
  def update_policy(self, state, action, delta):
    state = self.flatten_state(state)
    sap = (state, action)
    if sap in self.policy:
      current_policy = self.policy[sap]
      self.policy[sap] = current_policy + actor_learning_rate*delta*self.eligibilities[sap]