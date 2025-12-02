from __future__ import annotations

from typing import Dict, List, Optional

from core.entities import Task
from core.ports import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    """メモリ上にタスクを保持するシンプルな実装。

    学習用のため、プロセスを終了するとデータは失われます。
    """

    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._current_id: int = 0

    def next_identity(self) -> int:
        self._current_id += 1
        return self._current_id

    def save(self, task: Task) -> None:
        self._tasks[task.id] = task

    def list_all(self) -> List[Task]:
        # 外から書き換えられないようにコピーを返すのも一案だが、
        # 今回はシンプルさを優先してそのまま返す。
        return list(self._tasks.values())

    def find_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)