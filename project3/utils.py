import numpy as np
import timeit

def normalize(a):
  total = np.sum(a)
  return np.array(a)/total

class Timer():
  
  def start(self, label=None):
    self.label=label
    self.start_time = timeit.default_timer()
  
  def stop(self):
    self.duration = timeit.default_timer() - self.start_time
    print("Time to execute '{}':{}".format(self.label, self.duration))