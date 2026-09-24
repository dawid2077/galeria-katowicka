---
last_mapped_commit: 2ab2e51140e076aa6f8585eb8cdf2b07d40351cb
last_mapped_at: 2026-09-24
---
<!-- refreshed: 2026-09-24 -->

# External Integrations

**Analysis Date:** 2026-09-24

## APIs & External Services

**LLM Provider:**

- OpenRouter - LLM API gateway
  - SDK/Client: `openai` (AsyncOpenAI with custom base_url)
  - Auth: `OPENROUTER_API_KEY` env var
  - Endpoint: `https://openrouter.ai/api/v1`
  - Usage: Streaming chat completions in `app/ai.py:9-12`
  - Model: Configurable via `settings.MODEL` (not yet in config, hardcoded in `ai.py:21`)

**Authentication Provider:**

- Clerk - User authentication & management
  - SDK/Client: `clerk-backend-api` / `clerk_backend-api`
  - Auth: `CLERK_SECRET_KEY` env var
  - Public Key: `CLERK_PUBLIC_KEY` env var (configured but may be unused)
  - Verification: `clerk.authenticate_request()` in `app/authClerk.py:23-29`
  - Authorized Parties: `AUTHORIZED_PARTIES` env var (list of allowed origins)
  - JWT Claims Used: `sub` (user ID), `email`

## Data Storage

**Databases:**

- PostgreSQL 18 (Alpine) - Primary relational database
  - Connection: `DATABASE_URL` env var (`postgresql+asyncpg://user:pass@host:port/db`)
  - Client: SQLAlchemy 2.0 async + asyncpg driver
  - ORM Models: `app/models.py` (UserModel, SessionModel, PlaceModel)
  - Connection Pool: Size 2, max_overflow 3, timeout 10s, pre_ping enabled (`app/database.py:11-19`)
  - Session Management: `AsyncSessionLocal` factory with `expire_on_commit=False` (`app/database.py:21-25`)
  - Migrations: Auto-create on startup via `Base.metadata.create_all()` (`app/init.py:6-8`)

**File Storage:**

- Local filesystem only (no cloud storage integration detected)

**Caching:**

- None detected (no Redis, Memcached, or in-memory cache implementation)

## Authentication & Identity

**Auth Provider:**

- Clerk (External SaaS)
  - Implementation: Backend API JWT verification via `clerk_backend_api.Clerk`
  - Flow: Client gets JWT from Clerk → sends Bearer token → backend verifies via Clerk API → extracts `sub` and `email` → gets/creates local UserModel
  - User Sync: `UserMethods.get_or_create_user()` creates local user on first verified request (`app/userMethods.py:36-57`)
  - Local User Model: `UserModel` with `clerk_id` (unique, indexed), `user_id` (UUID v7), `email`, `created_at` (`app/models.py:13-25`)

## Monitoring & Observability

**Error Tracking:**

- None configured (no Sentry, Datadog, etc.)

**Logs:**

- structlog for structured logging (`app/ai.py:8`, `app/userMethods.py:31` TODO)
- Log output: stdout/stderr (no file logging configured)
- Levels: Error logging in `app/ai.py:37`, TODO for user creation errors in `app/userMethods.py:31`

**Health Checks:**

- Liveness: `GET /health/live` returns `{"status": "up"}` (`app/routes.py:55-59`)
- Readiness: Not implemented (commented out in `app/routes.py:65-68`)
- Monitoring placeholder: `app/monitoring.py` has commented schedule-based health checker

## CI/CD & Deployment

**Hosting:**

- Not configured (no Dockerfile, no cloud provider configs detected)

**CI Pipeline:**

- None detected (no GitHub Actions, GitLab CI, etc.)

**Containerization:**

- Docker Compose for local development only (`docker-compose.yml`)
  - Services: postgres (18-alpine), pgadmin4
  - No application container defined

## Environment Configuration

**Required env vars (from `configs/.env.example`):**

- `OPENROUTER_API_KEY` - LLM API access
- `DATABASE_URL` - PostgreSQL connection string
- `CLERK_PUBLIC_KEY` - Clerk public key
- `CLERK_SECRET_KEY` - Clerk secret key (required for JWT verification)
- `AUTHORIZED_PARTIES` - JSON array of allowed origins for JWT audience validation

**Secrets location:**

- `configs/.env` (gitignored, not committed)
- `configs/.env.example` (committed template)
- No external secret manager detected

## Webhooks & Callbacks

**Incoming:**

- None implemented (no webhook endpoints in `app/routes.py`)

**Outgoing:**

- None implemented (no webhook delivery code detected)

---

*Integration audit: 2026-09-24*
