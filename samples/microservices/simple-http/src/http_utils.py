## src/http_utils.py
"""
http.server を使った簡易JSON API用のユーティリティ関数群。
"""

import json
from http.server import BaseHTTPRequestHandler


def read_json(handler: BaseHTTPRequestHandler) -> dict:
    """リクエストボディを JSON として読み込む。空の場合は {} を返す。"""
    length_str = handler.headers.get("Content-Length")
    if not length_str:
        return {}
    try:
        length = int(length_str)
    except ValueError:
        return {}

    raw = handler.rfile.read(length)
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def send_json(handler: BaseHTTPRequestHandler, status_code: int, payload: dict | list) -> None:
    """レスポンスとして JSON を送信する。"""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def send_error_json(handler: BaseHTTPRequestHandler, status_code: int, message: str) -> None:
    """エラーを JSON 形式で返す。"""
    payload = {"error": message}
    send_json(handler, status_code, payload)