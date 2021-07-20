from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import math

img = ImageOps.grayscale(Image.open("l.png"))
img = np.array(img)
threshold = 30

feature_map = np.full(img.shape, 0)

pixels_around = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),           (1, 0),
    (-1, 1),  (0, 1),  (1, 1)
]

horizontal_kernel = [
    -1, 0, 1,
    -2,    2,
    -1, 0, 1
]

vertical_kernel = [
    -1, -2, -1,
     0,      0,
     1,  2,  1
]

# Create feature map
for y in range(1, img.shape[0] - 1):
    for x in range(1, img.shape[1] - 1):

        horizontal_kernel_value = 0
        vertical_kernel_value = 0

        for i, pixel in enumerate(pixels_around):
            value_of_pixel = img[y + pixel[1], x + pixel[0]]
            horizontal_kernel_value += value_of_pixel * horizontal_kernel[i]
            vertical_kernel_value += value_of_pixel * vertical_kernel[i]

        kernel_value = math.sqrt(math.pow(horizontal_kernel_value, 2) + math.pow(vertical_kernel_value, 2))
        kernel_value = 255 if kernel_value > threshold else 0
        feature_map[y, x] = kernel_value

print(np.count_nonzero(feature_map == 255))
plt.imshow(feature_map)
plt.show()
# TODO
# https://www.analyticsvidhya.com/blog/2021/03/edge-detection-extracting-the-edges-from-an-image/
