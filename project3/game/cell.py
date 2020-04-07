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