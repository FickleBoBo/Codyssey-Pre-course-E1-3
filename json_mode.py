import json

from mac_core import ITERATIONS, is_tie, mac, measure_mac_avg_ms, validate_matrix_pair
from optimize_1d import flatten, measure_mac_1d_avg_ms

DATA_FILE = "data.json"


def normalize_label(raw):
    if raw == "+" or raw == "cross":
        return "Cross"
    if raw == "x":
        return "X"
    return None


def load_dataset():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{DATA_FILE} 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print(f"{DATA_FILE} 파일의 형식이 올바르지 않습니다.")
        return None

    return data


def json_mode():
    data = load_dataset()
    if data is None:
        return

    print("#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")

    if "filters" not in data:
        print(f"{DATA_FILE}에 'filters' 키가 없습니다.")
        return
    if not isinstance(data["filters"], dict):
        print(f"{DATA_FILE}의 'filters' 값이 올바른 형식(객체)이 아닙니다.")
        return

    for size_key, filter_pair in data["filters"].items():
        if not isinstance(filter_pair, dict):
            print(f"{DATA_FILE}의 '{size_key}' 필터 값이 올바른 형식이 아닙니다.")
            return

        labeled = {}
        for filter_key, matrix in filter_pair.items():
            label = normalize_label(filter_key)
            if label is None:
                print(
                    f"{DATA_FILE}의 '{size_key}' 필터에서 인식할 수 없는 키가 있습니다: {filter_key!r}"
                )
                return
            labeled[label] = matrix

        data["filters"][size_key] = labeled
        print(f"✓ {size_key} 필터 로드 완료 ({', '.join(labeled)})")
    print()

    print("#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")

    if "patterns" not in data:
        print(f"{DATA_FILE}에 'patterns' 키가 없습니다.")
        return
    if not isinstance(data["patterns"], dict):
        print(f"{DATA_FILE}의 'patterns' 값이 올바른 형식(객체)이 아닙니다.")
        return

    perf_samples = {}
    results = []
    for pattern_key, entry in data["patterns"].items():
        try:
            pattern_input = entry["input"]

            size_key = f"size_{pattern_key.split('_')[1]}"
            filter_pair = data["filters"][size_key]

            validate_matrix_pair(pattern_input, filter_pair["Cross"])
            validate_matrix_pair(pattern_input, filter_pair["X"])
            score_cross = mac(pattern_input, filter_pair["Cross"])
            score_x = mac(pattern_input, filter_pair["X"])

            if size_key not in perf_samples:
                perf_samples[size_key] = (pattern_input, filter_pair)

            pattern_expected = normalize_label(entry["expected"])
            if pattern_expected is None:
                raise ValueError(
                    f"expected 값을 인식할 수 없습니다: {entry['expected']!r}"
                )

            tie = is_tie(score_cross, score_x)
            verdict = (
                "UNDECIDED" if tie else ("Cross" if score_cross > score_x else "X")
            )
            result = "PASS" if verdict == pattern_expected else "FAIL"

            reason = None
            if result == "FAIL":
                reason = (
                    "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
                    if tie
                    else f"판정({verdict})이 expected({pattern_expected})와 다름"
                )

            results.append({"key": pattern_key, "result": result, "reason": reason})

            print(f"--- {pattern_key} ---")
            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")
            print(f"판정: {verdict} | expected: {pattern_expected} | {result}")
            print()
        except (KeyError, TypeError, ValueError, IndexError) as e:
            reason = f"스키마/크기 오류: {e}"
            results.append({"key": pattern_key, "result": "FAIL", "reason": reason})
            print(f"--- {pattern_key} ---")
            print(f"판정 불가: {reason}")
            print()

    print("#---------------------------------------")
    print(f"# [3] 성능 분석 (평균/{ITERATIONS}회)")
    print("#---------------------------------------")

    perf_targets = []
    for size_key, (pattern_input, filter_pair) in perf_samples.items():
        n = int(size_key.split("_")[1])
        avg_ms = (
            measure_mac_avg_ms(pattern_input, filter_pair["Cross"])
            + measure_mac_avg_ms(pattern_input, filter_pair["X"])
        ) / 2

        flat_pattern = flatten(pattern_input)
        flat_cross = flatten(filter_pair["Cross"])
        flat_x = flatten(filter_pair["X"])
        avg_ms_1d = (
            measure_mac_1d_avg_ms(flat_pattern, flat_cross)
            + measure_mac_1d_avg_ms(flat_pattern, flat_x)
        ) / 2

        perf_targets.append((n, avg_ms, avg_ms_1d))

    print(f"{'크기':>15}{'평균 시간(ms)':>15}{'1D 평균(ms)':>15}{'연산 횟수':>15}")
    print("-" * 60)
    for n, avg_ms, avg_ms_1d in perf_targets:
        size_label = f"{n}x{n}"
        print(f"{size_label:>15}{avg_ms:>15.6f}{avg_ms_1d:>15.6f}{n * n:>15}")
    print()

    print("#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")

    total = len(results)
    passed = sum(1 for r in results if r["result"] == "PASS")
    failed = total - passed

    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")

    if failed > 0:
        print()
        print("실패 케이스:")
        for r in results:
            if r["result"] == "FAIL":
                print(f"- {r['key']}: {r['reason']}")
