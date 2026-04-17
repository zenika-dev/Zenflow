# Frontend Review Guidelines (React)

Purpose: define frontend-specific review checklist for React frontend changes.

## Scope

Apply this file when reviewing React frontend handovers or React frontend files.

## Frontend Checklist

### Security
- [ ] No dangerous raw HTML rendering without sanitization
- [ ] No API keys, tokens, or secrets in frontend source
- [ ] User-provided content is handled safely
- [ ] No sensitive data in logs

### React + TypeScript Quality
- [ ] Props and data contracts are typed per project conventions
- [ ] Loading, error, and success states are handled
- [ ] Hook dependencies and effects are stable and intentional
- [ ] API configuration follows project conventions (no hardcoded base URLs where disallowed)
- [ ] Changes align with architecture-frontend conventions

### Accessibility
- [ ] Inputs have labels or equivalent accessible naming
- [ ] Interactive controls have meaningful accessible names
- [ ] Error messaging is perceivable and announced where needed
- [ ] Color is not the only state indicator

### Testing
- [ ] Components and integration points have test coverage
- [ ] API calls are mocked when appropriate
- [ ] Loading/error/success states are tested

## Output Policy

The canonical Code Review Report format and status rules are defined in `@.github/agents/reviewer.agent.md`.
This file defines frontend review criteria only.
