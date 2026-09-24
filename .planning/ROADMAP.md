# ROADMAP.md — Galeria Katowicka

**Created:** 2026-09-24
**Mode:** Vertical MVP slices

---

## Phase Overview

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | **Foundation & Auth** | Working Astro + Clerk auth on landing page | AUTH-01 | User lands → sees Clerk SignIn → signs in with Google → sees authenticated state |
| 2 | **Chat Core MVP** | Streaming chat with SSE (no persistence) | CHAT-01 | User sends message → sees tokens stream in real-time → response completes |
| 3 | **Theming & Polish** | Dark/light theme with persistence | UI-01 | User toggles theme → preference persists across refresh → system preference detected |

---

### Phase 1: Foundation & Auth
**Goal:** Working Astro project with Clerk authentication on landing page
**Mode:** mvp
**Requirements:** AUTH-01

**Success Criteria:**
1. **Astro dev server runs** — `astro dev` starts on `http://localhost:4321` without errors
2. **Landing page renders** — Visits `http://localhost:4321` → sees Galeria Katowicka branding + Clerk `<SignIn />` widget
3. **Google sign-in works** — Clicks "Continue with Google" → completes OAuth flow → redirected back to landing page
4. **Authenticated state visible** — After sign-in, sees `<UserButton />` or user email in header
5. **Clerk token accessible** — `useAuth().getToken()` returns valid JWT for API calls

**Technical Tasks:**
- Initialize Astro project in `apps/frontend/` with React + Tailwind integration
- Install `@clerk/clerk-react`, configure `PUBLIC_CLERK_PUBLISHABLE_KEY`
- Create landing page (`src/pages/index.astro`) with `<ClerkProvider>` + `<SignIn client:visible />`
- Add `<UserButton client:visible />` for authenticated users
- Configure Vite proxy for `/api` → `http://localhost:8000` (FastAPI backend)
- Add CORS middleware to FastAPI: `allow_origins=["http://localhost:4321"]`, `allow_credentials=True`

---

### Phase 2: Chat Core MVP
**Goal:** Streaming chat with SSE (no session persistence yet)
**Mode:** mvp
**Requirements:** CHAT-01

**Success Criteria:**
1. **Chat page accessible** — Authenticated user visits `/chat` → sees chat interface
2. **Message sends** — Types message → presses Enter → request sent to `/chat/stream`
3. **Tokens stream in real-time** — Response appears character-by-character via SSE `EventSource`
4. **Stream completes** — Receives `done` event → final message rendered
5. **Error handling** — Network/LLM error shows toast; manual retry works

**Technical Tasks:**
- Create chat page (`src/pages/chat.astro`) with protected route (redirect to `/` if unauthenticated)
- Build React chat island (`src/components/ChatInterface.tsx` with `client:visible`)
- Implement `useChatStream` hook with native `EventSource` + Clerk token injection
- Add message list component with streaming token accumulation
- FastAPI: Ensure `/chat/stream` accepts `Authorization: Bearer` + `ChatHistory` body
- FastAPI: Return `EventSourceResponse` with `streamingResponse` / `done` / `error` events

---

### Phase 3: Theming & Polish
**Goal:** Dark/light theme with persistence
**Mode:** mvp
**Requirements:** UI-01

**Success Criteria:**
1. **Theme toggle visible** — Chat header shows sun/moon icon button
2. **Dark mode works** — Click toggle → entire app switches to dark palette (Tailwind `dark:`)
2. **Light mode works** — Click toggle → entire app switches to light palette
3. **Preference persists** — Refresh page → theme choice remembered (localStorage)
4. **System preference detected** — First visit with no localStorage → respects `prefers-color-scheme`

**Technical Tasks:**
- Add `ThemeProvider` context + `useTheme` hook in React
- Create `ThemeToggle` component in chat header
- Configure Tailwind `darkMode: 'class'` on `<html>` element
- Persist theme to `localStorage` on change; read on mount
- Add CSS variables for consistent theming across Astro + React island

---

## Requirements Coverage

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | 1 | Planned |
| CHAT-01 | 2 | Planned |
| UI-01 | 3 | Planned |

**100% v1 requirements mapped to phases ✓**

---

## Risks & Dependencies

| Risk | Phase | Mitigation |
|------|-------|------------|
| Clerk token expiry during chat | 2 | Auto-refresh in `useAuth`; retry failed requests |
| SSE proxy issues in dev | 2 | Vite proxy config with `ws: true`; test early |
| CORS misconfiguration | 1 | Explicit origins + credentials; test with browser devtools |
| OpenRouter streaming failures | 2 | Error event handling; non-stream fallback |
| Type drift FE/BE | 1-3 | pydantic2ts in CI (deferred to v2) |

---

*Roadmap created: 2026-09-24*