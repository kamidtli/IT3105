from game.pegSolitaire import Game
from game.game_config import *


class Environment():

  def __init__(self, viz=False):
    self.game = Game(visualize=viz)

  def get_current_state(self):
    return self.game.get_state()

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def move(self, move):
    pos = (move[0], move[1]) # Get the pos of the cell to move
    direction = (move[2], move[3]) # Get the direction to move
    self.game.move_cell(pos, direction) # Move the peg

    return self.get_current_state() # Return the new state, with reward

  def get_remaining_pegs(self):
    return self.game.get_remaining_pegs()

  def show(self):
    self.game.show()