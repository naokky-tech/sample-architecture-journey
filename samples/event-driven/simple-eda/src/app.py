"""
アプリケーションのエントリーポイント。

- EventBus を作成
- Consumer を登録（= サービス間の疎結合の中心）
- OrderService の create_order を呼び、イベント連鎖を発生させる

「イベントが流れるとどう処理が進むのか」を可視化するため、
print と event_log を残している。
"""

from __future__ import annotations

from datetime import datetime

from consumers.billing import BillingConsumer
from consumers.inventory import InventoryConsumer
from consumers.notification import NotificationConsumer
from domain.events import (
    InventoryReserved,
    OrderCompleted,
    OrderCreated,
    OrderFailed,
    PaymentSucceeded,
)
from domain.models import InMemoryInventory
from event_bus import EventBus
from producers.order_service import OrderService


def setup_event_bus() -> tuple[EventBus, OrderService]:
    event_bus = EventBus()

    # 在庫初期化
    inventory_model = InMemoryInventory()
    inventory_model.add_stock("BOOK-ARCH-001", 10)
    inventory_model.add_stock("BOOK-ARCH-002", 5)

    billing = BillingConsumer(event_bus)
    inventory = InventoryConsumer(event_bus, inventory_model)
    notification = NotificationConsumer()

    # イベント購読登録（疎結合の中心）
    event_bus.subscribe(OrderCreated, billing.handle_order_created)
    event_bus.subscribe(OrderCreated, inventory.handle_order_created)

    event_bus.subscribe(InventoryReserved, handle_inventory_reserved)
    event_bus.subscribe(PaymentSucceeded, handle_payment_succeeded)

    # 最終通知はここで接続
    event_bus.subscribe(OrderCompleted, notification.handle_order_completed)
    event_bus.subscribe(OrderFailed, notification.handle_order_failed)

    return event_bus, OrderService(event_bus)


def handle_inventory_reserved(event: InventoryReserved) -> None:
    print(f"[Orchestrator] Inventory reserved for order={event.order_id}")


def handle_payment_succeeded(event: PaymentSucceeded) -> None:
    print(f"[Orchestrator] Payment succeeded for order={event.order_id}")
    # ※後で app.main() 内でより実践的なハンドラが上書きされる


def main() -> None:
    event_bus, order_service = setup_event_bus()

    print("=== Event-Driven Sample (simple-eda) ===\n")

    order_id = f"ORD-{int(datetime.utcnow().timestamp())}"
    user_id = "user-123"
    items = [
        ("BOOK-ARCH-001", 1),
        ("BOOK-ARCH-002", 2),
    ]

    # 本番なら「在庫確保 & 決済成功の両方が揃ったら完了」となるが、
    # デモでは PaymentSucceeded のハンドラを上書きして即 OrderCompleted を出す。
    def on_payment(event: PaymentSucceeded) -> None:
        print(f"[Orchestrator] Payment succeeded for order={event.order_id}")
        event_bus.publish(
            OrderCompleted(
                order_id=event.order_id,
                completed_at=datetime.utcnow(),
            )
        )

    # デモのためにハンドラを差し替え
    event_bus._subscribers[PaymentSucceeded].clear()  # type: ignore
    event_bus.subscribe(PaymentSucceeded, on_payment)

    # 流れスタート（注文作成 → イベント連鎖）
    order_service.create_order(order_id, user_id, items)

    print("\n=== Event Log ===")
    for e in event_bus.event_log:
        print(f"- {type(e).__name__}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()