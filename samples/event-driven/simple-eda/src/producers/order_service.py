"""
注文を受け付けて OrderCreated イベントを発行する「Producer」。

Producer は「イベントを投げるだけ」で、実際の処理フローは知りません。
これが“疎結合”を生み、後からいくらでも Consumer を追加できます。
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Tuple

from domain.events import OrderCreated, OrderItem
from event_bus import EventBus


class OrderService:
    """注文作成（＝状態変化の起点）"""

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def create_order(
        self,
        order_id: str,
        user_id: str,
        items: Iterable[Tuple[str, int]],
    ) -> None:
        """注文作成 → OrderCreated を publish。"""

        order_items = [OrderItem(sku=sku, quantity=qty) for sku, qty in items]

        event = OrderCreated(
            order_id=order_id,
            user_id=user_id,
            items=order_items,
            created_at=datetime.utcnow(),
        )

        # EventBus にイベントを流す
        self._event_bus.publish(event)