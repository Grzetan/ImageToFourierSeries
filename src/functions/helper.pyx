import numpy as np
cimport numpy
cimport cython

ctypedef numpy.float64_t DTYPE_float64
ctypedef numpy.int64_t DTYPE_int64
ctypedef numpy.uint8_t DTYPE_uint8
ctypedef numpy.complex128_t DTYPE_complex128

def convolve(numpy.ndarray[DTYPE_uint8, ndim=2] img, numpy.ndarray[DTYPE_complex128, ndim=2] kernel):
    cdef int kernel_size, pad_size, x, y, i, j, w, h
    cdef numpy.ndarray[DTYPE_complex128, ndim=2] gradient_map
    cdef DTYPE_complex128 sum

    kernel_size = kernel.shape[0]
    pad_size = (kernel_size - 1) / 2
    w, h = img.shape[1], img.shape[0]
    gradient_map = np.zeros((h, w), dtype=np.complex128)
    img = np.pad(img, int(pad_size), 'edge')

    for y in range(pad_size, h):
        for x in range(pad_size, w):
            sum = 0

            for i in range(kernel_size):
                for j in range(kernel_size):
                    sum += img[y+(pad_size - i), x+(pad_size - j)] * kernel[i,j]

            gradient_map[y-pad_size,x-pad_size] = sum

    return gradient_map

def non_maximum_suppression(numpy.ndarray[DTYPE_float64, ndim=2] img, numpy.ndarray[DTYPE_float64, ndim=2] angles):
    cdef int w, h, y, x, xx, yy
    cdef numpy.ndarray[DTYPE_float64, ndim=2] new_img
    cdef DTYPE_float64 angle, PI

    PI = np.pi
    w, h = img.shape[0], img.shape[1]
    new_img = np.zeros((w,h), dtype=np.float64)
    img = np.pad(img, 1, 'edge')

    for y in range(w):
        for x in range(h):
            angle = abs(angles[y, x])
            xx = 0
            yy = 0

            if (0 < angle < PI / 8) or (PI > angle > 7 * PI / 8):
                xx = -1
                yy = 0
            elif PI / 8 < angle < 3 * PI / 8:
                xx = -1
                yy = -1
            elif 3 * PI / 8 < angle < 5 * PI / 8:
                xx = 0
                yy = 1
            elif 5 * PI / 8 < angle < 7 * PI / 8:
                xx = 1
                yy = -1

            if img[y + 1 + yy, x + 1 + xx] > img[y + 1, x + 1] or img[y + 1 - yy, x + 1 - xx] > img[y + 1, x + 1]:
                new_img[y, x] = 0
            else:
                new_img[y, x] = img[y + 1, x + 1]

    return new_img

def create_path(numpy.ndarray[DTYPE_int64, ndim=2] points):
    cdef int len, added, min_dist, r, i
    cdef numpy.ndarray[DTYPE_int64, ndim=2] path, not_added
    cdef numpy.ndarray[DTYPE_float64, ndim=1] vector_lengths, vector_len
    cdef numpy.ndarray[DTYPE_int64, ndim=2] dist


    len = points.shape[0]
    path = np.zeros((len, 2), dtype=np.int)
    path[0] = points[0]
    added = 1
    not_added = points[1:].astype(np.int)
    vector_lengths = np.zeros((len,), dtype=np.float64)

    while added != len:
        dist = np.abs(path[added-1] - not_added)

        r = 5
        empty_circle = True
        vector_len = np.zeros((dist.shape[0], ), dtype=np.float64)
        while empty_circle:
            for i in range(dist.shape[0]):
                if dist[i,0] <= r and dist[i,1] <= r:
                    empty_circle = False
                    vector_len[i] = np.sqrt(dist[i,0]**2 + dist[i,1]**2)
                else:
                    vector_len[i] = 10000

            r += 5

        min_dist = np.argsort(vector_len)[0]
        path[added] = not_added[min_dist]
        vector_lengths[added] = vector_len[min_dist]
        not_added = np.delete(not_added, min_dist, axis=0)
        added += 1

    return path, vector_lengths

def double_threshold(numpy.ndarray[DTYPE_int64 ,ndim=2] img, DTYPE_float64 high, DTYPE_float64 low):
    cdef DTYPE_float64 high_threshold, low_threshold, val
    cdef int strong, week, x, y

    high_threshold = img.max() * high
    low_threshold = high_threshold * low
    strong = np.int(255)
    week = np.int(30)

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

def hysteresis(numpy.ndarray[DTYPE_int64, ndim=2] img):
    cdef int x, y
    cdef DTYPE_int64 week, strong

    img = np.pad(img, 1)
    week = np.int64(30)
    strong = np.int64(255)

    for y in range(1,img.shape[0]-1):
        for x in range(1,img.shape[1]-1):
            if img[y,x] == week:
                if img[y-1, x-1] == strong or img[y-1, x] == strong or img[y-1,x+1] == strong or img[y,x-1] == strong or img [y, x+1] == strong or img[y+1, x-1] == strong or img[y+1, x] == strong or img[y+1, x+1] == strong:
                    img[y,x] = strong
                else:
                    img[y,x] = 0

    return img[1:-1, 1:-1]

@cython.boundscheck(False)
@cython.wraparound(False)
def discrete_fourier_transform(numpy.ndarray[DTYPE_complex128, ndim=1] signal):
    cdef int N, k, i
    cdef DTYPE_float64 amplitude, phase, TWO_PI
    cdef DTYPE_complex128 sum
    cdef numpy.ndarray[DTYPE_float64, ndim=2] epicycles
    cdef numpy.ndarray[DTYPE_float64, ndim=1] alphas, nn

    TWO_PI = np.pi * 2
    N = len(signal)
    nn = np.arange(N) * TWO_PI
    epicycles = np.zeros((N, 3), dtype=np.float64)

    for k in range(N):
        alphas = (nn * k) / N
        sum = np.sum((np.cos(alphas) + (np.sin(alphas) * -1) * 1j) * signal) / N

        amplitude = np.sqrt(sum.real * sum.real + sum.imag * sum.imag)
        phase = np.arctan2(sum.imag, sum.real)

        epicycles[k] = [k, amplitude, phase]

    return epicycles[epicycles[:,1].argsort()[::-1]]