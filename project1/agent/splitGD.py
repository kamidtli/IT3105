import math
import tensorflow as tf
import numpy as np

from agent.agent_config import nn_learning_rate

# ************** Split Gradient Descent (SplitGD) **********************************
# This "exposes" the gradients during gradient descent by breaking the call to "fit" into two calls: tape.gradient
# and optimizer.apply_gradients.  This enables intermediate modification of the gradients.  You can find many other
# examples of this concept online and in the (excellent) book "Hands-On Machine Learning with Scikit-Learn, Keras,
# and Tensorflow", 2nd edition, (Geron, 2019).

# This class serves as a wrapper around a keras model.  Then, instead of calling keras_model.fit, just call
# SplitGD.fit.  To use this class, just subclass it and write your own code for the "modify_gradients" method.

class SplitGD():

  def __init__(self, keras_model):
    self.model = keras_model
    self.td_errors = []
    self.eligibilities = []

  def modify_gradients(self,gradients):
    # Create the eligibilities with the same shape as the gradients
    if len(self.eligibilities) == 0:
      for grad in gradients:
        # Only add weights not biases
        if len(grad.shape) > 1:
          self.eligibilities.append(tf.zeros(grad.shape))

    # Update the eligibilities with the gradient
    for index, grad in enumerate(gradients):
      if len(grad.shape) > 1:
        self.eligibilities[int(index/2)] += grad

    new_gradient = []

    # Combine the eligibilities with the biases to create the new gradient
    for i in range(len(gradients)):
      if len(gradients[i].shape) > 1:
        # Append the updated eligibility
        weigth_updates = nn_learning_rate*self.td_errors[-1]*self.eligibilities[int(i/2)]
        new_gradient.append(weigth_updates)
      else:
        # Append the bias
        new_gradient.append(gradients[i])

    return new_gradient

  # This returns a tensor of losses, OR the value of the averaged tensor.  Note: use .numpy() to get the
  # value of a tensor.
  def gen_loss_and_td(self,features,targets,avg=False):
    predictions = self.model(features)  # Feed-forward pass to produce outputs/predictions
    loss = self.model.loss_functions[0](targets,predictions)
    self.td_errors.append(targets[0] - features[0][0])
    return tf.reduce_mean(loss).numpy() if avg else loss

  def fit(self, features, targets, epochs=1, mbs=1,vfrac=0.1,verbose=True):
    params = self.model.trainable_weights
    train_ins, train_targs, val_ins, val_targs = split_training_data(features,targets,vfrac=vfrac)
    for _ in range(epochs):
      for _ in range(math.floor(epochs / mbs)):
        with tf.GradientTape() as tape:  # Read up on tf.GradientTape !!
          feaset,tarset = gen_random_minibatch(train_ins,train_targs,mbs=mbs)
          loss = self.gen_loss_and_td(feaset,tarset,avg=False)
          gradients = tape.gradient(loss,params)
          gradients = self.modify_gradients(gradients)
          self.model.optimizer.apply_gradients(zip(gradients,params))
      if verbose: self.end_of_epoch_display(train_ins,train_targs,val_ins,val_targs)
    return self.td_errors

  # Use the 'metric' to run a quick test on any set of features and targets.  A typical metric is some form of
  # 'accuracy', such as 'categorical_accuracy'.  Read up on Keras.metrics !!
  # Note that the model.metrics__names slot includes the name of the loss function (as 0th entry),
  # whereas the model.metrics slot does not include the loss function, hence the index+1 in the final line.
  # Use your debugger and go through the long list of slots for a keras model.  There are a lot of useful things
  # that you have access to.

  def gen_evaluation(self, features, targets, avg=False, index=0):
      predictions = self.model(features)
      evaluation = self.model.metrics[index](targets, predictions)
      #  Note that this returns both a tensor (or value) and the NAME of the metric
      return (tf.reduce_mean(evaluation).numpy() if avg else evaluation, self.model.metrics_names[index + 1])

  def status_display(self, features, targets, mode='Train'):
      print(mode + ' *** ', end='')
      print('Loss: ', self.gen_loss(features, targets, avg=True), end=' : ')
      val, name = self.gen_evaluation(features, targets)
      print('Eval({0}): {1} '.format(name, val))

  def end_of_epoch_display(self, train_ins, train_targs, val_ins, val_targs):
      self.status_display(train_ins, train_targs, mode='Train')
      if len(val_ins) > 0:
          self.status_display(val_ins, val_targs, mode='      Validation')

  def evaluate(self, states):
    states = np.asarray(states)
    predictions = self.model(states)
    return predictions

  def summary(self):
    self.model.summary()

  def reset_eligibilities(self):
    self.eligibilities = []
    self.td_errors = []

# A few useful auxiliary functions

def gen_random_minibatch(inputs, targets, mbs=1):
    indices = np.random.randint(len(inputs), size=mbs)
    return inputs[indices], targets[indices]

# This returns: train_features, train_targets, validation_features, validation_targets
def split_training_data(inputs,targets,vfrac=0.1,mix=True):
  vc = round(vfrac * len(inputs))  # vfrac = validation_fraction
  # pairs = np.array(list(zip(inputs,targets)))
  if vfrac > 0:
    pairs = list(zip(inputs,targets))
    if mix: np.random.shuffle(pairs)
    vcases = pairs[0:vc]; tcases = pairs[vc:]
    return np.array([tc[0] for tc in tcases]), np.array([tc[1] for tc in tcases]),\
          np.array([vc[0] for vc in vcases]), np.array([vc[1] for vc in vcases])
    #  return tcases[:,0], tcases[:,1], vcases[:,0], vcases[:,1]  # Can't get this to work properly
  else:
    return inputs,targets,[],[]