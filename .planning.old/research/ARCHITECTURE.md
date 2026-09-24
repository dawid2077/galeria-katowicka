# Architecture Research

**Domain:** Astro Frontend + FastAPI Backend Integration for AI Chat
**Researched:** 2026-09-24

## Recommended Architecture

### High-Level Pattern: Separated Frontend/Backend (Dev) → Monorepo (Prod)

```
galeria-katowicka/
├── apps/
│   ├── frontend/          # Astro app
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── ChatInterface.tsx    # Interactive island
│   │   │   │   ├── MessageList.tsx      # Streaming message display
│   │   │   │   ├── SessionSidebar.tsx   # History sidebar
│   │   │   │   ├── VenueSelector.tsx    # Venue context switcher
│   │   │   │   └── ClerkAuth.tsx        # Sign in/up widget
│   │   │   ├── pages/
│   │   │   │   ├── index.astro          # Landing + auth
│   │   │   │   └── chat.astro           # Authenticated chat page
│   │   │   ├── hooks/
│   │   │   │   ├── useChatStream.ts     # SSE hook
│   │   │   │   └── useAuth.ts           # Clerk auth hook
│   │   │   ├── lib/
│   │   │   │   └── api.ts               # API client with auth
│   │   │   └── styles/
│   │   │       └── global.css           # Tailwind + custom
│   │   ├── astro.config.mjs
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   └── backend/           # Existing FastAPI app (app/)
│       ├── app/
│       ├── configs/
│       ├── pyproject.toml
│       └── uv.lock
│
├── packages/
│   └── shared/            # Shared types (optional)
│       ├── schemas.ts     # Generated from Pydantic
│       └── api-contract.ts
│
├── docker-compose.yml
├── turbo.json (if Turborepo)
└── package.json (root)
```

### Data Flow

```
┌─────────────┐     SSE/HTTP      ┌─────────────┐
│   Astro     │ ◄──────────────►  │  FastAPI    │
│  (Browser)  │                   │  (Server)   │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│   Clerk     │                   │ PostgreSQL  │
│  (Auth)     │                   │ (Sessions)  │
└─────────────┘                   └─────────────┘
```

### Key Integration Points

| Integration | Pattern | Implementation |
|-------------|---------|----------------|
| **Auth (Frontend)** | Clerk React SDK | `<SignIn />`, `<UserButton />`, `useAuth()` |
| **Auth (Backend)** | Clerk Backend API | `clerk.authenticate_request()` + `get_current_user()` |
| **Token Forwarding** | Header injection | `fetch()` interceptor adds `Authorization: Bearer` |
| **SSE Streaming** | Native EventSource | React `useEffect` with `EventSource` cleanup |
| **CORS** | FastAPI middleware | `allow_origins=["http://localhost:4321"]`, `allow_credentials=True` |
| **Venue Context** | System prompt injection | Backend reads `app/context/*.md` → prepends to LLM messages |

### Development vs Production

| Environment | Frontend | Backend | Proxy |
|-------------|----------|---------|-------|
| **Dev** | `astro dev` (port 4321) | `uv run fastapi dev` (port 8000) | Vite proxy `/api` → `localhost:8000` |
| **Prod** | Static build + Netlify/Vercel | Docker container + Cloud Run/Fly.io | Nginx/Traefik reverse proxy |

### Clerk Integration Details

**Frontend (Astro):**
- `PUBLIC_CLERK_PUBLISHABLE_KEY` in `.env`
- `<ClerkProvider>` wraps app/layout
- `<SignIn />` on landing page
- `<UserButton />` in chat header
- `useAuth()` → `getToken()` for API calls

**Backend (FastAPI):**
- `CLERK_SECRET_KEY`, `CLERK_PUBLIC_KEY` in `configs/.env`
- `AUTHORIZED_PARTIES` = `[frontend_origin]`
- `get_current_user()` dependency extracts `sub`, `email`
- `UserMethods.get_or_create_user()` syncs to PostgreSQL

### SSE Handling in Astro Island

```tsx
// src/hooks/useChatStream.ts
export function useChatStream(messages: ChatMessage[], venueId: string) {
  const [streamingContent, setStreamingContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  
  const sendMessage = async (content: string) => {
    setIsStreaming(true);
    setStreamingContent('');
    
    const token = await getToken(); // Clerk
    const eventSource = new EventSource(
      `${API_URL}/chat/stream?venue_id=${venueId}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    eventSource.addEventListener('streamingResponse', (e) => {
      setStreamingContent(prev => prev + e.data);
    });
    
    eventSource.addEventListener('done', (e) => {
      // Save complete message to state
      eventSource.close();
      setIsStreaming(false);
    });
    
    eventSource.onerror = () => {
      eventSource.close();
      setIsStreaming(false);
    };
    
    // POST the message
    await fetch(`${API_URL}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ conversation: [...messages, { role: 'user', content }] })
    });
  };
  
  return { streamingContent, isStreaming, sendMessage };
}
```

### Deployment Strategy

**Option A: Separate Deployments (Recommended for MVP)**
- Frontend: Vercel/Netlify (static + edge functions)
- Backend: Fly.io/Cloud Run/Railway (containerized FastAPI)
- Database: Neon/PostgreSQL managed
- Auth: Clerk (managed)

**Option B: Monorepo + Single Container**
- Build Astro → static files served by FastAPI (starlette StaticFiles)
- Single Dockerfile, single deploy
- Simpler but less flexible scaling

## Sources

- Astro 5 deployment guides (Vercel, Netlify, Docker)
- Clerk Astro integration guide + React SSR docs
- FastAPI CORS + SSE production patterns
- OpenRouter streaming API reference
- Turborepo / Nx monorepo patterns for Astro + Python