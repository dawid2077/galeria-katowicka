# CONVENTIONS.md

**Project:** galeria-katowicka  
**Analysis date:** 2026-09-22  
**Scope:** Active application code in `app/`; legacy code in `app.old/` and `app.old2/` is documented separately where relevant.

---

## 1. Project Overview

`galeria-katowicka` is a FastAPI backend for a venue/chat application centered on cultural sites in Katowice, Poland (Muzeum Śląskie, Strefa Kultury). It provides AI-powered streaming chat via OpenRouter, Clerk-based authentication, and PostgreSQL persistence via SQLAlchemy async.

- **Active code:** `app/` — the current working application (12 Python files).
- **Legacy code:** `app.old/` and `app.old2/` — superseded iterations; not imported or executed by active code. These contain commented-out `main.py` files, book-centric models, and an in-memory `Database` class.
- **Untracked working-tree file:** `app/userMethods.py` — a utility class not yet referenced elsewhere in the active codebase.
- **Configuration:** `configs/.env`, `configs/.env.example`, `configs/config.conf`.
- **Container:** `docker-compose.yml` (PostgreSQL 18 + pgadmin).
- **Package manager:** `uv` (see `pyproject.toml`, `uv.lock`).
- **Shell environment:** `shell.nix` (Nix dev shell, Python 3.11).

---

## 2. Code Style

### Formatting and Linting

- **No formatter or linter is configured.** There is no `.black`, `.flake8`, `ruff`, `pylint`, `mypy.ini`, or `pyproject.toml` `[tool.*]` section. The project relies entirely on manual discipline.
- `pyproject.toml` contains only a minimal `[project]` table with dependency declarations — no build-system, no tool configuration.
- **Line length:** No enforced limit. Lines routinely exceed 88 characters (e.g., `app/schemas.py:10` `email : Emailstr` is a typo, not style).
- **Type hints:** Inconsistent. Some function signatures are annotated (e.g., `app/database.py:26` `async def get_db() -> AsyncGenerator[AsyncSession, None]`), others are not (e.g., `app/userMethods.py:5` `async def User_Exists(db: AsyncSession, clerk_user_id)` — `clerk_user_id` is untyped).

### Import Style

- **Bare imports (no package prefix).** All modules in `app/` import each other using bare names, not `app.config`, `app.database`, etc. This means the `app/` directory must be on `PYTHONPATH` or the process must be launched from within `app/`.
  - Example: `app/main.py:15` `from config import settings`
  - Example: `app/main.py:17` `from init import init_db`
  - Example: `app/main.py:18` `from routes import router as book_router`
  - **This is fragile and not idiomatic for a package.** Recommended fix: prefix with `from app.config import settings`, or add `__init__.py` to `app/` and run as a module.
- **Standard library and third-party imports follow conventional ordering** (stdlib, then third-party, then local), but there is no enforced sorting within groups.

### Comment and Docstring Conventions

- Comments are informal and often in English with occasional Polish (e.g., `app/kubernetes.py` uses Polish comments like "Sprawdza, czy aplikacja ma połączenie").
- TODOs and inline notes are common and use `# TODO`, `#!`, `#*`, and `#?` prefixes inconsistently.
- Docstrings are sparse; only `app/ai.py:43` `full_response()` has a docstring.
- Many comments in `app.old/` and `app.old2/` are outdated or reference deleted functionality.

---

## 3. Naming Conventions

### Files and Modules

| Pattern | Location | Example |
|---------|----------|---------|
| snake_case Python modules | `app/` | `routes.py`, `schemas.py`, `database.py`, `config.py`, `main.py`, `ai.py`, `init.py`, `kubernetes.py`, `crud.py` |
| CamelCase utility classes | `app/` | `app/userMethods.py` → `class UserMethods` |
| `app.old/`, `app.old2/` | Legacy | Mirror `app/` structure but contain superseded code (book models, in-memory DB) |

### Classes and Functions

