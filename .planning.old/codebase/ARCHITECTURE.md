---
last_mapped_commit: 2ab2e51140e076aa6f8585eb8cdf2b07d40351cb
last_mapped_at: 2026-09-24
---
<!-- refreshed: 2026-09-24 -->

# Architecture

**Analysis Date:** 2026-09-24

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                      │
│                     `app/main.py`                             │
├──────────────────────┬──────────────────────┬────────────────┤
│   API Layer          │   Service Layer      │   Data Layer   │
│  `app/routes.py`     │  `app/ai.py`         │  `app/models.py`│
│  `app/authClerk.py`  │  `app/userMethods.py`│  `app/database.py`│
│  `app/schemas.py`    │  `app/monitoring.py` │  `app/init.py`   │
└──────────┬───────────┴──────────┬───────────┴────────┬───────┘
           │                      │                    │
           ▼                      ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Clerk     │  │  OpenRouter │  │   PostgreSQL        │  │
│  │   Auth      │  │   (LLM)     │  │   (via asyncpg)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| **FastAPI App** | Application entry point, lifespan management, router registration | `app/main.py` |
| **API Routes** | HTTP endpoints for chat streaming, health checks, user info | `app/routes.py` |
| **Authentication** | Clerk JWT verification, user sync with database | `app/authClerk.py` |
| **User Management** | Get-or-create user pattern with Clerk ID deduplication | `app/userMethods.py` |
| **AI Service** | Streaming LLM calls via OpenRouter, response accumulation | `app/ai.py` |
| **Data Models** | SQLAlchemy ORM models for Users, Sessions, Places | `app/models.py` |
| **Schemas** | Pydantic models for request/response validation | `app/schemas.py` |
| **Database** | Async engine, session factory, dependency injection | `app/database.py` |
| **Initialization** | Database table creation on startup | `app/init.py` |
| **Configuration** | Pydantic Settings from `.env` file | `app/config.py` |
| **Monitoring** | Placeholder for health check scheduling | `app/monitoring.py` |

## Pattern Overview

**Overall:** Layered architecture with dependency injection (FastAPI `Depends`)

**Key Characteristics:**

- Async-first design using `asyncio` and `async/await` throughout
- Dependency injection for database sessions, authentication, and configuration
- Streaming responses via Server-Sent Events (SSE) for LLM interactions
- External authentication (Clerk) with local user synchronization
- Pydantic v2 for settings and schema validation
- SQLAlchemy 2.0 async ORM with asyncpg driver

## Layers

**API Layer (Routes):**

- Purpose: HTTP endpoint definitions, request/response handling, status codes
- Location: `app/routes.py`
- Contains: Route handlers for `/chat/stream`, `/test/endpoint`, `/health/live`
- Depends on: Auth dependencies, AI service, UserMethods
- Used by: FastAPI app (`app/main.py`)

**Authentication Layer:**

- Purpose: Verify Clerk JWT tokens, extract user identity, sync with local DB
- Location: `app/authClerk.py`
- Contains: `get_current_user` (token verification), `auth_user` (DB sync)
- Depends on: `clerk-backend-api`, `app/config.py`, `app/database.py`, `app/userMethods.py`
- Used by: Route handlers via `Depends(auth_user)`

**Service Layer:**

- Purpose: Business logic, external API integration, data transformation
- Location: `app/ai.py`, `app/userMethods.py`, `app/monitoring.py`
- Contains: `llm_call` (streaming), `full_response` (accumulated), `UserMethods.get_or_create_user`
- Depends on: `openai` (AsyncOpenAI), `app/schemas.py`, `app/models.py`, `app/database.py`
- Used by: Route handlers

**Data Layer:**

- Purpose: Database schema definition, connection management, migrations
- Location: `app/models.py`, `app/database.py`, `app/init.py`
- Contains: `UserModel`, `SessionModel`, `PlaceModel`, async engine, session factory
- Depends on: `sqlalchemy`, `asyncpg`, `app/config.py`
- Used by: Services, authentication layer

**Configuration Layer:**

- Purpose: Centralized settings management from environment
- Location: `app/config.py`
- Contains: `Settings` class with `CLERK_PUBLIC_KEY`, `CLERK_SECRET_KEY`, `DATABASE_URL`, `OPENROUTER_API_KEY`, `AUTHORIZED_PARTIES`
- Depends on: `pydantic-settings`, `configs/.env`
- Used by: All layers

## Data Flow

### Primary Request Path: Chat Streaming

1. **Client POST** `/chat/stream` with `ChatHistory` payload (`app/routes.py:14-20`)
2. **Authentication** via `Depends(auth_user)` → Clerk JWT verification → user sync (`app/authClerk.py:59-62`)
3. **AI Service** processes conversation via `full_response(chat_data)` (`app/ai.py:42-56`)
4. **OpenRouter API** streams tokens via AsyncOpenAI (`app/ai.py:20-24`)
5. **SSE Response** yields chunks as `EventSourceResponse` (`app/routes.py:20`)

### Authentication Flow

1. **Request** arrives with `Authorization: Bearer <jwt>`
2. **HTTPBearer** extracts credentials (`app/authClerk.py:13`)
3. **Clerk SDK** verifies JWT with secret key & authorized parties (`app/authClerk.py:23-29`)
4. **Payload extraction** → `sub` (user_id) and `email` claims (`app/authClerk.py:38-49`)
5. **UserMethods.get_or_create_user** → upsert by `clerk_id` (`app/userMethods.py:36-57`)
6. **Returns** `UserModel` instance for route handler use

