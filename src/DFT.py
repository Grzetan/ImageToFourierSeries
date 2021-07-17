import math


def discrete_fourier_transform(signal):
    N = len(signal)
    epicycles = []

    for k in range(N):
        sum = complex(0, 0)
        for n in range(N):
            alpha = (2 * math.pi * k * n) / N
            formula_complex = complex(math.cos(alpha), -math.sin(alpha)) * signal[n]
            sum += formula_complex
        sum /= N

        frequency = k
        amplitude = math.sqrt(sum.real * sum.real + sum.imag * sum.imag)
        phase = math.atan2(sum.imag, sum.real)

        epicycles.append({"frequency": frequency, "amplitude": amplitude, "phase": phase})

    epicycles = sorted(epicycles, key=lambda elem: elem['amplitude'], reverse=True)

    return epicycles
