import random
from state_manager import StateManager

sm = StateManager()
while (not sm.is_game_over()):
  move = random.choice(sm.get_legal_moves())
  sm.move(move)

  sm.print_board()
