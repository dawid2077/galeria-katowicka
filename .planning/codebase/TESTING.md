# TESTING.md

**Project:** galeria-katowicka  
**Analysis date:** 2026-09-22  
**Scope:** Active application code in `app/`; legacy code in `app.old/` and `app.old2/` documented where relevant.

---

## 1. Current Test State

### No Tests Exist

The repository contains **zero test files**. There are no:

- `pytest` test files (`test_*.py` or `*_test.py`) anywhere in the repo.
- `conftest.py` files (no shared test fixtures or configuration).
- `tests/` directories.
- Test configuration in `pyproject.toml` (no `[tool.pytest.ini_options]`).
- Test runner scripts or `Makefile` test targets.

A full-text search for `pytest`, `TestClient`, `httpx` (as test client), `unittest`, and `coverage` across all Python files returned no results in `app/`, `app.old/`, or `app.old2/`.

### Test Dependencies

None are declared. `pyproject.toml` (at `pyproject.toml:1-24`) lists only runtime dependencies — no `[project.optional-dependencies.dev]` or `[project.optional-dependencies.test]` group.

`uv.lock` confirms the absence:
- **No** `pytest` package entry.
- **No** `pytest-asyncio` package entry.
- **No** `pytest-mock` or `pytest-fastapi` package entry.
- **No** `coverage` or `pytest-cov` package entry.
- **No** `factory-boy` or `factory_dataclass` package entry.
- `httpx` (line 742) appears as a transitive dependency of `fastapi`, not as an explicit test dependency.

---

## 2. Recommended Test Framework

Given the technology stack, the following testing stack is recommended:

### Primary Framework: pytest

| Tool | Purpose | Why |
|------|---------|-----|
| `pytest` | Test runner | Industry standard; FastAPI documentation uses it |
| `pytest-asyncio` | Async test support | All app endpoints are `async`; all DB operations are async |
| `httpx` | Async test client | FastAPI's `TestClient` uses `httpx` under the hood; already a transitive dependency |
| `pytest-mock` | Mocking helper | Wraps `unittest.mock` with pytest fixtures |
| `coverage` / `pytest-cov` | Coverage reporting | No coverage exists today; establish baseline |

### Installation (add to `pyproject.toml`)

```toml
[project.optional-dependencies]
test = [
    "pytest",
    "pytest-asyncio",
    "pytest-mock",
    "httpx[cli]",
    "coverage[toml]",
    "pytest-cov",
]
```

### Test Configuration (add to `pyproject.toml`)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---

## 3. Recommended Test Structure

```
galeria-katowicka/
  tests/                    # Test root (not inside app/)
    conftest.py            # Shared fixtures (lifespan, client, DB session)
    __init__.py            # Makes tests a package
    test_main.py           # App startup, lifespan, router inclusion
    test_routes.py         # Endpoint tests (stream_chat, test/endpoint)
    test_auth.py           # Clerk auth, get_current_user
    test_schemas.py        # Pydantic model validation
    test_models.py         # SQLAlchemy model behavior
    test_database.py       # Engine/session factory configuration
    test_ai.py             # LLM streaming, error handling
    test_config.py         # Settings loading, env var handling
    test_user_methods.py   # UserMethods utility (app/userMethods.py)
    fixtures/
      db.py                # Database session fixture (overrides get_db)
      client.py            # FastAPI TestClient fixture
```

### Rationale for Location

Tests live at the **repo root** (alongside `app/`), not inside `app/`. This:
- Avoids interfering with `app/` as a (potential) importable package.
- Keeps test code separate from production code.
- Aligns with FastAPI and Python community conventions.

---

## 4. Key Test Targets and Strategies

### 4.1 Endpoint Tests (`tests/test_routes.py`)

**Target:** `app/routes.py` — the only active router with defined endpoints.

| Endpoint | Test Focus |
|----------|------------|
| `POST /chat/stream` | SSE streaming response format; event structure; error event on LLM failure |
| `GET /test/endpoint` | Returns user payload dict; requires auth |

