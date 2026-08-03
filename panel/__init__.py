"""Panel — the parent-facing web control surface.

The panel is the *only* place approval decisions are made, and the only UI that sees
pending proposals. It is bound to the local network, authenticated, and never exposes a
camera stream — there is no preview endpoint, by design.

It may import ``shared`` and call into ``orchestrator`` services. It must not import
``agents`` directly, and it must not construct a sealer.
"""
