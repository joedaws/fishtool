import tensorflow as tf

class MultilayerPerceptron(tf.keras.Model):
  """A constant width multilayer perceptron."""
  def __init__(self, num_layers, width, activation=tf.nn.relu):
    super(MultilayerPerceptron, self).__init__()
    self.num_layers = num_layers
    self.width = width
    self.activation = activation
    self.dense = [tf.keras.layers.Dense(self.width, activation=self.activation)
                  for _ in range(self.num_layers)]

  def call(self, inputs):
    x = self.dense[0](inputs)
    for layer in self.dense[1:]:
      x = layer(x)

    return self.dense2(x)