- **Class names:** PascalCase (e.g., `class Settings` in `app/config.py:5`, `class CRUD` in `app.old/crud.py:11`, `class Database` in `app.old/old_Database.py:3`).
- **Function names:** snake_case (e.g., `async def stream_chat`, `async def get_db`, `async def init_db`). Exception: `app/userMethods.py:5` `User_Exists` — starts with capital (non-standard).
- **Constants:** ALL_CAPS for settings fields (e.g., `CLERK_PUBLIC_KEY`, `CLERK_SECRET_KEY`, `DATABASE_URL`, `OPENROUTER_API_KEY` in `app/config.py:6-9`).
- **SQLAlchemy models:** PascalCase with `Model` suffix (e.g., `UserModel`, `SessionModel`, `PlaceModel` in `app/models.py`). Legacy models omit suffix (e.g., `Book_table`, `Author_table` in `app.old/models.py`).

### Pydantic Schemas

- Suffix pattern: `*Create`, `*Response` (e.g., `UserCreate`, `UserResponse`, `SessionCreate`, `SessionResponse`, `PlaceCreate`, `PlaceResponse` in `app/schemas.py`).
- Legacy schemas use different naming: `Book`, `Author`, `BookUpdate`, `BookNotFound` (in `app.old/schemas.py`, `app.old2/schemas.py`).

---

## 4. Architecture Patterns

### Active Application (`app/`)

The active app follows a layered structure:

```
app/
  main.py        — FastAPI app factory, lifespan, router inclusion
  routes.py      — API endpoint definitions (APIRouter)
  schemas.py     — Pydantic models (request/response validation)
  models.py      — SQLAlchemy ORM models
  database.py    — Async engine, session factory, get_db() dependency
  config.py      — Pydantic Settings (env-driven)
  ai.py          — OpenRouter streaming LLM integration
  authClerk.py   — Clerk JWT authentication middleware
  init.py        — Database table initialization (lifespan)
  kubernetes.py  — K8s healthcheck skeleton (incomplete, references undefined app/db)
  userMethods.py — Untracked utility class (UserMethods)
  context/       — Venue documentation (MuzeumŚląskie, StrefaKultury)
  docs/          — Planning notes (MVP, auth, frontend)
```

Key patterns:
- **FastAPI lifespan:** `app/main.py:21-24` uses `@asynccontextmanager` for startup (calls `init_db()`).
- **Dependency injection:** Database sessions via `Depends(get_db)` in routes (e.g., `app/routes.py:25`).
- **Streaming responses:** SSE via `sse_starlette.sse.EventSourceResponse` (e.g., `app/routes.py:19`).
- **Settings:** Single `settings` singleton instantiated at module load in `app/config.py:18`.

### Legacy Application (`app.old/`, `app.old2/`)

- Both directories contain earlier versions of the same codebase, primarily book/author focused (CRUD on `Book_table`, `Author_table`).
- `app.old/main.py` and `app.old2/main.py` are entirely commented out (wrapped in triple-quoted strings), so they are dead code.
- `app.old/crud.py` and `app.old2/crud.py` contain a `CRUD` class with static methods (`post_book`, `get_by_id`, `delete_book`, etc.) — a pattern that was replaced in the active app by direct SQLAlchemy usage in routes.
- `app.old/old_Database.py` defines an in-memory `Database` class (dict-backed) — an early prototype before SQLAlchemy was adopted.
- `app.old/kubernetes.py` and `app.old2/kubernetes.py` are identical skeletons with undefined references (`app`, `Response`, `check_db_connection`, `database`) — they will not execute.

### `app/userMethods.py` (Untracked)

- Defines `UserMethods` class with a single static method `User_Exists`.
- References `AsyncSession` type without importing it (would raise `NameError` at runtime).
- Not imported or used by any active module.

---

## 5. Error Handling

### Active Code (`app/`)

