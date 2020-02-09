import random

# The actor uses a policy to map state-action pairs (s, a), to the corresponding desireability
class Actor():

  def __init__(self):
    self.policy = {}
    self.eligibilities = {}
    print("Initialized the actor.")

  def reset_eligibilities(self):
    # TODO: Reset eligibilites
    print("Reset eligibilities in actor")

  def choose_action(self, state):
    action = self.get_optimal_action(state=state[0], actions=state[1])
    return action

  def get_optimal_action(self, state, actions):
    flat_state = [cell for row in state for cell in row] # Flatten the 2D state list
    state = tuple(flat_state) # Make state a tuple so it is hashable

    max_value = -1
    best_actions = []
    for action in actions:
      if (state, action) in self.policy:
        value = self.policy[(state, action)]
        if value > max_value:
          max_value = value 
          best_actions = [action]
        elif value == max_value:
          best_actions.append(action)
      else:
        self.policy[(state, action)] = 0
        best_actions.append(action)
    return random.choice(best_actions)