# Technology Stack Research

**Domain:** AI Chat Application with Astro + Clerk + FastAPI + OpenRouter
**Researched:** 2026-09-24

## Recommended Stack (with versions)

| Layer | Package | Version | Notes |
|-------|---------|---------|-------|
| **Frontend Framework** | Astro | 5.x | Static-first, islands for chat component |
| **UI Library** | React | 19.x | For interactive chat island (`client:visible`) |
| **Styling** | Tailwind CSS | 4.x | Utility-first, dark mode, responsive |
| **Authentication** | @clerk/clerk-react | 5.x | Clerk React SDK for widget + hooks |
| **Auth Backend** | clerk-backend-api | 7.x | Already in backend (FastAPI) |
| **State Management** | Zustand / React Context | - | Lightweight session/chat state |
| **SSE Client** | EventSource (native) | - | Browser API for streaming |
| **Type Safety** | TypeScript | 5.x | Strict mode across frontend/backend |
| **Build Tool** | Vite (via Astro) | 6.x | Fast HMR, optimized builds |
| **Package Manager** | pnpm / npm | - | Monorepo-friendly if needed |
| **Backend (Existing)** | FastAPI | 0.110+ | Keep current |
| **Backend (Existing)** | SQLAlchemy | 2.0.x | Keep current |
| **Backend (Existing)** | asyncpg | 0.31+ | Keep current |
| **Backend (Existing)** | openai | 3.x | OpenRouter client |
| **Backend (Existing)** | structlog | 26.x | Keep current |
| **Database** | PostgreSQL | 18 | Keep current |

## Integration Patterns

### Clerk + Astro (Frontend)
```astro
--- 
// src/pages/index.astro
import { ClerkProvider, SignIn, SignUp } from '@clerk/clerk-react';
import { client:visible } from 'astro:components';
---
<ClerkProvider publishableKey={import.meta.env.PUBLIC_CLERK_PUBLISHABLE_KEY}>
  <SignIn client:visible />
</ClerkProvider>
```

### Clerk Token → FastAPI (Backend)
```python
# Frontend gets token via Clerk hook
const token = await window.Clerk.session.getToken();

// FastAPI expects Authorization: Bearer <token>
fetch('/chat/stream', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

### SSE Streaming in Astro Island (React)
```tsx
// src/components/ChatStream.tsx
useEffect(() => {
  const eventSource = new EventSource('/chat/stream', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  eventSource.addEventListener('streamingResponse', (e) => {
    appendToken(JSON.parse(e.data));
  });
  
  eventSource.addEventListener('done', () => { /* complete */ });
  eventSource.addEventListener('error', () => { /* handle */ });
  
  return () => eventSource.close();
}, [conversation]);
```

## Known Incompatibilities / Gotchas

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Astro 5 + React 19 | React 19 concurrent features may conflict with Astro islands | Use `client:visible` or `client:idle`; avoid `client:only` unless needed |
| Clerk React 5 + Astro | ClerkProvider must wrap entire app or specific islands | Wrap in layout.astro or per-island |
| SSE + Astro dev server | Vite proxy needed for `/chat/stream` in dev | Configure `vite.config.ts` proxy to FastAPI |
| CORS + credentials | Clerk cookies + custom headers need proper CORS | FastAPI: `allow_credentials=True`, explicit origins |
| OpenRouter streaming | Some models don't stream; fallback needed | Check model capabilities; implement non-stream fallback |
| TypeScript shared types | Frontend/backend schema drift | Generate types from Pydantic schemas (pydantic2ts) |

## Migration Paths

- **From current backend:** No breaking changes needed; add CORS, ensure SSE works with proxy
- **Astro 4 → 5:** Update config; check island hydration behavior
- **Clerk React 4 → 5:** Update imports; `useAuth()` → `useUser()` hooks changed

## Sources

- Astro 5 docs: islands, integrations, deployment
- Clerk React SDK docs: Astro guide, SSR support
- FastAPI streaming: SSE Starlette, CORS middleware
- OpenRouter docs: model streaming support, rate limits
- Vercel AI SDK patterns (for chat UI reference)