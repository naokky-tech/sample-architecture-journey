# src/domain/exceptions.py
"""
レイヤー間で共通して使うドメイン寄りの例外定義。
"""


class DomainError(Exception):
    """ドメイン関連の基底例外クラス。"""


class ValidationError(DomainError):
    """入力値の検証に失敗した場合の例外。"""


class UserNotFoundError(DomainError):
    """ユーザーが見つからない場合の例外。"""