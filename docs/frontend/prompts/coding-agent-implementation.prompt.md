You are the coding agent for CasaBricks BuyNoida frontend.

## Objective
Implement the frontend incrementally using the architecture and phase plan in:
- `docs/frontend/project.md`
- `docs/frontend/architecture/frontend-architecture.md`
- `docs/frontend/phases/implementation-plan.md`
- `docs/srs.md`

## Mandatory Constraints
1. Keep implementation modular. Do not implement major flows in a single file.
2. Follow folder boundaries and import direction rules from architecture doc.
3. Use React + Vite + Tailwind existing setup; avoid unnecessary framework changes.
4. Use Axios for API communication through a centralized client instance.
5. Respect environment-based config and logging strategy.
6. Keep AI-enhanced image disclosure and disclaimer behavior compliant with SRS.
7. Keep docs updated in `docs/**` as features are implemented.

## Implementation Order
1. **Phase 0**: app reset, route shell, env config module, logger module, axios client scaffold.
2. **Phase 1**: home hero and 3-step guided discovery flow.
3. **Phase 2**: Noida-only listings with visual cards and AI label support.
4. **Phase 3**: property detail with required disclaimer and original-image availability.
5. **Phase 4**: visual analytics widgets and mini-map.
6. **Phase 5**: inquiry/callback/save property flows.
7. **Phase 6**: performance/accessibility/security hardening.

## Per-Task Definition of Done
- Clear feature boundary (component/hook/service separation).
- Loading, error, and empty states present.
- Input validation and safe error messaging applied.
- Logs include module context and avoid sensitive data leakage.
- Documentation section updated for the feature.

## API & Auth Guidelines
- Assume backend exposes OpenAPI/Swagger contract.
- Use auth-ready axios interceptors and token refresh placeholders.
- Keep auth implementation adaptable to backend finalization.

## Dependency Guardrail
Before adding any package:
1. Check npm package health and active maintenance.
2. Avoid deprecated APIs in documentation examples.
3. Record dependency choice and reason in frontend docs.

## Security Baseline
- Do not log tokens or PII.
- Sanitize/escape untrusted display fields.
- Do not bypass guarded routes for protected actions.
- Maintain visible AI image disclaimers and labels.

## Output Expectations
For each phase, produce:
- File change summary,
- Remaining risks/open questions,
- Suggested next phase tasks.
