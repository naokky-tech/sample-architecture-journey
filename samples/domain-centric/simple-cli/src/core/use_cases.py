from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .entities import Task
from .ports import TaskRepository


@dataclass
class AddTaskUseCase:
    """タスクを新規登録するユースケース。"""

    repository: TaskRepository

    def execute(self, title: str) -> Task:
        # ドメイン中心の世界では ID 発行も「ルール」として repo に委譲することが多い
        new_id = self.repository.next_identity()
        task = Task(id=new_id, title=title)
        self.repository.save(task)
        return task


@dataclass
class ListTasksUseCase:
    """タスク一覧を取得するユースケース。"""

    repository: TaskRepository

    def execute(self) -> List[Task]:
        return self.repository.list_all()


@dataclass
class CompleteTaskUseCase:
    """タスクを完了状態にするユースケース。"""

    repository: TaskRepository

    def execute(self, task_id: int) -> Task | None:
        task = self.repository.find_by_id(task_id)
        if task is None:
            return None

        task.complete()
        self.repository.save(task)
        return task