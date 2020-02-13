from agent.agent_config import *

# The critic maps each state to values, either by using a table or a neural network
class Critic():

  def __init__(self):
    if critic_type == "neural_net":
      self.value_func = self.init_nn()
    else:
      self.value_func = {}
    
    self.eligibilities = {}
    self.delta = 0 # The Temporal Differencing error

    print("Critic initialized with {} as mapping function.".format(critic_type))

  def init_nn(self):
    # TODO: Initialize neural net table
    return None
  
  def reset_eligibilities(self):
    for key in self.eligibilities.keys():
      self.eligibilities[key] = 0

  def evaluate(self, state):
    if critic_type == "table":
      return self.value_func[state]
    else:
      # TODO: Evaluate state with neural net
      return None

  def update_delta(self, reward, new_state, old_state):
    new_state = self.flatten_state(new_state)
    old_state = self.flatten_state(old_state)
    # print("Updating delta: reward:{}".format(reward))
    self.delta = reward + discount*self.evaluate(new_state) - self.evaluate(old_state)

  def update_eval(self, state):
    state = self.flatten_state(state)
    current_eval = self.value_func[state]
    eligibility = self.eligibilities[state]
    # print("Updating eval: elig:{}, current:{}".format(eligibility, current_eval))
    self.value_func[state] = current_eval + critic_learning_rate*self.delta*eligibility

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