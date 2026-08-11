def generate_cross(n):
    center = n // 2
    return [
        [1.0 if i == center or j == center else 0.0 for j in range(n)] for i in range(n)
    ]


def generate_x(n):
    return [
        [1.0 if i == j or i == n - 1 - j else 0.0 for j in range(n)] for i in range(n)
    ]
