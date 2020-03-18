from game_simulator import GameSimulator

import random

def run():
  gs = GameSimulator(
    game="nim",
    G=10,
    P=1,
    M=500,
    N=10,
    K=3,
    c=1,
    verbose=True
  )

  # gs = GameSimulator(
  #   game="ledge", 
  #   G=10, 
  #   B=[0, 0, 0, 1, 0, 2, 0, 0, 1, 0], 
  #   P=1, 
  #   M=500,
  #   c=1, 
  #   verbose=True
  # )

  gs.run_batch()

if __name__=="__main__":
  run()