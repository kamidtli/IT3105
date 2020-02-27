import tensorflow as tf
from tensorflow import keras

import numpy as np

from game.game_config import shape, size
from agent.agent_config import hidden_layer_sizes
from agent.splitGD import SplitGD

def init_nn():

  if shape == "triangle":
    input_shape = int((size * (size+1)) / 2)
  else:
    input_shape = int(size**2)

  # Create the network
  model = keras.Sequential()

  # Add the first layer
  model.add(keras.layers.Dense(input_shape, input_shape=(input_shape, )))

  # Add hidden layers
  for layer_size in hidden_layer_sizes:
    model.add(keras.layers.Dense(layer_size, activation='sigmoid'))
  
  # Add output layer
  model.add(keras.layers.Dense(1))

  # Compile the model
  model.compile(
    optimizer="SGD",
    loss=tf.keras.losses.MSE,
    metrics=['accuracy']
  )

  wrapped_model = SplitGD(model)  

  return wrapped_model
