# src/presentation/controller.py
"""
Presentation Layer（UI / Controller）

- ユーザー入力（文字列の user_id）を受け取る
- Application Layer を呼び出す
- 例外を捕捉して、UI 向けのメッセージに変換する

HTTP の代わりに CLI を使っているだけで、考え方は同じです。
"""

from application.user_service import get_user
from domain.exceptions import UserNotFoundError, ValidationError


def get_user_view(user_id_str: str) -> str:
    """
    CLI 向けの「1ユーザー取得」ハンドラ。
    HTTP であれば Web フレームワークの Controller に相当します。
    """
    try:
        # Presentation の責務として、HTTP 文字列をそのまま Application に渡す
        user = get_user(user_id_str)
    except ValidationError as e:
        return f"[Validation Error] {e}"
    except UserNotFoundError as e:
        return f"[Not Found] {e}"
    except Exception as e:  # 想定外のエラーはまとめて処理
        return f"[Unexpected Error] {e}"

    # UI 向けの表現に整形（ここではシンプルなテキスト）
    lines = [
        "User:",
        f"  id: {user.id}",
        f"  name: {user.name}",
        f"  email: {user.email}",
        f"  is_active: {user.is_active}",
    ]
    return "\n".join(lines)