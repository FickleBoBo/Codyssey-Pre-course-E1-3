from json_mode import json_mode
from manual_mode import manual_mode


def main():
    print("=== Mini NPU Simulator ===")
    print()
    print("[모드 선택]")
    print()
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    try:
        choice = input("선택: ").strip()
        print()

        if choice == "1":
            manual_mode()
        elif choice == "2":
            json_mode()
        else:
            print("잘못된 선택입니다. 프로그램을 종료합니다.")
    except (KeyboardInterrupt, EOFError):
        print("프로그램이 종료되었습니다.")


if __name__ == "__main__":
    main()
