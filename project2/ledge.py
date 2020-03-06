import random
import copy
import numpy as np

class Ledge():
  def __init__(self, B, P, verbose=False):
    """
    Class for the game Ledge.
    param B: Initial board
    param P: The starting player, 1, 2 or 3 (random).
    param verbose: Should play-by-play be displayed?
    """
    self.verbose = verbose
    self.initial_state = B
    self.state = copy.deepcopy(B)
    self.game_over = False
    
    if P == 3:
      self.active_player = random.randint(1, 2)
    else:
      self.active_player = P
    
    if verbose:
      print("Start board: {}".format(np.asarray(self.initial_state)).rjust(35+len(self.state)*2, " "))

  def move(self, from_index, to_index):
    """
    Decides if the desired move is to pick up coin at ledge
    or to move a coin. Calls the corresponding method.
    param from_index: Passed to move_coin
    param to_index: Passed to move_coin
    """
    assert(not self.game_over) # Check if game is over
    if from_index == -1 or to_index == -1:
      # Want to pick up coin at ledge
      self.pickup_coin()
    else:
      # Want to move coin
      self.move_coin(from_index, to_index)

  def pickup_coin(self):
    """
    Picks up the coin at the ledge if it is a legal move.
    If not throws an AssertionError
    """
    assert(self.state[0] != 0) # Ledge must contain a coin

    coin_type = "copper" if self.state[0] == 1 else " gold "

    self.state[0] = 0

    if self.verbose:
      print("P{} picks up {}: {}".format(
        self.active_player,
        coin_type,
        np.asarray(self.state)
        ).rjust(35+len(self.state)*2, " "))

    if not 2 in self.state:
      self.game_over = True
      if self.verbose:
        print("Player {} wins".format(self.active_player).rjust(35+len(self.state)*2, " "))
    else:
      self.switch_active_player()
  
  def move_coin(self, from_index, to_index):
    """
    Performs a single move, moving/removing a single coin.
    The move is performed by the active player. After the move the
    active player switches if the game is not over.
    param from_index: The index of the coin to move.
    param to_index: The index of the target position for the move.
    """
    assert(self.state[from_index] != 0) # Cannot move empty cell
    assert(to_index < from_index) # Must move coin left
    assert(sum(self.state[to_index:from_index]) == 0) # Cannot jump over a coin

    coin_type = "copper" if self.state[from_index] == 1 else " gold "

    self.state[to_index] = self.state[from_index]
    self.state[from_index] = 0

    if self.verbose:
      print("P{} moves {} from cell {} to {}: {}".format(
        self.active_player,
        coin_type,
        from_index,
        to_index,
        np.asarray(self.state)
        ))

    if not 2 in self.state:
      self.game_over = True
      if self.verbose:
        print("Player {} wins".format(self.active_player).rjust(35+len(self.state)*2, " "))
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
    return self.initial_state

  def get_state(self):
    """
    Returns the current state of the game
    """
    return self.state

  def get_active_player(self):
    """
    Returns the active player: 1 or 2
    """
    return self.active_player

  def get_legal_moves(self):
    """
    Returns a list of legal moves to perform at the
    current state of the game. Format of the list is
    [(from_index, to_index), (from_index, to_index), ...]
    """
    legal_moves = []
    for i in range(len(self.state)-1, 0, -1):
      if self.state[i] != 0:
        for j in range(i-1, -1, -1):
          if self.state[j] == 0:
            legal_moves.append((i, j))
          else:
            break
    
    if self.state[0] != 0:
      legal_moves.append((-1, -1))
    
    return legal_moves

  def is_terminal_state(self):
    """
    Return True if the game is over, False if not.
    """
    return not 2 in self.state