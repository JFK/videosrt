---
description: All I/O must be async. No sync database calls, no sync file I/O, no sync HTTP requests.
---

# Async-First Rule

## Database
- Always use `AsyncSession` from `database.py`
- Never import or use synchronous SQLAlchemy sessions

## External API calls
- Use `httpx.AsyncClient` or provider SDK async methods
- For SDKs without async support (e.g., Google API client), wrap with `asyncio.to_thread()`

## File I/O
- Use `aiofiles` for file read/write
- Use `asyncio.create_subprocess_exec()` for ffmpeg and other CLI tools

## Background work
- Use FastAPI `BackgroundTasks` for long-running pipelines
- Never use `threading` or `concurrent.futures` directly

## Timeouts
- All external API calls must have explicit timeouts
- Reference: `GEMINI_TIMEOUT_SEC = 600` pattern in gemini.py
