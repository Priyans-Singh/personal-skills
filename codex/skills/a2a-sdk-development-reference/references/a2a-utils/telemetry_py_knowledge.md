# `utils/telemetry.py` execution reference

a2a-sdk 1.1.4 · inspected 2026-10-07 · Python 3.11

Inspected source: `/Users/priyanssingh/Desktop/Wedn-Demo/.venv/lib/python3.11/site-packages/a2a/utils/telemetry.py`. SHA-256: `4219d9f1a4fcafb0e95f9bfbb7824d9e259d922ef5b90cae57811ab78293968d`.

## Responsibility and dependencies

Imports (conditional imports remain conditional; this list does not imply runtime availability):

```python
import asyncio
import functools
import inspect
import logging
import os
from collections.abc import Callable
from typing import TYPE_CHECKING, Any
from typing_extensions import Self
from a2a.utils._async_queue_compat import QueueShutDown
from opentelemetry.trace import SpanKind as SpanKindType
from opentelemetry import trace
from opentelemetry.trace import SpanKind as _SpanKind
from opentelemetry.trace import StatusCode
```

This file implements local utility policy; it has no task-store persistence or built-in retries. Any I/O, mutation, cancellation, and optional dependency exceptions are specified below. Helpers are explicit, including closure-local functions and duplicate version branches.

## Public/constants/type aliases and module initialization

```python
logger = logging.getLogger(__name__)
```

```python
ENABLED_ENV_VAR = 'OTEL_INSTRUMENTATION_A2A_SDK_ENABLED'
```

```python
INSTRUMENTING_MODULE_NAME = 'a2a-python-sdk'
```

```python
INSTRUMENTING_MODULE_VERSION = '1.0.0'
```

```python
env_value = os.getenv(ENABLED_ENV_VAR, 'true')
```

```python
otel_enabled = env_value.lower() == 'true'
```

```python
SpanKind = _SpanKind
```

```python
__all__ = ['SpanKind']
```

```python
_NON_ERROR_EXCEPTIONS: tuple[type[BaseException], ...] = (asyncio.CancelledError, QueueShutDown)
```

## Declarations and execution

### `_NoOp` (line 126)

Coverage ID: `telemetry.py:126:_NoOp`.

Conditional tracing stand-in instantiated when import unavailable or env disabled; absorbs calls/attributes/context entry; exits without suppressing exceptions.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
class _NoOp:

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object, **kwargs: Any) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return self
```

### `_NoOp.__call__` (line 129)

Coverage ID: `telemetry.py:129:_NoOp.__call__`.

Any args/kwargs ignored; returns self.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def __call__(self, *args: Any, **kwargs: Any) -> Any:
    return self
```

### `_NoOp.__enter__` (line 132)

Coverage ID: `telemetry.py:132:_NoOp.__enter__`.

Returns self for with scope.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def __enter__(self) -> Self:
    return self
```

### `_NoOp.__exit__` (line 135)

Coverage ID: `telemetry.py:135:_NoOp.__exit__`.

Returns None, leaving original exception unsuppressed.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def __exit__(self, *args: object, **kwargs: Any) -> None:
    pass
```

### `_NoOp.__getattr__` (line 138)

Coverage ID: `telemetry.py:138:_NoOp.__getattr__`.

Any missing attribute returns self, enabling chained tracer/span calls.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def __getattr__(self, name: str) -> Any:
    return self
```

### `trace_function` (line 155)

Coverage ID: `telemetry.py:155:trace_function`.

Direct decorator or factory via functools.partial. Chooses coroutine wrapper using inspect.iscoroutinefunction only; async generators follow sync path so iteration falls outside span. Span names default module.function; static attributes set before try. Runtime errors propagate; no exporter/provider configured here.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def trace_function(func: Callable | None=None, *, span_name: str | None=None, kind: SpanKindType=SpanKind.INTERNAL, attributes: dict[str, Any] | None=None, attribute_extractor: Callable | None=None) -> Callable:
    if func is None:
        return functools.partial(trace_function, span_name=span_name, kind=kind, attributes=attributes, attribute_extractor=attribute_extractor)
    actual_span_name = span_name or f'{func.__module__}.{func.__name__}'
    is_async_func = inspect.iscoroutinefunction(func)
    logger.debug('Start tracing for %s, is_async_func %s', actual_span_name, is_async_func)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        """Async Wrapper for the decorator."""
        logger.debug('Start async tracer')
        tracer = trace.get_tracer(INSTRUMENTING_MODULE_NAME, INSTRUMENTING_MODULE_VERSION)
        with tracer.start_as_current_span(actual_span_name, kind=kind) as span:
            if attributes:
                for k, v in attributes.items():
                    span.set_attribute(k, v)
            result = None
            exception = None
            try:
                result = await func(*args, **kwargs)
                span.set_status(StatusCode.OK)
            except _NON_ERROR_EXCEPTIONS as ge:
                exception = None
                logger.debug('%s in span %s', type(ge).__name__, actual_span_name)
                span.record_exception(ge)
                raise
            except Exception as e:
                exception = e
                span.record_exception(e)
                span.set_status(StatusCode.ERROR, description=str(e))
                raise
            finally:
                if attribute_extractor:
                    try:
                        attribute_extractor(span, args, kwargs, result, exception)
                    except Exception:
                        logger.exception('attribute_extractor error in span %s', actual_span_name)
            return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        """Sync Wrapper for the decorator."""
        tracer = trace.get_tracer(INSTRUMENTING_MODULE_NAME)
        with tracer.start_as_current_span(actual_span_name, kind=kind) as span:
            if attributes:
                for k, v in attributes.items():
                    span.set_attribute(k, v)
            result = None
            exception = None
            try:
                result = func(*args, **kwargs)
                span.set_status(StatusCode.OK)
            except Exception as e:
                exception = e
                span.record_exception(e)
                span.set_status(StatusCode.ERROR, description=str(e))
                raise
            finally:
                if attribute_extractor:
                    try:
                        attribute_extractor(span, args, kwargs, result, exception)
                    except Exception:
                        logger.exception('attribute_extractor error in span %s', actual_span_name)
            return result
    return async_wrapper if is_async_func else sync_wrapper
```

