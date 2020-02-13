# Parameters for the agent

# Critic: Mapping from state to value ("neural_net" or "table")
critic_type = "table"

# Discount rate (Gamma)
discount = 0.9

# Critic learning rate (Alpha_c)
critic_learning_rate = 0.1

# Actor learning rate (Alpha_a)
actor_learning_rate = 0.9

# trace decay (Lambda)
trace_decay = 0.1

# Epsilon greedy value
epsilon = 0.9

# Decay value for the epsilon value
epsilon_decay = 0.9