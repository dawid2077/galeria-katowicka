# Technology Stack

**Analysis Date:** 2026-09-22

## Scope

**Active application:** `app/` is the current backend working tree. It is the directory selected by the Nix development shell and contains the current FastAPI entry point, Clerk authentication module, OpenRouter client, SQLAlchemy models, and route definitions (`shell.nix:26`, `app/main.py:25`, `app/authClerk.py:10`, `app/ai.py:9`, `app/database.py:11`). The untracked `app/userMethods.py` is part of the current working tree but is not imported by the active application (`app/userMethods.py:1`, `app/routes.py:1`).

**Legacy application:** `app.old2/` is an archived chat/OpenRouter iteration. Its FastAPI application body is entirely inside a triple-quoted string, and its route module contains only the streaming chat endpoint (`app.old2/main.py:2`, `app.old2/routes.py:13`). `app.old/` is an older archived book/catalog iteration with SQLAlchemy author/book models and CRUD code; its FastAPI application body is also commented out (`app.old/main.py:2`, `app.old/models.py:15`, `app.old/crud.py:11`). Neither legacy directory is referenced by `pyproject.toml`, `shell.nix`, Docker Compose, or the active `app/` modules (`pyproject.toml:1`, `shell.nix:26`, `docker-compose.yml:1`).

## Languages

**Primary:**
- Python 3.11 or newer - all executable application, persistence, authentication, AI client, and configuration code is Python (`pyproject.toml:4`, `app/main.py:1`, `app/database.py:1`, `app/authClerk.py:1`, `app/ai.py:1`).
- Python type hints and Pydantic models are used throughout the active backend (`app/models.py:13`, `app/schemas.py:8`, `app/userMethods.py:5`).

**Secondary:**
- Markdown - product notes, venue context, and legacy request examples are stored as Markdown rather than executable code (`app/docs/mvp.md:1`, `app/context/MuzeumSlaskie.md:1`, `app/context/StrefaKultury.md:1`, `app.old/request_types/post.md:1`).
- YAML - Docker Compose defines local PostgreSQL and pgAdmin infrastructure (`docker-compose.yml:1`).
- Nix - `shell.nix` defines the Python development environment (`shell.nix:1`).

**Not detected:**
- No JavaScript or TypeScript source, Astro configuration, or frontend package manifest exists. The only Astro artifact is `astro/here_frontend.md`, which contains no implementation (`astro/here_frontend.md:1`). The repository therefore has no active frontend runtime despite the future Astro note in `app/docs/frontend.md:1`.

## Runtime

**Environment:**
- CPython 3.11 is the pinned development interpreter in the Nix shell; the project metadata permits Python 3.11 and newer (`shell.nix:7`, `pyproject.toml:4`).
- The Nix shell also supplies `uv`, OpenSSL, PostgreSQL client tooling, and the C/C++ runtime needed by Python wheels (`shell.nix:8`, `shell.nix:11`, `shell.nix:13`, `shell.nix:14`).
- The documented development flow changes into `app/`, runs `uv sync`, and starts FastAPI with `uv run fastapi dev` (`shell.nix:26`, `shell.nix:28`, `shell.nix:29`).

**HTTP runtime:**
- FastAPI 0.141.1 provides the ASGI application and routing (`uv.lock:341`, `app/main.py:25`).
- Starlette 1.6.0 is the ASGI foundation resolved for FastAPI and SSE responses (`uv.lock:1641`, `app/routes.py:6`).
- Uvicorn 0.52.3 is the declared ASGI server and is included by the FastAPI standard extra (`pyproject.toml:9`, `uv.lock:1747`).
- The application uses an async lifespan that initializes the database schema before serving requests (`app/main.py:21`, `app/init.py:6`).

**Package manager:**
- `uv` is the package manager and lockfile generator (`shell.nix:8`, `uv.lock:1`).
- `uv.lock` is present, uses lock format version 1/revision 3, and requires Python 3.11 or newer (`uv.lock:1`, `uv.lock:3`).
- `pyproject.toml` declares unpinned direct dependencies, so the lockfile is the reproducible version source (`pyproject.toml:6`, `uv.lock:370`).

## Frameworks

