from pegSolitaire import Game

game = Game()

legal_moves = game.get_legal_moves()
game.show()
print(game.get_state())
while len(legal_moves) > 0:
  pos = (legal_moves[0][0], legal_moves[0][1])
  direction = (legal_moves[0][2], legal_moves[0][3])
  print("Legal moves:", legal_moves)
  game.move_cell(pos, direction)
  game.show()
  print(game.get_state())
  legal_moves = game.get_legal_moves()