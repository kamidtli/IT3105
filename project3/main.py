import random
from state_manager import StateManager

sm = StateManager()

while len(sm.get_legal_moves()) > 0:
  move = random.choice(sm.get_legal_moves())
  sm.move(move)

  sm.print_board()

print("Game over, no more legal moves")