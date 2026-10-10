# `utils/push_url_validator.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/push_url_validator.py`. SHA-256: `f9efe2c7c4d28277e688f738deda4f695309c0d99c80229c28d38a7963c6dedd`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import asyncio
import ipaddress
import logging
import socket
import urllib.parse
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
logger = logging.getLogger(__name__)
```

## Declarations and execution

### `_ip_is_blocked` (line 13)

Coverage ID: `push_url_validator.py:13:_ip_is_blocked`.

Strips IPv6 zone suffix then ip_address parse. Invalid string returns True. Blocks private, loopback, link-local, multicast, reserved, unspecified addresses. Uses installed Python ipaddress classification, not remote policy.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _ip_is_blocked(ip_str: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip_str.split('%', maxsplit=1)[0])
    except ValueError:
        return True
    return addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_multicast or addr.is_reserved or addr.is_unspecified
```

### `validate_push_notification_url` (line 29)

Coverage ID: `push_url_validator.py:29:validate_push_notification_url`.

Parses URL and port; ValueError rejects. Only http/https with hostname. Resolves via running loop.getaddrinfo SOCK_STREAM, explicit port or 443/80. OSError rejects; any blocked address rejects; otherwise True (even empty resolver list). No HTTP fetch, redirect check, DNS pinning, credential stripping, timeout, or retry; cancellation propagates. DNS re-resolution at send time can change destination; use network egress controls too.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
async def validate_push_notification_url(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        explicit_port = parsed.port
    except ValueError:
        logger.warning('Push-notification URL is unparseable: %s', url)
        return False
    if parsed.scheme not in ('http', 'https'):
        logger.warning('Push-notification URL scheme %r is not http/https: %s', parsed.scheme, url)
        return False
    host = parsed.hostname
    if not host:
        logger.warning('Push-notification URL has no hostname: %s', url)
        return False
    port = explicit_port or (443 if parsed.scheme == 'https' else 80)
    try:
        loop = asyncio.get_running_loop()
        infos = await loop.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError:
        logger.warning('Push-notification host %r could not be resolved: %s', host, url)
        return False
    for info in infos:
        if _ip_is_blocked(str(info[4][0])):
            logger.warning('Push-notification host %r resolves to a non-public address: %s', host, url)
            return False
    return True
```
