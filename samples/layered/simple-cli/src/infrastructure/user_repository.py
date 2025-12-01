# src/infrastructure/user_repository.py
"""
Infrastructure Layer（Repository / DB / 外部API）

ここでは実際のDBの代わりに、インメモリ辞書を「なんちゃってDB」として使っています。
将来、本物の RDB や外部API に差し替えるときも、この層を置き換えるだけで済みます。
"""

from typing import Dict, Optional

from domain.entities import User

# 擬似的な「ユーザーテーブル」
_FAKE_USER_TABLE: Dict[int, User] = {
    1: User(id=1, name="Alice", email="alice@example.com", is_active=True),
    2: User(id=2, name="Bob", email="bob@example.com", is_active=True),
    3: User(id=3, name="Charlie", email="charlie@example.com", is_active=False),
}


def find_by_id(user_id: int) -> Optional[User]:
    """
    ユーザーIDからユーザーを1件取得する Repository 関数。
    DB/外部API による取得処理は、この関数の中に閉じ込めます。
    """
    return _FAKE_USER_TABLE.get(user_id)