**Strategy:**
- Use FastAPI `TestClient` (via `httpx`) with a test database override.
- Override `get_db` dependency (from `app/database.py:26`) to use an in-memory SQLite or a test-scoped session.
- Mock `llm_call` / `full_response` from `app/ai.py` for deterministic tests.

**Example pattern:**

```python
# tests/test_routes.py
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import override_get_db  # fixture

client = TestClient(app, raise_server_exceptions=False)

def test_stream_chat_returns_sse(override_get_db):
    response = client.post("/chat/stream", json={
        "conversation": [{"role": "user", "content": "hello"}]
    })
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
```

### 4.2 Auth Tests (`tests/test_auth.py`)

**Target:** `app/authClerk.py` — `get_current_user()`.

| Scenario | Expected |
|----------|----------|
| Valid Clerk token | Returns `AuthUser` with `user_id` and `email` |
| Invalid/expired token | Raises `HTTPException` 401 |
| Token missing `sub` claim | Raises `HTTPException` 401 |
| No `Authorization` header | Raises `HTTPException` 401 (HTTPBearer triggers) |

**Strategy:** Mock `Clerk.authenticate_request` from `clerk_backend_api` (imported at `app/authClerk.py:3`).

**Known issue to test around:** `app/routes.py:4` imports `from auth import get_current_user` — the file is `app/authClerk.py`, not `app/auth.py`. Tests should import from `app.authClerk` directly until this import bug is fixed.

### 4.3 AI/LLM Tests (`tests/test_ai.py`)

**Target:** `app/ai.py` — `llm_call()` and `full_response()`.

| Scenario | Expected Behavior |
|----------|-------------------|
| Successful stream | Yields `streamingResponse` events, then `done` event |
| LLM API error | Yields `error` event, then returns (in `llm_call`) |
| Empty response | Yields `done` with empty data |
| Partial failure in `full_response` | Yields error event, stops without `done` (per `app/ai.py:53`) |

**Strategy:** Mock `AsyncOpenAI` client from `openai` package. Use `AsyncMock` for the streaming iterator.

**Key difference between active and legacy:**
- Active `app/ai.py` (line 36-38): catches exception inside `llm_call()`, yields error event, and returns — meaning the `finally`-style `done` is NOT sent after error.
- Legacy `app.old2/ai.py` (line 24-25): uses `finally` block that always yields `done` even after errors — different behavior; do not port legacy pattern to active code.

### 4.4 Database/Session Tests (`tests/test_database.py`)

**Target:** `app/database.py` — engine, session factory, `get_db()`.

| Test | Focus |
|------|-------|
| Engine creation | Verifies `DATABASE_URL` used; pool settings applied |
| Session factory | `AsyncSessionLocal` creates `AsyncSession` instances |
| `get_db()` dependency | Yields session; closes after yield |

**Strategy:** Use a separate `DATABASE_URL_TEST` env var (e.g., `postgresql+asyncpg://test` or SQLite `sqlite+aiosqlite:///test.db`) for test isolation.

### 4.5 Schema Validation Tests (`tests/test_schemas.py`)

**Target:** `app/schemas.py` — all Pydantic models.

| Model | Test Focus |
|-------|------------|
| `AuthUser` | `user_id` (str), `email` (EmailStr) validation |
| `ChatMessage` | `role` Literal constraint; `content` min/max length |
| `ChatHistory` | `conversation` list of `ChatMessage` |
| `UserCreate` | `user_id` default via `uuid7`; required `email`/`clerk_id` |
| `UserResponse` | `model_config = ConfigDict(from_attributes=True)` — ORM compatibility |
| `SessionCreate`/`SessionResponse` | UUID + chat history + timestamp |
| `PlaceCreate`/`PlaceResponse` | Session-scoped place data |

**Important:** `app/schemas.py:10` uses `Emailstr` (typo — should be `EmailStr`). This is a runtime bug. Tests for email validation should verify and document this issue.

### 4.6 Model Tests (`tests/test_models.py`)

