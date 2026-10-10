# `langchain/rate_limiters`

The only source is `__init__.py`, re-exporting Core `BaseRateLimiter` and `InMemoryRateLimiter`. This package layer has no limiter algorithm, scheduling, async synchronization, store, persistence, or network activity.

Exact rate-limit behavior belongs to `langchain_core.rate_limiters`. Do not infer distributed coordination from `InMemoryRateLimiter`; it is process-local by design.
