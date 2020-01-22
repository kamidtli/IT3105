import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import config as params

class Visualizer():

  def __init__(self, board):
    self.game_graphs = [] # List of all graphs corresponding to states in an episode 
    self.add_game_state(board)

  def create_graph(self, nodes, edges, layout):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    G.graph["color_map"] = self.create_color_map(G)
    G.graph["layout"] = layout
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

  def create_color_map(self, graph):
    color_map = []
    for node in graph:
      if node.isOccupied:
        color_map.append("#e83023")
      else:
        color_map.append("#424242")
    return color_map

  def add_game_state(self, new_board):
    nodes, layout, edges = self.unpack_board(new_board)
    new_graph = self.create_graph(nodes, edges, layout)
    self.game_graphs.append(new_graph)

  def draw_graph(self, G):
    color_map = G.graph["color_map"]
    layout = G.graph["layout"]
    nx.draw(G, pos=layout, node_color=color_map, node_size=[1000], with_labels=False)

  def show(self):

    fig = plt.figure()

    def animate(i):
      graph = self.game_graphs[i]
      self.draw_graph(graph)

    # Init only required for blitting to give a clean slate.
    def init():
      plt.subplot(111)
      self.draw_graph(self.game_graphs[0])
      
    ani = animation.FuncAnimation(fig, animate, range(1, len(self.game_graphs)), init_func=init, interval=params.delay, blit=False, repeat=False)

    plt.show()
