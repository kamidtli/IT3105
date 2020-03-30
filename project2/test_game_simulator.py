import unittest
from game_simulator import GameSimulator

class TestNim(unittest.TestCase):

  def test_initialize_ledge(self):
    try:
      gs = GameSimulator("ledge", G=100, B=[0, 0, 0, 1, 0, 2, 0, 0, 1, 0], P=1, M=100, verbose=False)
      # Initialization did not throw AssertionError: Test passed
      self.assertTrue(True)
    except AssertionError:
      # Initialization threw AssertionError: Test failed
      self.assertTrue(False)

  def test_initialize_nim(self):
    try:
      gs = GameSimulator("nim", G=1, P=1, M=100, N=10, K=3, verbose=True)
      # Initialization did not throw AssertionError: Test passed
      self.assertTrue(True)
    except AssertionError:
      # Initialization threw AssertionError: Test failed
      self.assertTrue(False)
  
  def test_illegal_game_value(self):
    try:
      gs = GameSimulator("this is an illegal value for game", G=100, B=[0, 0, 0, 1, 0, 2, 0, 0, 1, 0], P=1, M=100, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_G_value(self):
    try:
      gs = GameSimulator("ledge", G=-1, B=[0, 0, 0, 1, 0, 2, 0, 0, 1, 0], P=1, M=100, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_B_value(self):
    try:
      gs = GameSimulator("ledge", G=-1, B=[2, 2, 0, 1, 0, 2, 0, 0, 1, 0], P=1, M=100, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_P_value(self):
    try:
      gs = GameSimulator("ledge", G=-1, B=[2, 2, 0, 1, 0, 2, 0, 0, 1, 0], P=5, M=100, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_N_value(self):
    try:
      gs = GameSimulator("nim", G=1, P=1, M=100, N=1, K=3, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_K_value(self):
    try:
      gs = GameSimulator("nim", G=1, P=1, M=100, N=10, K=0, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

  def test_illegal_M_value(self):
    try:
      gs = GameSimulator("nim", G=1, P=1, M=0, N=10, K=0, verbose=False)
      # Initialization did not throw AssertionError: Test failed
      self.assertTrue(False)
    except AssertionError:
      # Initialization threw AssertionError: Test passed
      self.assertTrue(True)

if __name__=="__main__":
  unittest.main()