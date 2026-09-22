# External Integrations

**Analysis Date:** 2026-09-22

## Integration Inventory

| Integration | Active status | Purpose | Primary files |
|---|---|---|---|
| OpenRouter chat completions | Intended active integration, currently misconfigured | Streams model responses to the FastAPI chat endpoint | `app/ai.py`, `app/routes.py`, `app/config.py` |
| Clerk token verification | Intended active identity integration, currently not wired correctly | Verifies bearer JWTs and extracts the user identifier/email | `app/authClerk.py`, `app/routes.py`, `app/schemas.py` |
| PostgreSQL | Intended active persistence integration | Stores users, sessions, and places through SQLAlchemy | `app/database.py`, `app/models.py`, `app/init.py`, `docker-compose.yml` |
| Static venue context | Present as local content, not connected to requests | Supplies human-authored Katowice venue information | `app/context/MuzeumSlaskie.md`, `app/context/StrefaKultury.md` |
| Astro frontend | Not implemented | Planned frontend shell and per-place pages | `astro/here_frontend.md`, `app/docs/frontend.md` |
| Google sign-in | Planned through Clerk only | Passwordless identity flow described in notes | `app/docs/auth.md`, `app/docs/user_auth.md` |
| PostGIS/RAG | Not implemented | Future database/search capabilities described in notes | `app/docs/mvp.md` |

The active integration surface is `app/`; `app.old2/` is an archived OpenRouter chat iteration and `app.old/` is an archived SQLAlchemy book/catalog iteration. The active application is not a clean end-to-end integration yet because its route imports, settings, and schemas contain unresolved references (`app/routes.py:4`, `app/routes.py:5`, `app/schemas.py:10`, `app/config.py:5`).

## APIs & External Services

### OpenRouter / LLM API

- The active client is an `AsyncOpenAI` instance configured with `base_url="https://openrouter.ai/api/v1"` and `api_key=settings.OPENROUTER_API_KEY` (`app/ai.py:9`, `app/ai.py:10`, `app/ai.py:11`).
- `llm_call()` sends the conversation as chat-completion messages with `stream=True`, reads streamed choices, and yields `streamingResponse`, `error`, and `done` events (`app/ai.py:13`, `app/ai.py:20`, `app/ai.py:26`, `app/ai.py:34`, `app/ai.py:41`).
- The active route exposes `POST /chat/stream`, accepts `ChatHistory`, and wraps `full_response(chat_data)` in an `EventSourceResponse` (`app/routes.py:15`, `app/routes.py:19`, `app/routes.py:21`).
- `full_response()` accumulates streamed text and emits one final `done` event, or returns an `error` event when the LLM stream reports an error (`app/ai.py:42`, `app/ai.py:46`, `app/ai.py:53`, `app/ai.py:56`).
- The OpenAI SDK is resolved as version 3.2.0, and OpenRouter is reached through the SDK's configurable base URL rather than a direct `httpx` client (`uv.lock:984`, `app/ai.py:9`).
- The active settings schema does not declare `MODEL`, although `llm_call()` reads `settings.MODEL` (`app/config.py:5`, `app/ai.py:21`). The example environment file also has no model variable (`configs/.env.example:1`). This makes the active LLM call incomplete until a model setting is added and supplied.
- The chat route has no authentication dependency, CORS policy, or rate limiting; the only route dependency shown is the request body (`app/routes.py:15`, `app/routes.py:19`, `app/main.py:25`). The main module's comment about authentication does not add middleware or route protection (`app/main.py:19`).
- `app/ai.py` logs LLM failures with Structlog and returns the exception text in the SSE error payload (`app/ai.py:8`, `app/ai.py:36`, `app/ai.py:38`). No external log sink or tracing exporter is configured.

### Clerk Identity API

