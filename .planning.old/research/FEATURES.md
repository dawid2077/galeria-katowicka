# Feature Landscape

**Domain:** AI Chat Application for Cultural Venues (Museums, Cultural Districts)
**Researched:** 2026-09-24

## Table Stakes

Features users expect from any AI chat application in 2024–2025. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Streaming token delivery** | Users expect character-by-character response rendering (ChatGPT, Claude standard) | Medium | SSE or WebSocket; abort/regenerate support required |
| **Session persistence & history** | Conversations must survive refresh, device switch, app restart | Medium | Database-backed; JSON or structured message storage |
| **User authentication** | Personal history, preferences, multi-device sync | Low | Clerk/Google OAuth standard; JWT verification |
| **Typing/streaming indicators** | Visual feedback during AI generation prevents perceived hangs | Low | Animated dots, token counter, "thinking" states |
| **Message regeneration** | Users retry failed/unsatisfactory responses | Medium | Branching UI to compare variants; one-click regenerate |
| **Conversation search & filtering** | History grows; users need to find past topics | Medium | Full-text search on message content; date/venue filters |
| **Multi-language UI & responses** | Global audiences; 40+ languages table stakes for cultural venues | Medium | i18n framework; LLM handles output language via prompt |
| **Copy/export/share messages** | Users share insights, save references | Low | Copy button per message; export conversation as JSON/Markdown |
| **Dark/light theme** | Accessibility & user preference standard | Low | CSS variables; persist preference |
| **Error handling with retry** | Network/LLM failures common; graceful degradation expected | Low | Toast notifications; auto-retry with backoff; manual retry button |
| **Conversation management** | Rename, delete, archive, pin, folder/organize | Medium | Sidebar with drag-drop; project/workspace grouping (ChatGPT Projects pattern) |
| **Mobile-responsive chat UI** | Majority of venue visitors use phones on-site | Medium | Touch-friendly; virtual keyboard handling; bottom-sheet patterns |
| **Accessibility (WCAG 2.1 AA)** | Public sector venues legally required; screen readers, contrast, keyboard nav | Medium | Semantic HTML; ARIA live regions for streaming; focus management |

## Differentiators

Features that set a cultural venue chat app apart from generic AI chat. Not expected, but highly valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Venue context injection (RAG-lite)** | AI knows current venue, exhibits, hours, tickets without user prompting | Medium | System prompt injection with curated venue markdown; < 4k tokens per venue |
| **Per-venue session isolation** | Chat history scoped to venue; Muzeum Śląskie session ≠ Strefa Kultury session | Medium | Compound key: `user_id + venue_id`; separate context windows |
| **Spatial/location awareness** | AI adapts responses based on visitor's gallery/room/zone | High | Requires indoor positioning (BLE beacons, WiFi RTT, QR zones) or manual zone selection |
| **Exhibit/artwork visual recognition** | Photo of artwork → instant context, audio, related info | High | On-device or cloud vision API; integrate with chat as multimodal input |
| **Visit planning & ticketing integration** | "Book tickets for Tuesday 2pm" → deep link to ticketing; itinerary builder | Medium | API integration with venue ticketing (bilety.muzeumslaskie.pl, nospr.org.pl); calendar export |
| **Guided tour + live chat hybrid** | Structured narrative path + free-form Q&A; context persists across tour stops | High | State machine for tour steps; "continue tour" / "ask question" modes |
| **Curator-controlled knowledge base** | Venue owns facts; no hallucination from open web; instant content updates | Medium | CMS for venue markdown; versioned prompts; guardrails/citations |
| **Multilingual audio/hands-free mode** | Visitors listen while looking at exhibits; 40+ languages from single source | High | TTS (ElevenLabs, OpenAI TTS); speech-to-text for questions; background audio playback |
| **No-app-required (QR/web)** | Zero friction; scan QR at entrance → instant chat in browser | Low | PWA with service worker; works offline for cached venue context |
| **Accessibility-first personas** | Kid-friendly, audio-described, simplified language, sign language avatar | High | Persona system in system prompt; curated simplified content variants |
| **Venue analytics dashboard** | Curators see top questions, confusing exhibits, dwell time, language distribution | Medium | Anonymous aggregation; GDPR-compliant; export for reporting |
| **Cross-venue context (cultural district)** | Strefa Kultury: chat carries context between Muzeum Śląskie, NOSPR, MCK, Spodek | High | Shared session namespace; venue-hopping context transfer; district-wide itinerary |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Open-web RAG / internet search** | Hallucination risk; venue wants controlled narrative; brand safety | Curated venue markdown only; explicit "I don't know" for out-of-scope |
| **Persistent cross-venue memory (default)** | Privacy: Muzeum Śląskie visit shouldn't leak to Strefa Kultury session | Opt-in only; explicit "link my visits" user action; separate sessions by default |
| **User-generated content in knowledge base** | Accuracy risk; curatorial authority | Staff-only CMS; visitor feedback → curator review queue |
| **Real-time translation of live human speech** | Latency, accuracy, privacy; not core chat value | Pre-translated venue content; TTS in 40+ languages |
| **Social features (share to feed, comments, likes)** | Distraction from visit; privacy; moderation burden | Private "save to my notes"; export for personal use |
| **Gamification (badges, points, leaderboards)** | Undermines contemplative cultural experience | Subtle progress: "You've explored 3 of 5 galleries" |
| **AI-generated images of exhibits** | Copyright, authenticity, misrepresentation | Use venue-approved photography only |
| **Autonomous agent actions (book tickets, pay)** | Liability, error cost, user trust | Deep links to ticketing with pre-filled params; user confirms purchase |

