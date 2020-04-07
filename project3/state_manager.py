from config import *
from game.hex import Hex
from game.viz_hex import print_board

class StateManager():

  def __init__(self):
    self.game = Hex(board_size)
  
  def get_nn_state(self):
    return self.game.get_state()
  
  def get_state(self):
    return self.game.board.state

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def move(self, move):
    self.game.move(move)
  
  def print_board(self):
    print_board(self.get_state())
