# `auth/user.py`: identity contract

Source: [user.py](/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/auth/user.py). Inspected a2a-sdk 1.1.4, 2026-10-07.

## Mental model and API

`User` is an abstract Python object answering two questions: is an identity authenticated, and what stable name identifies it? It carries no token, permissions, account record, expiry or tenant. A `ServerCallContext` contains a User; stores can resolve an owner string from it. **Authentication** verifies a caller; **authorization** decides what that verified caller may access. Neither follows automatically from declaring a User class.

| Declaration | Input / output / actual behavior |
|---|---|
| `User` | ABC with two abstract read-only properties; cannot be instantiated until a subclass implements both |
| `User.is_authenticated` | Abstract property returning bool; method body has no implementation or I/O |
| `User.user_name` | Abstract property returning str; no normalization, uniqueness or authorization check |
| `UnauthenticatedUser` | Concrete User subclass, with inherited object construction and no stored fields |
| `UnauthenticatedUser.is_authenticated` | Always False |
| `UnauthenticatedUser.user_name` | Always empty string |

These are properties, so access `user.user_name`, not `user.user_name()`. There are no declared constructors, async methods, retries, credential caches, serialization APIs, mutations or destructive operations in this module. Errors in a custom property propagate to callers. Abstract-property instantiation errors are standard ABC behavior.

## Execution boundaries

Default ServerCallContext construction creates a fresh UnauthenticatedUser. HTTP builder adapts a Starlette user when middleware supplied one; its user_name uses display_name. Default gRPC builder returns UnauthenticatedUser regardless of transport metadata. Default owner resolver returns user.user_name directly, so all anonymous calls share the empty owner scope. It does not inspect is_authenticated; a custom object reporting False but a name can still produce that owner string.

A User is call-scoped identity data, but background agent execution may retain the call context. It is not evidence that credentials remain valid indefinitely. Application authentication must validate issuer/audience/expiry and revocation policy before constructing a trusted identity. This package neither obtains nor forwards credentials; do not place bearer strings into user_name. Caller authorization headers belong to the receiving endpoint, not an arbitrary webhook or downstream tool.

## Usage

```python
from a2a.auth.user import User
from a2a.server.context import ServerCallContext

class VerifiedUser(User):
    def __init__(self, subject: str):
        if not subject:
            raise ValueError("Verified subject is required")
        self._subject = subject

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def user_name(self) -> str:
        return self._subject

# Construct only after real request authentication has verified this subject.
context = ServerCallContext(user=VerifiedUser("example-subject"))
assert context.user.is_authenticated
assert context.user.user_name == "example-subject"
```

This example demonstrates the contract, not a token-verification implementation. Use a stable opaque subject rather than mutable display name; include a validated tenant in custom owner resolution if needed. Do not trust a caller-selected name or task ID as an identity. Enforce authentication separately for private task access and extended cards; card security advertisements do not authenticate requests.

## Limits and integration practices

No direct dependency beyond Python abc. Supporting server adapters/stores implement actual use; their schema uses globally keyed task IDs even when reads filter owner. Changing User scope does not fix ID collisions. Keep identity immutable through a request/background execution and ensure application resources do not disappear before execution completes. Local checks verify abstract contract, defaults and property access, without network/auth services.
