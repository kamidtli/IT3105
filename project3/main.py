import random
from config import *
from anet import ANET
from state_manager import StateManager
from mcts import MCTS
from tree import Tree
from utils import Timer
import numpy as np

def progress_bar(current_game):
  percentage = int((current_game / num_of_games)*100)
  print("Episode: {}/{} {}%".format(current_game, num_of_games, percentage))

def train_anet(anet, RBUF):
  # Creates a minibatch of the RBUF and trains the anet on the minibatch
  batch_size = np.random.randint(1, len(RBUF))
  random.shuffle(RBUF)
  minibatch = RBUF[:batch_size]
  anet.train(minibatch)

""" Initializations """
anet = ANET(board_size**2 + 1, board_size**2)
agent = MCTS(exploration_rate=1, anet=anet)
sm = StateManager()
game = sm.create_game()
tree = Tree(game)
win_stats = []

# TODO: Remove timer
timer = Timer()

# TODO: Save interval for ANET parameters
RBUF = []
# TODO: Randomly initialize parameters of ANET

for i in range(num_of_games):
  progress_bar(i+1)
  state = tree.root

  while (not sm.is_game_over()):
    timer.start("choose move")
    best_child, training_case = agent.uct_search(tree, state, num_search_games)
    timer.stop()
    RBUF.append(training_case)
    game.move(best_child.move)
    state = best_child

  # Train ANET on a random minibatch from RBUF
  t2 = Timer()
  t2.start('training')
  train_anet(anet, RBUF)
  t2.stop()

  if i % save_interval == 0:
    # TODO: Save ANET parameters for later use in tournament play
    print("TODO: Save ANET parameters for later use in tournament play")

  win_stats.append(game.get_winner())
  print("Player {} won the game!".format(1 if game.get_winner() == 1 else 2))

  game = sm.create_game()
  tree = Tree(game)

player1_wins = win_stats.count(1)
percentage = int((player1_wins / num_of_games) * 100)
print("Player 1 won {} of {} games ({}%)".format(player1_wins, num_of_games, percentage))
