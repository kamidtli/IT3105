from agent.agent_config import *

# The critic maps each state to values, either by using a table or a neural network
class Critic():

  def __init__(self):
    if critic_type == "neural_net":
      self.value_func = self.init_nn()
    else:
      self.value_func = self.init_table()
    
    self.eligibilities = {}
    print("Critic initialized with {} as mapping function.".format(critic_type))

  def init_nn(self):
    # TODO: Initialize neural net table
    return None
  
  def init_table(self):
    table = {}
    return table
  
  def reset_eligibilities(self):
    # TODO: Reset eligibilites
    print("Reset eligibilities in critic")