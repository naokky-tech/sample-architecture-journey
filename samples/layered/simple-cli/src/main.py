# src/main.py
"""
シンプルな CLI エントリポイント。
Presentation Layer の controller を呼び出しているだけです。
"""

from presentation.controller import get_user_view


def main() -> None:
    print("=== Layered Architecture Sample ===")
    print("Available user ids: 1, 2, 3")
    user_id = input("Enter user id: ").strip()

    result = get_user_view(user_id)

    print("\n--- Result ---")
    print(result)
    print("--------------")


if __name__ == "__main__":
    main()