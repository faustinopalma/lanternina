"""What a token has to survive before it becomes a subject.

The valid-token case is the least interesting one here. The tests that earn their place
are the forgeries: an algorithm swapped underneath us, a token minted for a different
application, one that expired, one with no signature at all.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from panel.tokens import Claims, TokenVerifier
from shared.errors import NotAuthenticated

ISSUER = "https://lantepwhrr.ciamlogin.com/07702e41/v2.0"
AUDIENCE = "11111111-2222-3333-4444-555555555555"
SUBJECT = "sub-abc"
CONTACT = "parent@example.test"


def segment(data: dict[str, Any]) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


@pytest.fixture(scope="module")
def keypair() -> tuple[Any, Any]:
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private, private.public_key()


class FixedKey:
    def __init__(self, key: Any) -> None:
        self._key = key

    def key_for(self, token: str) -> Any:
        return self._key


@pytest.fixture
def verifier(keypair: tuple[Any, Any]) -> TokenVerifier:
    _, public = keypair
    return TokenVerifier(issuer=ISSUER, audience=AUDIENCE, keys=FixedKey(public))


def make_token(private: Any, **overrides: Any) -> str:
    now = int(time.time())
    claims: dict[str, Any] = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "sub": SUBJECT,
        "email": CONTACT,
        "iat": now,
        "exp": now + 300,
    }
    claims.update(overrides)
    for key, value in list(claims.items()):
        if value is None:
            del claims[key]
    return jwt.encode(claims, private, algorithm="RS256")


def test_a_well_formed_token_yields_the_subject(
    verifier: TokenVerifier, keypair: tuple[Any, Any]
) -> None:
    private, _ = keypair
    assert verifier.verify(make_token(private)) == Claims(subject=SUBJECT, contact=CONTACT)


def test_contact_falls_back_to_preferred_username(
    verifier: TokenVerifier, keypair: tuple[Any, Any]
) -> None:
    private, _ = keypair
    token = make_token(private, email=None, preferred_username=CONTACT)
    assert verifier.verify(token).contact == CONTACT


@pytest.mark.parametrize(
    ("label", "overrides"),
    [
        ("wrong audience", {"aud": "some-other-application"}),
        ("wrong issuer", {"iss": "https://evil.example/v2.0"}),
        ("expired", {"exp": int(time.time()) - 60}),
        ("no subject", {"sub": None}),
        ("no expiry", {"exp": None}),
        ("no issued-at", {"iat": None}),
        ("empty subject", {"sub": "   "}),
    ],
)
def test_tokens_that_must_be_refused(
    verifier: TokenVerifier, keypair: tuple[Any, Any], label: str, overrides: dict[str, Any]
) -> None:
    private, _ = keypair
    with pytest.raises(NotAuthenticated):
        verifier.verify(make_token(private, **overrides))


def test_a_token_signed_by_someone_else_is_refused(verifier: TokenVerifier) -> None:
    stranger = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(NotAuthenticated):
        verifier.verify(make_token(stranger))


def test_an_unsigned_token_is_refused(verifier: TokenVerifier) -> None:
    """``alg: none`` is a token that asks to be trusted because it says so."""
    now = int(time.time())
    header = segment({"alg": "none", "typ": "JWT"})
    payload = segment(
        {"iss": ISSUER, "aud": AUDIENCE, "sub": SUBJECT, "iat": now, "exp": now + 300}
    )

    with pytest.raises(NotAuthenticated):
        verifier.verify(f"{header}.{payload}.")


def test_an_hmac_token_is_refused_even_though_the_key_is_public(
    verifier: TokenVerifier, keypair: tuple[Any, Any]
) -> None:
    """The algorithm-confusion attack, as an attacker would mount it.

    Forged by hand rather than with ``jwt.encode``, which refuses PEM keys as HMAC
    secrets — an attacker does not use our library.

    Measured, not assumed: this forgery is refused by PyJWT's own key guard, which fires
    on decode too, so it passes even with the algorithm list left wide open. It proves
    the forgery fails; it does **not** prove our pinning is what fails it. That is what
    the next test is for.
    """
    _, public = keypair
    pem = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    now = int(time.time())
    signing_input = "{}.{}".format(
        segment({"alg": "HS256", "typ": "JWT"}),
        segment({"iss": ISSUER, "aud": AUDIENCE, "sub": SUBJECT, "iat": now, "exp": now + 300}),
    )
    signature = hmac.new(pem, signing_input.encode(), hashlib.sha256).digest()
    forged = f"{signing_input}.{base64.urlsafe_b64encode(signature).rstrip(b'=').decode()}"

    with pytest.raises(NotAuthenticated):
        verifier.verify(forged)


def test_hs256_is_refused_even_when_its_signature_is_genuinely_valid() -> None:
    """This one isolates the pinning, and nothing else.

    A real HS256 token, signed with exactly the key the resolver hands back, and not in
    PEM form so PyJWT's key guard stays out of the way. The only thing standing between
    this token and a trusted subject is ``algorithms=["RS256"]``.
    """
    secret = "a-plain-shared-secret-long-enough-for-sha256"
    verifier = TokenVerifier(issuer=ISSUER, audience=AUDIENCE, keys=FixedKey(secret))
    now = int(time.time())
    token = jwt.encode(
        {"iss": ISSUER, "aud": AUDIENCE, "sub": SUBJECT, "iat": now, "exp": now + 300},
        secret,
        algorithm="HS256",
    )

    with pytest.raises(NotAuthenticated):
        verifier.verify(token)


def test_every_refusal_says_the_same_thing(
    verifier: TokenVerifier, keypair: tuple[Any, Any]
) -> None:
    """Otherwise the endpoint becomes an oracle for what is wrong with a token."""
    private, _ = keypair
    stranger = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    messages = set()

    for token in (
        make_token(private, aud="another-app"),
        make_token(private, exp=int(time.time()) - 60),
        make_token(stranger),
        "not-even-a-token",
    ):
        with pytest.raises(NotAuthenticated) as raised:
            verifier.verify(token)
        messages.add(str(raised.value))

    assert messages == {"token rejected"}
