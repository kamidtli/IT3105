# Parameters for the agent

# Critic: Mapping from state to value ("neural_net" or "table")
critic_type = "neural_net"

# Discount rate (Gamma)
discount = 0.9

# Critic learning rate (Alpha_c)
critic_learning_rate = 0.9

# Actor learning rate (Alpha_a)
actor_learning_rate = 0.9

# trace decay (Lambda)
trace_decay = 0.1

# Epsilon greedy value
epsilon_greedy_value = 0.9

# Neural net layer sizes (only for hidden layers
# since the input layer is bounded by the board size,
# and the output layer is always 1).
hidden_layer_sizes = [16, 8]