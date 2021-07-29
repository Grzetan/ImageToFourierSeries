# For edge detection I use canny edge detection algorithm
import numpy as np

def generate_gaussian_kernel(kernel_size, sigma):
    ax = np.linspace(-(kernel_size - 1) / 2, (kernel_size - 1) / 2, kernel_size)
    x, y = np.meshgrid(ax, ax)
    kernel = np.exp(-0.5 * (np.square(x) + np.square(y)) / np.square(sigma))
    return kernel / np.sum(kernel)


def convolve(img, kernel):
    kernel_size = kernel.shape[0]
    pad_size = (kernel_size - 1) / 2
    gradient_map = np.zeros(img.shape)
    img = np.pad(img, int(pad_size), 'edge')

    for y in range(gradient_map.shape[0]):
        for x in range(gradient_map.shape[1]):
            gradient_map[y, x] = np.sum(img[y:y + kernel_size, x:x + kernel_size] * kernel)

    return gradient_map


def non_maximum_suppression(img, angles):
    w, h = img.shape
    new_img = np.zeros(img.shape)
    img = np.pad(img, 1, 'edge')

    for y in range(w):
        for x in range(h):
            angle = abs(angles[y, x])
            xx = 0
            yy = 0

            if (0 < angle < np.pi / 8) or (np.pi > angle > 7 * np.pi / 8):
                xx = -1
                yy = 0
            elif np.pi / 8 < angle < 3 * np.pi / 8:
                xx = -1
                yy = -1
            elif 3 * np.pi / 8 < angle < 5 * np.pi / 8:
                xx = 0
                yy = 1
            elif 5 * np.pi / 8 < angle < 7 * np.pi / 8:
                xx = 1
                yy = -1

            if img[y + 1 + yy, x + 1 + xx] > img[y + 1, x + 1] or img[y + 1 - yy, x + 1 - xx] > img[y + 1, x + 1]:
                new_img[y, x] = 0
            else:
                new_img[y, x] = img[y + 1, x + 1]

    return new_img

def double_threshold(img, high, low):
    high_threshold = img.max() * high
    low_threshold = high_threshold * low
    strong = np.int16(255)
    week = np.int16(30)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            val = img[y,x]
            if val >= high_threshold:
                img[y,x] = strong
            elif val < low_threshold:
                img[y,x] = 0
            else:
                img[y,x] = week

    return img

def hysteresis(img):
    img = np.pad(img, 1)
    week = np.int16 = 30
    strong = np.int16 = 255

    for y in range(1,img.shape[0]-1):
        for x in range(1,img.shape[1]-1):
            if img[y,x] == week:
                area = img[y-1:y+1, x-1:x+1]
                if area.max() == strong:
                    img[y,x] = strong
                else:
                    img[y,x] = 0

    return img[1:-1, 1:-1]

def get_points(img):
    points = np.array([])
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y,x] == 255:
                points = np.append(points, (x,y))

    return np.reshape(points, (-1,2))

def create_path(points):
    path = np.array([points[0]])
    not_added = points[1:]
    vector_lengths = np.array([0])

    while len(not_added) != 0:
        dist = np.abs(path[-1] - not_added)
        vector_len = np.sqrt(np.square(dist[:,0]) + np.square(dist[:,1]))
        min_dist = np.argsort(vector_len)[0]
        path = np.vstack([path, not_added[min_dist]])
        vector_lengths = np.append(vector_lengths, vector_len[min_dist])
        not_added = np.delete(not_added, min_dist, axis=0)

    return path, vector_lengths

def image_to_path(img):
    # Apply gaussian blur
    print("\rConverting image to path: 0/6", end="")
    kernel = generate_gaussian_kernel(5, 2)
    img = convolve(img, kernel)

    # Calculate gradients
    print("\rConverting image to path: 1/6", end="")
    x_kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    y_kernel = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])

    g_x = convolve(img, x_kernel)
    g_y = convolve(img, y_kernel)

    gradients = np.sqrt(np.square(g_x) + np.square(g_y))
    gradients = gradients / gradients.max() * 255

    # Get direction for every pixel
    theta = np.arctan2(g_y, g_x)

    # Apply non-maximum suppression
    print("\rConverting image to path: 2/6", end="")
    img = non_maximum_suppression(gradients, theta)

    # Apply double thresholding
    print("\rConverting image to path: 3/6", end="")
    img = double_threshold(img, 0.2, 0.05)

    # Apply edge tracking
    print("\rConverting image to path: 4/6", end="")
    img = hysteresis(img)

    # Convert image to set of points
    points = get_points(img)

    # Create path
    print("\rConverting image to path: 5/6", end="")
    path = create_path(points)
    print("\rConverting image to path: 6/6\n", end="")

    return path