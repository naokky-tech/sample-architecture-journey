from __future__ import annotations


class DataTool:
    """エージェントが呼び出すツールの最小実装。

    実際にはここに、SaaS API / DB クエリ / 社内サービス などがぶら下がる。
    """

    def read_data(self) -> dict:
        """読み取り専用の操作（安全度が高い想定）。"""
        return {"message": "hello from data"}

    def write_data(self, msg: str) -> str:
        """書き込み操作（より慎重な権限が必要になる想定）。"""
        return f"write: {msg}"