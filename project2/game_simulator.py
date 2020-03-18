from nim import Nim
from ledge import Ledge
from mcts import MCTS
from tree import Tree

class GameSimulator():

  def __init__(self, game, G=None, B=None, P=None, M=None, N=None, K=None, c=1, verbose=False):
    """
    Intiialize the game simulator by checking if all parameters have legal values.
    Will throw AssertionError if illegal arguments are passed in
    """
    assert(game in ["nim", "ledge"]) # Check legal values for game
    assert(G != None and G > 0) # Check legal values for number of episodes
    assert(P != None and P in [1, 2, 3]) # Check legal values for starting player
    assert(M != None) # Check legal values for rollout number
    
    if game == "nim":
      assert(K != None and K > 1) # Check legal values for max removable stones
      assert(N != None and N > K) # Check legal values for stones
    else:
      assert(B != None and type(B) == type([])) # Check legal values for inital board
      assert(B.count(1) < len(B)) # Check legal values for copper coins
      assert(B.count(2) == 1) # Check legal values for gold coin

    self.type = game
    self.G = G
    self.P = P
    self.M = M
    self.B = B
    self.N = N
    self.K = K
    self.c = c
    self.verbose = verbose

  def create_game(self):
    if self.type == "nim":
      game = Nim(self.N, self.K, self.P, self.verbose)
    else:
      game = Ledge(self.B, self.P, self.verbose)
    return game

  def run_batch(self):
    """
    Runs G games of the specified type (Nim or Ledge). All parameters are fixed
    for all runs. Summarizes the results of the batch run in a print-sentence. 
    Creates a new instance of the game and for each move, asks the agent for an
    action. This action is applied and chancges the state of the board. When a
    final state is reached, the results are given to the agent for backpropagation
    and a new game instance is made.
    Returns a list of round winners
    """
    agent = MCTS(exploration_rate=self.c)
    win_stats = []

    game = self.create_game()
    tree = Tree(game)

    for i in range(self.G):
      state = tree.root

      while (not game.is_terminal_state()):
        best_child = agent.uct_search(tree, state, self.M)
        game.move(best_child.move)
        state = best_child
      
      win_stats.append(game.get_active_player())
      game = self.create_game()
      tree = Tree(game)

    self.summarize_batch(win_stats)
    return win_stats

  def summarize_batch(self, batch_stats):
    player1_wins = batch_stats.count(1)
    percentage = int((player1_wins / self.G) * 100)
    print("Player 1 won {} of {} games ({}%)".format(player1_wins, self.G, percentage))
