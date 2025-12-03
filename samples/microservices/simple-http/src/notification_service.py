"""
notification_service.py

通知を担当する HTTP サービス。
port=8003 で待ち受ける。

GET  /notifications       -> 通知一覧
POST /notifications       -> 通知作成
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from dataclasses import dataclass, asdict
from typing import List

from http_utils import read_json, send_json, send_error_json


@dataclass
class Notification:
    id: int
    user_id: int
    message: str


_notifications: List[Notification] = []
_next_notification_id: int = 1


class NotificationServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/notifications":
            self._handle_list_notifications()
        else:
            send_error_json(self, 404, "Not Found")

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/notifications":
            self._handle_create_notification()
        else:
            send_error_json(self, 404, "Not Found")

    def _handle_list_notifications(self) -> None:
        payload = [asdict(n) for n in _notifications]
        send_json(self, 200, payload)

    def _handle_create_notification(self) -> None:
        global _next_notification_id

        data = read_json(self)
        try:
            user_id = int(data.get("user_id"))
        except (TypeError, ValueError):
            send_error_json(self, 400, "user_id is required and must be int")
            return

        message = data.get("message")
        if not message:
            send_error_json(self, 400, "message is required")
            return

        notification = Notification(
            id=_next_notification_id,
            user_id=user_id,
            message=message,
        )
        _notifications.append(notification)
        _next_notification_id += 1

        print(f"[notification-service] {notification.message}")
        send_json(self, 201, asdict(notification))

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def run_server(port: int = 8003) -> None:
    server = HTTPServer(("localhost", port), NotificationServiceHandler)
    print(f"[notification-service] Listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()