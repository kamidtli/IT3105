import game.game_config as params

class Cell():

  def __init__(self, pos, isOccupied=True):
    self.isOccupied = isOccupied
    self.pos = pos
    self.neighbors = {}

  def addNeighbor(self, direction, cell):
    if direction not in self.neighbors:
      self.neighbors[direction] = cell
      oppositeDirection = (-direction[0], -direction[1])
      cell.addNeighbor(oppositeDirection, self)

  def setOccupied(self, newState):
    self.isOccupied = newState

  def is_legal(self, direction, verbose=True):
    info_message = ""

    if not self.isOccupied: # Cell does not contain a peg
      info_message += "Illegal move: Cell {} does not contain a peg".format(self.pos)
      return False

    if direction in self.neighbors: # If the peg can move in the chosen direction
      adjacentCell = self.neighbors[direction] # Get the cell to jump over
      if not adjacentCell.isOccupied:
        info_message += "Illegal move: Cannot jump over an empty cell"
        return False
      elif direction not in adjacentCell.neighbors:
        info_message += "Illegal move: Destination cell does not exist"
        return False
      elif adjacentCell.neighbors[direction].isOccupied:
        info_message += "Illegal move: Destination cell is occupied"
        return False
    else:
      info_message += "Illegal move: Cannot jump out of the board"
      return False

    if verbose:
      print(info_message)

    return True

  def move(self, direction):
    if self.is_legal(direction):
      adjacentCell = self.neighbors[direction] # Get the cell to jump over
      self.setOccupied(False)
      adjacentCell.setOccupied(False)
      adjacentCell.neighbors[direction].setOccupied(True)

  def get_legal_moves(self):
    legal_moves = []
    for key, move in params.directions.items():
      # print("Cell: {} Move: ".format(self.pos), move)
      if self.is_legal(move, verbose=False):
        x_coord = self.pos[0]
        y_coord = self.pos[1]
        x_move = move[0]
        y_move = move[1]
        legal_moves.append((x_coord, y_coord, x_move, y_move))
    # print("Cell {} has the legal moves:".format(self.pos), legal_moves)
    return legal_moves

  # def move(self, direction):
  #   if not self.isOccupied:
  #     print("Illegal move: Cell {} does not contain a peg".format(self.pos))
  #     return False
  #   if direction in self.neighbors: # If the peg can move in the chosen direction
  #     adjacentCell = self.neighbors[direction] # Get the cell to jump over
  #     if not adjacentCell.isOccupied:
  #       print("Illegal move: Cannot jump over an empty cell")
  #       return False
      
  #     if direction not in adjacentCell.neighbors:
  #       print("Illegal move: Destination cell does not exist")
  #       return False

  #     if adjacentCell.neighbors[direction].isOccupied:
  #       print("Illegal move: Destination cell is occupied")
  #       return False
      
  #     self.setOccupied(False)
  #     adjacentCell.setOccupied(False)
  #     adjacentCell.neighbors[direction].setOccupied(True)
  #     return True

  #   print("Illegal move: Cannot jump out of the board")
  #   return False
  
  def __repr__(self):
    # if (self.isOccupied):
    #   return "●"
    # return "○"

    return str(self.pos)
