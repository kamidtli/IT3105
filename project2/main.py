from game_simulator import GameSimulator

import random

def run():
  gs = GameSimulator("nim", G=1, P=1, M=0, N=10, K=3, verbose=True)
  # gs = GameSimulator("ledge", G=1, B=[0, 0, 0, 1, 0, 2, 0, 0, 1, 0], P=1, M=0, verbose=True)

  while not gs.is_over():
    moves = gs.get_legal_moves()
    move = random.choice(moves)
    gs.move(move)
  


if __name__=="__main__":
  run()