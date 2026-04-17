# Backend Review Guidelines (Go + Gin)

Purpose: define backend-specific review checklist for Go backend changes.

## Scope

Apply this file when reviewing Go backend handovers or Go backend files.

## Backend Checklist

### Security
- [ ] No hardcoded secrets, tokens, or passwords in source files
- [ ] Request and path/query input validation is present
- [ ] No SQL concatenation with untrusted input
- [ ] Sensitive data is not logged
- [ ] API errors do not leak internal implementation details

### Go Quality
- [ ] Handlers are thin and delegate business logic to services/use-cases
- [ ] Data access is isolated to repository/store layer
- [ ] Context usage and timeouts are handled consistently
- [ ] Errors are wrapped/handled consistently and returned with stable API shapes
- [ ] Package layout and naming follow project conventions

### Testing
- [ ] New or changed logic has handler test coverage using table-driven patterns
- [ ] Tests use `net/http/httptest` for request/response mocking
- [ ] Edge cases are covered (invalid input, not found, constraints)
- [ ] Tests verify behavior, not internal implementation details
- [ ] Test names clearly describe the test case
- [ ] Data access layer tests are present only if custom SQL queries exist or explicitly planned

## Output Policy

The canonical Code Review Report format and status rules are defined in `@.github/agents/reviewer.agent.md`.
This file defines backend review criteria only.