## Feature Dependencies

```
User Authentication
    └── Session Persistence (per user)
            └── Per-Venue Session Isolation (user_id + venue_id)
                    ├── Venue Context Injection (RAG-lite)
                    │       └── Guided Tour + Live Chat Hybrid
                    ├── Visit Planning & Ticketing Integration
                    ├── Spatial Awareness (requires venue map + positioning)
                    │       └── Exhibit Visual Recognition (requires vision API)
                    └── Multilingual Audio Mode (requires TTS + STT)
                            └── Accessibility Personas
Venue Analytics Dashboard ← aggregates from all venue sessions
Cross-Venue Context (Cultural District) ← requires per-venue isolation + opt-in linking
```

## MVP Recommendation

**Prioritize (Phase 1 — Core Chat + Venue Context):**
1. **Streaming chat with SSE** — OpenRouter + FastAPI `EventSourceResponse` (already in codebase)
2. **Clerk/Google authentication** — `authClerk.py` + `UserMethods.get_or_create_user` (already in codebase)
3. **Per-venue session persistence** — Extend `SessionModel` with `venue_id`; JSON `chat_history` per session
3. **Venue context injection (RAG-lite)** — System prompt with `MuzeumSlaskie.md` / `StrefaKultury.md` content
4. **Venue selector in UI** — Switch context; loads new session or creates venue-scoped session
5. **Basic conversation history** — Sidebar with session list; rename/delete

**Defer to Phase 2 (Visit Experience):**
- **Visit planning & ticketing deep links** — Requires venue API partnerships
- **Spatial awareness / zone selection** — Requires venue map data + positioning strategy
- **Multilingual audio mode** — Requires TTS integration; high value but separable
- **Exhibit visual recognition** — High complexity; validate demand first

**Defer to Phase 3 (District Intelligence):**
- **Cross-venue context (Strefa Kultury district)** — Requires multi-venue governance agreement
- **Curator CMS for knowledge base** — Build after validating content update frequency
- **Analytics dashboard** — Build after usage data exists

## Sources

- **Table stakes patterns:** Vercel AI SDK chatbot persistence guide, Vapi session management docs, Microsoft Agent Framework chat history patterns, OpenAI community discussions on conversation management (2024–2025)
- **Museum chatbot differentiators:** Musa.guide (AI-native audio guide, spatial awareness, 40+ languages, curator governance), Amuseapp (multilingual chatbot, animations, donations), Ask Mona / Centre Pompidou (visual recognition, web app, 17k users/2mo), Qarts.ai (AI audio/video guides), ChatLab (80+ languages), ACM IMX 2025 "Experiencing Art Museum with Generative AI Chatbot", CHI 2025 "Exploring User Preferences for Museum Guides", MuseumNext 2025 "How Museums Can Use ChatGPT"
- **Session management:** Vapi `previousChatId` vs `sessionId` patterns, Gemini CLI project-scoped sessions (30-day retention), Amazon Bedrock Session Management APIs (2025), Microsoft Agent Framework client-managed vs service-managed storage
- **RAG-lite vs full RAG:** OpenAI community "context injection vs RAG tools" (Sep 2025), Redis blog "RAG vs Large Context Window", arXiv 2606.09204 "Injection Paradox" (indirect prompt injection risks in RAG), arXiv 2601.10923 "Hidden-in-Plain-Text" benchmark
- **Streaming UI patterns:** Tajaddin/streaming-chat-ui (React + SSE, incremental markdown, abort/regenerate, branching), GetStream typing indicator docs (debounce, timeout, aggregation), WebSocket.org production chat guide (message ordering, presence, reconnection)
- **Multi-tenant isolation:** MUXI user isolation (compound user IDs, PostgreSQL row-level), Stream Chat multi-tenant mode (teams, channel isolation), CometChat multi-tenancy (apps per tenant), IEEE "End-to-End Contextual Isolation for Large-Scale Multi-Tenant" (2026)
- **User expectations for venue chat:** Museum websites (British Museum, London Museum, Museum of Science, Albuquerque Museum) — planning pages emphasize hours, tickets, accessibility, floorplans, events; iMuseumA context-aware system (location, interests, expertise level); MuseumNext 2025 use cases (24/7 visitor support, personalized guides, multilingual, visit planning)