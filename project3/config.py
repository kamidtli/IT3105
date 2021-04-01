""" The size of the hex board """
board_size = 4

""" The number of actual games to play """
num_of_games = 15
offset = 1

""" The number of epochs to train after each episode """
train_epochs = 1

""" The number of rollouts/simulations to perform """
num_search_games = 10

""" The sizes of the hidden layers of the ANET """
hidden_layer_sizes = [10]

""" Activation function for the hidden layer nodes ("linear", "sigmoid", "tanh", "relu") """
activation_function = "tanh"

""" Optimizer for the ANET ("SGD", "RMSprop", "Adagrad", "Adam") """
optimizer = "RMSprop"

""" The learning rate for the ANET """
learning_rate = 0.001

""" The interval of which to save ANET parameters (episode number) """
save_interval = 0

""" The directory to save the model during training """
save_dir = "demo_models"

""" The number of games to play in a series of a TOPP match """
G = 10

""" Percentage of random moves instead of ANET during rollout, and the decay rate for this parameter """
epsilon_start_value = 1
epsilon_decay_rate = 0.99

""" Max size of the replay buffer. If max length is exceeded, items are appended from the beginning again """
rbuf_max_size = 500

""" The model to load for use on the OHT server """
oht_agent = "oht_agent.h5"

""" Verbose (print the last episode during training) """
verbose = True

""" The number of random moves to start off a TOPP game. The value indicates the number of random
moves PER player, so if it is 3, then each player plays 3 random moves """
topp_random_moves = 1

""" Directory to load TOPP models from """
models_dir = "topp_models"
