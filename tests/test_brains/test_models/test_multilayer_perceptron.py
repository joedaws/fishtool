from aicard.brains.models.builders.multilayer_perceptron import MultilayerPerceptronBuilder
from aicard.brains.models.config.multilayer_perceptron import Config as MLPConfig
from aicard.brains.models.config.multilayer_perceptron import DEFAULT
import pytest
import tensorflow as tf


@pytest.fixture
def model():
    builder = MultilayerPerceptronBuilder(DEFAULT)

    return builder.build()


def test_save_and_load(model):
    save_file_path = '/Users/joe/PycharmProjects/aicard/data/test_file'
    model.save(save_file_path)

    model2 = tf.keras.models.load_model(save_file_path)

    for weights1, weights2 in zip(model.weights, model2.weights):
        diff_bool = weights1.numpy() == weights2.numpy()
        v = diff_bool.all()
        assert v
