"""
event_bus.py

イベント駆動（EDA）の中心となる「Event Bus（イベント配信ハブ）」の最小実装。

● やること
- subscribe(event_type, handler)
- publish(event)

● やらないこと（本番システムでは必要になるが、このサンプルでは省略）
- 永続化（Kafka / SQS / PubSub）
- リトライ
- デッドレターキュー
- 非同期実行

EDA を理解するうえでは、この“できるだけ薄い EventBus” が最も学習効果が高い。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, List, Type, Any, Protocol


class Event(Protocol):
    """イベントであることを示すための Marker Protocol。
    dataclass のイベントがこのプロトコルを満たす。
    """
    ...


EventHandler = Callable[[Event], None]


class EventBus:
    """最小の Event Bus 実装。
    
    - イベント型ごとにハンドラを登録し
    - publish(event) 呼び出し時に該当するハンドラへ配送する
    
    ※ シンプルすぎるほどシンプルだが、基本原理は Kafka でも同じ。
    """

    def __init__(self) -> None:
        # {イベント型: [ハンドラ群]} の形で管理
        self._subscribers: DefaultDict[Type[Any], List[EventHandler]] = defaultdict(list)
        self._event_log: List[Event] = []

    def subscribe(self, event_type: Type[Event], handler: EventHandler) -> None:
        """イベント種別とハンドラをひも付ける。"""
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        """イベントを配送する中心メソッド。
        
        - 発行された event をログに記録し
        - その型を購読するすべてのハンドラへ通知
        """
        self._event_log.append(event)
        for handler in list(self._subscribers.get(type(event), [])):
            handler(event)

    @property
    def event_log(self) -> List[Event]:
        """publish されたイベントの履歴（Event Sourcing の最小イメージ）"""
        return list(self._event_log)