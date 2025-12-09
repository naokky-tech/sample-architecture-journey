from __future__ import annotations

from dataclasses import dataclass

from .control_plane import ControlPlane
from .policies import Action, AgentId
from .tools import DataTool


@dataclass
class Agent:
    """AI エージェントを簡易に表現したクラス。

    - id: エージェント固有の ID（Identity Plane に相当）
    - control_plane: 行動許可を問い合わせる先
    - tool: 実際に行動を実行するツール（Data Plane に相当）
    """

    agent_id: AgentId
    control_plane: ControlPlane
    tool: DataTool

    def act(self, action: Action):
        """指定された行動（Action）を実行する。

        実行前に ControlPlane に問い合わせ、
        許可されない行動であれば PermissionError を送出する。
        """

        # 1. 行動が許可されているか、必ず事前に確認する
        if not self.control_plane.authorize(self.agent_id, action):
            # deny-by-default（許可されていないものは必ず拒否）
            raise PermissionError(
                f"Agent '{self.agent_id}' cannot perform '{action}'"
            )

        # 2. 許可された場合のみツールを呼び出す
        if action == "read_data":
            return self.tool.read_data()
        if action == "write_data":
            return self.tool.write_data("updated")

        # 想定外のアクションは ValueError として扱い、実装ミスに気付けるようにする
        raise ValueError(f"Unknown action: {action}")