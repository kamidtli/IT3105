from game.cell import Cell

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