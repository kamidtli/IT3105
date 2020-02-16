import tensorflow as tf
from tensorflow import keras

import numpy as np

from game.game_config import shape, size
from agent.agent_config import hidden_layer_sizes
from agent.splitGD import SplitGD

def init_nn(size):

  if shape == "triangle":
    input_shape = (size * (size+1)) / 2
  else:
    input_shape = size**2

  # Create the network
  model = keras.Sequential()

  # Add the first layer
  model.add(keras.layers.Dense(input_shape, input_shape=(input_shape, )))

  # Add hidden layers
  for layer_size in hidden_layer_sizes:
    model.add(keras.layers.Dense(layer_size, activation='relu'))
  
  # Add output layer
  model.add(keras.layers.Dense(1))

  # Compile the model
  model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
  )

  wrapped_model = SplitGD(model)  

  return wrapped_model


if (__name__=="__main__"):
  model = init_nn(4)
  test_state = np.asarray([(1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])
  prediction = model.predict(test_state)[0][0] # predict returns a 2D array, so we get the prediction value by using [0][0]
  print(prediction)
