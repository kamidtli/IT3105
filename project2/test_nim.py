import unittest
from nim import Nim

class TestNim(unittest.TestCase):

  def test_initialize(self):
    N = 50
    K = 7
    P = 1
    game = Nim(N, K, P)

    self.assertEqual(game.get_initial_state(), N)
    self.assertEqual(game.get_state(), N)
    self.assertEqual(game.get_max_removable(), K)
    self.assertEqual(game.get_active_player(), P)

  def test_random_initial_player(self):
    game = Nim(10, 5, 3)
    self.assertIn(game.get_active_player(), [1, 2])

  def test_legal_move(self):
    game = Nim(10, 5, 1)
    game.move(2)
    self.assertEqual(game.get_state(), 8)
    self.assertFalse(game.is_terminal_state())
    self.assertEqual(game.get_active_player(), 2)

  def test_illegal_move(self):
    try:
      game = Nim(10, 5, 1)
      game.move(6)
    except AssertionError:
      # Exception caught, passed test
      self.assertTrue(True)

  def test_terminal_move(self):
    game = Nim(10, 9, 1)
    game.move(9)
    game.move(1)
    self.assertTrue(game.is_terminal_state())
    self.assertEqual(game.get_active_player(), 2)

  def test_get_legal_moves(self):
    game = Nim(7, 5, 1)
    self.assertEqual(game.get_legal_moves(), [1, 2, 3, 4, 5])
    game.move(5)
    self.assertEqual(game.get_legal_moves(), [1, 2])

  def test_full_game(self):
    game = Nim(10, 3, 1)
    game.move(1)
    game.move(3)
    game.move(2)
    game.move(3)
    game.move(1)
    self.assertTrue(game.is_terminal_state())

if __name__=="__main__":
  unittest.main()