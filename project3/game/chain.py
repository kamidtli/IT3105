class Chain():

  def __init__(self, sides=[], connected=False, nodes=[]):
    self.sides = sides
    self.nodes = nodes
    self.connected = connected

  def __repr__(self):
    return "Chain: sides={}, connected={}, nodes={}".format(self.sides, self.connected, self.nodes)