"""Exception hierarchy.

Every failure the system can recover from should be one of these, so the orchestrator
can decide between "degrade" and "stop" without string-matching messages.
"""

from __future__ import annotations


class LanterninaError(Exception):
    """Base class for every error raised by this system."""


# -- boundary violations: these are bugs, never user-facing conditions ------------------


class BoundaryViolation(LanterninaError):
    """An architectural rule was broken at runtime."""


class SealVerificationError(BoundaryViolation):
    """A seal was missing, malformed, or not signed by the expected authority."""


class NotApprovedError(BoundaryViolation):
    """Something tried to deliver content the parent has not greenlit."""


class UnscreenedContentError(BoundaryViolation):
    """Model output reached a user-facing path without passing the safety gate."""


class RetentionViolation(BoundaryViolation):
    """An attempt to persist or serialise data the retention policy forbids.

    Raised by :class:`shared.vision_contracts.RawFrame` when anything tries to pickle,
    copy or write a full camera frame.
    """


# -- operational conditions: expected, recoverable, must degrade not crash --------------


class OperationalError(LanterninaError):
    """A recoverable runtime condition."""


class CloudUnavailable(OperationalError):
    """Azure AI Foundry could not be reached or refused the request."""


class LocalModelUnavailable(OperationalError):
    """The on-device small language model is not loaded or failed."""


class NoCapacityError(OperationalError):
    """No tier — cloud, local, or cache — can serve the request.

    The orchestrator must translate this into a calm, pre-approved fallback for the
    user. It must never surface as a stack trace on a device the learner can see.
    """


class SafetyBlocked(OperationalError):
    """Content Safety rejected the payload. Not an error in the system; a normal outcome."""


class VisionError(OperationalError):
    """The vision pipeline could not produce a reliable reading."""


class MarkersNotFound(VisionError):
    """Fewer than four ArUco markers were located, so the page cannot be rectified."""


class SheetNotRecognised(VisionError):
    """The QR code was unreadable or references an unknown sheet."""
