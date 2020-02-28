import unittest
from ledge import Ledge

class TestNim(unittest.TestCase):

  def test_initialize(self):
    B = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
    P = 1
    game = Ledge(B, P)

    self.assertEqual(game.get_initial_state(), B)
    self.assertEqual(game.get_state(), B)
    self.assertEqual(game.get_active_player(), P)

  def test_random_initial_player(self):
    B = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
    P = 3
    game = Ledge(B, P)
    self.assertIn(game.get_active_player(), [1, 2])

  def test_legal_move(self):
    B = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
    P = 1
    game = Ledge(B, P)
    game.move(5, 4)
    self.assertEqual(game.get_state(), [0, 0, 0, 1, 2, 0, 0, 0, 1, 0])
    self.assertFalse(game.is_terminal_state())
    self.assertEqual(game.get_active_player(), 2)

  def test_illegal_move(self):
    try:
      B = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
      P = 1
      game = Ledge(B, P)
      game.move(5, 2) # Should thor AssertionError
    except AssertionError:
      # Exception caught, passed test
      self.assertTrue(True)

  def test_terminal_move(self):
    B = [2, 0, 0, 1, 0, 0, 0, 0, 1, 0]
    P = 1
    game = Ledge(B, P)
    game.move(-1, 3)
    self.assertTrue(game.is_terminal_state())
    self.assertEqual(game.get_active_player(), 1)

  def test_get_legal_moves(self):
    B = [0, 0, 1, 0, 0, 2, 1, 0, 0, 1]
    P = 1
    game = Ledge(B, P)
    self.assertEqual(game.get_legal_moves(), [(9, 8), (9, 7), (5, 4), (5, 3), (2, 1), (2, 0)])
    game.move(9, 7)
    self.assertEqual(game.get_legal_moves(), [(5, 4), (5, 3), (2, 1), (2, 0)])

  def test_full_game(self):
    B = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
    P = 1
    game = Ledge(B, P)
    game.move(3, 0)
    game.move(-1, -1)
    game.move(5, 0)
    game.move(1, -1)
    self.assertTrue(game.is_terminal_state())

if __name__=="__main__":
  unittest.main()