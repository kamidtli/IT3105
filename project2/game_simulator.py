from nim import Nim


class GameSimulator():

  def __init__(self, game, G, P, M, N, K, verbose=False):
    if game == "nim":
      self.game = Nim(N, K, P, verbose)
    else:
      print("TODO: Create Ledge game")

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def move(self, amount):
    self.game.move(amount)

  def is_over(self):
    return self.game.is_terminal_state()