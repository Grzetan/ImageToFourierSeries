# For edge detection I use canny edge detection algorithm
import numpy as np
from scipy.ndimage import gaussian_filter
import time
import helper

def get_points(img):
    return np.argwhere(img == 255)[:, ::-1]

def image_to_path(img):
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

    start = time.time()
    g = helper.convolve(img, kernel)
    gradients = np.sqrt(np.square(g.real) + np.square(g.imag))
    gradients = gradients / gradients.max() * 255
    end = time.time()
    print(f"CONVOLVE: {end - start}")

    # Get direction for every pixel
    theta = np.arctan2(g.imag, g.real)

    # Apply non-maximum suppression
    print("\rConverting image to path: 2/6", end="")
    start = time.time()
    img = helper.non_maximum_suppression(gradients, theta)
    img = img.astype('int')
    end = time.time()
    print(f"NON: {end-start}")

    # Apply double thresholding
    print("\rConverting image to path: 3/6", end="")
    start = time.time()
    img = helper.double_threshold(img, 0.2, 0.05)
    end = time.time()
    print(f"THRESH: {end-start}")

    # Apply edge tracking
    print("\rConverting image to path: 4/6", end="")
    start = time.time()
    img = helper.hysteresis(img)
    end = time.time()
    print(f"EDGE: {end - start}")

    # Convert image to set of points
    points = get_points(img)

    # Create path
    print("\rConverting image to path: 5/6", end="")
    start = time.time()
    path = helper.create_path(points)
    end = time.time()
    print(f"PATH {end-start}")
    print("\rConverting image to path: 6/6\n", end="")

    return path