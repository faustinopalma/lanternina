"""Agents — one module per agent, each implementing a protocol from ``shared.agents``.

Hard rule, enforced by ``tests/test_boundaries.py``: **no module in this package may
import another module in this package.** If two agents need to cooperate, the planner in
``orchestrator/`` composes them; they do not know about each other.

Agents may import ``shared`` and the standard library. They may not import
``orchestrator``, ``panel``, an Azure SDK, or a model runtime — all model access goes
through the router handed to them in :class:`shared.agents.AgentContext`.
"""
