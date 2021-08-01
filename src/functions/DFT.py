import numpy as np

def discrete_fourier_transform(signal):
    N = len(signal)
    epicycles = np.empty((N, 3))

    for k in range(N):
        alphas = (2 * np.pi * np.arange(N) * k) / N
        sum = np.sum((np.cos(alphas) + (np.sin(alphas) * -1) * 1j) * signal) / N

        frequency = k
        amplitude = np.sqrt(sum.real * sum.real + sum.imag * sum.imag)
        phase = np.arctan2(sum.imag, sum.real)

        epicycles[k] = [frequency, amplitude, phase]

        print(f"\rCalculating fourier transform: {round(k/N * 100)}%", end="")

    print("\n")
    return epicycles[epicycles[:,1].argsort()[::-1]]
