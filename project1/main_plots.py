import matplotlib.pyplot as plt

def plot_remaining_pegs(pegs, epsilons):
  plt.plot(pegs)
  plt.plot(epsilons)
  plt.ylabel('Remaining pegs')
  plt.xlabel('Episode')
  plt.show()