from pegSolitaire import Game
from config import *

for i in range(num_of_episodes):
  game = Game(visualize=False)
  legal_moves = game.get_legal_moves()
  while len(legal_moves) > 0:
    pos = (legal_moves[0][0], legal_moves[0][1])
    direction = (legal_moves[0][2], legal_moves[0][3])
    game.move_cell(pos, direction)
    legal_moves = game.get_legal_moves()

  game.show()
