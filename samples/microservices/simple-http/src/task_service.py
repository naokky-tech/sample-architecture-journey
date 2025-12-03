"""
task_service.py

タスク管理を担当する HTTP サービス。
port=8002 で待ち受ける。

GET  /tasks          -> タスク一覧
POST /tasks          -> タスク作成（通知サービスに通知）
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from dataclasses import dataclass, asdict
from typing import Dict, List
import json
import urllib.request
import urllib.error

from http_utils import read_json, send_json, send_error_json


@dataclass
class Task:
    id: int
    title: str
    user_id: int


_tasks: Dict[int, Task] = {}
_next_task_id: int = 1

NOTIFICATION_SERVICE_URL = "http://localhost:8003"


class TaskServiceHandler(BaseHTTPRequestHandler):
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
        tasks: List[Task] = list(_tasks.values())
        payload = [asdict(t) for t in tasks]
        send_json(self, 200, payload)

    def _handle_create_task(self) -> None:
        global _next_task_id

        data = read_json(self)
        title = data.get("title")
        if not title:
            send_error_json(self, 400, "title is required")
            return

        try:
            user_id = int(data.get("user_id"))
        except (TypeError, ValueError):
            send_error_json(self, 400, "user_id is required and must be int")
            return

        task = Task(id=_next_task_id, title=title, user_id=user_id)
        _tasks[task.id] = task
        _next_task_id += 1

        # 通知サービスへ連携（失敗してもタスク作成自体は成功扱い）
        self._notify_task_created(task)

        send_json(self, 201, asdict(task))

    def _notify_task_created(self, task: Task) -> None:
        payload = {
            "user_id": task.user_id,
            "message": f"Task '{task.title}' was created for user {task.user_id}",
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{NOTIFICATION_SERVICE_URL}/notifications",
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=2) as resp:
                resp.read()  # レスポンスは特に使わない
        except urllib.error.URLError as exc:
            print(f"[task-service] Failed to call notification-service: {exc}")

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def run_server(port: int = 8002) -> None:
    server = HTTPServer(("localhost", port), TaskServiceHandler)
    print(f"[task-service] Listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()