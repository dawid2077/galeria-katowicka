# PROJECT.md — Galeria Katowicka

**Last updated:** 2026-09-24 after initialization

---

## What This Is

**Galeria Katowicka** is an AI-powered chat application focused on cultural venues in Katowice, Poland — specifically **Muzeum Śląskie** and **Strefa Kultury**. Users can ask questions about these venues and receive streaming AI responses via OpenRouter.

**Core value:** A conversational interface for discovering Katowice cultural venues with authenticated, session-persisted chat history.

---

## Context

### Current State (Brownfield)

The backend (`app/`) is a **functional FastAPI application** with:
- Streaming chat via OpenRouter (SSE)
- Clerk JWT authentication with local user sync
- PostgreSQL persistence (users, sessions, places)
- Venue context documents (Markdown) for Muzeum Śląskie and Strefa Kultury

### What Works Today
- `POST /chat/stream` — SSE streaming AI responses
- `GET /health/live` — Liveness probe
- `GET /test/endpoint` — Authenticated user info
- Clerk token verification → local user upsert
- Database schema: users, sessions, places
- Nix development shell with uv, PostgreSQL via Docker Compose

### Known Gaps
- No frontend (Astro planned)
- No session persistence in chat endpoint
- No venue context injection into LLM prompts
- No rate limiting
- Incomplete health/readiness endpoints
- Missing imports in `userMethods.py` (IntegrityError, select)
- No test suite
- Legacy directories (`app.old/`, `app.old2/`) need cleanup

### Tech Stack
- **Backend:** FastAPI, SQLAlchemy 2.0 async, asyncpg, Pydantic v2
- **Auth:** Clerk (Google sign-in flow)
- **AI:** OpenRouter via AsyncOpenAI SDK
- **Database:** PostgreSQL 18 (Docker Compose for dev)
- **Frontend (planned):** Astro with spec-driven development
- **Package manager:** uv

---

## Requirements

### Validated (Existing Capabilities)

- ✓ **Auth** — Clerk JWT verification with local user sync (`app/authClerk.py`, `app/userMethods.py`)
- ✓ **Chat streaming** — SSE via OpenRouter (`app/ai.py`, `app/routes.py`)
- ✓ **User persistence** — PostgreSQL users table with clerk_id linkage (`app/models.py`)
- ✓ **Session model** — Chat history stored as JSON in sessions table (`app/models.py`)
- ✓ **Venue content** — Markdown docs for Muzeum Śląskie & Strefa Kultury (`app/context/`)
- ✓ **Health check** — Liveness endpoint (`app/routes.py`)
- ✓ **Configuration** — Pydantic Settings from `configs/.env` (`app/config.py`)

### Active (v1 Scope)

#### Frontend (Astro)
- [ ] **FE-01**: Astro project initialized with minimal chat UI (ChatGPT-like)
- [ ] **FE-02**: Clerk authentication widget (sign in/up) on landing page
- [ ] **FE-03**: Authenticated chat page with streaming message display
- [ ] **FE-04**: Session history sidebar (list past conversations)
- [ ] **FE-05**: New chat button / session creation
- [ ] **FE-06**: Responsive layout (mobile-friendly)

#### Backend Enhancements
- [ ] **BE-01**: Fix `userMethods.py` missing imports (IntegrityError, select)
- [ ] **BE-02**: Implement session persistence in `/chat/stream` (save chat history)
- [ ] **BE-03**: Inject venue context into LLM system prompt
- [ ] **BE-04**: Add rate limiting (per-user/IP)
- [ ] **BE-05**: Implement `/health/ready` with database connectivity check
- [ ] **BE-06**: Add request size limits
- [ ] **BE-07**: Configure structured logging (structlog globally)
- [ ] **BE-08**: Clean up legacy directories (`app.old/`, `app.old2/`)

#### Integration
- [ ] **INT-01**: Frontend → Backend API integration (CORS, auth token forwarding)
- [ ] **INT-02**: Clerk frontend widget → backend token verification flow

### Out of Scope (v1)

- PostGIS / RAG / semantic search — future enhancement
- Multi-venue directory with search — future enhancement
- Per-venue themes / individual building pages — future enhancement
- Email/password auth (Clerk-only for now)
- User profile management (email update, etc.) — future enhancement
- Admin dashboard — future enhancement

---

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Astro for frontend | User preference; spec-driven development; static-first with islands for interactivity | — Pending |
| Clerk widget on landing | Passwordless Google sign-in; no custom auth UI needed | — Pending |
| MVP vertical slices | Get working chat UI fast; iterate on features | — Pending |
| Session-per-chat model | Matches existing SessionModel schema; enables history sidebar | — Pending |
| Venue context as system prompt | Low-effort RAG alternative; uses existing Markdown docs | — Pending |

---

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---

*Last updated: 2026-09-24 after initialization*