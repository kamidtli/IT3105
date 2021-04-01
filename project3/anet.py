import os
import tensorflow as tf
from tensorflow import keras
import random
from config import hidden_layer_sizes, board_size, optimizer, learning_rate, activation_function, train_epochs
import numpy as np
from utils import normalize

class ANET():

  def __init__(self, size):
    self.input_size = size**2 + 1
    self.output_size = size**2
    self.model = self.get_model()
  
  def get_model(self):
    return self.generate_model()

  def generate_model(self):
    # Create the network
    model = keras.Sequential()

    # Add the first layer
    model.add(keras.layers.Dense(self.input_size, input_shape=(self.input_size, )))

    # Add hidden layers
    for layer_size in hidden_layer_sizes:
      model.add(keras.layers.Dense(layer_size, activation=activation_function))
    
    # Add output layer
    model.add(keras.layers.Dense(self.output_size, activation="softmax"))

    # Compile the model
    model.compile(
      optimizer=self.get_optimizer(),
      loss=tf.keras.losses.MSE,
      metrics=['accuracy']
    )
    return model
  
  def get_optimizer(self):
    if optimizer == "SGD":
      return keras.optimizers.SGD(learning_rate=learning_rate)
    elif optimizer == "RMSprop":
      return keras.optimizers.RMSprop(learning_rate=learning_rate)
    elif optimizer == "Adagrad":
      return keras.optimizers.Adagrad(learning_rate=learning_rate)
    elif optimizer == "Adam":
      return keras.optimizers.Adam(learning_rate=learning_rate)
    else:
      raise AssertionError("Illegal optimizer: '{}'".format(optimizer))

  def choose_move(self, board):
    state = np.array([list(board.get_nn_state())])
    predictions = self.model.predict(state)[0]
    normalized = self.normalize_predictions(board, predictions)
    return board.get_legal_moves()[np.argmax(normalized)]

  def normalize_predictions(self, board, predictions):
    state = board.get_nn_state()
    indices_to_remove = []
    for i in range(len(predictions)):
      if state[i+1] != 0:
        indices_to_remove.append(i)
    
    legal_predictions = np.delete(predictions, indices_to_remove)
    return normalize(legal_predictions)

  def split_cases(self, cases):
    return zip(*cases)

  def train(self, cases):
    x_train, y_train = self.split_cases(cases)
    self.model.fit(np.asarray(x_train), np.asarray(y_train), epochs=train_epochs)
