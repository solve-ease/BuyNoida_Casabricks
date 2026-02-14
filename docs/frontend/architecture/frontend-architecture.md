# Frontend Architecture Blueprint

## 1) Target Folder Structure
```text
src/
  app/
    providers/
    router/
    layouts/
  pages/
    home/
    listings/
    property-detail/
    inquiry/
    auth/
  features/
    guided-discovery/
    property-card/
    property-visuals/
    save-property/
    inquiry-form/
    auth-session/
  entities/
    property/
    user/
    inquiry/
  services/
    api/
      client/
      endpoints/
      interceptors/
      adapters/
    analytics/
    telemetry/
  shared/
    components/
    hooks/
    utils/
    constants/
    styles/
  config/
    env/
    runtime/
  assets/
```

## 2) Layer Responsibilities
- `app`: application shell, providers, routing, top-level composition.
- `pages`: route-level compositions only; no low-level API details.
- `features`: user-facing business capabilities composed from entities/shared.
- `entities`: domain models, mappers, schemas, and simple entity UI.
- `services`: external integrations (API, analytics, telemetry).
- `shared`: reusable generic components, hooks, utilities.
- `config`: environment parsing, defaults, and runtime toggles.

## 3) Import Direction Rules
- Allowed direction: `app -> pages -> features -> entities -> shared`.
- `services` and `config` can be consumed by `features/pages/app` through stable public interfaces.
- No cross-feature deep imports; expose index barrels for public contracts.

## 4) API Client Pattern (Axios)
- Single axios instance in `services/api/client`.
- Request interceptors:
  - attach auth headers (when available),
  - correlation/request IDs,
  - default timeout and content headers.
- Response interceptors:
  - normalize API errors,
  - auth refresh handoff,
  - user-safe error mapping.
- Use `AbortController`; avoid deprecated cancel-token patterns.

## 5) State Strategy
- Server state: React Query.
- Ephemeral UI state: local component state/hooks.
- Session/auth state: dedicated feature module + minimal global context.
- Form state: React Hook Form + Zod schemas.

## 6) Quality Gates
- Every feature provides:
  - route/page composition,
  - API adapter,
  - loading/error/empty states,
  - accessibility checks for primary interactions.
- No feature ships without docs and acceptance criteria.
