from cell import Cell

class Board():

  def __init__(self, shape, size, openCells):
    self.size = size
    self.shape = shape
    self.openCells = openCells
    self.grid = self.generateGrid(shape, size)

  # Returns a complete grid (2D-list containing cell objects) with the defined 'shape' and 'size', where
  # all nodes are assigned neighbors
  def generateGrid(self, shape, size):
    if (shape == "triangle"):
      return self.generateTriangleGrid(size)
    elif (shape == "diamond"):
      return self.generateDiamondGrid(size)
    else:
      print("Invalid shape: {}".format(shape))
      return None

  def generateTriangleGrid(self, size):
    grid = []
    prevRow = []
    for i in range(size):
      row = []
      currentRow = []
      for j in range(i+1):
        cell = Cell(pos=(i, j), isOccupied=(i, j) not in self.openCells)
        if (i > 0 and j < i):
          cell.addNeighbor((0, -1), prevRow[j]) # Add top neighbor

        if (j > 0):
          cell.addNeighbor((-1, 0), currentRow[-1]) # Add left neighbor
          cell.addNeighbor((-1, -1), prevRow[j-1]) # Add top-left neighbor

        row.append(cell)
        currentRow.append(cell)
      prevRow = currentRow
      currentRow = []
      grid.append(row)
    return grid

  def generateDiamondGrid(self, size):
    grid = []
    prevRow = []
    for i in range(size):
      row = []
      currentRow = []
      for j in range(size):
        cell = Cell(pos=(i, j), isOccupied=(i, j) not in self.openCells)
        if (i > 0):
          cell.addNeighbor((0, -1), prevRow[j]) # Add top neighbor

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

  def get_cell(self, pos):
    try:
      return self.grid[pos[0]][pos[1]]
    except IndexError:
      print("Index {} out of bounds".format(pos))
    
  def get_remaining_pegs(self):
    remaining_pegs = 0
    for row in self.grid:
      for cell in row:
        if cell.isOccupied:
          remaining_pegs += 1
    return remaining_pegs

  def get_legal_moves(self):
    legal_moves = []
    for row in self.grid:
      for cell in row:
        single_cell_legal_moves = cell.get_legal_moves()
        for move in single_cell_legal_moves:
          legal_moves.append(move)
    return legal_moves


  def get_state(self):
    # Creates a 2D grid representing the state of the board, where 0 indicates
    # an empty cell and 1 indicates an occupied cell
    state = []
    for i in range(len(self.grid)):
      row = []
      for j in range(len(self.grid[i])):
        if self.grid[i][j].isOccupied:
          row.append(1)
        else:
          row.append(0)
      state.append(row)
    return state

  def show(self):
    print()

    if (self.shape == "triangle"):
      for row in self.grid:
        rowStr = ""
        for cell in row:
          if cell.isOccupied:
            rowStr += "● "
          else:
            rowStr += "○ "
        centeredStr = rowStr.center(self.size * 2) 
        print(centeredStr)
    else:
      display_lines = []
      for i in range(self.size):
        for j in range(self.size):
          try:
            display_lines[i+j].append(self.get_cell((j, i)))
          except:
            display_lines.append([])
            display_lines[i+j].append(self.get_cell((j, i)))

      for line in display_lines:
        rowStr = ""
        for cell in line:
          if cell.isOccupied:
            rowStr += "● "
          else:
            rowStr += "○ "
        centeredStr = rowStr.center(self.size * 2) 
        print(centeredStr)

    print()