**Target:** `app/models.py` — SQLAlchemy ORM models.

| Model | Test Focus |
|-------|------------|
| `UserModel` | Table name `users`; UUID PK; unique `clerk_id`; auto `created_at` |
| `SessionModel` | Table name `sessions`; FK to users; JSON chat_history |
| `PlaceModel` | Table name `places`; basic fields |

**Strategy:** Use SQLAlchemy's `ModelMetadata` inspection or a test SQLite engine to verify table definitions without hitting a real database.

### 4.7 Config Tests (`tests/test_config.py`)

**Target:** `app/config.py` — `Settings` class.

| Test | Focus |
|------|-------|
| Settings load from `configs/.env` | Verifies env file path and field mapping |
| Required fields | `CLERK_PUBLIC_KEY`, `CLERK_SECRET_KEY`, `DATABASE_URL`, `OPENROUTER_API_KEY` are required |
| `extra="ignore"` | Unknown env vars do not cause errors |

**Caution:** `app/config.py:18` instantiates `Settings()` at module load. Tests that override settings need to patch the singleton or use monkeypatch on environment variables before import.

### 4.8 Utility Tests (`tests/test_user_methods.py`)

**Target:** `app/userMethods.py` (untracked) — `UserMethods.User_Exists()`.

| Scenario | Expected |
|----------|----------|
| Clerk user ID exists in DB | Returns `True` |
| Clerk user ID not found | Returns `False` |

**Note:** `UserMethods.User_Exists()` (line 5) references `AsyncSession` without importing it — this must be fixed before tests can pass.

### 4.9 Legacy Code Testing

`app.old/` and `app.old2/` are **not tested** and should **not** be tested. They are dead code (main.py is commented out, no Python process imports from these directories). Document for historical reference only.

---

## 5. Mocking Strategy

### External Service Mocks

| Service | Mock Target | Module |
|---------|-------------|--------|
| Clerk Auth | `Clerk.authenticate_request` | `clerk_backend_api` (imported in `app/authClerk.py:3`) |
| OpenRouter LLM | `AsyncOpenClient.chat.completions.create` | `openai` (imported in `app/ai.py:4`) |

### Database Mocks/Overrides

The primary strategy is **dependency injection override**, not mocking:

- `app/routes.py` uses `Depends(get_db)` — override with a test fixture that provides a session backed by SQLite or a transaction rollback pattern.
- `app/main.py:17` calls `init_db()` in lifespan — override lifespan to skip table creation in tests.

### Fixture Pattern

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import AsyncSessionLocal
from app import models

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    async with async_session() as session:
        yield session
        await session.rollback()
```

---

## 6. Coverage

### Current State

**0% coverage.** No test infrastructure exists. No `.coveragerc`, `pyproject.toml` coverage config, or HTML coverage reports.

### Recommended Coverage Targets

Set initial coverage goals once the test suite is established:

| Target | Minimum | Stretch |
|--------|---------|---------|
| Overall | 50% | 80% |
| `app/routes.py` | 70% | 90% |
| `app/ai.py` | 60% | 80% |
| `app/authClerk.py` | 70% | 90% |
| `app/schemas.py` | 90% | 100% (validation logic) |
| `app/database.py` | 50% | 70% |
| `app/models.py` | 40% | 60% |
| `app/config.py` | 60% | 80% |
| `app/init.py` | 30% | 50% |
| `app/userMethods.py` | 60% | 80% |
| Legacy (`app.old/`, `app.old2/`) | 0% | 0% (do not test) |

### Coverage Configuration (add to `pyproject.toml`)

```toml
[tool.coverage.run]
source = ["app"]
omit = ["app.old/*", "app.old2/*", "*/__pycache__/*"]

