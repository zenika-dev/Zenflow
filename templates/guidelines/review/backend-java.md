# Backend Review Guidelines (Java)

Purpose: define backend-specific review checklist for Java backend changes.

## Scope

Apply this file when reviewing Java backend handovers or Java backend files.

## Backend Checklist

### Security
- [ ] No hardcoded secrets, tokens, or passwords in source files
- [ ] Request/input validation is present on external inputs
- [ ] No raw SQL string concatenation with untrusted input
- [ ] Sensitive data is not logged
- [ ] No sensitive implementation details leaked in client-facing errors

### Java + Spring Quality
- [ ] Controllers stay thin; business logic is in service/use-case layer
- [ ] Data access is isolated to repository/data access layer
- [ ] Validation annotations and exception handlers are used consistently
- [ ] Transaction boundaries are explicit where needed
- [ ] Package and naming conventions match the project

### Testing
- [ ] New or changed service logic has test coverage (service-layer integration or unit tests)
- [ ] Edge cases are covered (invalid input, not found, constraints)
- [ ] Tests verify behavior, not private implementation details
- [ ] Test names clearly describe behavior
- [ ] Controller tests are present only if explicitly planned or user-requested
- [ ] Repository tests are present only if custom queries exist or explicitly planned

## Output Policy

The canonical Code Review Report format and status rules are defined in `@.github/agents/reviewer.agent.md`.
This file defines backend review criteria only.
