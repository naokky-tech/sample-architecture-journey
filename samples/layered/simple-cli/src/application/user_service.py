# src/application/user_service.py
"""
Application Layer（ユースケース・アプリの振る舞い）

- ユースケース単位の処理をまとめる層
- UI やインフラの詳細には依存せず、
  ドメインとインフラを使って「何をするか」を記述する
"""

from typing import Final

from domain.entities import User
from domain.exceptions import UserNotFoundError, ValidationError
from infrastructure.user_repository import find_by_id


def _parse_user_id(user_id_str: str) -> int:
    """
    プレゼンテーション層から渡された user_id（文字列）を検証して int に変換する。
    """
    if not user_id_str:
        raise ValidationError("user_id is required")

    if not user_id_str.isdigit():
        raise ValidationError("user_id must be a positive integer")

    user_id = int(user_id_str)
    if user_id <= 0:
        raise ValidationError("user_id must be greater than 0")

    return user_id


def get_user(user_id_str: str) -> User:
    """
    「ユーザーを1件取得する」というユースケース。

    1. user_id のバリデーション
    2. Repository からユーザー取得
    3. 見つからなければ UserNotFoundError
    """
    user_id = _parse_user_id(user_id_str)

    user = find_by_id(user_id)
    if user is None:
        raise UserNotFoundError(f"user with id={user_id} not found")

    # ここで追加のビジネスルールを入れることもできる
    # 例: 非アクティブユーザーは取得させないなど
    return user