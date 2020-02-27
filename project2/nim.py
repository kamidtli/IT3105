import random

class Nim():
  def __init__(self, N, K, P, verbose=False):
    """
    Class for the game Nim.
    param N: Number of pieces to start the game with.
    param K: The maximum number of pieces allowed to remove each turn.
    param P: The starting player, 1, 2 or 3 (random).
    param verbose: Should play-by-play be displayed?
    """
    self.verbose = verbose
    self.start_pieces = N
    self.game_pile = N
    self.max_removable = K
    self.game_over = False
    
    if P == 3:
      self.active_player = random.randint(1, 2)
    else:
      self.active_player = P
    
    if verbose:
      print("Start pile: {} stones".format(self.start_pieces))

  def move(self, amount):
    """
    Performs a single move, removing 'amount' from the game pile.
    The move is performed by the active player. After the move the
    active player switches if the game is not over.
    param amount: The amount to remove from the game pile.
    """
    assert(1 <= amount <= self.max_removable and amount <= self.game_pile and not self.game_over)

    self.game_pile -= amount

    if self.verbose:
      print("Player {} removed {} stone(s): Remaining stone(s) = {}".format(
        self.active_player,
        amount,
        self.game_pile
        ))

    if self.game_pile == 0:
      self.game_over = True
      if self.verbose:
        print("Player {} wins".format(self.active_player))
    else:
      self.switch_active_player()


  def switch_active_player(self):
    """
    Switches the active player from 1 to 2, or 2 to 1
    """
    if self.active_player == 1:
      self.active_player = 2
    elif self.active_player == 2:
      self.active_player = 1
    else:
      print("Illegal value: {} for variable active_player in Nim.".format(self.active_player))

  def get_initial_state(self):
    """
    Returns the initial game state for this instance of Nim
    """
    return self.start_pieces

  def get_state(self):
    """
    Returns the current state of the game
    """
    return self.game_pile

  def get_active_player(self):
    """
    Returns the active player: 1 or 2
    """
    return self.active_player

  def get_max_removable(self):
    """
    Returns the maximum legal amount of stones to remove each round
    """
    return self.max_removable

  def get_legal_moves(self):
    """
    Returns a list of legal moves to perform at the
    current state of the game.
    """
    temp = min(self.max_removable, self.game_pile)
    return [i for i in range(1, temp+1)]

  def is_terminal_state(self):
    """
    Return True if the game is over, False if not.
    """
    return self.game_pile == 0