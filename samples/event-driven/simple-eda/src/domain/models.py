"""
在庫を表す最小のモデル。

「モデル」は本来 RDB や別サービスに置かれるが、
イベント駆動のサンプルでは in-memory で十分理解できる。

InventoryConsumer がこのモデルを参照する。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .events import OrderItem


@dataclass
class InMemoryInventory:
    """非常に簡易的な在庫管理。

    reserve_items が True を返せば在庫確保成功とする。
    """

    stock: Dict[str, int] = field(default_factory=dict)

    def add_stock(self, sku: str, quantity: int) -> None:
        self.stock[sku] = self.stock.get(sku, 0) + quantity

    def has_enough(self, sku: str, quantity: int) -> bool:
        return self.stock.get(sku, 0) >= quantity

    def reserve_items(self, items: List[OrderItem]) -> bool:
        """在庫が足りるかチェックし、問題なければ減らす。"""
        for item in items:
            if not self.has_enough(item.sku, item.quantity):
                return False

        for item in items:
            self.stock[item.sku] -= item.quantity

        return True