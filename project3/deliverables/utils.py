import numpy as np
import timeit
from math import ceil

def normalize(a):
  total = np.sum(a)
  return np.array(a)/total

def get_legal_moves(state, size=6):
  state = list(state)[1:]
  legal_moves = []
  for i in range(len(state)):
    if state[i] == 0:
      legal_moves.append((i // size, i % size))
  # print("State to get legal moves from:", state)
  # print("Legal moves:", legal_moves)
  return legal_moves

# Print iterations progress
def progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total-1: 
        print()

class Timer():
  
  def start(self, label=None):
    self.label=label
    self.start_time = timeit.default_timer()
  
  def stop(self):
    self.duration = timeit.default_timer() - self.start_time
    print("Time to execute '{}':{}".format(self.label, self.duration))