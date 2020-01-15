from pegSolitaire import Game

game = Game()

game.show()

print(game.get_state())

game.move_cell((2, 0), "RIGHT")

game.show()

print(game.get_state())
# game.move_cell((3, 3), "LEFT")

# game.show()