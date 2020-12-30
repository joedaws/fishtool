import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class MultilayerPerceptronBuilder:
    """A simple constant width multilayer perceptron.

    If input_dim = x then the inputs passed to the model that is built by
    this class should have shape ()

    Args:
        config (aicard.brains.models.config.multilayer_perceptron.Config): A dataclass for configuring
            a multilayer perceptron model.
    """
    ALLOWED_INITIALIZATIONS = ['random']

    def __init__(self, config):
        self.config = config
        self.num_layers = config.num_layers
        self.input_dim = config.input_dim
        self.width = config.width
        self.output_dim = config.output_dim
        try:
            self.activation = getattr(tf.nn, config.activation)
        except AttributeError:
            print(f'The activation function {config.activation} cannot be imported from tf.nn!'
                  f' Will use relu instead.')
            self.activation = getattr(tf.nn, 'relu')

    def build(self):
        """Instantiates a multilayer perceptron model."""
        model = None
        initialization = self.config.initialization
        if initialization == 'random':
            model = self.build_base_model()
        elif initialization not in self.ALLOWED_INITIALIZATIONS:
            raise ValueError(f'Cannot initialize multilayer perceptron with {initialization}')

        return model

    def build_base_model(self):
        """Build the base model with randomly initialized weights.

        Based on the source code I believe that glorot normal initialization
        is the default.
        """
        # create the model
        model = Sequential()
        # create input layer
        model.add(Dense(self.width,
                        activation=self.activation,
                        input_shape=(self.input_dim,),
                        kernel_initializer='glorot_uniform',
                        bias_initializer='zeros'
                        )
                  )

        # create the middle layers
        for _ in range(1, self.num_layers-1):
            model.add(Dense(self.width, activation=self.activation))

        # create output layer
        model.add(Dense(self.output_dim, activation=None))

        return model
