import networkx as nx
import matplotlib.pyplot as plt
import config as params

class Visualizer():

  def __init__(self, board):
    self.nodes, self.layout, self.edges = self.unpack_board(board)
    self.graph = self.create_graph()
    self.color_map = self.create_color_map()

  def create_graph(self):
    G = nx.Graph()
    G.add_nodes_from(self.nodes)
    G.add_edges_from(self.edges)
    return G

  def unpack_board(self, board):
    nodes = []
    layout = {}
    edges = []
    # Iterates over the board and adds the nodes and corresponding positions
    for row in board.grid:
      for node in row:
        nodes.append(node)
        layout[node] = self.rotate(node.pos)
        for neighbor in node.neighbors.values():
          if (node, neighbor) or (neighbor, node) not in edges:
            edges.append((node, neighbor))
    return nodes, layout, edges

  def rotate(self, pos, shape=params.shape):
    grid_width = 2*params.size - 2  # 0-indexed
    if shape == "triangle":
      x = grid_width/2 - pos[0] + 2 * pos[1]
      y = grid_width/2 - pos[0]
    else:
      x = grid_width/2 - pos[0] + pos[1] - 2
      y = grid_width - (pos[0] + pos[1])
    return (x, y)

  def create_color_map(self):
    color_map = []
    for node in self.graph:
      if node.isOccupied:
        color_map.append("green")
      else:
        color_map.append("black")
    return color_map

  def update_board(self):
    self.graph = self.create_graph()
    self.color_map = self.create_color_map()

  def show_plot(self, timeout):

    def close_event():
      plt.close()

    # Create a timer object with an interval of timeout (ms), then adding a callback function
    fig = plt.figure()
    timer = fig.canvas.new_timer(interval=timeout)
    timer.add_callback(close_event)
  
    # Start the timer before plotting. The code continues while the timer is active
    timer.start()
    plt.show()

  def show(self):
    self.update_board()
    plt.subplot(111)
    nx.draw(self.graph, pos=self.layout, node_color=self.color_map, with_labels=False)
    # self.show_plot(2000)
    plt.show()
