from viz_hex import print_board

class Cell():
  def __init__(self, pos, value):
    self.pos = pos
    self.value = value
    self.neighbors = {}

  def addNeighbor(self, direction, cell):
    if direction not in self.neighbors:
      self.neighbors[direction] = cell
      oppositeDirection = (-direction[0], -direction[1])
      cell.addNeighbor(oppositeDirection, self)
  
  def __repr__(self):
    return str(self.value)

class Board():
  def __init__(self, size):
    self.size = size
    self.state = self.generateBoard(size)
  
  def generateBoard(self, size):
    grid, prevRow = ([], [])
    for i in range(size):
      row, currentRow = ([], [])
      for j in range(size):
        cell = Cell(pos=(i, j), value=(0))
        if (i > 0): cell.addNeighbor((0, -1), prevRow[j]) # Add top neighbor

        if (i > 0 and j < size-1):
          cell.addNeighbor((1, -1), prevRow[j+1]) # Add top-right neighbor

        if (j > 0):
          cell.addNeighbor((-1, 0), currentRow[-1]) # Add left neighbor

        row.append(cell)
        currentRow.append(cell)
      prevRow = currentRow
      currentRow = []
      grid.append(row)
    return grid

  def __repr__(self):
    return str(self.state)

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
    
    if self.connected_path():
      print("Game over!")
      return True
    
    return False

  def connected_path(self):
    return False

game = Hex(4)
game.move((0, 0))
game.move((1, 0))
game.move((0, 1))
game.move((1, 1))
game.move((0, 2))
game.move((1, 2))
game.move((0, 3))

print_board(game.board.state)
