from dataclasses import dataclass

@dataclass
class Task:
    """タスクのドメインモデル。

    ドメインルールが増えてきたら、このクラスにメソッドとして追加していきます。
    """

    id: int
    title: str
    is_completed: bool = False

    def complete(self) -> None:
        """タスクを完了状態にする。"""
        self.is_completed = True