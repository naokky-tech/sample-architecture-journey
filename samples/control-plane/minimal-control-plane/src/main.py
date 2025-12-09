from __future__ import annotations

from control_plane.agents import Agent
from control_plane.control_plane import ControlPlane
from control_plane.policies import Policy, PolicyStore
from control_plane.tools import DataTool


def build_demo_control_plane() -> ControlPlane:
    """デモ用のポリシーを持つ ControlPlane を構築する。"""

    # agent-A は read_data だけ許可
    # agent-B は read_data / write_data を許可
    store = PolicyStore(
        policies={
            "agent-A": Policy(allowed_actions=["read_data"]),
            "agent-B": Policy(allowed_actions=["read_data", "write_data"]),
        }
    )
    return ControlPlane(policy_store=store)


def run_demo() -> None:
    cp = build_demo_control_plane()
    tool = DataTool()

    # 2 つのエージェントを用意
    agent_a = Agent(agent_id="agent-A", control_plane=cp, tool=tool)
    agent_b = Agent(agent_id="agent-B", control_plane=cp, tool=tool)

    print("=== Demo: agent-A (read only) ===")
    print("-> agent-A: read_data")
    print("   result:", agent_a.act("read_data"))

    print("-> agent-A: write_data")
    try:
        result = agent_a.act("write_data")
        print("   result:", result)
    except PermissionError as exc:
        print("   PermissionError:", exc)

    print("\n=== Demo: agent-B (read + write) ===")
    print("-> agent-B: read_data")
    print("   result:", agent_b.act("read_data"))

    print("-> agent-B: write_data")
    print("   result:", agent_b.act("write_data"))


if __name__ == "__main__":
    run_demo()