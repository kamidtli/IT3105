import random
from config import *
from state_manager import StateManager
from mcts import MCTS
from tree import Tree

def progress_bar(current_game):
  percentage = int((current_game / num_of_games)*100)
  print("Games: {}/{} {}%".format(current_game, num_of_games, percentage), end='\r')

""" Initializations """
agent = MCTS(exploration_rate=1)
sm = StateManager()
game = sm.create_game()
tree = Tree(game)
win_stats = []

# TODO: Save interval for ANET parameters
# TODO: Clear replay buffer
# TODO: Randomly initialize parameters of ANET

for i in range(num_of_games):
  progress_bar(i+1)
  state = tree.root

  while (not sm.is_game_over()):
    best_child = agent.uct_search(tree, state, num_search_games)
    game.move(best_child.move)
    state = best_child

  win_stats.append(game.get_winner())

  game = sm.create_game()
  tree = Tree(game)

player1_wins = win_stats.count(1)
percentage = int((player1_wins / num_of_games) * 100)
print("Player 1 won {} of {} games ({}%)".format(player1_wins, num_of_games, percentage))
