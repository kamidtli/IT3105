import random
from config import num_of_games, num_search_games, save_interval, board_size, offset, rbuf_max_size, verbose, save_dir
from anet import ANET
from state_manager import StateManager
from mcts import MCTS
from tree import Tree
import numpy as np
import collections

def train_anet(anet, RBUF):
  # Creates a minibatch of the RBUF and trains the anet on the minibatch
  batch_size = min(len(RBUF), 32)
  minibatch = random.sample(RBUF, batch_size)
  anet.train(minibatch)

""" Initializations """
anet = ANET(size=board_size)
agent = MCTS(exploration_rate=1, anet=anet)
sm = StateManager()
game = sm.create_game()
tree = Tree(game)
win_stats = []
RBUF = collections.deque(maxlen=rbuf_max_size)

for i in range(offset, num_of_games+1):
  print("Episode: {}/{}".format(i, num_of_games))
  state = tree.root

  while (not sm.is_game_over()):
    best_child, training_case = agent.uct_search(tree, state, num_search_games)
    RBUF.append(training_case)
    sm.move(best_child.move)
    state = best_child
    if verbose and i == num_of_games:
      sm.print_board()

  if save_interval > 0 and i == offset:
    anet.model.save("./{}/size_{}-ep_{}.h5".format(save_dir, board_size, i))
    print("Saved model to: ./{}/size_{}-ep_{}.h5".format(save_dir, board_size, i))

  train_anet(anet, RBUF)

  if save_interval > 0 and (i % save_interval == 0):
    anet.model.save("./{}/size_{}-ep_{}.h5".format(save_dir, board_size, i))
    print("Saved model to: ./{}/size_{}-ep_{}.h5".format(save_dir, board_size, i))

  win_stats.append(game.get_winner())
  print("Player {} won the game!".format(1 if game.get_winner() == 1 else 2))

  agent.decay_epsilon()
  game = sm.create_game()
  tree = Tree(game)

player1_wins = win_stats.count(1)
percentage = int((player1_wins / num_of_games) * 100)
print("Player 1 won {} of {} games ({}%)".format(player1_wins, num_of_games, percentage))
