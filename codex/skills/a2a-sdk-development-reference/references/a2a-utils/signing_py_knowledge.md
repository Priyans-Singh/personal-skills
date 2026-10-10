# `utils/signing.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/signing.py`. SHA-256: `3c4b7d38894b90ae4f6bcc2fd31068c10442546f417ade3de780675f8facb297`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import json
from collections.abc import Callable
from typing import Any, TypedDict
from google.protobuf.json_format import MessageToDict
from a2a.types import AgentCard, AgentCardSignature
from a2a.utils._jcs import MAX_DEPTH, CanonicalizationError, canonicalize
import jwt
from jwt import api_jws
from jwt.api_jwk import PyJWK
from jwt.exceptions import PyJWTError
from jwt.utils import base64url_decode, base64url_encode
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

## Declarations and execution

### `SignatureVerificationError` (line 27)

Coverage ID: `signing.py:27:SignatureVerificationError`.

Base Exception for signature-verification failures; no extra fields.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class SignatureVerificationError(Exception):
    pass
```

### `NoSignatureError` (line 31)

Coverage ID: `signing.py:31:NoSignatureError`.

SignatureVerificationError subclass raised before canonicalization when signatures is empty.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class NoSignatureError(SignatureVerificationError):
    pass
```

### `InvalidSignaturesError` (line 35)

Coverage ID: `signing.py:35:InvalidSignaturesError`.

SignatureVerificationError subclass for canonicalization failure or exhaustion of signatures without valid PyJWT verification.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class InvalidSignaturesError(SignatureVerificationError):
    pass
```

### `ProtectedHeader` (line 39)

Coverage ID: `signing.py:39:ProtectedHeader`.

TypedDict only (not runtime schema validation). kid, alg, jku, typ annotations; optional-valued keys still declared required in typing unless caller uses get.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class ProtectedHeader(TypedDict):
    kid: str
    ' Key identifier. '
    alg: str | None
    ' Algorithm used for signing. '
    jku: str | None
    ' JSON Web Key Set URL. '
    typ: str | None
    ' Token type.\n\n    Best practice: SHOULD be "JOSE" for JWS tokens.\n    '
```

### `create_agent_card_signer` (line 55)

Coverage ID: `signing.py:55:create_agent_card_signer`.

Captures signing key/header in returned synchronous closure for its lifetime. Private/shared key goes only to local PyJWT signing call, not AgentCard. Caller owns storage/disposal. No key fetching, rotation, authentication, or certificate validation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def create_agent_card_signer(signing_key: PyJWK | str | bytes, protected_header: ProtectedHeader, header: dict[str, Any] | None=None) -> Callable[[AgentCard], AgentCard]:

    def agent_card_signer(agent_card: AgentCard) -> AgentCard:
        """Signs agent card."""
        canonical_payload = _canonicalize_agent_card(agent_card)
        jws_string = api_jws.encode(payload=canonical_payload.encode('utf-8'), key=signing_key, algorithm=protected_header.get('alg', 'HS256'), headers=dict(protected_header))
        protected, _, signature = jws_string.split('.')
        agent_card_signature = AgentCardSignature(header=header, protected=protected, signature=signature)
        agent_card.signatures.append(agent_card_signature)
        return agent_card
    return agent_card_signer
```

### `create_agent_card_signer.agent_card_signer` (line 71)

Coverage ID: `signing.py:71:create_agent_card_signer.agent_card_signer`.

Canonicalizes card with signatures excluded, UTF-8 bytes passed to api_jws.encode, algorithm header.get(alg,HS256) (present None does not default). Splits compact JWS, stores protected/signature and unprotected header in appended AgentCardSignature; mutates and returns same card. Signing/canonicalization failures propagate. Repeated calls append signatures.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def agent_card_signer(agent_card: AgentCard) -> AgentCard:
    canonical_payload = _canonicalize_agent_card(agent_card)
    jws_string = api_jws.encode(payload=canonical_payload.encode('utf-8'), key=signing_key, algorithm=protected_header.get('alg', 'HS256'), headers=dict(protected_header))
    protected, _, signature = jws_string.split('.')
    agent_card_signature = AgentCardSignature(header=header, protected=protected, signature=signature)
    agent_card.signatures.append(agent_card_signature)
    return agent_card
```

### `create_signature_verifier` (line 101)

Coverage ID: `signing.py:101:create_signature_verifier`.

