"""
simple-serverless/src/invoke_local.py

クラウドを使わずに handler をローカル実行し動作確認するためのスクリプト。
"""

import json
from pathlib import Path
from handler import handler


def load_event() -> dict:
    event_path = Path(__file__).resolve().parent.parent / "event.json"
    with event_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    event = load_event()
    result = handler(event, context={})

    print("=== Input Event ===")
    print(json.dumps(event, ensure_ascii=False, indent=2))

    print("\n=== Handler Result ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()