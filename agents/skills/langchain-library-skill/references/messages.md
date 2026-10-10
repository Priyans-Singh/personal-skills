# `langchain/messages`

This directory only contains `__init__.py`, a public re-export facade for `langchain_core.messages`. It exports human, AI, system, and tool messages; chunks; tool-call/result representations; citations/annotations; usage/token details; text/image/audio/video/file/data/reasoning blocks; `RemoveMessage`; and `trim_messages`.

There is no local message implementation, persistence, validation, serialization, or I/O. Trace exact normalization, chunk merging, trimming, and token behavior into `langchain_core.messages`.