- `app/authClerk.py` imports the generated Clerk client and `AuthenticateRequestOptions` from `clerk_backend_api` (`app/authClerk.py:3`).
- A module-level `Clerk` client is constructed with `settings.CLERK_SECRET_KEY`, and FastAPI `HTTPBearer` supplies the incoming bearer credential (`app/authClerk.py:9`, `app/authClerk.py:10`, `app/authClerk.py:13`).
- `get_current_user()` calls `clerk.authenticate_request()` with `settings.CLERK_PUBLIC_KEY`, then checks `request_state.is_authenticated` and returns 401 responses for rejected tokens (`app/authClerk.py:17`, `app/authClerk.py:20`, `app/authClerk.py:25`, `app/authClerk.py:26`).
- The verifier extracts the JWT `sub` claim as the user ID and an `email` claim, then constructs `AuthUser` (`app/authClerk.py:32`, `app/authClerk.py:41`, `app/authClerk.py:44`).
- Authorized parties are hard-coded to `http://localhost:3000` and the placeholder `https://your-app.com`; there is no environment-driven production audience (`app/authClerk.py:21`).
- The active route imports `get_current_user` from a module named `auth`, but the repository file is named `authClerk.py` and no `app/auth.py` exists (`app/routes.py:4`, `app/authClerk.py:1`). The route also requests the dependency twice and references an undefined `user_payloaduser_id`, so the intended test endpoint cannot currently execute (`app/routes.py:23`, `app/routes.py:25`, `app/routes.py:26`, `app/routes.py:28`).
- `AuthUser` contains an undefined `Emailstr` annotation instead of Pydantic's `EmailStr`, which is another active import/runtime failure (`app/schemas.py:8`, `app/schemas.py:10`).
- The active database model has a unique `clerk_id` column, but no active endpoint creates or links a Clerk identity to `UserModel` (`app/models.py:19`, `app/routes.py:15`). The untracked `app/userMethods.py` attempts a `User_Exists` helper, but it does not import `AsyncSession`, queries the UUID primary key rather than `clerk_id`, and is not imported by `app/` (`app/userMethods.py:1`, `app/userMethods.py:5`, `app/models.py:15`).
- The notes describe Google-based passwordless authentication through Clerk, but there is no Google SDK, OAuth callback route, session cookie, or Clerk webhook implementation (`app/docs/auth.md:1`, `app/docs/auth.md:3`, `app/docs/user_auth.md:1`).

### Static Venue Content

- `app/context/MuzeumSlaskie.md` and `app/context/StrefaKultury.md` are Markdown content files containing venue facts, addresses, links, and visitor information (`app/context/MuzeumSlaskie.md:1`, `app/context/StrefaKultury.md:1`).
- The active AI client receives only the caller-supplied `ChatHistory`; it does not load either context file or inject venue context into the OpenRouter request (`app/ai.py:2`, `app/ai.py:15`, `app/ai.py:20`).
- `app/docs/connecting_other_sites.md` describes a future directory of individual building pages, separate message histories, and themes, but no route, frontend, or data loader implements that design (`app/docs/connecting_other_sites.md:1`).
- The Markdown files contain public URLs for maps, ticketing, and venue websites, but these are static references rather than runtime API calls (`app/context/MuzeumSlaskie.md:5`, `app/context/MuzeumSlaskie.md:53`, `app/context/MuzeumSlaskie.md:84`).

### Frontend and Astro

- `astro/here_frontend.md` contains only a placeholder statement and there is no Astro configuration, source tree, package manifest, or lockfile (`astro/here_frontend.md:1`).
- `app/docs/frontend.md` says the frontend will use Astro and spec-driven development, but that is a roadmap note rather than an implemented integration (`app/docs/frontend.md:1`).
- No frontend-to-backend client, CORS allowlist, proxy configuration, or browser authentication flow exists in the repository (`app/main.py:25`, `app/authClerk.py:21`).

## Data Storage

### PostgreSQL

