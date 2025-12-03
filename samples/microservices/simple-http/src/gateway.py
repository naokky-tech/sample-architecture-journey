"""
gateway.py

クライアントからの入口となる API Gateway。
port=8000 で待ち受ける。

POST /tasks   -> user-service でユーザ存在確認 → task-service にタスク作成を委譲
GET  /tasks   -> task-service の /tasks をプロキシ
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import urllib.request
import urllib.error

from http_utils import read_json, send_json, send_error_json

USER_SERVICE_URL = "http://localhost:8001"
TASK_SERVICE_URL = "http://localhost:8002"


class GatewayHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/tasks":
            self._handle_list_tasks()
        else:
            send_error_json(self, 404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/tasks":
            self._handle_create_task()
        else:
            send_error_json(self, 404, "Not Found")

    def _handle_list_tasks(self) -> None:
        try:
            with urllib.request.urlopen(f"{TASK_SERVICE_URL}/tasks", timeout=2) as resp:
                raw = resp.read()
                status = resp.getcode()
        except urllib.error.URLError as exc:
            print(f"[gateway] Failed to call task-service: {exc}")
            send_error_json(self, 502, "Failed to reach task-service")
            return

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            payload = {"error": "Invalid JSON from task-service"}
            status = 502

        send_json(self, status, payload)

    def _handle_create_task(self) -> None:
        data = read_json(self)
        title = data.get("title")
        user_id = data.get("user_id")

        if not title:
            send_error_json(self, 400, "title is required")
            return

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            send_error_json(self, 400, "user_id is required and must be int")
            return

        # 1. user-service でユーザが存在するか確認
        if not self._check_user_exists(user_id):
            send_error_json(self, 400, "User does not exist")
            return

        # 2. task-service にタスク作成を依頼
        payload = {"title": title, "user_id": user_id}
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{TASK_SERVICE_URL}/tasks",
            data=data_bytes,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=2) as resp:
                raw = resp.read()
                status = resp.getcode()
        except urllib.error.URLError as exc:
            print(f"[gateway] Failed to call task-service: {exc}")
            send_error_json(self, 502, "Failed to reach task-service")
            return

        try:
            task_payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            send_error_json(self, 502, "Invalid JSON from task-service")
            return

        send_json(self, status, task_payload)

    def _check_user_exists(self, user_id: int) -> bool:
        try:
            with urllib.request.urlopen(f"{USER_SERVICE_URL}/users/{user_id}", timeout=2) as resp:
                if resp.getcode() == 404:
                    return False
                resp.read()
                return True
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            print(f"[gateway] HTTP error from user-service: {exc}")
            return False
        except urllib.error.URLError as exc:
            print(f"[gateway] Failed to call user-service: {exc}")
            return False

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def run_server(port: int = 8000) -> None:
    server = HTTPServer(("localhost", port), GatewayHandler)
    print(f"[gateway] Listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()