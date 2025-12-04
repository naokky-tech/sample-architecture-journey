"""
在庫確保を行う Consumer。

OrderCreated を受けて在庫チェックを行い、成功なら InventoryReserved、
失敗なら OrderFailed を EventBus に publish する。
"""

from __future__ import annotations

from datetime import datetime

from domain.events import OrderCreated, InventoryReserved, OrderFailed
from domain.models import InMemoryInventory
from event_bus import EventBus


class InventoryConsumer:
    """在庫確保処理"""

    def __init__(self, event_bus: EventBus, inventory: InMemoryInventory) -> None:
        self._event_bus = event_bus
        self._inventory = inventory

    def handle_order_created(self, event: OrderCreated) -> None:
        print(f"[Inventory] Checking stock for order={event.order_id}")

        ok = self._inventory.reserve_items(event.items)

        if ok:
            reserved_skus = [item.sku for item in event.items]
            self._event_bus.publish(
                InventoryReserved(
                    order_id=event.order_id,
                    reserved_skus=reserved_skus,
                    reserved_at=datetime.utcnow(),
                )
            )
        else:
            self._event_bus.publish(
                OrderFailed(
                    order_id=event.order_id,
                    reason="Insufficient stock",
                    failed_at=datetime.utcnow(),
                )
            )