- The active database layer creates an async SQLAlchemy engine from `settings.DATABASE_URL` with a pool size of 2, maximum overflow of 3, a 10-second pool timeout, and `pool_pre_ping=True` (`app/database.py:11`, `app/database.py:12`, `app/database.py:15`, `app/database.py:16`, `app/database.py:17`, `app/database.py:18`).
- `AsyncSessionLocal` creates async sessions with `expire_on_commit=False`, and `get_db()` yields a session for dependency injection (`app/database.py:21`, `app/database.py:24`, `app/database.py:26`, `app/database.py:28`).
- The application lifespan calls `init_db()`, which runs `Base.metadata.create_all()` against the engine (`app/main.py:21`, `app/init.py:6`, `app/init.py:8`). There is no Alembic or other migration tool in `pyproject.toml` (`pyproject.toml:6`).
- Active ORM models define `users`, `sessions`, and `places` tables; sessions store chat history as JSON and reference users by UUID (`app/models.py:13`, `app/models.py:26`, `app/models.py:31`, `app/models.py:34`, `app/models.py:45`).
- The chat route imports database and CRUD symbols but does not open a session, persist a session, or save chat history; its implementation only calls the AI response generator (`app/routes.py:2`, `app/routes.py:5`, `app/routes.py:19`, `app/routes.py:21`).
- Docker Compose defines a PostgreSQL 18 Alpine service with a persistent Compose volume and a pgAdmin service for local development (`docker-compose.yml:2`, `docker-compose.yml:3`, `docker-compose.yml:12`, `docker-compose.yml:15`, `docker-compose.yml:16`, `docker-compose.yml:27`). The Compose file contains development credentials, which are not reproduced here.
- The example configuration documents a PostgreSQL asyncpg URL shape, while the active settings file expects the same `DATABASE_URL` variable (`configs/.env.example:2`, `app/config.py:8`).
- `psycopg`, `psycopg[binary]`, and `psycopg2-binary` are declared, but active code uses SQLAlchemy's async interface and the lock's asyncpg driver; the extra drivers are not directly used by the active modules (`pyproject.toml:14`, `pyproject.toml:22`, `app/database.py:3`).
- PostGIS is only a future note; the active `places.location` column is a string and no spatial type or extension is configured (`app/docs/mvp.md:1`, `app/models.py:52`).

### File Storage

- No object store, filesystem persistence layer, upload endpoint, or media service is implemented. Venue context is committed Markdown, while application state is intended to reside in PostgreSQL (`app/context/MuzeumSlaskie.md:1`, `app/context/StrefaKultury.md:1`, `app/database.py:11`).

### Caching

- No Redis, Memcached, HTTP cache, response cache, or application cache client is declared or imported (`pyproject.toml:6`, `app/`).

## Authentication & Identity

**Auth provider:** Clerk is the intended provider, with Google sign-in described as the user-facing flow (`app/docs/auth.md:1`, `app/docs/auth.md:3`, `app/authClerk.py:3`).

**Current mechanism:**
- Bearer tokens are read with FastAPI's `HTTPBearer` and verified by the Clerk backend SDK (`app/authClerk.py:9`, `app/authClerk.py:13`, `app/authClerk.py:17`).
- Verification uses both a Clerk secret key and public JWT key, rejects unauthenticated requests with 401, and extracts `sub` plus `email` claims (`app/authClerk.py:10`, `app/authClerk.py:20`, `app/authClerk.py:25`, `app/authClerk.py:32`, `app/authClerk.py:41`).
- No password hashing, local login endpoint, refresh-token flow, session cookie, or OAuth callback is present (`app/routes.py:14`, `app/authClerk.py:13`).
- The active `/chat/stream` endpoint is unauthenticated, while the intended `/test/endpoint` is the only route attempting to use `get_current_user` (`app/routes.py:15`, `app/routes.py:23`, `app/routes.py:25`).
- The active `UserModel` stores `clerk_id` as a unique indexed value, but there is no active identity provisioning path (`app/models.py:19`, `app/routes.py:15`).
- The untracked `app/userMethods.py` is relevant current working-tree code but is disconnected and incomplete; it should not be treated as an established integration contract (`app/userMethods.py:1`, `app/userMethods.py:5`).

