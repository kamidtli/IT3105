from game.board import Board

class Hex():
  def __init__(self, size):
    self.board = Board(size)
    self.active_player = 1
    self.game_over = False

  def move(self, pos):
    if (not self.game_over and self.legal_move(pos)):
      self.board.state[pos[0]][pos[1]].value = self.active_player
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
    flattened_state = [cell.value for row in self.board.state for cell in row]
    if flattened_state.count(self.active_player) < self.board.size:
      return False
    
    if len(self.get_legal_moves()) == 0:
      return True
    
    if self.connected_path():
      print("Game over!")
      return True
    
    return False

  def connected_path(self):
    active_player = self.active_player

    return False

  def get_nn_state(self):
    flattened_state = [cell.value for row in self.board.state for cell in row]
    flattened_state.insert(0, self.active_player)
    return tuple(flattened_state)

