from nim import Nim
from ledge import Ledge

class GameSimulator():

  def __init__(self, game, G=None, B=None, P=None, M=None, N=None, K=None, verbose=False):
    self.type = game
    if game == "nim":
      self.game = Nim(N, K, P, verbose)
    elif game == "ledge":
      self.game = Ledge(B, P, verbose)
    else:
      print("Illegal value '{}' for paramter 'game'".format(game))

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def move(self, move):
    if isinstance(move, int):
      if self.type == "nim":
        self.move_nim(move)
    elif isinstance(move, tuple):
      if self.type == "ledge":
        self.move_ledge(move[0], move[1])
    else:
      print("Illegal value {} for parameter 'move'".format(move))

  def is_over(self):
    return self.game.is_terminal_state()

  def move_nim(self, amount):
    if amount != None:
      self.game.move(amount)
    else:
      print("You must specify a value for 'amount'")

  def move_ledge(self, from_index, to_index):
    if from_index == None or to_index == None:
      print("You must specify a value for 'from_index' and 'to_index'")
    else:
      self.game.move(from_index, to_index)