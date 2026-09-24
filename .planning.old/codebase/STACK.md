---
last_mapped_commit: 2ab2e51140e076aa6f8585eb8cdf2b07d40351cb
last_mapped_at: 2026-09-24
---
<!-- refreshed: 2026-09-24 -->

# Technology Stack

**Analysis Date:** 2026-09-24

## Languages

**Primary:**

- Python 3.11+ - Backend API (`pyproject.toml` requires-python >=3.11)

**Secondary:**

- SQL (PostgreSQL dialect) - Database queries via SQLAlchemy ORM

## Runtime

**Environment:**

- Python 3.11 (venv at `.venv/`)

**Package Manager:**

- uv (modern Python package manager)
- Lockfile: `uv.lock` present (445KB)

## Frameworks

**Core:**

- FastAPI 0.110+ - Async web framework for building APIs
  - Location: `app/main.py`, `app/routes.py`
- Uvicorn - ASGI server (included in `fastapi[standard]`)
- Pydantic v2 / Pydantic Settings - Data validation and settings management
  - Location: `app/config.py`, `app/schemas.py`

**Database/ORM:**

- SQLAlchemy 2.0 (async) - Async ORM with asyncpg driver
  - Location: `app/database.py`, `app/models.py`, `app/init.py`
- asyncpg - Async PostgreSQL driver
- psycopg2-binary / psycopg[binary] - PostgreSQL adapters

**AI/ML Integration:**

- OpenAI Python SDK (AsyncOpenAI) - LLM API client
  - Location: `app/ai.py`
- OpenRouter - LLM gateway (configured via base_url)

**Authentication:**

- Clerk Backend API (`clerk-backend-api` / `clerk_backend-api`) - JWT verification
  - Location: `app/authClerk.py`

**Utilities:**

- structlog - Structured logging
  - Location: `app/ai.py`, `app/userMethods.py`
- uuid6 / uuid-extension - UUID v7 generation
  - Location: `app/models.py`, `app/schemas.py`, `app/userMethods.py`
- python-dotenv - Environment variable loading
- sse-starlette - Server-Sent Events for streaming responses
  - Location: `app/routes.py`
- PyJWT - JWT handling (dependency of Clerk)

**Testing:**

- Not detected (no test files in `app/`, no pytest/vitest config)

**Build/Dev:**

- No build step (pure Python)
- Development: `uvicorn app.main:app --reload` (inferred)

## Key Dependencies

**Critical:**

- fastapi - Web framework foundation
- sqlalchemy + asyncpg - Database layer
- clerk-backend-api - Authentication provider integration
- openai - LLM provider integration (via OpenRouter)
- structlog - Observability

**Infrastructure:**

- pydantic-settings - Configuration management (`app/config.py`)
- sse-starlette - Real-time streaming (`app/routes.py:18-20`)
- uv - Fast Python package installer (lockfile present)

## Configuration

**Environment:**

- Settings via `pydantic_settings.BaseSettings` (`app/config.py:5-16`)
- Loads from `configs/.env` (committed `.env.example` exists)
- Config class: `Settings` with `model_config = SettingsConfigDict(env_file="configs/.env", extra="ignore")`

**Required Settings:**
| Setting | Purpose |
|---------|---------|
| `CLERK_PUBLIC_KEY` | Clerk public key (may be unused) |
| `CLERK_SECRET_KEY` | Clerk secret key for JWT verification |
| `DATABASE_URL` | PostgreSQL async connection string (`postgresql+asyncpg://...`) |
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM access |
| `AUTHORIZED_PARTIES` | List of allowed JWT audiences (origins) |

**Build:**

- `pyproject.toml` - Project metadata and dependencies
- `uv.lock` - Reproducible dependency lockfile
- `docker-compose.yml` - Local development infrastructure

## Platform Requirements

**Development:**

- Python 3.11+
- uv (recommended) or pip
- PostgreSQL 18 (via Docker Compose)
- Clerk account for authentication

**Production:**

- Containerized deployment (Docker)
- PostgreSQL database
- Clerk authentication service
- OpenRouter API access
- ASGI server (Uvicorn/Gunicorn)
- Reverse proxy (nginx/Traefik) recommended

---

*Stack analysis: 2026-09-24*