**Core:**
- FastAPI - HTTP API, dependency injection, request validation, OpenAPI metadata, and bearer-token dependencies (`app/main.py:25`, `app/routes.py:14`, `app/authClerk.py:9`).
- Pydantic 2.13.4 - request/response schemas, email validation, UUID fields, and settings validation (`uv.lock:1155`, `app/schemas.py:5`, `app/config.py:1`).
- SQLAlchemy 2.0.52 with the async extension - declarative models, async engine, session factory, and schema creation (`uv.lock:1586`, `app/database.py:3`, `app/models.py:11`).
- OpenAI Python SDK 3.2.0 - asynchronous chat-completions client redirected to OpenRouter (`uv.lock:984`, `app/ai.py:4`, `app/ai.py:9`).
- Clerk Backend API 7.0.0 - bearer-token request authentication and JWT verification (`uv.lock:208`, `app/authClerk.py:3`, `app/authClerk.py:10`).
- SSE Starlette 3.4.8 - `text/event-stream` response handling for streamed model output (`uv.lock:1628`, `app/routes.py:6`, `app/routes.py:21`).

**Data and identity:**
- Asyncpg 0.31.0 is the async PostgreSQL driver used by the SQLAlchemy URL (`uv.lock:53`, `app/database.py:11`).
- Psycopg 3.3.6 with binary extras is declared alongside asyncpg (`pyproject.toml:14`, `uv.lock:1003`).
- Psycopg2-binary 2.9.13 is also declared, although no active module imports psycopg2 (`pyproject.toml:22`, `uv.lock:1083`).
- PyJWT 2.14.0 is a transitive/directly declared JWT dependency used by the Clerk authentication stack (`pyproject.toml:20`, `uv.lock:1313`, `app/authClerk.py:3`).
- UUID Extension 0.2.0 supplies the `uuid7` default factory used by active schemas (`uv.lock:1738`, `app/schemas.py:30`).
- Structlog 26.1.0 is the active AI client's logging facade (`uv.lock:1654`, `app/ai.py:5`, `app/ai.py:37`).

**Testing:**
- No test framework, test runner configuration, test files, or CI test command is present. The repository contains no `test` or `spec` files (`pyproject.toml:1`, `.planning/codebase/TESTING.md:1`).

**Build/development:**
- Nix provides the local Python/PostgreSQL development shell (`shell.nix:3`).
- Docker Compose provides only local PostgreSQL and pgAdmin services; it does not define or build the backend (`docker-compose.yml:1`).
- Astro is documentation-only at present; there is no `package.json`, `astro.config.*`, `src/`, or frontend dependency lockfile (`astro/here_frontend.md:1`, `app/docs/frontend.md:1`).

## Key Dependencies

| Dependency | Resolved version | Role and evidence |
|---|---:|---|
| `fastapi` | 0.141.1 | Active ASGI API framework (`uv.lock:341`, `app/main.py:25`). |
| `starlette` | 1.6.0 | ASGI and response foundation (`uv.lock:1641`, `app/routes.py:6`). |
| `uvicorn` | 0.52.3 | ASGI server (`uv.lock:1747`, `pyproject.toml:9`). |
| `pydantic` | 2.13.4 | Schemas and settings (`uv.lock:1155`, `app/schemas.py:5`, `app/config.py:1`). |
| `pydantic-settings` | 2.15.0 | Environment-backed settings (`uv.lock:1290`, `app/config.py:2`). |
| `sqlalchemy` | 2.0.52 | Async ORM and metadata (`uv.lock:1586`, `app/models.py:5`). |
| `asyncpg` | 0.31.0 | Async PostgreSQL driver (`uv.lock:53`, `app/database.py:11`). |
| `openai` | 3.2.0 | OpenRouter chat client (`uv.lock:984`, `app/ai.py:4`). |
| `clerk-backend-api` | 7.0.0 | Clerk token verification (`uv.lock:208`, `app/authClerk.py:3`). |
| `sse-starlette` | 3.4.8 | Streaming HTTP responses (`uv.lock:1628`, `app/routes.py:6`). |
| `structlog` | 26.1.0 | AI error logging (`uv.lock:1654`, `app/ai.py:8`). |
| `uuid-extension` | 0.2.0 | UUIDv7 defaults (`uv.lock:1738`, `app/schemas.py:30`). |
| `email-validator` | 2.3.0 | Pydantic email fields (`uv.lock:328`, `app/schemas.py:5`). |
| `greenlet` | 3.5.5 | SQLAlchemy async support (`uv.lock:586`, `app/database.py:3`). |

