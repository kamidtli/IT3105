import os
import tensorflow as tf
from tensorflow import keras
import random
from config import hidden_layer_sizes
import numpy as np

seed_value = 0

""" Set all seed values to get reproducible results """
os.environ['PYTHONHASHSEED']=str(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)

class ANET():

  def __init__(self, input_size, output_size):
    self.input_size = input_size
    self.output_size = output_size
    self.model = self.get_model()
  
  def get_model(self):
    # TODO: If model exists load model, else create a new one
    return self.generate_model()

  def generate_model(self):
    # Create the network
    model = keras.Sequential()

    # Add the first layer
    model.add(keras.layers.Dense(self.input_size, input_shape=(self.input_size, )))

    # Add hidden layers
    for layer_size in hidden_layer_sizes:
      model.add(keras.layers.Dense(layer_size, activation='sigmoid'))
    
    # Add output layer
    model.add(keras.layers.Dense(self.output_size, activation="softmax"))

    # Compile the model
    model.compile(
      optimizer="SGD",
      loss=tf.keras.losses.MSE,
      metrics=['accuracy']
    )
    return model
  
  def choose_move(self, board):
    state = np.array([list(board.get_nn_state())])
    predictions = self.model.predict(state)[0]
    normalized = self.normalize_predictions(board, predictions)
    return board.get_legal_moves()[np.argmax(normalized)]

  def normalize_predictions(self, board, predictions):
    # TODO: Get predictions only for legal moves
    state = board.get_nn_state()
    indices_to_remove = []
    for i in range(len(predictions)):
      if state[i+1] != 0:
        indices_to_remove.append(i)
    
    legal_predictions = np.delete(predictions, indices_to_remove)
    total = np.sum(legal_predictions)
    return legal_predictions/total
