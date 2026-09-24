# Pitfalls & Gotchas Research

**Domain:** AI Chat Application with Astro + Clerk + FastAPI + Venue Context
**Researched:** 2026-09-24

## Critical Pitfalls

### 1. SSE Production Issues

| Pitfall | Severity | Mitigation |
|---------|----------|------------|
| **Connection drops on mobile/network changes** | High | Implement reconnection logic with exponential backoff; persist partial messages locally |
| **Proxy/timeouts kill long streams** | High | Configure nginx/proxy `proxy_read_timeout > 300s`; send periodic keepalive comments |
| **No native EventSource in some environments** | Medium | Polyfill for older browsers; fallback to fetch+ReadableStream |
| **Message ordering with parallel requests** | Medium | Sequence IDs on messages; client-side reordering buffer |
| **Backpressure / memory with huge responses** | Medium | Chunk size limits; client-side truncation with "show more" |

### 2. OpenRouter Cost Management

| Pitfall | Severity | Mitigation |
|---------|----------|------------|
| **Unbounded token usage per conversation** | Critical | Per-user daily/monthly token budgets in `SessionModel`; hard stop at limit |
| **Expensive models selected by default** | High | Default to `openai/gpt-4o-mini` or similar; require explicit opt-in for premium models |
| **No visibility into spend until bill arrives** | High | Log token usage per request; daily aggregation; alert at 80% budget |
| **Streaming duplicates on reconnection** | Medium | Idempotency keys on requests; deduplicate on backend |

### 3. Venue Context Injection Risks

| Pitfall | Severity | Mitigation |
|---------|----------|------------|
| **Indirect prompt injection via venue content** | Critical | Sanitize Markdown; escape special tokens; use delimiter blocks; monitor arXiv 2606.09204 |
| **Context window overflow with large venues** | High | Token-count venue markdown; truncate to ~3k tokens; prioritize current exhibit |
| **Hallucination when venue context insufficient** | Medium | Explicit "I don't know about X" instructions; cite venue doc sections |
| **Stale venue info (hours, prices, exhibits)** | Medium | Versioned venue docs; curator review schedule; `last_updated` in markdown frontmatter |

### 4. Clerk Integration Gotchas

| Pitfall | Severity | Mitigation |
|---------|----------|------------|
| **Token expiry during long chat sessions** | High | Auto-refresh via `useAuth()`; retry failed requests with new token |
| **CORS + credentials + custom headers** | High | FastAPI: `allow_credentials=True`, explicit `allow_origins`, `allow_headers=["Authorization"]` |
| **Authorized parties mismatch (dev vs prod)** | Medium | Dynamic `AUTHORIZED_PARTIES` from env; validate on startup |
| **Clerk webhook for user deletion not handled** | Medium | Implement `/clerk/webhook` → soft-delete local user + sessions |

### 5. Database Connection Pool Scaling

| Pitfall | Severity | Mitigation |
|---------|----------|------------|
| **Pool exhaustion under concurrent streams** | High | Monitor `pool.checkedout()`; increase `pool_size` based on load test; consider PgBouncer |
| **Stale connections after DB restart** | Medium | `pool_pre_ping=True` (already set); health check endpoint |
| **Transaction leakage from exceptions** | Medium | `expire_on_commit=False` + explicit rollback in exception handlers |

## Operational Pitfalls

### 6. Observability Gaps

| Area | Gap | Fix |
|------|-----|-----|
| **Structured logging** | Only `ai.py` uses structlog | Global structlog config in `main.py`; JSON output; correlation IDs |
| **Request tracing** | None | OpenTelemetry + FastAPI instrumentation; trace SSE streams |
| **Error alerting** | Print to stdout only | Sentry/LogRocket integration; alert on 5xx rate |
| **Usage analytics** | None | PostHog/Plausible for frontend; custom events for chat actions |

### 7. Development Experience

| Issue | Fix |
|-------|-----|
| **Vite proxy + SSE in dev** | `vite.config.ts`: `server.proxy: { '/chat': { target: 'http://localhost:8000', ws: true } }` |
| **Type drift between Pydantic ↔ TypeScript** | `pydantic2ts` or `fastapi-typescript` codegen in CI |
| **Hot reload breaks SSE connections** | Acceptable in dev; document expectation |
| **Clerk localhost vs 127.0.0.1** | Use `http://localhost:4321` consistently; add to `AUTHORIZED_PARTIES` |

## Security Pitfalls

### 8. Prompt Injection via Chat Input

- **Risk:** User crafts input to override venue context instructions
- **Mitigation:** Delimit user messages clearly; system prompt last; input sanitization; monitor for injection patterns

### 9. Session Hijacking

- **Risk:** Stolen Clerk token → access to user's chat history
- **Mitigation:** Short JWT TTL; HTTPS only; `Secure` + `HttpOnly` cookies; implement session revocation endpoint

### 10. Data Leakage Across Venues

- **Risk:** Cross-venue session contamination
- **Mitigation:** Enforce `venue_id` in all session queries; RLS policies; integration tests for isolation

## Recommended Monitoring

```yaml
# Key metrics to track from Day 1
metrics:
  - chat_requests_total{status,venue}
  - chat_tokens_used_total{user,venue,model}
  - chat_stream_duration_seconds{venue}
  - auth_failures_total{reason}
  - db_pool_usage{active,idle}
  - openrouter_cost_usd_daily
  - session_created_total{venue}
  - errors_total{component,type}
```

## Sources

- **SSE production:** WebSocket.org production guide, Vercel AI SDK streaming docs, Cloudflare SSE limits
- **Prompt injection:** arXiv 2606.09204 "Injection Paradox", arXiv 2601.10923 "Hidden-in-Plain-Text", Simon Willison's blog on prompt injection
- **Clerk production:** Clerk security best practices, CORS + credentials RFC
- **Database pooling:** PgBouncer docs, SQLAlchemy async pooling guide, asyncpg performance tuning
- **OpenRouter costs:** OpenRouter pricing page, community discussions on token budgeting
- **Museum AI security:** Centre Pompidou Ask Mona architecture, Musa.guide governance model

---

*Pitfalls research: 2026-09-24*