## Monitoring & Observability

**Error tracking:**
- No application-level Sentry, OpenTelemetry, Datadog, or equivalent tracing/error-tracking integration is configured (`pyproject.toml:6`, `app/`).
- `sentry-sdk` appears in the lock only as a transitive dependency of the FastAPI cloud CLI package; no source module imports or configures it (`uv.lock:433`, `uv.lock:444`, `app/`).

**Logs:**
- `structlog.get_logger()` is created in `app/ai.py`, and LLM exceptions are logged with the exception string (`app/ai.py:8`, `app/ai.py:36`, `app/ai.py:37`).
- No Structlog processors, JSON formatter, log level configuration, request ID middleware, or external log destination is present (`app/ai.py:8`, `app/main.py:25`).

**Health checks:**
- `app/kubernetes.py` sketches liveness/readiness routes and a lifespan, but references undefined `app`, `status`, `Response`, `check_db_connection`, and `database` symbols; it is not an active health integration (`app/kubernetes.py:1`, `app/kubernetes.py:4`, `app/kubernetes.py:10`, `app/kubernetes.py:12`, `app/kubernetes.py:26`).
- Docker Compose defines no healthcheck for PostgreSQL or pgAdmin (`docker-compose.yml:1`).

## CI/CD & Deployment

**Hosting:**
- No hosting provider, production process definition, Dockerfile, or backend Compose service is present (`docker-compose.yml:1`, `pyproject.toml:1`).
- Docker Compose is limited to local PostgreSQL and pgAdmin infrastructure (`docker-compose.yml:1`).
- `shell.nix` is the only explicit development environment definition and launches the app from `app/` using `uv` (`shell.nix:3`, `shell.nix:26`, `shell.nix:28`, `shell.nix:29`).

**CI pipeline:**
- No GitHub Actions, GitLab CI, tox, pytest configuration, lint configuration, or type-check configuration is present (`pyproject.toml:1`, `.github/`).
- No build or deployment command is defined beyond the Nix/uv development instructions (`shell.nix:28`, `shell.nix:29`).

**Kubernetes:**
- `app/kubernetes.py` is an unfinished skeleton and is not imported by `app/main.py`; it cannot currently serve as a deployment contract (`app/kubernetes.py:1`, `app/main.py:14`, `app/main.py:17`).

## Environment Configuration

**Required active variables:**
- `CLERK_PUBLIC_KEY` - Clerk JWT verification key (`app/config.py:6`, `app/authClerk.py:20`).
- `CLERK_SECRET_KEY` - Clerk backend client authentication (`app/config.py:7`, `app/authClerk.py:10`).
- `DATABASE_URL` - async SQLAlchemy PostgreSQL connection URL (`app/config.py:8`, `app/database.py:12`).
- `OPENROUTER_API_KEY` - OpenRouter API credential (`app/config.py:9`, `app/ai.py:11`).
- `MODEL` - read by the active LLM client but absent from `Settings` and the example file (`app/ai.py:21`, `app/config.py:5`, `configs/.env.example:1`).

**Secrets location:**
- The active settings class loads `configs/.env` with UTF-8 encoding and ignores unknown variables (`app/config.py:11`, `app/config.py:12`, `app/config.py:14`).
- `configs/.env` exists and is ignored by Git; its contents are not reproduced (`configs/.env`, `.gitignore:1`).
- `configs/.env.example` is the non-secret template for environment setup (`configs/.env.example`).
- Docker Compose uses development-only database and pgAdmin credentials; those values are infrastructure configuration and are not copied into this document (`docker-compose.yml:6`, `docker-compose.yml:19`).

