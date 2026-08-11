import time

EPSILON = 1e-9
ITERATIONS = 10


def is_square_matrix(matrix):
    return all(len(row) == len(matrix) for row in matrix)


def validate_matrix_pair(matrix1, matrix2):
    size1 = len(matrix1)
    size2 = len(matrix2)

    if not is_square_matrix(matrix1):
        raise ValueError(
            f"첫 번째 행렬이 정사각형이 아닙니다: {size1}행 기준 각 행 길이가 일치하지 않습니다"
        )
    if not is_square_matrix(matrix2):
        raise ValueError(
            f"두 번째 행렬이 정사각형이 아닙니다: {size2}행 기준 각 행 길이가 일치하지 않습니다"
        )
    if size1 != size2:
        raise ValueError(
            f"두 행렬의 크기가 일치하지 않습니다: 첫 번째 {size1}행 vs 두 번째 {size2}행"
        )


def mac(matrix1, matrix2):
    size = len(matrix1)
    return sum(matrix1[i][j] * matrix2[i][j] for i in range(size) for j in range(size))


def measure_mac_avg_ms(matrix1, matrix2):
    start_time = time.perf_counter()
    for _ in range(ITERATIONS):
        mac(matrix1, matrix2)
    end_time = time.perf_counter()

    return (end_time - start_time) / ITERATIONS * 1000


def is_tie(score_a, score_b):
    return abs(score_a - score_b) < EPSILON