### Database Initialization

1. **App startup** triggers `lifespan` async context manager (`app/main.py:21-24`)
2. **init_db()** runs `Base.metadata.create_all` via async engine (`app/init.py:6-8`)
3. **Tables created**: `users`, `sessions`, `places` (`app/models.py`)

## Key Abstractions

**UserModel (SQLAlchemy):**

- Purpose: Persistent user record linked to Clerk identity
- Location: `app/models.py:13-25`
- Pattern: Declarative ORM with UUID PK, unique `clerk_id` index
- Fields: `user_id` (UUID PK), `email`, `clerk_id` (unique), `created_at`

**SessionModel (SQLAlchemy):**

- Purpose: Chat session storage with JSON history
- Location: `app/models.py:26-42`
- Pattern: UUID PK, FK to UserModel, JSON column for chat history
- Fields: `session_id`, `session_user_id` (FK), `chat_history` (JSON), `created_at`

**PlaceModel (SQLAlchemy):**

- Purpose: Place/location data for future features
- Location: `app/models.py:45-52`
- Pattern: Simple entity with name, info, location strings

**ChatHistory / ChatMessage (Pydantic):**

- Purpose: Request validation for chat streaming endpoint
- Location: `app/schemas.py:11-24`
- Pattern: Typed conversation array with role/content structure
- Constraints: `content` 1-10000 chars, role enum (user/assistant/system)

**AuthUser (Pydantic):**

- Purpose: Validated user identity from Clerk token
- Location: `app/schemas.py:8-10`
- Pattern: Simple DTO with `clerk_user_id` and `email` (EmailStr)

**Settings (Pydantic Settings):**

- Purpose: Type-safe configuration from environment
- Location: `app/config.py:5-16`
- Pattern: `BaseSettings` with `env_file="configs/.env"`, required fields

## Entry Points

**Main Application:**

- Location: `app/main.py`
- Triggers: `uvicorn app.main:app` or `python -m app.main`
- Responsibilities: Create FastAPI instance, configure lifespan (DB init), include router

**Health Endpoints:**

- `/health/live` → Liveness probe (no dependencies) (`app/routes.py:55-59`)
- `/health/ready` → Readiness probe (commented out, would check DB) (`app/routes.py:65-68`)

**API Endpoints:**

- `POST /chat/stream` → Streaming AI chat (`app/routes.py:14-20`)
- `GET /test/endpoint` → Authenticated user info (`app/routes.py:44-53`)

## Architectural Constraints

- **Threading:** Single-threaded async event loop (ASGI/uvicorn). No worker threads used.
- **Global State:** Module-level singletons in `app/database.py` (engine, AsyncSessionLocal), `app/ai.py` (OpenAI client), `app/authClerk.py` (Clerk client). These are initialized at import time.
- **Circular Imports:** None detected. Import graph flows: `main.py` → `routes.py` → (`ai.py`, `authClerk.py`, `userMethods.py`) → (`database.py`, `models.py`, `schemas.py`, `config.py`). `config.py` is a leaf.
- **Database Sessions:** Request-scoped via `Depends(get_db)` yielding `AsyncSession` from `AsyncSessionLocal` factory.

## Anti-Patterns

### Incomplete Error Handling in UserMethods

**What happens:** `get_or_create_user` catches only `IntegrityError` but imports it from nowhere (missing import)
**Why it's wrong:** Will raise `NameError` at runtime on duplicate key; other DB errors unhandled
**Do this instead:** Add `from sqlalchemy.exc import IntegrityError` at top of `app/userMethods.py`; consider broader exception handling with structlog

### Debug Print in Production Code

**What happens:** `print(uuid7())` executes at module import in `app/userMethods.py:5`
**Why it's wrong:** Leaks UUID to stdout on every import; not configurable logging
**Do this instead:** Remove or guard behind debug flag; use `structlog` consistently

### Commented-Out Code in Routes

**What happens:** Large commented blocks for `/health/ready` and alternative auth (`app/routes.py:61-68`)
**Why it's wrong:** Dead code confuses maintenance; suggests incomplete implementation
**Do this instead:** Remove or implement properly in separate PR

### Missing MODEL Setting

**What happens:** `app/ai.py:21` references `settings.MODEL` but `app/config.py` has no `MODEL` field
**Why it's wrong:** Will raise `AttributeError` at runtime
**Do this instead:** Add `MODEL: str = Field(default="openai/gpt-4o-mini")` to `Settings` in `app/config.py`

## Error Handling

**Strategy:** FastAPI exception handlers + structured logging via structlog

**Patterns:**

- Authentication errors → `HTTPException 401` with `WWW-Authenticate: Bearer` (`app/authClerk.py:32-36, 54-58`)
- LLM streaming errors → Yield error event in SSE stream, log via structlog (`app/ai.py:36-38`)
- Database integrity errors → Catch `IntegrityError`, rollback, retry fetch (`app/userMethods.py:50-57`)
- Validation errors → Pydantic/FastAPI automatic 422 responses

## Cross-Cutting Concerns

**Logging:** `structlog` with `get_logger()` in `app/ai.py:8`. Not yet configured globally (no processors/formatters set).

**Validation:** Pydantic models for all request/response bodies (`app/schemas.py`). FastAPI automatic request validation.

**Authentication:** Clerk JWT verification on protected routes via `Depends(auth_user)`. Public routes: `/health/live`.

---

*Architecture analysis: 2026-09-24*
