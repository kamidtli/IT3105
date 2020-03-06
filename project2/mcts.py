import random

class MCTS():

  def choose_move(self, game_state):
    moves = game_state.get_legal_moves()
    move = random.choice(moves)
    return move

  def tree_search(self):
    """
    Traversing the tree from the root to a leaf node by using the tree policy.
    """
    # TODO: Implement method
    return None

  def node_expansion(self):
    """
    Generating some or all child states of a parent state, and then connecting
    the tree node housing the parent state (a.k.a. parent node) to the nodes
    housing the child states (a.k.a. child nodes).
    """
    # TODO: Implement method
    return None

  def leaf_evaluation(self):
    """
    Estimating the value of a leaf node in the tree by doing a rollout
    simulation using the default policy from the leaf node’s state to a
    final state.
    """
    # TODO: Implement method
    return None

  def backpropagation(self):
    """
    Passing the evaluation of a final state back up the tree, updating
    relevant data (see course lecture notes) at all nodes and edges on
    the path from the final state to the tree root.
    """
    # TODO: Implement method
    return None