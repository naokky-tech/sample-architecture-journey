from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Task

class TaskRepository(ABC):
    """タスクに関する永続化のポート（インターフェース）。

    ドメインから見た「やってほしいこと」だけを定義します。
    具体的に「どこにどう保存するか（メモリ、ファイル、DB）」はここでは決めません。
    """

    @abstractmethod
    def next_identity(self) -> int:
        """新しいタスク ID を発行する。"""
        raise NotImplementedError

    @abstractmethod
    def save(self, task: Task) -> None:
        """タスクを保存する。新規・更新の両方を扱う想定。"""
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Task]:
        """全タスクを取得する。"""
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """ID でタスクを 1 件取得する。"""
        raise NotImplementedError