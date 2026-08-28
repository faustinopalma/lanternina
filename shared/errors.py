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

    Raised by :class:`shared.vision_contracts.WhatCameBack`, which is read and not kept, and
    by :class:`shared.vision_contracts.RawFrame`, which nothing constructs.
    """


# -- operational conditions: expected, recoverable, must degrade not crash --------------


class OperationalError(LanterninaError):
    """A recoverable runtime condition."""


class CloudUnavailable(OperationalError):
    """Microsoft Foundry could not be reached or refused the request."""


class NoCapacityError(OperationalError):
    """Neither the cloud nor the approved-content cache can serve the request.

    The orchestrator must translate this into a calm, pre-approved fallback for the
    user. It must never surface as a stack trace on a device the learner can see.
    """


class SafetyBlocked(OperationalError):
    """Content Safety rejected the payload. Not an error in the system; a normal outcome."""


class UnusableGeneration(OperationalError):
    """The model returned something the agent cannot use, e.g. malformed structure.

    Normal, and never shown to anyone: the caller drops this item and keeps going. The
    text cannot be repaired in place, because editing it would break the safety seal.
    """


class VisionError(OperationalError):
    """The vision pipeline could not produce a reliable reading."""


class MarkersNotFound(VisionError):
    """Fewer than four ArUco markers were located. Nothing raises this: the marker
    pipeline was retired, and a page is read against the blank it was printed from."""


class SheetNotRecognised(VisionError):
    """The QR code was unreadable or references an unknown sheet. Nothing raises this
    either — there is nothing printed on a page that is there for a machine."""


class AuthNotConfigured(OperationalError):
    """No way to establish who is calling.

    Refused rather than waved through: an unconfigured panel must serve nobody, not
    everybody.
    """


# -- access control: the caller proved who they are, and is still not allowed -----------
#
# Deliberately neither a BoundaryViolation nor an OperationalError. Refusing an
# unapproved account is the system working, so it must not be logged as a bug, and it
# must not be degraded around either.


class AccessDenied(LanterninaError):
    """Authenticated, but not permitted."""


class NotAuthenticated(AccessDenied):
    """No usable proof of identity was presented.

    Distinct from :class:`AccountNotApproved` because the remedy differs: sign in, rather
    than wait for someone to approve you. It reveals nothing, since it is reached before
    any account is looked up.
    """


class AccountNotApproved(AccessDenied):
    """The account exists but no administrator has activated it yet."""


class AccountNotFound(AccessDenied):
    """A valid token presented a subject this system has never seen.

    Denied rather than auto-provisioned: signing in to the identity provider must not be
    enough to obtain an account.
    """
