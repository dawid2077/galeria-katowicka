# REQUIREMENTS.md — Galeria Katowicka v1

**Last updated:** 2026-09-24 after initialization

---

## v1 Requirements

### Authentication

- [ ] **AUTH-01**: Clerk Google sign-in widget on landing page — Users can authenticate via Google OAuth using Clerk's pre-built `<SignIn />` component

### Chat Core

- [ ] **CHAT-01**: Streaming token delivery (SSE) — Character-by-character response rendering via Server-Sent Events from FastAPI `/chat/stream` endpoint

### UI/UX

- [ ] **UI-01**: Dark/light theme — User preference persisted in localStorage; CSS variables for theming; system preference detection

---

## v2 Requirements (Deferred)

### Session & History

- [ ] **SESS-01**: Session persistence & history — Conversations survive refresh, device switch, app restart
- [ ] **SESS-02**: Conversation search & filtering — Full-text search on message content; date/venue filters
- [ ] **SESS-03**: Conversation management — Rename, delete, archive, pin, folder/organize

### Venue Features

- [ ] **VENUE-01**: Venue context injection (RAG-lite) — System prompt with curated venue Markdown (< 4k tokens/venue)
- [ ] **VENUE-02**: Per-venue session isolation — Compound key `user_id + venue_id`; separate context windows
- [ ] **VENUE-03**: Venue selector / context switcher — Switch context; loads venue-scoped session
- [ ] **VENUE-04**: Visit planning & ticketing integration — Deep links to bilety.muzeumslaskie.pl, nospr.org.pl

### Chat Core (Extended)

- [ ] **CHAT-02**: Typing/streaming indicators — Animated dots, token counter, "thinking" states
- [ ] **CHAT-03**: Message regeneration — Branching UI to compare variants; one-click regenerate
- [ ] **CHAT-04**: Copy/export/share messages — Copy button per message; export conversation as JSON/Markdown

### UI/UX (Extended)

- [ ] **UI-02**: Mobile-responsive chat UI — Touch-friendly; virtual keyboard handling; bottom-sheet patterns
- [ ] **UI-03**: Accessibility (WCAG 2.1 AA) — Semantic HTML; ARIA live regions for streaming; focus management
- [ ] **UI-04**: Error handling with retry — Toast notifications; auto-retry with backoff; manual retry button

### Differentiators

- [ ] **DIFF-01**: Multi-language responses — 40+ languages via system prompt
- [ ] **DIFF-02**: Multilingual audio/hands-free mode — TTS (ElevenLabs, OpenAI TTS); STT for questions
- [ ] **DIFF-03**: No-app-required (PWA) — QR/web access; service worker for offline venue context
- [ ] **DIFF-04**: Curator-controlled knowledge base — CMS for venue markdown; versioned prompts; guardrails

---

## Out of Scope

| Exclusion | Reason |
|-----------|--------|
| Open-web RAG / internet search | Hallucination risk; venue wants controlled narrative; brand safety |
| Persistent cross-venue memory (default) | Privacy: Muzeum Śląskie visit shouldn't leak to Strefa Kultury session |
| User-generated content in knowledge base | Accuracy risk; curatorial authority |
| Real-time translation of live human speech | Latency, accuracy, privacy; not core chat value |
| Social features (share to feed, comments, likes) | Distraction from visit; privacy; moderation burden |
| Gamification (badges, points, leaderboards) | Undermines contemplative cultural experience |
| AI-generated images of exhibits | Copyright, authenticity, misrepresentation |
| Autonomous agent actions (book tickets, pay) | Liability, error cost, user trust |
| Spatial/location awareness (indoor positioning) | Requires venue infrastructure (BLE beacons, WiFi RTT, QR zones) |
| Exhibit/artwork visual recognition | Requires vision API; high complexity; validate demand first |
| Guided tour + live chat hybrid | Requires state machine for tour steps; high complexity |
| Venue analytics dashboard | Build after usage data exists; GDPR/RODO compliance needed |
| Cross-venue context (cultural district) | Requires multi-venue governance agreement |

---

## Traceability

| Requirement | Phase | Plan | Verification |
|-------------|-------|------|--------------|
| AUTH-01 | 1 | TBD | Manual: Sign in with Google on landing |
| CHAT-01 | 2 | TBD | Automated: SSE stream returns tokens |
| UI-01 | 3 | TBD | Manual: Theme toggle persists |

---

*Requirements defined: 2026-09-24*