[tool.coverage.report]
fail_under = 50
show_missing = true
exclude_lines = ["pragma: no cover", "if __name__ == .__main__.", "raise NotImplementedError"]
```

---

## 7. CI/Build Integration

### Current State

**No CI pipeline exists.** The repository has:
- No GitHub Actions (no `.github/workflows/` directory).
- No GitLab CI (no `.gitlab-ci.yml`).
- No other CI configuration.
- No `Makefile` with test targets.
- No `tox.ini` or `noxfile.py`.

### Recommended CI Commands

```bash
# Install dependencies
uv sync --group test

# Run tests
uv run pytest tests/ -v --tb=short

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=term-missing --cov-report=html

# Type check (recommended, not currently enforced)
uv run pyright app/ || uv run mypy app/

# Lint (recommended, not currently enforced)
uv run ruff check app/
uv run ruff format --check app/
```

### Suggested CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with: { python-version: "3.11" }
      - run: uv sync --group test
      - run: uv run pytest tests/ -v
      - run: uv run pytest tests/ --cov=app --cov-report=xml
```

---

## 8. Test Execution Commands

Once tests are added, the primary commands will be:

```bash
# Run all tests
uv run pytest

# Run tests verbosely
uv run pytest -v --tb=long

# Run specific test file
uv run pytest tests/test_routes.py -v

# Run specific test function
uv run pytest tests/test_auth.py::test_valid_token_returns_user -v

# Run with coverage report
uv run pytest --cov=app --cov-report=term-missing

# Run with HTML coverage report
uv run pytest --cov=app --cov-report=html

# Watch mode (requires pytest-watch or similar)
uv run ptw -- -v
```

---

## 9. Testing Challenges and Considerations

1. **Settings singleton at import time** — `app/config.py:18` instantiates `Settings()` when the module is imported. Tests that need different settings must use `monkeypatch.setenv()` before the module is first imported, or patch the singleton after import.

2. **No `__init__.py` in `app/`** — The `app/` directory lacks an `__init__.py`, which means it is not a regular Python package. Tests importing from `app/` may need to add the repo root to `sys.path` or rely on `uv run` behavior which handles this.

3. **Bare imports** — `from config import settings` style imports (e.g., `app/main.py:15`) require the working directory to be `app/` or `app/` on `PYTHONPATH`. Tests should be run with `uv run` from the repo root and imports should be prefixed (`from app.config import settings`) to avoid this issue.

4. **Database dependency** — All endpoint tests that touch the database need a test database or an in-memory SQLite override. The `get_db` dependency in `app/database.py:26` must be overridden per test.

5. **Clerk SDK mocking** — `app/authClerk.py` instantiates `Clerk(bearer_auth=settings.CLERK_SECRET_KEY)` at module level (line 10). Tests need to patch `Club` or the module to avoid real Clerk API calls.

6. **OpenRouter API mocking** — `app/ai.py` creates `AsyncOpenAI` at module level (line 9). Tests should mock this client to avoid network calls and ensure deterministic behavior.

7. **SSE streaming complexity** — `app/routes.py:19` returns `EventSourceResponse` wrapping a generator. Testing SSE responses with `TestClient` requires reading the stream events, which is more complex than standard JSON responses. Consider testing `full_response()` and `llm_call()` directly (in `app/ai.py`) rather than through the HTTP layer.

8. **Untracked `app/userMethods.py`** — Must be fixed (missing `AsyncSession` import) before it can be unit tested.

---

## 10. Summary

| Aspect | Current State | Recommendation |
|--------|--------------|----------------|
| Test framework | None | Add `pytest` + `pytest-asyncio` |
| Test client | None | Use FastAPI `TestClient` (via `httpx`) |
| Mocking | None | Mock `Clerk`, `AsyncOpenAI`; override `get_db` |
| Coverage | 0% | Establish baseline, target 50% minimum |
| CI pipeline | None | Add GitHub Actions with test + coverage |
| Test files | 0 | Create `tests/` directory at repo root |
| Test config | None | Add `[tool.pytest.ini_options]` to `pyproject.toml` |
| Lint/type check | None | Add `ruff` + `pyright`/`mypy` (optional but recommended) |
| Legacy code testing | N/A | Do not test `app.old/` or `app.old2/` |
