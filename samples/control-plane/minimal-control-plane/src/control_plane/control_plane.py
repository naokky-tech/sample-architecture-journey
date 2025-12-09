from __future__ import annotations

from dataclasses import dataclass

from .policies import Action, AgentId, PolicyStore


@dataclass
class ControlPlane:
    """エージェントの行動を判定する「制御プレーン」の最小実装。

    現実の世界ではここに、
    - OAuth2.1 / RAR / Resource Indicators による Action-level Authorization
    - DPoP / Token Binding によるトークンのなりすまし対策
    - Context Engine / ABAC によるコンテキストベースのポリシー評価
    - PDP（OPA / Cerbos）連携
    などが多層的にぶら下がることになる。
    """

    policy_store: PolicyStore

    def authorize(self, agent_id: AgentId, action: Action) -> bool:
        """このエージェントに対して行動（Action）を許可してよいか判定する。"""
        return self.policy_store.is_allowed(agent_id, action)