"""
最終結果を通知する Consumer。

EDA では「最後にどうなるか」を Producer（OrderService）が知る必要はない。
NotificationConsumer のような機能は、後から自由に追加できる。
"""

from __future__ import annotations

from domain.events import OrderCompleted, OrderFailed


class NotificationConsumer:
    """成功・失敗の通知（メール・Slack の代わりに print 出力）"""

    def handle_order_completed(self, event: OrderCompleted) -> None:
        print(f"[Notification] Order {event.order_id} completed successfully! 🎉")

    def handle_order_failed(self, event: OrderFailed) -> None:
        print(f"[Notification] Order {event.order_id} failed: {event.reason}")