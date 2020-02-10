import game.game_config as params
from game.board import Board
from game.visualization import Visualizer

class Game():

  def __init__(self, visualize=True):
    self.visualize = visualize
    self.board = Board(params.shape, params.size, params.openCells)
    if visualize:
      self.viz = Visualizer(self.board)

  def move_cell(self, pos, direction):
    cell_to_move = self.board.get_cell(pos)
    cell_to_move.move(direction)
    if self.visualize:
      self.viz.add_game_state(self.board) # Update the visualization

    return self.get_state()
  
  def game_won(self):
    return self.board.get_remaining_pegs() == 1

  def get_legal_moves(self):
    return self.board.get_legal_moves()

  def is_finished(self):
    return len(self.board.get_legal_moves()) == 0 or self.board.get_remaining_pegs() == 1

  def get_status(self):
    if self.game_won():
      return 1
    elif self.is_finished() and not self.game_won():
      return -1
    else:
      return 0

  def get_state(self):
    board = self.board.get_state()
    legal_moves = self.get_legal_moves()
    status = self.get_status()
    if self.is_finished() and not self.game_won():
      reward = -10
    elif self.game_won():
      reward = 10
    else:
      reward = 0
    return (board, legal_moves, reward, status)

  def show(self):
    if self.visualize:
      self.viz.show()


