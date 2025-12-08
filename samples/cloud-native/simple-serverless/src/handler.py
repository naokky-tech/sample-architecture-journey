"""
simple-serverless/src/handler.py

Serverless ランタイムから呼ばれることを想定した最小の handler 関数。
"""

from typing import Any, Dict


def handler(event: Dict[str, Any], context: Dict[str, Any] | None = None) -> Dict[str, str]:
    """
    Args:
        event: 呼び出し元から渡される辞書形式のイベント
        context: 実行時 Context（未使用）

    Returns:
        dict: レスポンス
    """
    name = event.get("name", "world")
    return {"message": f"Hello, {name}!"}