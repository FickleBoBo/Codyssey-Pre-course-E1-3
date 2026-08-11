import time

from mac_core import ITERATIONS


def flatten(matrix):
    n = len(matrix)
    return [matrix[i][j] for i in range(n) for j in range(n)]


def mac_1d(flat1, flat2):
    return sum(flat1[k] * flat2[k] for k in range(len(flat1)))


def measure_mac_1d_avg_ms(flat1, flat2):
    start_time = time.perf_counter()
    for _ in range(ITERATIONS):
        mac_1d(flat1, flat2)
    end_time = time.perf_counter()

    return (end_time - start_time) / ITERATIONS * 1000
