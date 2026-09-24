---
last_mapped_commit: 2ab2e51140e076aa6f8585eb8cdf2b07d40351cb
last_mapped_at: 2026-09-24
---
<!-- refreshed: 2026-09-24 -->

# Coding Conventions

**Analysis Date:** 2026-09-24

## Naming Patterns

**Files:**

- snake_case for Python modules: `routes.py`, `schemas.py`, `database.py`, `config.py`, `main.py`, `ai.py`, `init.py`, `authClerk.py`, `userMethods.py`, `models.py`, `monitoring.py`
- PascalCase for class names within files: `Settings`, `UserModel`, `SessionModel`, `PlaceModel`, `AuthUser`, `ChatMessage`, `ChatHistory`, `UserMethods`
- Legacy directories `app.old/`, `app.old2/` mirror active structure but are not imported

**Functions:**

- snake_case for functions: `get_db()`, `init_db()`, `stream_chat()`, `llm_call()`, `full_response()`, `get_current_user()`, `auth_user()`, `get_or_create_user()`
- Exception: `User_Exists` in `app/userMethods.py:5` starts with capital (non-standard)

**Variables:**

- snake_case for local variables and parameters: `chat_data`, `current_user`, `db_session`, `user_id`, `clerk_user_id`
- ALL_CAPS for settings constants: `CLERK_PUBLIC_KEY`, `CLERK_SECRET_KEY`, `DATABASE_URL`, `OPENROUTER_API_KEY`, `AUTHORIZED_PARTIES` in `app/config.py:6-10`

**Types:**

- PascalCase for SQLAlchemy models with `Model` suffix: `UserModel`, `SessionModel`, `PlaceModel` in `app/models.py`
- Pydantic schemas use `*Create`, `*Response` suffixes: `UserCreate`, `UserResponse`, `SessionCreate`, `SessionResponse`, `PlaceCreate`, `PlaceResponse` in `app/schemas.py`
- Legacy models use `_table` suffix: `Book_table`, `Author_table` in `app.old/models.py`

## Code Style

**Formatting:**

- No formatter configured (no Black, Ruff, Prettier)
- No line length limit enforced
- Lines routinely exceed 88 characters

**Linting:**

- No linter configured (no flake8, Ruff, pylint, mypy)
- `pyproject.toml` contains only `[project]` table with dependencies — no `[tool.*]` sections
- Project relies entirely on manual discipline

## Import Organization

**Order:**

1. Standard library imports (`typing`, `datetime`, `uuid`, `os`, `contextlib`)
2. Third-party imports (`fastapi`, `pydantic`, `sqlalchemy`, `openai`, `structlog`, `clerk_backend_api`, `sse_starlette`, `psycopg`, `uuid_extension`, `uuid6`)
3. Local imports using bare module names (no package prefix)

**Path Aliases:**

- Not used
- **Critical issue:** All local imports use bare names (`from config import settings`, `from routes import router`, `from database import ...`) — `app/` is not a proper package (no `__init__.py`). This requires CWD to be `app/` or `app/` on `PYTHONPATH`. Should use `from app.config import settings` instead.

**Examples from codebase:**

```python

# app/main.py

from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
import os
import psycopg
import uuid
from typing import Optional
from uuid_extension import uuid7
from pydantic import Field
from config import settings          # bare import
from init import init_db             # bare import
from routes import router as main_router  # bare import
```

## Error Handling

**Patterns:**

- **LLM streaming (`app/ai.py:36-38`):** Catches generic `Exception`, logs via `structlog.get_logger()`, yields error event `{"event": "error", "data": str(e)}`, then returns
- **Full response wrapper (`app/ai.py:57-58`):** Catches exceptions, yields error event, stops without sending "done" event
- **Auth (`app/authClerk.py:51-58`):** Re-raises `HTTPException`; wraps all other exceptions in 401 `HTTPException` with detail `"Invalid or expired token: {e}"`
- **Database (`app/userMethods.py:46-57`):** Uses try/except with `IntegrityError` catch — on conflict, rolls back, queries existing user, returns it
- **No global exception handler** registered in `app/main.py` — unhandled exceptions produce FastAPI default 500

**Anti-patterns observed:**

- Bare `except Exception` without specific error types in `app/ai.py`
- Print statement for errors in legacy commented code (`app/userMethods.py:32`): `print(f"error {e}")` — TODO mentions structlog
- `app/routes.py:4` imports `from auth import get_current_user` but file is `authClerk.py` — import bug

## Logging

**Framework:** `structlog` (imported in `app/ai.py:5`, `logger = structlog.get_logger()` at line 8)

**Patterns:**

- Used only in `app/ai.py` for LLM streaming errors
- Not used elsewhere in active codebase
- Legacy code (`app.old/crud.py`, `app.old2/crud.py`) also used structlog

**Example:**

```python

# app/ai.py

import structlog
logger = structlog.get_logger()

try:
    # ... LLM call
except Exception as e:
    logger.error("LLM stream call failed", error=str(e))
    yield {"event": "error", "data": str(e)}
    return
```

## Comments

**When to Comment:**

- Inline comments explaining intent or workarounds (e.g., `app/main.py:19` "this lacks rate limiting and can be targeted by ddos")
- Section markers using `#*`, `#!`, `#?` prefixes inconsistently
- TODO/FIXME comments present but not standardized

**JSDoc/TSDoc:**

- Not applicable (Python project)
- Docstrings are sparse — only `app/ai.py:43` `full_response()` has a docstring
- No consistent docstring format (Google, NumPy, Sphinx)

## Function Design

**Size:** No enforced guidelines — functions are generally small and focused

**Parameters:**

- Type hints inconsistent — some fully annotated (`app/database.py:26` `async def get_db() -> AsyncGenerator[AsyncSession, None]`), others missing types (`app/userMethods.py:5` `clerk_user_id` untyped)
- FastAPI `Depends()` used for dependency injection in route handlers

**Return Values:**

- Async generators for streaming (`llm_call`, `full_response` yield events)
- Pydantic models for structured responses (`UserResponse`, `SessionResponse`)
- `EventSourceResponse` for SSE endpoints
- Raw dicts for simple endpoints (`/health/live` returns `{"status": "up"}`)

## Module Design

**Exports:**

- Module-level singletons: `settings = Settings()` in `app/config.py:18`, `clerk = Clerk(...)` in `app/authClerk.py:14`, `client = AsyncOpenAI(...)` in `app/ai.py:9-12`, `engine`, `AsyncSessionLocal` in `app/database.py`
- Router instance: `router = APIRouter()` in `app/routes.py:12`
- FastAPI app: `app = FastAPI(...)` in `app/main.py:25-29`

**Barrel Files:**

- Not used — each module imports directly from source files

---

*Convention analysis: 2026-09-24*
