import numpy as np
from numpy.testing import assert_allclose
from pytest import raises

from menpo.feature import gradient
from menpo.image import Image

example_image = np.array([[1.0, 2.0, 6.0], [3.0, 4.0, 5.0]])
y_grad = np.array([[2.0, 2.0, -1.0], [2.0, 2.0, -1.0]])
x_grad = np.array([[1.0, 2.5, 4.0], [1.0, 1.0, 1.0]])


def test_gradient_float():
    dtype = np.float32
    p = example_image.astype(dtype)
    image = Image(p)
    grad_image = gradient(image)
    _check_assertions(grad_image, image.shape, image.n_channels * 2, dtype)
    np_grad = np.gradient(p)
    assert_allclose(grad_image.pixels[0], np_grad[0])
    assert_allclose(grad_image.pixels[1], np_grad[1])


def test_gradient_double():
    dtype = np.float64
    p = example_image.astype(dtype)
    image = Image(p)
    grad_image = gradient(image)
    _check_assertions(grad_image, image.shape, image.n_channels * 2, dtype)
    np_grad = np.gradient(p)
    assert_allclose(grad_image.pixels[0], np_grad[0])
    assert_allclose(grad_image.pixels[1], np_grad[1])


def test_gradient_uint8_exception():
    image = Image(example_image.astype(np.uint8))
    with raises(TypeError):
        gradient(image)


def _check_assertions(actual_image, expected_shape, expected_n_channels, expected_type):
    assert actual_image.pixels.dtype == expected_type
    assert type(actual_image) == Image
    assert actual_image.shape == expected_shape
    assert actual_image.n_channels == expected_n_channels
