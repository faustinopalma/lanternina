"""Orchestrator — the planner and the wiring, running on the Linux mini-PC.

This package owns the three things nothing else is allowed to own:

* ``router.py``   — the only module that may talk to Azure AI Foundry;
* ``safety.py``   — the only holder of the content-safety sealing key;
* ``approval.py`` — the only holder of the parent-approval sealing key.

It also hosts the planner, which is the only component that holds more than one agent.
Agents are handed a :class:`shared.agents.AgentContext` and nothing else.
"""
