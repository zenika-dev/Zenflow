# Frontend Review Guidelines (Next.js App Router)

Purpose: define frontend-specific review checklist for Next.js App Router frontend changes.

## Scope

Apply this file when reviewing Next.js frontend handovers or Next.js frontend files.

## Frontend Checklist

### Security
- [ ] No API keys, tokens, or secrets in frontend source
- [ ] No unsafe HTML rendering without sanitization
- [ ] User-provided content is handled safely
- [ ] No sensitive data in logs

### Next.js App Router Quality
- [ ] Server versus client component choice is intentional and justified
- [ ] Data fetching strategy is consistent with project conventions
- [ ] Route handlers and page logic are separated clearly where appropriate
- [ ] Loading and error boundaries are present where UX requires them
- [ ] Caching and revalidation behavior is explicit and appropriate

### Accessibility
- [ ] Inputs have labels or equivalent accessible naming
- [ ] Interactive controls have meaningful accessible names
- [ ] Error messaging is perceivable and announced where needed
- [ ] Color is not the only state indicator

### Testing
- [ ] Components and integration points have test coverage
- [ ] API calls are mocked where appropriate
- [ ] Loading/error/success states are tested

## Output Policy

The canonical Code Review Report format and status rules are defined in `@.github/agents/reviewer.agent.md`.
This file defines frontend review criteria only.
