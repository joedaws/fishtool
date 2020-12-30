from dataclasses import dataclass


@dataclass
class Config:
    """A config dataclass for assembling simple constant width multilayer perceptrons.
    Fields:
        num_layers (int): Number of layers that the MLP will have.
        input_dim (int): Dimension of the input to the network. When a batch of inputs
            is passed they will have shave (X, N) where N is the input_dim and X is the
            number of examples in the batch.
        width (int): Number of nodes on the hidden layers.
        output_dim (int): Dimension of the output of the network. When a batch of inputs
            of shape (X, N) is used, the output will have shape (X, M) where M is the
            output_dim.
        activation (str): Name of a function implemented in the module tf.nn.
            During construction, the builder will try to import tf.nn.<activation>
            and then use the imported function to construct the model.
        initialization (str): A string indicating what kind of initialization to use.
            The list of accepted values is a class attribute of MultilayerPerceptron.
    """
    num_layers: int
    input_dim: int
    width: int
    output_dim: int
    activation: str
    initialization: str


def make_default():
    """Return a default instance of Config."""
    params = {
        'num_layers': 3,
        'input_dim': 5,
        'width': 10,
        'output_dim': 2,
        'activation': 'relu',
        'initialization': 'random'
    }

    config = Config(**params)

    return config


DEFAULT = make_default()