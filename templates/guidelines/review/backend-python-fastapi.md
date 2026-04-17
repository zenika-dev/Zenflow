# Backend Review Guidelines (Python + FastAPI)

Purpose: define backend-specific review checklist for FastAPI backend changes.

## Scope

Apply this file when reviewing FastAPI backend handovers or FastAPI backend files.

## Backend Checklist

### Security
- [ ] No hardcoded secrets, tokens, or passwords in source files
- [ ] Request validation is enforced with Pydantic models
- [ ] No unsafe raw SQL composition with untrusted input
- [ ] Sensitive data is not logged
- [ ] API errors do not leak stack traces or internal details

### FastAPI Quality
- [ ] Routers are thin; business logic is in service layer
- [ ] Persistence logic is isolated to repository/data layer
- [ ] Response models are explicit and stable
- [ ] Dependency injection patterns are consistent with project style
- [ ] Error handling is consistent across endpoints

### Testing
- [ ] New or changed logic has TestClient integration test coverage
- [ ] Edge cases are covered (invalid input, not found, constraints)
- [ ] Dependencies are mocked via `app.dependency_overrides` where appropriate
- [ ] Tests verify behavior, not private internals
- [ ] Test names clearly describe behavior or test case

## Output Policy

The canonical Code Review Report format and status rules are defined in `@.github/agents/reviewer.agent.md`.
This file defines backend review criteria only.
