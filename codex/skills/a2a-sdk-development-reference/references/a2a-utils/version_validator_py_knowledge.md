# `utils/version_validator.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/version_validator.py`. SHA-256: `0f1d43225db102ecd375887b8814ba5ad54f7528c0c927b40c003593368c3209`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import functools
import inspect
import logging
from collections.abc import AsyncIterator, Callable
from typing import Any, TypeVar, cast
from packaging.version import InvalidVersion, Version
from a2a.server.context import ServerCallContext
from a2a.utils import constants
from a2a.utils.errors import VersionNotSupportedError
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
F = TypeVar('F', bound=Callable[..., Any])
```

```python
logger = logging.getLogger(__name__)
```

## Declarations and execution

### `validate_version` (line 23)

Coverage ID: `version_validator.py:23:validate_version`.

Parses expected_version once with packaging.Version; invalid expected accepts only exact equality. Returns decorator. Important implementation: same MAJOR is compatible; minor and patch ignored despite docstring claiming major/minor. Context absent bypasses by using expected_version.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def validate_version(expected_version: str) -> Callable[[F], F]:
    try:
        expected_v = Version(expected_version)
    except InvalidVersion:
        expected_v = None

    def decorator(func: F) -> F:

        def _get_actual_version(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
            context = kwargs.get('context')
            if context is None:
                for arg in args:
                    if isinstance(arg, ServerCallContext):
                        context = arg
                        break
            if context is None:
                return expected_version
            headers = context.state.get('headers', {})
            actual_version = headers.get(constants.VERSION_HEADER) or headers.get(constants.VERSION_HEADER.lower())
            if not actual_version:
                return constants.PROTOCOL_VERSION_0_3
            return str(actual_version)

        def _is_version_compatible(actual: str) -> bool:
            if actual == expected_version:
                return True
            if not expected_v:
                return False
            try:
                actual_v = Version(actual)
            except InvalidVersion:
                return False
            else:
                return actual_v.major == expected_v.major
        if inspect.isasyncgenfunction(inspect.unwrap(func)):

            @functools.wraps(func)
            def async_gen_wrapper(*args: Any, **kwargs: Any) -> AsyncIterator[Any]:
                actual_version = _get_actual_version(args, kwargs)
                if not _is_version_compatible(actual_version):
                    logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
                    raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
                return func(*args, **kwargs)
            return cast('F', async_gen_wrapper)

        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            actual_version = _get_actual_version(args, kwargs)
            if not _is_version_compatible(actual_version):
                logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
                raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
            return await func(*args, **kwargs)
        return cast('F', async_wrapper)
    return decorator
```

### `validate_version.decorator` (line 51)

Coverage ID: `version_validator.py:51:validate_version.decorator`.

Inspects unwrap(func) for async-generator classification. Returns synchronous async_gen_wrapper for generators or awaited async_wrapper otherwise. Helpers close over expected version.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def decorator(func: F) -> F:

    def _get_actual_version(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
        context = kwargs.get('context')
        if context is None:
            for arg in args:
                if isinstance(arg, ServerCallContext):
                    context = arg
                    break
        if context is None:
            return expected_version
        headers = context.state.get('headers', {})
        actual_version = headers.get(constants.VERSION_HEADER) or headers.get(constants.VERSION_HEADER.lower())
        if not actual_version:
            return constants.PROTOCOL_VERSION_0_3
        return str(actual_version)

    def _is_version_compatible(actual: str) -> bool:
        if actual == expected_version:
            return True
        if not expected_v:
            return False
        try:
            actual_v = Version(actual)
        except InvalidVersion:
            return False
        else:
            return actual_v.major == expected_v.major
    if inspect.isasyncgenfunction(inspect.unwrap(func)):

        @functools.wraps(func)
        def async_gen_wrapper(*args: Any, **kwargs: Any) -> AsyncIterator[Any]:
            actual_version = _get_actual_version(args, kwargs)
            if not _is_version_compatible(actual_version):
                logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
                raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
            return func(*args, **kwargs)
        return cast('F', async_gen_wrapper)

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        actual_version = _get_actual_version(args, kwargs)
        if not _is_version_compatible(actual_version):
            logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
            raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
        return await func(*args, **kwargs)
    return cast('F', async_wrapper)
```

### `validate_version.decorator._get_actual_version` (line 52)

Coverage ID: `version_validator.py:52:validate_version.decorator._get_actual_version`.

kwargs context wins; otherwise first positional ServerCallContext. No context returns expected version. Reads state[headers], checks A2A-Version and lowercase only; missing/empty returns 0.3; value converted with str. Does not normalize arbitrary casing or authenticate context.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _get_actual_version(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    context = kwargs.get('context')
    if context is None:
        for arg in args:
            if isinstance(arg, ServerCallContext):
                context = arg
                break
    if context is None:
        return expected_version
    headers = context.state.get('headers', {})
    actual_version = headers.get(constants.VERSION_HEADER) or headers.get(constants.VERSION_HEADER.lower())
    if not actual_version:
        return constants.PROTOCOL_VERSION_0_3
    return str(actual_version)
```

### `validate_version.decorator._is_version_compatible` (line 80)

Coverage ID: `version_validator.py:80:validate_version.decorator._is_version_compatible`.

Exact string match succeeds first. Otherwise valid packaging versions succeed if major equals expected major; malformed versions False. No minor comparison or supported-version registry.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def _is_version_compatible(actual: str) -> bool:
    if actual == expected_version:
        return True
    if not expected_v:
        return False
    try:
        actual_v = Version(actual)
    except InvalidVersion:
        return False
    else:
        return actual_v.major == expected_v.major
```

### `validate_version.decorator.async_gen_wrapper` (line 95)

Coverage ID: `version_validator.py:95:validate_version.decorator.async_gen_wrapper`.

Checks version immediately at iterator creation; logs and raises VersionNotSupportedError on mismatch, otherwise returns original iterator without consuming or wrapping it.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
@functools.wraps(func)
def async_gen_wrapper(*args: Any, **kwargs: Any) -> AsyncIterator[Any]:
    actual_version = _get_actual_version(args, kwargs)
    if not _is_version_compatible(actual_version):
        logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
        raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
    return func(*args, **kwargs)
```

### `validate_version.decorator.async_wrapper` (line 114)

Coverage ID: `version_validator.py:114:validate_version.decorator.async_wrapper`.

Checks version on awaiting wrapper; mismatch logs and raises VersionNotSupportedError, otherwise awaits function with unchanged arguments/result.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
@functools.wraps(func)
async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
    actual_version = _get_actual_version(args, kwargs)
    if not _is_version_compatible(actual_version):
        logger.warning("Version mismatch: actual='%s', expected='%s'", actual_version, expected_version)
        raise VersionNotSupportedError(message=f"A2A version '{actual_version}' is not supported by this handler. Expected version '{expected_version}'.")
    return await func(*args, **kwargs)
```