**Configuration gaps:**
- The documented shell changes into `app/`, while `Settings` requests `configs/.env` relative to the current working directory; this path needs to be reconciled before relying on local environment loading (`shell.nix:26`, `app/config.py:12`).
- `configs/config.conf` contains `VENUE_NAME`, but active `Settings` does not read that file or declare the value (`configs/config.conf:1`, `app/config.py:5`).
- Clerk authorized parties include a placeholder production domain, so production identity configuration is not complete (`app/authClerk.py:21`).

## Webhooks & Callbacks

**Incoming:**
- No Clerk webhook endpoint, signature verification route, Google OAuth callback, or other incoming callback is defined (`app/routes.py:14`, `app/authClerk.py:13`).
- FastAPI registers only the chat stream and intended test endpoint in the active route module (`app/routes.py:15`, `app/routes.py:23`).

**Outgoing:**
- The only explicit outbound API call is the OpenRouter chat-completions request made by `AsyncOpenAI` (`app/ai.py:9`, `app/ai.py:20`).
- Clerk verification is performed by the Clerk backend SDK; no application code sends a separate outbound webhook or callback (`app/authClerk.py:17`).
- No outbound event bus, email provider, analytics endpoint, or payment provider is configured (`pyproject.toml:6`, `app/`).

## Integration Data Flows

### Chat request flow

1. A client sends JSON matching `ChatHistory` to `POST /chat/stream` (`app/routes.py:15`, `app/schemas.py:23`).
2. FastAPI passes the body to `stream_chat()`, which creates an `EventSourceResponse` around `full_response()` (`app/routes.py:19`, `app/routes.py:21`).
3. `full_response()` consumes `llm_call()` and accumulates streamed text (`app/ai.py:42`, `app/ai.py:46`, `app/ai.py:51`).
4. `llm_call()` sends the messages to OpenRouter with the configured model and bearer API key (`app/ai.py:20`, `app/ai.py:21`, `app/ai.py:23`).
5. Stream chunks are translated into SSE events and returned to the client (`app/ai.py:26`, `app/ai.py:34`, `app/routes.py:21`).
6. No database session or venue context is used in this path (`app/routes.py:19`, `app/ai.py:2`, `app/context/MuzeumSlaskie.md:1`).

### Identity verification flow

1. A caller supplies an `Authorization: Bearer` token to a dependency-protected endpoint (`app/authClerk.py:9`, `app/authClerk.py:13`).
2. `get_current_user()` passes the token and Clerk keys to `authenticate_request()` (`app/authClerk.py:17`, `app/authClerk.py:20`).
3. A rejected or incomplete token produces a 401 response; a valid token produces `AuthUser` from `sub` and `email` (`app/authClerk.py:25`, `app/authClerk.py:32`, `app/authClerk.py:44`).
4. The intended protected endpoint is currently broken by the wrong module import, duplicate dependency, and undefined response attribute (`app/routes.py:4`, `app/routes.py:25`, `app/routes.py:26`, `app/routes.py:28`).

## Legacy Integration Boundaries

- `app.old2/` contains an earlier OpenRouter streaming client and chat route, but its `main.py` application is commented out and it has no Clerk authentication (`app.old2/main.py:2`, `app.old2/ai.py:5`, `app.old2/routes.py:13`).
- `app.old2/config.py` declares `DATABASE_URL`, `OPENROUTER_API_KEY`, `VENUE_NAME`, and a default `MODEL`, unlike the active settings module (`app.old2/config.py:5`, `app.old2/config.py:8`).
- `app.old/` contains the older author/book SQLAlchemy schema, async database layer, CRUD operations, and book routes; its application entry point is also commented out (`app.old/models.py:15`, `app.old/database.py:11`, `app.old/crud.py:11`, `app.old/routes.py:21`, `app.old/main.py:2`).
- Legacy request examples in `app.old/request_types/post.md` document book POST/curl usage and are not active API contracts (`app.old/request_types/post.md:13`, `app.old/request_types/post.md:28`).
- Changes to current integrations should target `app/` and its root configuration, not the archived copies in `app.old/` or `app.old2/`.

---

*Integration audit: 2026-09-22*
