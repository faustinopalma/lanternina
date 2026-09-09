"""Serialize activity mutations across hub services and camera threads."""

from __future__ import annotations

import os
import threading
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

from devices.house import House

_mutex = threading.RLock()
_local = threading.local()
Parameters = ParamSpec("Parameters")
Result = TypeVar("Result")


def exclusive(
    action: Callable[Concatenate[House, Parameters], Result],
) -> Callable[Concatenate[House, Parameters], Result]:
    @wraps(action)
    def wrapped(house: House, *args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        with _mutex:
            if getattr(_local, "held", False):
                return action(house, *args, **kwargs)
            house.sheets_dir.mkdir(parents=True, exist_ok=True)
            with (house.sheets_dir / ".activity.lock").open("a+b") as lock:
                if os.name == "posix":
                    import fcntl

                    fcntl.flock(lock, fcntl.LOCK_EX)
                _local.held = True
                try:
                    return action(house, *args, **kwargs)
                finally:
                    _local.held = False

    return wrapped
