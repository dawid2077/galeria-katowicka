---
last_mapped_commit: 2ab2e51140e076aa6f8585eb8cdf2b07d40351cb
last_mapped_at: 2026-09-24
---
<!-- refreshed: 2026-09-24 -->

# Directory Structure

**Analysis Date:** 2026-09-24

## Repository Root Layout

```
galeria-katowicka/
├── app/                    # Active FastAPI backend
│   ├── __pycache__/
│   ├── config.py          # Pydantic Settings (env-driven)
│   ├── database.py        # Async SQLAlchemy engine & session factory
│   ├── init.py            # Database table initialization (lifespan)
│   ├── main.py            # FastAPI app factory, lifespan, router inclusion
│   ├── models.py          # SQLAlchemy ORM models
│   ├── routes.py          # API endpoint definitions (APIRouter)
│   ├── schemas.py         # Pydantic models (request/response validation)
│   ├── ai.py              # OpenRouter streaming LLM integration
│   ├── authClerk.py       # Clerk JWT authentication middleware
│   ├── userMethods.py     # User sync utility (untracked working-tree file)
│   ├── monitoring.py      # Placeholder for health check scheduling
│   ├── kubernetes.py      # K8s healthcheck skeleton (incomplete)
│   ├── context/           # Venue documentation (Markdown)
│   │   ├── MuzeumSlaskie.md
│   │   └── StrefaKultury.md
│   └── docs/              # Planning notes
│       ├── auth.md
│       ├── connecting_other_sites.md
│       ├── frontend.md
│       ├── mvp.md
│       ├── test.md
│       └── user_auth.md
├── app.old/               # Legacy: book/catalog iteration (dead code)
├── app.old2/              # Legacy: chat/OpenRouter iteration (dead code)
├── app_future/            # Legacy: empty placeholder
├── astro/                 # Future frontend (placeholder only)
│   └── here_frontend.md
├── configs/               # Configuration files
│   ├── .env               # Actual secrets (gitignored)
│   ├── .env.example       # Environment template
│   └── config.conf        # Venue name config (not loaded by active app)
├── .planning/             # GSD planning artifacts
│   ├── codebase/          # Codebase map (this file's location)
│   └── onboarding/
├── .git/
├── .gitignore
├── docker-compose.yml     # Local PostgreSQL + pgAdmin
├── LICENSE
├── pyproject.toml         # Project metadata & dependencies
├── shell.nix              # Nix development shell
├── uv.lock                # uv lockfile
└── .venv/                 # Python virtual environment
```

## Active Application (`app/`)

### Module Organization

The active backend follows a flat module structure within `app/`:

| Module | Purpose | Key Exports |
|--------|---------|-------------|
| `main.py` | Application factory | `app` (FastAPI instance) |
| `routes.py` | API routes | `router` (APIRouter) |
| `schemas.py` | Pydantic schemas | `ChatHistory`, `ChatMessage`, `UserResponse`, `SessionCreate`, `SessionResponse`, `PlaceCreate`, `PlaceResponse`, `AuthUser`, `Message` |
| `models.py` | SQLAlchemy models | `Base`, `UserModel`, `SessionModel`, `PlaceModel` |
| `database.py` | DB connection | `engine`, `AsyncSessionLocal`, `get_db()` |
| `config.py` | Settings | `settings` (Settings singleton) |
| `ai.py` | LLM integration | `llm_call()`, `full_response()` |
| `authClerk.py` | Authentication | `get_current_user()`, `auth_user` |
| `userMethods.py` | User utilities | `UserMethods.get_or_create_user()` |
| `init.py` | DB init | `init_db()` |
| `monitoring.py` | Health monitoring | (placeholder) |
| `kubernetes.py` | K8s probes | (incomplete) |

### Import Conventions

**Current pattern (fragile):**

```python

# Bare imports — requires running from app/ directory

from config import settings
from init import init_db
from routes import router as main_router
```

