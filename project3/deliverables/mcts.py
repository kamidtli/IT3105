import random
import math
from copy import deepcopy
import numpy as np
from utils import normalize
from config import epsilon_start_value, epsilon_decay_rate

class MCTS():

  def __init__(self, exploration_rate, anet):
    self.c = exploration_rate
    self.epsilon = epsilon_start_value
    self.anet = anet

  def uct_search(self, tree, node, M):
    """
    The main MCTS algorithm. Runs M simulations to create the tree.
    Then selects the best child state for the given input state
    """
    board = deepcopy(node.board)
    for i in range(M):
      self.simulate(tree, node)

    D = self.get_node_arc_visits(node)
    training_case = (node.state, D)
    node.board = board

    best_move = (np.argmax(D)//node.board.board.size, np.argmax(D)%node.board.board.size)
    for child in node.children:
      if child.move == best_move:
        del board
        return (child, training_case)

  def get_node_arc_visits(self, node):
    board_size = node.board.board.size
    distributions = [0]*board_size**2
    for i, child in enumerate(node.children):
      row, col = child.move
      distributions[row * board_size + col] = child.visits
    D = normalize(distributions)
    return tuple(D)

  def simulate(self, tree, node):
    """
    The general simulation algorithm, tree traversal, rollout and backprop.
    """
    selected_node = self.sim_tree(tree, node)
    z = self.sim_default(selected_node.board)
    self.backup(selected_node, z)

  def sim_tree(self, tree, node):
    """
    Traversing the tree from the root to a leaf node by using the tree policy.
    """
    c = self.c
    board = deepcopy(node.board)
    board.verbose = False
    while (not board.is_game_over()):
      if not node in tree.nodes:
        self.new_node(tree, node)
        del board
        return node

      node = self.select_best_child(node, c)
      board.move(node.move)
    del board
    return node

  def new_node(self, tree, node):
    """
    Generating some or all child states of a parent state, and then connecting
    the tree node housing the parent state (a.k.a. parent node) to the nodes
    housing the child states (a.k.a. child nodes).
    """
    tree.nodes.append(node)
    node.Q = 0
    node.visits = 0
    for a in node.board.get_legal_moves():
      board = deepcopy(node.board)
      board.verbose = False
      board.move(a)
      child_node = tree.create_node(board, node, a)
      node.children.append(child_node)
      del board

  def sim_default(self, board):
    """
    Estimating the value of a leaf node in the tree by doing a rollout
    simulation using the default policy from the leaf node’s state to a
    final state.
    """
    def default_policy(board):
      return self.anet.choose_move(board)
      
    def random_policy(board):
      moves = board.get_legal_moves()
      return random.choice(moves)

    game = deepcopy(board)
    game.verbose = False
    while (not game.is_game_over()):
      if (random.uniform(0, 1) > self.epsilon):
        a = default_policy(game)
      else:
        a = random_policy(game)
      game.move(a)
    winner = game.get_winner()
    del game
    return winner

  def backup(self, selected_node, result):
    """
    Passing the evaluation of a final state back up the tree, updating
    relevant data (see course lecture notes) at all nodes and edges on
    the path from the final state to the tree root.
    """
    node = selected_node
    while node != None:
      node.visits += 1
      node.Q += (result - node.Q) / node.visits
      node = node.parent

  def select_best_child(self, node, c):
    """
    Selects the best child of a given state, based on the node visits
    and scores (Q-values).
    """
    board = node.board
    active_player = board.get_active_player()
    # True if player is 2 (2 - 1 = 1 = True), false if 1 (1-1=0=False)
    minimizing = active_player - 1 
    children = node.children
    child_scores = []
    for child in children:
      uct = c * math.sqrt(math.log(node.visits) / (child.visits + 1))
      score = child.Q - uct if minimizing else child.Q + uct
      child_scores.append(score)

    if (minimizing):
      best_child_index = np.argmin(child_scores)
    else:
      best_child_index = np.argmax(child_scores)
    
    return children[best_child_index]

  def decay_epsilon(self):
    self.epsilon = self.epsilon * epsilon_decay_rate