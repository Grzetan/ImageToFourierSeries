# For edge detection I use canny edge detection algorithm
import numpy as np
from scipy.ndimage import gaussian_filter
import time
import helper

def get_points(img):
    return np.argwhere(img == 255)[:, ::-1]

def image_to_path(img):
    start = time.time()
    # Apply gaussian blur
    print("\rConverting image to path: 0/6", end="")
    img = gaussian_filter(img, sigma=1)

    # Calculate gradients
    print("\rConverting image to path: 1/6", end="")
    kernel = np.array([
        [-1 - 1j, -2j, 1 - 1j],
        [-2, 0, 2],
        [-1 + 1j, 2j, 1 + 1j]
    ])

    g = helper.convolve(img, kernel)
    gradients = np.sqrt(np.square(g.real) + np.square(g.imag))
    gradients = gradients / gradients.max() * 255

    # Get direction for every pixel
    theta = np.arctan2(g.imag, g.real)

    # Apply non-maximum suppression
    print("\rConverting image to path: 2/6", end="")
    img = helper.non_maximum_suppression(gradients, theta)
    img = img.astype('int')

    # Apply double thresholding
    print("\rConverting image to path: 3/6", end="")
    img = helper.double_threshold(img, 0.2, 0.05)

    # Apply edge tracking
    print("\rConverting image to path: 4/6", end="")
    img = helper.hysteresis(img)

    # Convert image to set of points
    points = get_points(img)

    # Create path
    print("\rConverting image to path: 5/6", end="")
    path = helper.create_path(points)
    end = time.time()
    print(f"\rConverting image to path: 6/6, WHOLE PROCESS - {round(end-start, 3)} sec\n", end="")

    return path