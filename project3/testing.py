# from topp import TOPP
# topp = TOPP(verbose=True)
# topp.start()

from anet import ANET
from utils import Timer
import numpy as np

timer = Timer()
nn = ANET(5)
rbuf = np.load('/home/kim/skule/aiprog/project3/rbufs/size_5-ep_180.h5.npy', allow_pickle=True)
test_ex = rbuf[0][0]
to_predict = np.array([list(test_ex)])

timer.start("prediction")
prediction = nn.model.predict(to_predict)
timer.stop()

# import tensorflow as tf
# from tensorflow import keras
# import numpy as np
# import random
# import os

# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     e_x = np.exp(x - np.max(x))
#     return e_x / e_x.sum()

# # model = keras.models.load_model("./models/size_5-ep_180.h5")

# seed_value = 69

# """ Set all seed values to get reproducible results """
# os.environ['PYTHONHASHSEED']=str(seed_value)
# random.seed(seed_value)
# np.random.seed(seed_value)
# tf.random.set_seed(seed_value)

# hidden_layer_sizes = [64, 32]
# board_size = 5
# activation_function = "sigmoid"
# optimizer = keras.optimizers.Adam(learning_rate=0.01)
# model = keras.Sequential()
# model.add(keras.layers.Dense(board_size**2+1, input_shape=(board_size**2+1, )))

# for layer_size in hidden_layer_sizes:
#   model.add(keras.layers.Dense(layer_size, activation=activation_function))

# # Add output layer
# model.add(keras.layers.Dense(board_size**2, activation="softmax"))

# # Compile the model
# model.compile(
#   optimizer=optimizer,
#   loss=tf.keras.losses.MSE,
#   metrics=['accuracy']
# )

# rbuf = np.load('/home/kim/skule/aiprog/project3/rbufs/size_5-ep_180.h5.npy', allow_pickle=True)
# data = np.split(rbuf, 2, 1)
# cases = np.array([list(elem[0]) for elem in data[0]])
# labels = np.array([list(elem[0]) for elem in data[1]])

# # softmax_labels = np.apply_along_axis(softmax, 0, labels)
# model.fit(cases, labels, epochs=500)