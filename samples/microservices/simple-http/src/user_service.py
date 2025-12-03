"""
user_service.py

ユーザ管理を担当する HTTP サービス。
port=8001 で待ち受ける。

GET  /users           -> ユーザ一覧
POST /users           -> ユーザ作成
GET  /users/{id}      -> ユーザ取得
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from dataclasses import dataclass, asdict
from typing import Dict, List

from http_utils import read_json, send_json, send_error_json


@dataclass
class User:
    id: int
    name: str


_users: Dict[int, User] = {}
_next_user_id: int = 1


class UserServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")

        if parsed.path == "/users":
            self._handle_list_users()
        elif len(path_parts) == 2 and path_parts[0] == "users":
            self._handle_get_user(path_parts[1])
        else:
            send_error_json(self, 404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/users":
            self._handle_create_user()
        else:
            send_error_json(self, 404, "Not Found")

    def _handle_list_users(self) -> None:
        users: List[User] = list(_users.values())
        payload = [asdict(u) for u in users]
        send_json(self, 200, payload)

    def _handle_get_user(self, user_id_str: str) -> None:
        try:
            user_id = int(user_id_str)
        except ValueError:
            send_error_json(self, 400, "Invalid user id")
            return

        user = _users.get(user_id)
        if not user:
            send_error_json(self, 404, "User not found")
            return

        send_json(self, 200, asdict(user))

    def _handle_create_user(self) -> None:
        global _next_user_id

        data = read_json(self)
        name = data.get("name")
        if not name:
            send_error_json(self, 400, "name is required")
            return

        user = User(id=_next_user_id, name=name)
        _users[user.id] = user
        _next_user_id += 1

        send_json(self, 201, asdict(user))

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # ログを抑制（必要であれば print に切り替えてもOK）
        return


def run_server(port: int = 8001) -> None:
    server = HTTPServer(("localhost", port), UserServiceHandler)
    print(f"[user-service] Listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()