from game_simulator import GameSimulator

import numpy as np

def run():
  gs = GameSimulator("nim", G=1, P=1, M=0, N=10, K=3, verbose=True)
  while not gs.is_over():
    moves = gs.get_legal_moves()
    move = np.random.choice(np.asarray(moves))
    print("Moving", move)
    gs.move(move)


if __name__=="__main__":
  run()