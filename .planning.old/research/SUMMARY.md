# Project Research Summary

**Project:** Galeria Katowicka — AI Chat for Katowice Cultural Venues
**Synthesized:** 2026-09-24
**Source Files:** STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md

---

## Key Findings

### Stack Consensus

| Layer | Decision | Confidence |
|-------|----------|------------|
| **Frontend** | Astro 5 + React 19 islands + Tailwind 4 | HIGH |
| **Auth (FE)** | @clerk/clerk-react 5 (SignIn, UserButton, useAuth) | HIGH |
| **Auth (BE)** | clerk-backend-api 7 (existing, verified) | HIGH |
| **Backend** | FastAPI 0.110+ (existing) | HIGH |
| **Database** | PostgreSQL 18 + SQLAlchemy 2.0 async + asyncpg (existing) | HIGH |
| **LLM** | OpenRouter via openai 3.x AsyncOpenAI (existing) | HIGH |
| **Streaming** | Native EventSource (browser) + SSE Starlette (backend) | HIGH |
| **State** | Zustand or React Context for chat/session | MEDIUM |
| **Types** | TypeScript 5 strict; generate from Pydantic via pydantic2ts | MEDIUM |

**Key Integration Pattern:** Astro island (`client:visible`) for chat component → Clerk token → FastAPI SSE endpoint → PostgreSQL sessions.

### Table Stakes (Must Have for v1)

1. **Streaming token delivery** (SSE) — Already implemented in FastAPI
2. **Session persistence & history** — Extend existing `SessionModel` with `venue_id`
3. **User authentication** — Clerk Google OAuth (frontend widget + backend verification) — Already implemented
4. **Typing/streaming indicators** — React state during SSE stream
5. **Message regeneration** — Branching UI pattern (Vercel AI SDK reference)
6. **Conversation search & filtering** — Full-text on `chat_history` JSON
7. **Mobile-responsive chat UI** — Tailwind responsive + bottom-sheet patterns
8. **Accessibility (WCAG 2.1 AA)** — Semantic HTML, ARIA live regions for streaming
9. **Dark/light theme** — CSS variables + localStorage persistence
10. **Error handling with retry** — Toast + auto-retry with backoff

### Differentiators (Venue-Specific Value)

1. **Venue context injection (RAG-lite)** — System prompt with curated Markdown (< 4k tokens/venue)
2. **Per-venue session isolation** — Compound key `user_id + venue_id`; separate context windows
3. **Venue selector in UI** — Switch context; loads venue-scoped session
4. **Visit planning deep links** — "Book tickets" → bilety.muzeumslaskie.pl / nospr.org.pl
4. **Multilingual support** — 40+ languages via system prompt + LLM output control

### Anti-Features (Explicitly Out of Scope)

- Open-web RAG / internet search → Curated venue markdown only
- Persistent cross-venue memory (default) → Opt-in only; separate sessions by default
- User-generated content in knowledge base → Staff-only CMS
- Autonomous agent actions (book/pay) → Deep links only; user confirms

---

## Implications for Roadmap

### Phase 1: Core Chat + Venue Context (MVP)

| Requirement | Source | Implementation |
|-------------|--------|----------------|
| FE-01: Astro init + chat UI island | FEATURES table stakes | `astro create` + React island |
| FE-02: Clerk widget on landing | FEATURES table stakes | `<SignIn client:visible />` |
| FE-03: Authenticated chat page | FEATURES table stakes | Protected route + Clerk auth check |
| FE-04: Session history sidebar | FEATURES table stakes | Sidebar component + API |
| FE-05: New chat / session creation | FEATURES table stakes | POST /sessions endpoint |
| BE-01: Fix userMethods imports | CONCERNS critical bug | Add `IntegrityError`, `select` imports |
| BE-02: Session persistence in chat | ARCHITECTURE data flow | Extend `/chat/stream` to save history |
| BE-03: Venue context injection | FEATURES differentiator | System prompt with venue markdown |
| BE-04: Rate limiting | CONCERNS security | slowapi / per-user quota |
| INT-01: Frontend→Backend integration | ARCHITECTURE | CORS, token forwarding, Vite proxy |
| INT-02: Clerk widget→backend flow | ARCHITECTURE | `getToken()` + `Authorization` header |

### Phase 2: Visit Experience

- Visit planning & ticketing deep links (requires venue API partnerships)
- Spatial awareness / zone selection (requires venue map data)
- Multilingual audio mode (TTS integration)
- Exhibit visual recognition (vision API)

### Phase 3: District Intelligence

- Cross-venue context (Strefa Kultury district)
- Curator CMS for knowledge base
- Analytics dashboard

---

## Critical Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SSE connection drops on mobile | HIGH | HIGH | Reconnection logic + local persistence |
| OpenRouter cost overrun | HIGH | HIGH | Per-user token budgets + daily alerts |
| Prompt injection via venue content | MEDIUM | CRITICAL | Sanitize markdown; delimiter blocks; monitoring |
| Clerk token expiry mid-stream | MEDIUM | HIGH | Auto-refresh + request retry |
| DB pool exhaustion | MEDIUM | HIGH | Load test; PgBouncer; monitor pool |
| Type drift FE/BE | HIGH | MEDIUM | pydantic2ts in CI |

---

## Recommended Next Steps

1. **Immediate (pre-Phase 1):**
   - Fix `userMethods.py` missing imports (blocker)
   - Add `MODEL` setting to `app/config.py`
   - Configure global structlog

2. **Phase 1 Kickoff:**
   - `/gsd-discuss-phase 1` — Clarify Astro project structure
   - `/gsd-ui-phase 1` — Generate UI-SPEC.md for chat interface
   - `/gsd-plan-phase 1` — Create execution plan

3. **Architecture Decisions Needed:**
   - Monorepo (Turborepo) vs separate repos for FE/BE
   - Deployment target (Vercel + Fly.io vs single container)
   - Shared type generation strategy

---

## Sources Summary

| File | Key Contribution |
|------|------------------|
| STACK.md | Versioned stack, integration patterns, gotchas |
| FEATURES.md | 25 table stakes, 18 differentiators, 11 anti-features, MVP phasing |
| ARCHITECTURE.md | Monorepo structure, data flow, Clerk integration, SSE hook, deployment options |
| PITFALLS.md | 10 critical risk categories, monitoring metrics, security gaps |

---

*Research synthesis: 2026-09-24*