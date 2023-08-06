"""
A local neighborhood are groups of neighboring pixels.
These local neighborhoods have a height, a width and a stride, very
similar to kernels of convolutions in a neural network.
more information: https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html
Adapt the method below that is supposed to take an image and optimizes
this image, s.t. each pixel in every local neighborhood of the image
converges to the mean color of its respective neighborhood.
Only adapt the objective.
Generate a docstring.
Test your method.
"""
import numpy as np
from itertools import product

from tqdm import tqdm
from PIL import Image
import math
import matplotlib.pyplot as plt


def image_smoother(
    input_image: np.ndarray,
    kernel_height=5,
    kernel_width=5,
    stride_height=1,
    stride_width=1) -> np.ndarray:
    assert input_image.ndim == 4
    assert input_image.shape[0] == 1 and input_image.shape[-1] == 3
    # input_node = tf.placeholder(
    # dtype=tf.float32,
    # shape=input_image.shape
    # )
    # This objective is the only part you need to change.
    # try to use as less for-loops as possible
    height = input_image.shape[1]
    width = input_image.shape[2]
    n_channels = input_image.shape[3]
    assert height % stride_height == 0, 'Only works when stride height is dividable by height'
    assert width % stride_width == 0, 'Only works when stride width is dividable by width'

    # Pad image (if stride_width is even only to right, otherwise to right and left
    pad_right = math.floor(kernel_width / 2)
    pad_left = kernel_width - pad_right - 1  # if even then only pad to the right
    pad_image = np.concatenate((input_image, np.zeros((1, height, pad_right, n_channels))), axis=2)
    pad_image = np.concatenate((np.zeros((1, height, pad_left, n_channels)), pad_image), axis=2)
    pad_width = width + kernel_width - 1

    pad_top = math.floor((kernel_height / 2))
    pad_bottom = kernel_height - pad_top - 1
    pad_image = np.concatenate((pad_image, np.zeros((1, pad_bottom, pad_width, n_channels))), axis=1)
    pad_image = np.concatenate((np.zeros((1, pad_top, pad_width, n_channels)), pad_image), axis=1)
    pad_height = height + kernel_height - 1

    # Calculate dimensions of the new kernel
    pos_height = list(range(0, pad_height - kernel_height + 1, stride_height))
    pos_width = list(range(0, pad_width - kernel_width + 1, stride_width))
    mean_kernel = np.zeros((len(pos_height), len(pos_width), n_channels))
    kernel_pos = product(list(range(len(pos_height))), list(range(len(pos_width))))
    neighbor_pos = product(pos_height, pos_width)

    for k_pos, (height, width) in zip(kernel_pos, neighbor_pos):
        local_neighbor = pad_image[0, height:height + stride_height, width:width + stride_width, :]
        mean = np.mean(local_neighbor, axis=(0, 1))
        mean_kernel[k_pos] = mean
    mean_kernel = mean_kernel[np.newaxis, ...]

    # objective = tf.square(input_node - mean_kernel)
    # Please note that this objective would only be correct if
    # (kernel_height, kernel_width) == input_image.shape[1:3]
    # your approach must be flexible under kernel size and stride
    # gradient_node = tf.gradients(ys=objective, xs=input_node)
    # with tf.Session() as session:
    #     for _ in tqdm(range(1000), desc="optimize image"):
    #         _gradient = session.run(
    #             gradient_node,
    #             feed_dict={
    #                 input_node: input_image
    #             }
    #         )
            # gradient_step = np.sign(_gradient[0]) * (1 / 255)
            # print(input_image)
            # print(gradient_step)
            # input_image = np.clip(input_image - gradient_step)
    return mean_kernel


image = Image.open('data/imagenet_dogs/ILSVRC2012_val_00023440.JPEG')
x_test = np.asarray(image, dtype=np.float32)
x_test = x_test[np.newaxis, ...]
result = image_smoother(x_test)
result = np.asarray(result, dtype=np.uint8)
print(x_test.shape)
print(result.shape)
plt.imshow(result[0])
plt.show()
