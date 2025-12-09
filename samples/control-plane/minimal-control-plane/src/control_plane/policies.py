from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, TypedDict


# シンプルさを優先して、Action / AgentId は文字列エイリアスにしている。
Action = str
AgentId = str


@dataclass(frozen=True)
class Policy:
    """エージェントに許可された行動（Action）の集合。

    実際の世界では「行動 × リソース × 条件 × 有効期限」
    のような構造に拡張されていく。
    """

    allowed_actions: List[Action]


class PolicyRecord(TypedDict):
    allowed_actions: List[Action]


class PolicyStore:
    """エージェントごとのポリシーを保持する最小のストア。

    実運用では DB や外部 PDP（OPA / Cerbos など）に置き換わる想定。
    """

    def __init__(self, policies: Dict[AgentId, Policy] | None = None) -> None:
        # 内部的には Dict で完結させるシンプルな実装
        self._policies: Dict[AgentId, Policy] = policies or {}

    def set_policy(self, agent_id: AgentId, policy: Policy) -> None:
        """エージェントのポリシーを登録・更新する。"""
        self._policies[agent_id] = policy

    def get_policy(self, agent_id: AgentId) -> Policy | None:
        """エージェントのポリシーを取得する。存在しなければ None。"""
        return self._policies.get(agent_id)

    def is_allowed(self, agent_id: AgentId, action: Action) -> bool:
        """指定されたエージェントに、その行動が許可されているか判定する。

        ポリシーが存在しない場合は False（= deny-by-default）。
        """
        policy = self.get_policy(agent_id)
        if policy is None:
            return False
        return action in policy.allowed_actions