import os
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras

from config import G, topp_random_moves, models_dir
from state_manager import StateManager
from utils import normalize

class Agent():

  def __init__(self, model, name="default agent"):
    self.model = model
    self.name = name
  
  def predict(self, state):
    predictions = self.model.predict(np.array([list(state)]))[0]
    indices_to_remove = []
    for i in range(len(predictions)):
      if state[i+1] != 0:
        indices_to_remove.append(i)
    
    legal_predictions = np.delete(predictions, indices_to_remove)
    return normalize(legal_predictions)

class TOPP():

  def __init__(self, verbose=False):
    self.G = G # Number of games in a series
    self.verbose = verbose
    self.agents = os.listdir("./{}/".format(models_dir))
    print("Agents:", self.agents)

  def load(self, filename):
    return keras.models.load_model("./{}/{}".format(models_dir, filename))

  def get_name(self, model_filename):
    return "Agent {}".format(model_filename.split('.')[0].split('-')[1][3:])

  def get_size(self):
    return int(self.agents[0].split('.')[0].split('-')[0][5:])

  def start(self):
    for i in range(len(self.agents) - 1):
      agt1 = Agent(model=self.load(self.agents[i]), name=self.get_name(self.agents[i]))
      for j in range(i+1, len(self.agents)):
        agt2 = Agent(model=self.load(self.agents[j]), name=self.get_name(self.agents[j]))

        print("{} vs {}".format(agt1.name, agt2.name))
        self.play_series(agt1, agt2)
  
  def play_series(self, agt1, agt2):
    player1_wins = 0
    for i in range(self.G):
      print("[{}>{}]".format("-"*i, "."*(self.G - i - 1)), end="\r")
      game = StateManager(size=self.get_size())

      if i == self.G - 1:
        print_game = input("Print the last game? (Y/n): ")
      else:
        print_game = "n"

      move_counter = 0
      while not game.is_game_over():
        game_state = game.get_nn_state()
        player_turn = game_state[0]

        if player_turn == 1:
          predictions = agt1.predict(game_state)
        else:
          predictions = agt2.predict(game_state)
        
        legal_moves = game.get_legal_moves()
        
        if move_counter < topp_random_moves * 2:
          move = random.choice(legal_moves)
        else:
          move = legal_moves[np.argmax(predictions)]
        
        game.move(move)
        move_counter += 1
        if print_game.lower() == "y":
          game.print_board()

      if game.get_winner() == 1:
        player1_wins += 1

    print("{} won {}/{} against {}.".format(agt1.name, player1_wins, self.G, agt2.name))

if __name__ == "__main__":
  topp = TOPP(verbose=True)
  topp.start()