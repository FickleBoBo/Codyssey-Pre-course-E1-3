from mac_core import EPSILON, ITERATIONS, is_tie, mac, measure_mac_avg_ms
from pattern_generator import generate_cross, generate_x


def read_n_by_n(n):
    matrix = []
    error_msg = f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요."

    while len(matrix) < n:
        line = input()

        try:
            row = [float(x) for x in line.strip().split()]
        except ValueError:
            print(error_msg)
            continue

        if len(row) != n:
            print(error_msg)
            continue

        matrix.append(row)

    return matrix


def manual_mode():
    print("#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")

    print("필터 A (3줄 입력, 공백 구분)")
    filter_a = read_n_by_n(3)
    print("✓ 필터 A 저장 완료")
    print()

    print("필터 B (3줄 입력, 공백 구분)")
    filter_b = read_n_by_n(3)
    print("✓ 필터 B 저장 완료")
    print()

    print("#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")

    print("패턴 선택 (1: +, 2: X, 3: 사용자 지정 패턴)")
    while True:
        choice = input("선택: ").strip()
        if choice in ("1", "2", "3"):
            break
        print("잘못된 선택입니다. 1, 2, 3 중 하나를 입력하세요.")

    if choice == "1":
        pattern = generate_cross(3)
    elif choice == "2":
        pattern = generate_x(3)
    else:
        print("패턴 (3줄 입력, 공백 구분)")
        pattern = read_n_by_n(3)
    print()

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    avg_ms = (
        measure_mac_avg_ms(pattern, filter_a) + measure_mac_avg_ms(pattern, filter_b)
    ) / 2

    if not is_tie(score_a, score_b):
        print("#---------------------------------------")
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/{ITERATIONS}회): {avg_ms:.6f} ms")
        print(f"판정: {'A' if score_a > score_b else 'B'}")
    else:
        print("#---------------------------------------")
        print("# [3] MAC 결과 (판정 불가)")
        print("#---------------------------------------")
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/{ITERATIONS}회): {avg_ms:.6f} ms")
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
