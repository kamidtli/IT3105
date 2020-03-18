from copy import deepcopy

class Node():

  def __init__(self, board, parent=None, move=None):
    """
    A class representing a node in the MCTS tree.
    """
    self.state = board.get_state()
    self.parent = parent
    self.board = board
    self.move = move
    self.Q = 0
    self.visits = 0
    self.children = []

  def __repr__(self):
    return str(self.board.get_state())

  def print_info(self):
    print("Node:", self.state)
    print("\tParent:", self.parent)
    print("\tScore:", self.Q)
    print("\tVisits:", self.visits)
    print("\tChildren:", self.children)