**Recommended pattern:**

```python

# Package-relative imports (requires app/__init__.py)

from app.config import settings
from app.init import init_db
from app.routes import router as main_router
```

### Directory Conventions

| Pattern | Example |
|---------|---------|
| Python modules | `snake_case.py` |
| SQLAlchemy models | `PascalCaseModel` suffix |
| Pydantic schemas | `*Create`, `*Response` suffix |
| Utility classes | `PascalCase` + `Methods` suffix |
| Context docs | `PascalCase.md` |
| Planning docs | `snake_case.md` |

## Legacy Code Directories

### `app.old/` (11 files)

- Superseded book/author-focused version
- `main.py` entirely commented out (dead code)
- Contains `old_Database.py` (in-memory prototype)
- Contains `crud.py` with `CRUD` class
- Not imported by active code

### `app.old2/` (12 files)

- Further iteration, closer to active structure
- `main.py` entirely commented out (dead code)
- Only `/chat/stream` endpoint in routes
- `config.py` includes `MODEL` and `VENUE_NAME` settings
- Not imported by active code

### `app_future/` 

- Empty directory (22 bytes)

## Future Frontend (`astro/`)

### Current State

- Single placeholder file: `here_frontend.md`
- No `package.json`, `astro.config.*`, `src/`, or lockfile
- Documented as future Astro + spec-driven development in `app/docs/frontend.md`

## Configuration Directory (`configs/`)

| File | Purpose | Loaded By |
|------|---------|-----------|
| `.env` | Actual API keys, secrets | `app/config.py` (via `env_file="configs/.env"`) |
| `.env.example` | Template for required vars | Human reference |
| `config.conf` | `VENUE_NAME=Galeria Katowicka` | Not loaded by active `Settings` |

## Key File Relationships

### Dependency Graph

```
app/main.py
  ├─→ app/routes.py
  │    ├─→ app/ai.py
  │    ├─→ app/authClerk.py
  │    │    └─→ app/userMethods.py
  │    └─→ app/schemas.py
  ├─→ app/init.py
  │    └─→ app/models.py
  └─→ app/config.py
```

### Configuration Flow

```
configs/.env
      ↓
app/config.py:Settings (singleton at module load)
      ↓
app/database.py → engine, AsyncSessionLocal
      ↓
app/authClerk.py → Clerk client
app/ai.py → AsyncOpenAI client
app/routes.py → Depends(get_db), Depends(auth_user)
```

## Naming Conventions Summary

| Element | Convention | Examples |
|---------|------------|----------|
| Python files | `snake_case.py` | `authClerk.py`, `userMethods.py` |
| SQLAlchemy models | `PascalCaseModel` | `UserModel`, `SessionModel` |
| Pydantic schemas | `*Create` / `*Response` | `SessionCreate`, `UserResponse` |
| Utility classes | `PascalCase` + `Methods` | `UserMethods` |
| Settings fields | `UPPER_SNAKE_CASE` | `CLERK_SECRET_KEY` |
| Database tables | `snake_case` plural | `users`, `sessions`, `places` |
| UUID fields | `*_id` with `Uuid` type | `user_id`, `session_id`, `clerk_id` |
| Timestamp fields | `created_at` with timezone | `created_at: Mapped[datetime]` |

## Onboarding Entry Points

### Development Commands (from `shell.nix`)

```bash
cd app/
uv sync              # Install dependencies
uv run fastapi dev   # Run development server
```

### Docker Infrastructure

```bash
docker compose up -d  # Start PostgreSQL + pgAdmin
```

### Health Endpoints

- `GET /health/live` — Liveness (no dependencies)
- `GET /health/ready` — Readiness (commented out)

### API Endpoints

- `POST /chat/stream` — Streaming AI chat (SSE)
- `GET /test/endpoint` — Authenticated user info

---

*Structure analysis: 2026-09-24*