### `trace_function.async_wrapper` (line 226)

Coverage ID: `telemetry.py:226:trace_function.async_wrapper`.

Gets tracer with instrumentation name AND hardcoded version 1.0.0 (SDK is 1.1.4), starts current span, applies attributes, awaits function, marks OK. Cancellation/QueueShutDown recorded and re-raised without explicit ERROR and extractor exception argument remains None; span context manager may impose additional provider behavior. Other Exception recorded/status ERROR/re-raised. Finally calls synchronous extractor; extractor Exception logged/swallowed. Span creation/static attribute errors occur before try.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
@functools.wraps(func)
async def async_wrapper(*args, **kwargs) -> Any:
    logger.debug('Start async tracer')
    tracer = trace.get_tracer(INSTRUMENTING_MODULE_NAME, INSTRUMENTING_MODULE_VERSION)
    with tracer.start_as_current_span(actual_span_name, kind=kind) as span:
        if attributes:
            for k, v in attributes.items():
                span.set_attribute(k, v)
        result = None
        exception = None
        try:
            result = await func(*args, **kwargs)
            span.set_status(StatusCode.OK)
        except _NON_ERROR_EXCEPTIONS as ge:
            exception = None
            logger.debug('%s in span %s', type(ge).__name__, actual_span_name)
            span.record_exception(ge)
            raise
        except Exception as e:
            exception = e
            span.record_exception(e)
            span.set_status(StatusCode.ERROR, description=str(e))
            raise
        finally:
            if attribute_extractor:
                try:
                    attribute_extractor(span, args, kwargs, result, exception)
                except Exception:
                    logger.exception('attribute_extractor error in span %s', actual_span_name)
        return result
```

### `trace_function.sync_wrapper` (line 272)

Coverage ID: `telemetry.py:272:trace_function.sync_wrapper`.

Gets tracer with name only, starts span, attributes, calls function, OK or Exception ERROR/re-raise. Finally extractor(span,args,kwargs,result,exception), errors logged/swallowed. Does not special-case QueueShutDown; BaseException not caught. Returned generator/awaitable consumed outside span.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
@functools.wraps(func)
def sync_wrapper(*args, **kwargs) -> Any:
    tracer = trace.get_tracer(INSTRUMENTING_MODULE_NAME)
    with tracer.start_as_current_span(actual_span_name, kind=kind) as span:
        if attributes:
            for k, v in attributes.items():
                span.set_attribute(k, v)
        result = None
        exception = None
        try:
            result = func(*args, **kwargs)
            span.set_status(StatusCode.OK)
        except Exception as e:
            exception = e
            span.record_exception(e)
            span.set_status(StatusCode.ERROR, description=str(e))
            raise
        finally:
            if attribute_extractor:
                try:
                    attribute_extractor(span, args, kwargs, result, exception)
                except Exception:
                    logger.exception('attribute_extractor error in span %s', actual_span_name)
        return result
```

### `trace_class` (line 309)

Coverage ID: `telemetry.py:309:trace_class`.

Decorator factory; excludes dunders, truthy include_list takes precedence, otherwise excludes names in exclude_list. Empty include_list behaves as trace-all. Does not install export pipeline.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def trace_class(include_list: list[str] | None=None, exclude_list: list[str] | None=None, kind: SpanKindType=SpanKind.INTERNAL) -> Callable:
    logger.debug('Trace all class %s, %s', include_list, exclude_list)
    exclude_list = exclude_list or []

    def decorator(cls: Any) -> Any:
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith('__') and name.endswith('__'):
                continue
            if include_list and name not in include_list:
                continue
            if not include_list and name in exclude_list:
                continue
            span_name = f'{cls.__module__}.{cls.__name__}.{name}'
            setattr(cls, name, trace_function(span_name=span_name, kind=kind)(method))
        return cls
    return decorator
```

### `trace_class.decorator` (line 366)

Coverage ID: `telemetry.py:366:trace_class.decorator`.

inspect.getmembers(cls,inspect.isfunction) includes eligible inherited functions; setattr replaces on class with trace_function wrapper named module.Class.method. Classmethods/properties excluded by predicate; staticmethods may lose descriptor semantics when assigned plain function. Mutates class and returns it; repeated application can double-wrap.

Implementation evidence (docstring removed; nested bodies retained to make control flow reviewable):

```python
def decorator(cls: Any) -> Any:
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith('__') and name.endswith('__'):
            continue
        if include_list and name not in include_list:
            continue
        if not include_list and name in exclude_list:
            continue
        span_name = f'{cls.__module__}.{cls.__name__}.{name}'
        setattr(cls, name, trace_function(span_name=span_name, kind=kind)(method))
    return cls
```