Captures key_provider and allowed algorithms, returns synchronous closure. No caching/retry or network code here; provider controls any external fetching and key lifetimes.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def create_signature_verifier(key_provider: Callable[[str | None, str | None], PyJWK | str | bytes], algorithms: list[str]) -> Callable[[AgentCard], None]:

    def signature_verifier(agent_card: AgentCard) -> None:
        """Verifies agent card signatures."""
        if not agent_card.signatures:
            raise NoSignatureError('AgentCard has no signatures to verify.')
        try:
            canonical_payload = _canonicalize_agent_card(agent_card)
        except CanonicalizationError as e:
            raise InvalidSignaturesError('AgentCard cannot be canonicalized for verification') from e
        encoded_payload = base64url_encode(canonical_payload.encode('utf-8')).decode('utf-8')
        for agent_card_signature in agent_card.signatures:
            try:
                protected_header_json = base64url_decode(agent_card_signature.protected.encode('utf-8')).decode('utf-8')
                protected_header = json.loads(protected_header_json)
                kid = protected_header.get('kid')
                jku = protected_header.get('jku')
                verification_key = key_provider(kid, jku)
                token = f'{agent_card_signature.protected}.{encoded_payload}.{agent_card_signature.signature}'
                jwt.decode(jwt=token, key=verification_key, algorithms=algorithms)
                break
            except PyJWTError:
                continue
        else:
            raise InvalidSignaturesError('No valid signature found')
    return signature_verifier
```

### `create_signature_verifier.signature_verifier` (line 118)

Coverage ID: `signing.py:118:create_signature_verifier.signature_verifier`.

No signatures → NoSignatureError. CanonicalizationError → InvalidSignaturesError. Rebuilds shared encoded payload once. Per signature decodes protected JSON, reads untrusted kid/jku, calls key_provider, rebuilds JWS and jwt.decode with algorithm allowlist. First success returns None; only PyJWTError is swallowed to try next. JSON/Unicode/base64/provider/non-dict AttributeError can escape. Never trust arbitrary jku without provider policy; no declared token expiry on cards.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def signature_verifier(agent_card: AgentCard) -> None:
    if not agent_card.signatures:
        raise NoSignatureError('AgentCard has no signatures to verify.')
    try:
        canonical_payload = _canonicalize_agent_card(agent_card)
    except CanonicalizationError as e:
        raise InvalidSignaturesError('AgentCard cannot be canonicalized for verification') from e
    encoded_payload = base64url_encode(canonical_payload.encode('utf-8')).decode('utf-8')
    for agent_card_signature in agent_card.signatures:
        try:
            protected_header_json = base64url_decode(agent_card_signature.protected.encode('utf-8')).decode('utf-8')
            protected_header = json.loads(protected_header_json)
            kid = protected_header.get('kid')
            jku = protected_header.get('jku')
            verification_key = key_provider(kid, jku)
            token = f'{agent_card_signature.protected}.{encoded_payload}.{agent_card_signature.signature}'
            jwt.decode(jwt=token, key=verification_key, algorithms=algorithms)
            break
        except PyJWTError:
            continue
    else:
        raise InvalidSignaturesError('No valid signature found')
```

### `_clean_empty` (line 167)

Coverage ID: `signing.py:167:_clean_empty`.

Depth-limited recursive cleanup: empty dict/list/string removed as None; actual None also removed from containers. Nonempty scalars (including 0/False) retained. Returns new dict/list or None; nested >128 CanonicalizationError. No mutation of original.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _clean_empty(d: Any, depth: int=0) -> Any:
    if depth > MAX_DEPTH:
        raise CanonicalizationError(f'nesting exceeds the maximum depth of {MAX_DEPTH}')
    if isinstance(d, dict):
        cleaned_dict = {k: cleaned_v for k, v in d.items() if (cleaned_v := _clean_empty(v, depth + 1)) is not None}
        return cleaned_dict or None
    if isinstance(d, list):
        cleaned_list = [cleaned_v for v in d if (cleaned_v := _clean_empty(v, depth + 1)) is not None]
        return cleaned_list or None
    if isinstance(d, str) and (not d):
        return None
    return d
```

### `_canonicalize_agent_card` (line 198)

Coverage ID: `signing.py:198:_canonicalize_agent_card`.

MessageToDict proto JSON → drop signatures → _clean_empty → canonicalize. Uses JSON field aliases and default omission, so protobuf presence influences signed bytes. Empty card can canonicalize to null. Returns str; no card mutation.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _canonicalize_agent_card(agent_card: AgentCard) -> str:
    card_dict = MessageToDict(agent_card)
    card_dict.pop('signatures', None)
    cleaned_dict = _clean_empty(card_dict)
    return canonicalize(cleaned_dict)
```