- **`app/ai.py:36-38`** — `llm_call()` catches generic `Exception`, logs via structlog, yields an error event, and returns. This is the primary error boundary for LLM streaming.
- **`app/ai.py:57-58`** — `full_response()` catches exceptions and yields error events.
- **`app/authClerk.py:46-52`** — `get_current_user()` re-raises `HTTPException` and wraps all other exceptions in a 401. This is idiomatic FastAPI error handling.
- **`app/main.py`** — No global exception handler is registered. Unhandled exceptions will produce FastAPI's default 500 response.
- **`app/routes.py`** — The `/test/endpoint` handler has no error handling.

### Legacy Code (`app.old/`, `app.old2/`)

- `app.old/crud.py` returns `False` or `None` on failures (e.g., `delete_book` returns `False` if book not found). No exceptions raised.
- `app.old/schemas.py` defines `BookNotFound(Exception)` but it is never raised in the codebase.

### Conventions

- No consistent error response schema. `app/schemas.py` has a `Message(BaseModel)` with a `detail` field, but not all error responses use it.
- No custom exception handler registered in active FastAPI app.

---

## 6. Configuration Management

- **Primary config:** `app/config.py` — Pydantic `BaseSettings` reading from `configs/.env` (env_file path is relative to the CWD when `settings` is imported).
- **Environment file:** `configs/.env` — contains actual API keys (should be in `.gitignore` and not committed; it is NOT in `.gitignore` despite `.gitignore` line 1 listing `.env` — the file is `configs/.env`, not `.env`).
- **Example config:** `configs/.env.example` — documents expected variables. Contains a typo: `CERK_PUBLIC_KEY` instead of `CLERK_PUBLIC_KEY` (line 3).
- **Extra field handling:** `app/config.py:14` sets `extra="ignore"` — unknown env vars are silently ignored.
- **Legacy config:** `app.old/config.py` and `app.old2/config.py` — similar `BaseSettings` but read from `../configs/.env` (one level up) and include `VENUE_NAME` and `MODEL` settings not present in active config.

### Settings Fields Comparison

| Field | Active (`app/config.py`) | Legacy (`app.old/config.py`) |
|-------|-------------------------|------------------------------|
| `CLERK_PUBLIC_KEY` | ✓ | ✗ |
| `CLERK_SECRET_KEY` | ✓ | ✗ |
| `DATABASE_URL` | ✓ | ✓ |
| `OPENROUTER_API_KEY` | ✓ | ✓ |
| `VENUE_NAME` | ✗ | ✓ (default "Galeria Katowicka") |
| `MODEL` | ✗ | ✓ (in app.old2 only) |

---

## 7. Database Patterns

- **Engine:** `app/database.py:11-19` — `create_async_engine` with connection pool settings: `pool_size=2`, `max_overflow=3`, `pool_timeout=10`, `pool_pre_ping=True`.
- **Session factory:** `app/database.py:21-25` — `async_sessionmaker` with `expire_on_commit=False`.
- **Table creation:** `app/init.py:6-8` — `init_db()` calls `Base.metadata.create_all` on startup via lifespan. No migration tool (no Alembic).
- **Active models:** `app/models.py` — `UserModel`, `SessionModel`, `PlaceModel` with UUID primary keys, timezone-aware datetimes.
- **Legacy models:** `app.old/models.py` — `Author_table`, `Book_table` (snake_case naming, relationship back_populates).

---

## 8. Known Issues and Anti-Patterns

