from game.pegSolitaire import Game
from game.game_config import *


class Environment():

  def __init__(self):
    self.game = Game()

  def get_current_state(self):
    return self.game.get_state()

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def play(self):
    for i in range(num_of_episodes):
      legal_moves = self.game.get_legal_moves()
      while len(legal_moves) > 0:
        pos = (legal_moves[0][0], legal_moves[0][1])
        direction = (legal_moves[0][2], legal_moves[0][3])
        self.game.move_cell(pos, direction)
        legal_moves = self.game.get_legal_moves()

      game.show()

  def move(self, move):
    pos = (move[0], move[1]) # Get the pos of the cell to move
    direction = (move[2], move[3]) # Get the direction to move
    self.game.move_cell(pos, direction) # Move the peg

    return self.get_current_state()

  def show(self):
    self.game.show()

# for i in range(num_of_episodes):
#   game = Game(visualize=(i==0))
#   legal_moves = game.get_legal_moves()
#   while len(legal_moves) > 0:
#     pos = (legal_moves[0][0], legal_moves[0][1])
#     direction = (legal_moves[0][2], legal_moves[0][3])
#     game.move_cell(pos, direction)
#     legal_moves = game.get_legal_moves()

#   game.show()