from motherbrain.brains.models.builders.multilayer_perceptron import MultilayerPerceptronBuilder
from motherbrain import MOTHERBRAIN_PATH
from motherbrain.brains.models.config.multilayer_perceptron import DEFAULT
import os
import pytest
import tensorflow as tf


@pytest.fixture
def model():
    builder = MultilayerPerceptronBuilder(DEFAULT)
    return builder.build()


def test_save_and_load(model):
    project_path = os.path.dirname(MOTHERBRAIN_PATH)
    save_file_path = os.path.join(project_path, 'data/test_MLP')
    model.save(save_file_path)

    model2 = tf.keras.models.load_model(save_file_path)

    for weights1, weights2 in zip(model.weights, model2.weights):
        diff_bool = weights1.numpy() == weights2.numpy()
        v = diff_bool.all()
        assert v