## Configuration

**Environment:**
- Active settings require `CLERK_PUBLIC_KEY`, `CLERK_SECRET_KEY`, `DATABASE_URL`, and `OPENROUTER_API_KEY` (`app/config.py:5`, `app/config.py:6`, `app/config.py:7`, `app/config.py:8`, `app/config.py:9`).
- `app/config.py` loads `configs/.env` relative to the process working directory and ignores extra keys (`app/config.py:11`, `app/config.py:12`, `app/config.py:14`). Because the documented shell changes into `app/`, that relative path does not point to the repository-level `configs/.env` without a different working directory (`shell.nix:26`, `configs/.env`).
- `MODEL` is read by the active AI client but is not declared in active `Settings`; access therefore fails unless supplied through a mechanism outside the declared schema (`app/ai.py:21`, `app/config.py:5`).
- `VENUE_NAME` exists only in `configs/config.conf` and is not loaded by the active settings class (`configs/config.conf:1`, `app/config.py:5`).
- The ignored `configs/.env` and the example file `configs/.env.example` provide local environment configuration; no secret values are reproduced here (`.gitignore:1`, `configs/.env`, `configs/.env.example`).

**Application configuration:**
- The active FastAPI app is titled `FastAPI Backend`, reports version `0.1.0`, and includes the router from `app/routes.py` (`app/main.py:25`, `app/main.py:28`, `app/main.py:33`).
- No CORS middleware, rate limiting, request-size middleware, or production-specific settings are configured in the active app (`app/main.py:25`, `app/routes.py:14`).
- The legacy configuration files use different environment paths and defaults and must not be copied into the active app without reconciliation (`app.old/config.py:10`, `app.old2/config.py:10`).

## Platform Requirements

**Development:**
- Python 3.11+, `uv`, OpenSSL, PostgreSQL tooling, and a C/C++ runtime are supplied by `shell.nix` (`shell.nix:4`, `shell.nix:7`, `shell.nix:8`, `shell.nix:11`, `shell.nix:13`, `shell.nix:14`).
- Local PostgreSQL 18 and pgAdmin are available through Docker Compose on their declared development ports (`docker-compose.yml:2`, `docker-compose.yml:3`, `docker-compose.yml:15`, `docker-compose.yml:16`).
- The active backend is not containerized by the Compose file; there is no backend service, Dockerfile, healthcheck, or application environment mapping (`docker-compose.yml:1`).

**Production:**
- No production hosting target, container image, process manager configuration, migration strategy, or CI/CD pipeline is defined (`pyproject.toml:1`, `docker-compose.yml:1`, `.github/`).
- `app/kubernetes.py` is an incomplete skeleton rather than a runnable Kubernetes integration; it references undefined application objects and database helpers (`app/kubernetes.py:1`, `app/kubernetes.py:4`, `app/kubernetes.py:12`, `app/kubernetes.py:26`).
- The active application currently has import and runtime defects that prevent treating the documented startup command as a verified production entry point: `app/routes.py` imports missing `auth` and `crud` modules, `app/schemas.py` references `Emailstr` instead of `EmailStr`, `app/ai.py` reads an undeclared `MODEL`, and the test endpoint contains an undefined attribute (`app/routes.py:4`, `app/routes.py:5`, `app/schemas.py:10`, `app/ai.py:21`, `app/routes.py:28`).

## Dependency and Runtime Notes

- `pyproject.toml` lists both `fastapi` and `fastapi[standard]`; the lock resolves one FastAPI package with the standard extra (`pyproject.toml:7`, `pyproject.toml:8`, `uv.lock:357`).
- `pyproject.toml` lists both spellings `clerk-backend-api` and `clerk_backend-api`; the lock normalizes this to one Clerk package (`pyproject.toml:21`, `pyproject.toml:23`, `uv.lock:208`).
- Both psycopg 3 and psycopg2-binary are installed, while active database code uses SQLAlchemy's async interface and asyncpg (`pyproject.toml:14`, `pyproject.toml:22`, `app/database.py:3`).
- No dependency in the active application provides database migrations; schema creation is limited to `Base.metadata.create_all()` at startup (`app/init.py:6`, `app/init.py:8`).
- No frontend package manager or Astro runtime is configured; `astro/here_frontend.md` is a placeholder (`astro/here_frontend.md:1`).

---

*Stack analysis: 2026-09-22*
