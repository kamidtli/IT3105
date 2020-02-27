import matplotlib.pyplot as plt

def plot_remaining_pegs(pegs):
  plt.plot(pegs)
  plt.ylabel('Remaining pegs')
  plt.xlabel('Episode')
  plt.show()