1. **Bare imports** — all local imports lack package prefix (`from config` not `from app.config`). Will break if `app/` is used as a proper package.
2. **Import bug** — `app/routes.py:4` imports `from auth import get_current_user` but the file is named `authClerk.py`, not `auth.py`. This will fail at import time.
3. **Untracked `app/userMethods.py`** — references `AsyncSession` without importing it; not integrated into the app.
4. **Kubernetes skeleton is broken** — `app/kubernetes.py` references undefined names (`app`, `Response`, `check_db_connection`, `database`) and will not execute.
5. **Secret exposure** — `configs/.env` contains real API keys and is not in `.gitignore` (`.gitignore` only covers `.env`, not `configs/.env`).
6. **Typo in config** — `app/schemas.py:10` uses `Emailstr` (lowercase `str`) instead of `EmailStr`; this will cause a Pydantic validation error at runtime.
7. **Duplicate dependency** — `pyproject.toml` lists both `clerk-backend-api` (line 21) and `clerk_backend-api` (line 23) — same package, different hyphen/underscore variants.
8. **Inconsistent model naming** — active models use `PascalCaseModel` suffix, legacy models use `_table` suffix.
9. **No logging** in active app — `app/ai.py` uses structlog but the rest of active code does not. Legacy code (`app.old/crud.py`, `app.old2/crud.py`) also used structlog.
10. **Hardcoded ports/hosts** — `app/authClerk.py:21` hardcodes `authorized_parties=["http://localhost:3000", "https://your-app.com"]`.

---

## 9. Dependency Summary (from `pyproject.toml` and `uv.lock`)

### Core Runtime Dependencies

| Package | Purpose | Version (uv.lock) |
|---------|---------|-------------------|
| `fastapi` | Web framework | (resolved in lock) |
| `uvicorn` | ASGI server | (resolved in lock) |
| `openai` | OpenRouter client | (resolved in lock) |
| `psycopg[binary]` | PostgreSQL driver | (resolved in lock) |
| `sqlalchemy` | ORM | (resolved in lock) |
| `pydantic-settings` | Settings management | (resolved in lock) |
| `sse-starlette` | SSE streaming | (resolved in lock) |
| `structlog` | Structured logging | (resolved in lock) |
| `asyncpg` | Async PostgreSQL | (resolved in lock) |
| `clerk-backend-api` | Clerk auth SDK | (resolved in lock) |
| `pyjwt` | JWT handling | (resolved in lock) |
| `uuid-extension` | UUID7 generation | (resolved in lock) |
| `python-dotenv` | Env file loading | (resolved in lock) |

### Dev/Test Dependencies

- **None declared.** `pyproject.toml` has no `[project.optional-dependencies]` or `[tool.pytest.ini_options]`. `uv.lock` contains no `pytest`, `pytest-asyncio`, `httpx` (test client), `coverage`, or `coverage-python` packages (only `httpx` as a transitive dependency of FastAPI, and `httpx2` as an unrelated package).

---

## 10. Build and Run Commands

From `shell.nix:28-29`:

```bash
uv sync          # Install dependencies
uv run fastapi dev  # Run development server
```

From `docker-compose.yml`:

```bash
docker compose up -d  # Start PostgreSQL and pgadmin
```

**No CI/CD pipeline exists.** No GitHub Actions, GitLab CI, or similar configuration file found. No `Makefile`, no `tox.ini`, no `justfile`.

---

## 11. Legacy Code Directory Summary

### `app.old/` (11 files)
- Superseded book/author-focused version of the app.
- `main.py` is entirely commented out (dead code).
- Contains `old_Database.py` (in-memory dict-based DB prototype).
- Contains `crud.py` with `CRUD` class (static methods for book CRUD).
- `routes.py` has book endpoints (`/book`, `/book/{book_uuid}`) but imports `EventSourceResponse` and `llm_call` without importing `ai.py` — would fail.
- `request_types/post.md` — HTTP request examples for book API.

### `app.old2/` (12 files)
- Further iteration, closer to active structure but still book-focused.
- `main.py` is entirely commented out (dead code).
- `routes.py` only has `/chat/stream` endpoint (book routes removed).
- `ai.py` present with streaming LLM logic (slightly different from active `app/ai.py`).
- `config.py` includes `MODEL` setting and `VENUE_NAME` (active config does not).
- `request_types/post.md` is empty (0 lines).

Both legacy directories are **not on the Python path** and are **not imported** by active code. They serve as historical reference only.
