from nim import Nim
from ledge import Ledge
from mcts import MCTS

class GameSimulator():

  def __init__(self, game, G=None, B=None, P=None, M=None, N=None, K=None, verbose=False):
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
    self.verbose = verbose

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
    win_stats = []
    for i in range(self.G):
      if self.type == "nim":
        game = Nim(self.N, self.K, self.P, self.verbose)
      else:
        game = Ledge(self.B, self.P, self.verbose)

      agent = MCTS()

      while (not game.is_terminal_state()):
        move = agent.choose_move(game)
        self.move(game, move)
      
      win_stats.append(game.get_active_player())

    self.summarize_batch(win_stats)
    return win_stats

  def get_legal_moves(self):
    """
    Returns the a list of the legal moves for the
    specified game, by calling get_legal_moves
    """
    return self.game.get_legal_moves()

  def move(self, game, move):
    """
    Call the correct move method for either Nim or Ledge
    param move: Either an int or a tuple. Int if the move
    is for Nim, tuple of from_index and to_index if move is
    for Ledge.
    """
    if isinstance(move, int):
      if self.type == "nim":
        self.move_nim(game, move)
    elif isinstance(move, tuple):
      if self.type == "ledge":
        self.move_ledge(game, move[0], move[1])
    else:
      print("Illegal value {} for parameter 'move'".format(move))

  def is_over(self):
    """
    Returns True if the current game state is terminal, False if not
    """
    return self.game.is_terminal_state()

  def move_nim(self, game, amount):
    """
    Performs a move for the game Nim
    param amount: The amount of stones to remove from the pile
    """
    if amount != None:
      game.move(amount)
    else:
      print("You must specify a value for 'amount'")

  def move_ledge(self, game, from_index, to_index):
    """
    Performs a move for the game Ledge
    param from_index: The index to move coin from
    param to_index: The index to move coin to
    """
    if from_index == None or to_index == None:
      print("You must specify a value for 'from_index' and 'to_index'")
    else:
      game.move(from_index, to_index)

  def summarize_batch(self, batch_stats):
    player1_wins = batch_stats.count(1)
    percentage = int((player1_wins / self.G) * 100)
    print("Player 1 won {} of {} games ({}%)".format(player1_wins, self.G, percentage))