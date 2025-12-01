# src/domain/entities.py
"""
Domain Layer（ビジネスロジック・エンティティ）

ここではシンプルな User エンティティだけを定義しています。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    is_active: bool = True

    def display_name(self) -> str:
        """
        ドメインロジックの例。
        UI 向けに「表示名」を組み立てるメソッドなどを置けます。
        """
        return f"{self.name} <{self.email}>"