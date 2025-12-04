"""
ドメインイベントの定義。

イベント駆動アーキテクチャでは「状態そのもの」ではなく、
「状態の変化」をイベントとして表現する。

→ Event Sourcing では、このイベント群が“真実の源泉（Source of Truth）”になる。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class OrderItem:
    """注文内の商品を表現する値オブジェクト。"""
    sku: str
    quantity: int


@dataclass(frozen=True)
class OrderCreated:
    """注文が作成された（= write model に変化が起きた）ことを表すイベント。"""
    order_id: str
    user_id: str
    items: List[OrderItem]
    created_at: datetime


@dataclass(frozen=True)
class PaymentSucceeded:
    """決済が成功したことを表すイベント。"""
    order_id: str
    user_id: str
    paid_at: datetime
    amount: int


@dataclass(frozen=True)
class InventoryReserved:
    """在庫が確保できたことを表すイベント。"""
    order_id: str
    reserved_skus: List[str]
    reserved_at: datetime


@dataclass(frozen=True)
class OrderCompleted:
    """注文が完了したことを表す最終イベント。"""
    order_id: str
    completed_at: datetime


@dataclass(frozen=True)
class OrderFailed:
    """注文処理が失敗したときに publish されるイベント。"""
    order_id: str
    reason: str
    failed_at: datetime