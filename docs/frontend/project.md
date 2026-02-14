# CasaBricks BuyNoida Frontend Project Plan

## 1) Purpose
This document defines the frontend implementation approach for CasaBricks (BuyNoida) based on [docs/srs.md](../srs.md). It converts SRS requirements into an executable, modular, and maintainable plan for a React + Vite + Tailwind application integrated with a REST API backend (implemented by another team).

## 2) Scope Boundary (Frontend)
### In Scope
- Responsive web frontend (mobile-first) for visitors and authenticated users.
- Guided 3-question discovery flow (budget, property type, preference).
- Noida-only property listing and detail experiences.
- AI-enhanced image labeling and disclaimer UX.
- Visual analytics UI (compass/meters, price-vs-area chart, nearby amenities mini-map).
- Inquiry/callback/save-property flows.
- API integration layer and environment-based configuration.
- Logging/observability abstraction with environment-tier behavior.

### Out of Scope
- Backend API implementation.
- AI image generation pipeline implementation.
- Database and admin backend services.
- Infrastructure provisioning and SRE operations.

## 3) Product Requirements Traceability (Frontend)
| SRS Area | Frontend Requirement | Planned Output |
|---|---|---|
| Home Hero | Interactive visual hero section | Hero module in home page |
| Guided Selection | 3-step guided questionnaire, no classic filters | Wizard component + results handoff |
| Listing | Noida-only cards, AI-enhanced marker, key metrics | Listing page + card system |
| Detail AI Image | One enhanced front image and original visibility | Image gallery + badge + disclosure component |
| Disclaimer | Permanent disclaimer on detail page; visible indicator elsewhere | Disclosure widget with non-removable block |
| Visual Data | Compass, heat/vastu/light meters, price/area chart, mini-map | Dedicated visualization components |
| Inquiry/Leads | Inquiry form, callback request, save property | Form modules + API adapters |
| NFR Performance | ≤3s load target, fast visual rendering | Performance budget + lazy loading plan |
| NFR Security | Authn/authz, encrypted transit assumptions | Secure client patterns + guardrails |
| NFR Usability | Mobile-first, low-effort discovery | Responsive-first design system |

## 4) Technical Stack (Proposed)
### Existing (already in repository)
- React 19 + Vite 7 + Tailwind CSS 4
- ESLint 9 (flat config)

### Add for implementation
- `axios` for HTTP client.
- `@tanstack/react-query` for server-state caching and retries.
- Routing strategy: prefer `react-router` (modern package) while allowing `react-router-dom` if needed for migration compatibility.
- `react-hook-form` + `zod` for scalable validated forms.
- Charts: `recharts` for price/area and dashboard indicators.
- Map: `leaflet` + `react-leaflet` for amenities mini-map.
- Logging: custom logger facade (`debug/info/warn/error/audit`) with env policies.

### Deprecation/Compatibility Notes
- npm package pages were checked for core candidates; no package-level deprecation banner was observed for selected libraries.
- `react-router-dom` currently states it re-exports from `react-router`; prefer new imports from `react-router` to avoid future migration churn.
- Axios docs indicate legacy `CancelToken` and some APIs are deprecated; use `AbortController` and modern patterns.

## 5) Architecture Principles
- Feature-first modular structure; avoid monolithic files.
- Shared primitives in `src/shared` and domain logic in `src/features`/`src/entities`.
- Strict separation: UI components, business logic hooks, API services, and config.
- Environment-driven behavior (logging level, API base URL, feature toggles).
- Secure defaults: minimal PII logs, defensive error handling, token handling rules.
- Documentation-first changes for every major feature phase.

## 6) Configuration Management Requirements
- Centralized environment schema (required/optional vars, validation at boot).
- Environment tiers: `development`, `staging`, `production`.
- Config categories:
  - API (`API_BASE_URL`, timeout, retry policy).
  - Logging (`LOG_LEVEL`, remote logging toggle).
  - Feature flags (`ENABLE_MAP`, `ENABLE_SAVE_PROPERTY`, etc.).
  - Security (`AUTH_STRATEGY`, cookie/token mode flags).
- Never hardcode secrets in frontend code.

## 7) Logging & Observability Requirements
- Dev: verbose console diagnostics enabled.
- Staging: structured logs + warning/error telemetry hooks.
- Production: sanitized logs, no sensitive payloads, audit events only where needed.
- Required log context fields: `timestamp`, `level`, `module`, `action`, `requestId` (if present).
- PII rules: redact phone/email/token fields before output.

## 8) Security Baseline (Frontend)
- Treat auth as backend-driven JWT access/refresh flow.
- Prefer secure transport (`https`) and never persist sensitive data unnecessarily.
- Guard protected routes and fail closed on auth uncertainty.
- Use safe rendering patterns to avoid XSS (no unsafe HTML rendering without sanitation).
- Add CSRF strategy if cookies are used by backend.
- Ensure AI-enhanced media is clearly labeled as non-original representation.

## 9) Collaboration and Maintainability Rules
- Keep docs in `docs/**` as source of truth.
- Keep components small and reusable; single responsibility per module.
- Enforce naming conventions and import boundaries.
- Each phase must define acceptance criteria and Definition of Done.
- Avoid adding unapproved dependencies without compatibility review.

## 10) Immediate Next Outputs
- Detailed implementation phases document.
- Coding-agent execution prompt with task-level acceptance criteria.
- Folder architecture specification for multi-team collaboration.
