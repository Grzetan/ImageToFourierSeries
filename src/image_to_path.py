from PIL import Image, ImageOps, ImageFilter
import numpy as np
import matplotlib.pyplot as plt
import math

img = Image.open("face.jpeg")
img = ImageOps.grayscale(img)
img = np.array(img)

def generate_gaussian_kernel(kernel_size, sigma):
    ax = np.linspace(-(kernel_size - 1) / 2, (kernel_size - 1) / 2, kernel_size)
    x,y =  np.meshgrid(ax, ax)
    kernel = np.exp(-0.5 * (np.square(x) + np.square(y)) / np.square(sigma))
    return kernel / np.sum(kernel)

def convolve(img, kernel):
    kernel_size = kernel.shape[0]
    pad_size = (kernel_size - 1) / 2
    gradient_map = np.zeros(img.shape)
    img = np.pad(img, int(pad_size))

    for y in range(gradient_map.shape[0]):
        for x in range(gradient_map.shape[1]):
            gradient_map[y,x] = np.sum(img[y:y+kernel_size, x:x+kernel_size] * kernel)

    return gradient_map

# Apply gaussian blur
kernel = generate_gaussian_kernel(5, 2)
img = convolve(img, kernel)

# Find gradients
x_kernel = np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
])

y_kernel = np.array([
    [-1,-2,-1],
    [0,0,0],
    [1,2,1]
])

g_x = convolve(img, x_kernel)
g_y = convolve(img, y_kernel)

gradients = np.sqrt(np.square(g_x) + np.square(g_y))
gradients = gradients / gradients.max() * 255
theta = np.arctan2(g_y, g_x)

img = Image.fromarray(gradients)
img.show()



#
#
# feature_map = np.full((img.shape[0], img.shape[1], 2), 0)
#
# pixels_around = [
#     (-1, -1), (0, -1), (1, -1),
#     (-1, 0),           (1, 0),
#     (-1, 1),  (0, 1),  (1, 1)
# ]
#
# horizontal_kernel = [
#     -1, 0, 1,
#     -1,    1,
#     -1, 0, 1
# ]
#
# vertical_kernel = [
#     -1, -1, -1,
#      0,      0,
#      1,  1,  1
# ]
#
# # Create feature map
# for y in range(1, img.shape[0] - 1):
#     for x in range(1, img.shape[1] - 1):
#
#         horizontal_kernel_value = 0
#         vertical_kernel_value = 0
#
#         for i, pixel in enumerate(pixels_around):
#             value_of_pixel = img[y + pixel[1], x + pixel[0]]
#             horizontal_kernel_value += value_of_pixel * horizontal_kernel[i]
#             vertical_kernel_value += value_of_pixel * vertical_kernel[i]
#
#         gradient = math.sqrt(math.pow(horizontal_kernel_value, 2) + math.pow(vertical_kernel_value, 2))
#         feature_map[y, x, 0] = gradient
#         feature_map[y, x, 1] = math.atan2(vertical_kernel_value, horizontal_kernel_value)
#         print(feature_map[y,x,1])


# TODO
# https://www.analyticsvidhya.com/blog/2021/03/edge-detection-extracting-the-edges-from-an-image/
