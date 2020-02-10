# This file contains declaration of the pivotal parameters to be used when initializing a game.

# Shape of the board: 'triangle' or 'diamond'
shape = "triangle"

# Size of the board: Integer larger than 1
size = 3

# Cells not containing pegs when initialized: (i, j) where i and j are coordinates (0-indexed)
openCells = [(0, 0), (1, 0), (2, 2)]

# Legal directions to move
directions = {"UP": (0, -1), "UPRIGHT": (1, -1), "RIGHT": (1, 0), "DOWNRIGHT": (1, 1), "DOWN": (0, 1), "DOWNLEFT": (-1, 1), "LEFT": (-1, 0), "UPLEFT": (-1, -1)}

# Visualization delay between frames, in ms 
delay = 1000

# Number of episodes
num_of_episodes = 2