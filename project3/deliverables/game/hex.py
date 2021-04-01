import random

from game.board import Board
from game.chain import Chain

class Hex():
  def __init__(self, size):
    self.board = Board(size)
    self.active_player = random.randint(1,2)
    self.game_over = False
    self.chains = {1: [], 2: []}

  def move(self, pos):
    if (not self.game_over and self.legal_move(pos)):
      cell = self.board.state[pos[0]][pos[1]]
      cell.value = self.active_player
      self.perform_chaining(cell)
      self.game_over = self.is_game_over()
      if not self.game_over:
        self.active_player = 3 % (self.active_player+1) + 1 # 1=>2, 2=>1
    else: print("Illegal move {}".format(pos))

  def legal_move(self, pos):
    return 0 <= pos[0] <= self.board.size-1 and 0 <= pos[1] <= self.board.size-1 and self.board.state[pos[0]][pos[1]].value == 0

  def get_legal_moves(self):
    legal = []
    for i in range(self.board.size):
      for j in range(self.board.size):
        if self.board.state[i][j].value == 0:
          legal.append((i, j))
    return legal

  def is_game_over(self):
    if self.connected_path():
      # print("Game over!\tWinner: {}".format(self.active_player))
      return True
    return False

  def connected_path(self):
    chains = self.chains[self.active_player]
    for chain in chains:
      if chain.connected:
        return True
    return False

  def perform_chaining(self, cell):
    c = self.create_chain(cell)
    neighbors = self.get_neighbor_chains(cell)
    if len(neighbors) > 0:
      merged_chain = self.merge_chains(c, neighbors)
      self.remove_chains(neighbors)
      self.chains[self.active_player].append(merged_chain)
    else:
      self.chains[self.active_player].append(c)

  def create_chain(self, cell):
    row, col = cell.pos
    if row == 0:
      if col == 0:
        sides = [1, 0] 
      elif col == self.board.size-1:
        sides = [1, 3]
      else:
        sides = [1]

    elif row == self.board.size-1:
      if col == 0:
        sides = [2, 0] 
      elif col == self.board.size-1:
        sides = [2, 3]
      else:
        sides = [2]

    elif col == 0:
      if row == 0:
        sides = [0, 1] 
      elif row == self.board.size-1:
        sides = [0, 2]
      else:
        sides = [0]

    elif col == self.board.size-1:
      if row == 0:
        sides = [3, 1] 
      elif row == self.board.size-1:
        sides = [3, 2]
      else:
        sides = [3]

    else:
      sides = []
    return Chain(sides=sides, nodes=[cell])

  def get_neighbor_chains(self, cell):
    chains = self.chains[self.active_player]
    neighbor_chains = []
    for neighbor in cell.neighbors.values():
      for chain in chains:
        if neighbor in chain.nodes:
          neighbor_chains.append(chain)
    return neighbor_chains

  def merge_chains(self, single_chain, chains_to_merge):
    if len(chains_to_merge) == 1:
      return self.merge(single_chain, chains_to_merge[0])
    else:
      new_chain = self.merge(single_chain, chains_to_merge[0])
      for i in range(1, len(chains_to_merge)):
        new_chain = self.merge(new_chain, chains_to_merge[i])
      return new_chain
      
  def merge(self, chain1, chain2):
    sides = list(set().union(chain1.sides, chain2.sides))
    nodes = list(set().union(chain1.nodes, chain2.nodes))
    connected = False
    if self.active_player == 1 and (1 in sides and 2 in sides):
      connected = True
    elif self.active_player == 2 and (0 in sides and 3 in sides):
      connected = True
    return Chain(sides=sides, connected=connected, nodes=nodes)

  def remove_chains(self, neighbors):
    self.chains[self.active_player] = list(set(self.chains[self.active_player])^set(neighbors))

  def get_nn_state(self):
    flattened_state = [cell.value for row in self.board.state for cell in row]
    flattened_state.insert(0, self.active_player)
    return tuple(flattened_state)

  def get_state(self):
    return self.board.state

  def get_winner(self):
    if self.is_game_over():
      return 1 if self.active_player == 1 else -1

  def get_active_player(self):
    return self.active_player