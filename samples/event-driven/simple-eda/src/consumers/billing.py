"""
決済処理を担当する Consumer。

OrderService とは一切結合しておらず、「OrderCreatedが来たら処理する」というだけ。
この独立性が EDA の強み。
"""

from __future__ import annotations

from datetime import datetime

from domain.events import OrderCreated, PaymentSucceeded, OrderFailed
from event_bus import EventBus


class BillingConsumer:
    """決済処理（単純化されたサンプル）"""

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus

    def handle_order_created(self, event: OrderCreated) -> None:
        """OrderCreated 発生時に決済サービスとして反応。"""

        amount = sum(item.quantity * 1000 for item in event.items)
        print(f"[Billing] Processing payment for order={event.order_id}, amount={amount} JPY")

        payment_ok = True  # デモでは常に成功する

        if payment_ok:
            self._event_bus.publish(
                PaymentSucceeded(
                    order_id=event.order_id,
                    user_id=event.user_id,
                    paid_at=datetime.utcnow(),
                    amount=amount,
                )
            )
        else:
            self._event_bus.publish(
                OrderFailed(
                    order_id=event.order_id,
                    reason="Payment failed",
                    failed_at=datetime.utcnow(),
                )
            )