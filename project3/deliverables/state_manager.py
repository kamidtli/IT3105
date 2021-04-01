from config import *
from game.hex import Hex
from game.viz_hex import print_board

class StateManager():

  def __init__(self, size=None):
    self.game = Hex(size if size != None else board_size)
  
  def create_game(self):
    game = Hex(board_size)
    self.game = game
    return game

  def get_nn_state(self):
    return self.game.get_nn_state()
  
  def get_state(self):
    return self.game.board.state

  def get_legal_moves(self):
    return self.game.get_legal_moves()

  def move(self, move):
    self.game.move(move)
  
  def is_game_over(self):
    return self.game.is_game_over()

  def get_winner(self):
    return self.game.get_winner()

  def print_board(self):
    print_board(self.get_state(), self.game.active_player)
