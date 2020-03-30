from node import Node

class Tree():

  def __init__(self, game):
    self.root = self.create_node(game)
    self.nodes = []

  def create_node(self, game, parent=None, move=None):
    return Node(board=game, parent=parent, move=move)
