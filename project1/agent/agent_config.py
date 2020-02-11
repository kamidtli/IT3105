# Parameters for the agent

# Critic: Mapping from state to value ("neural_net" or "table")
critic_type = "table"

# Discount rate (Gamma)
discount = 0.9

# Critic learning rate (Alpha_c)
critic_learning_rate = 0.1

# Actor learning rate (Alpha_a)
actor_learning_rate = 0.1

# trace decay (Lambda)
trace_decay = 0.1