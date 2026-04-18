# Backend Architecture Guidelines (Go + Gin)

Purpose: backend single source of truth for architecture, implementation order, testing, and backend handover format.

## Stack Profile

- Language: Go 1.22+
- Framework: Gin
- Data: SQL database via `database/sql`, sqlc, GORM, or project standard

## Project Structure Expectations

- Keep HTTP handlers thin and focused on transport concerns.
- Keep business logic in service/use-case packages.
- Keep persistence in repository/store packages.
- Keep DTOs/models and mapping logic explicit.
- Follow project conventions for package layout and naming.

## API and Validation Conventions

- Validate request payloads before business logic execution.
- Return stable JSON response envelopes and error formats.
- Use middleware for auth, tracing, and request logging.
- Avoid leaking internal error details in API responses.
- Wrap and handle errors consistently throughout the call chain.
- Handle context propagation and timeouts consistently across handlers and services.
- Do not hardcode secrets, tokens, or passwords in source files.
- Do not log sensitive data.

## Persistence and Data Rules

- Never build SQL from untrusted input by string concatenation.
- Use migrations for schema changes.
- Keep transaction boundaries explicit in service/repository layer.

## Testing Strategy (Mandatory)

- Prefer handler/integration tests using table-driven test patterns (idiomatic Go).
- Use `net/http/httptest` package to test handlers with mocked requests/responses.
- For complex business logic in services, add unit tests with mocks as needed.
- Cover edge cases including invalid input, not found, and constraint violations.
- Tests should verify behavior, not internal implementation details.
- Test names should clearly describe the test case.
- Do not create repository/data layer tests by default.
- Add data layer tests only when custom SQL queries exist, or when explicitly requested by the user or required by the approved plan.

## Required Workflow Contract (Backend)

Use this file as the source of truth for:
- backend plan format
- backend implementation checklist
- backend handover format

## Backend Plan Format

```markdown
## Feature Plan: [Feature Name]

### What we are building
[1 short paragraph in plain language]

### Backend scope
- New or changed endpoints: [list]
- Files to create/modify: [list]
- Data/storage changes: [yes/no and details]

### Frontend impact
- New or changed UI areas: [list]
- API calls required by frontend: [list]

### API Contract
| Method | Path | Auth Required | Request | Response | Error Codes |
|--------|------|---------------|---------|----------|-------------|
| POST | /api/example | No | { "name": "string" } | { "id": 1 } | 400, 500 |

### Testing plan
- Backend tests to add/update: [list]
- Integration points to verify: [list]

### Risks and unknowns
- [list]
```

## Backend Implementation Checklist

- [ ] Read this file before coding
- [ ] Update data model or schema if required
- [ ] Update data access layer
- [ ] Update business logic layer
- [ ] Update API entry points
- [ ] Add or update tests following this architecture
- [ ] Run project backend test command
- [ ] Verify no sensitive data exposure in logs/errors

## Backend Handover Format

```markdown
### Backend Handover

**Endpoints Created / Modified**
| Method | Path | Auth Required | Request Body | Response Body | Status Codes |
|--------|------|---------------|--------------|---------------|--------------|
| POST | /api/example | No | { "name": "string" } | { "id": 1 } | 201, 400, 500 |

**Data and Schema Changes**
- [none or list migrations/schema updates]

**Files Changed**
| File | Change |
|------|--------|
| internal/path/to/file.go | Created or Modified with short reason |

**Test Result**
- Status: PASS or FAIL
- Command: [exact command]
- Notes: [summary or failure excerpt]

**Notes for Frontend**
- [validation rules]
- [auth requirements]
- [pagination/sorting/filter behavior]

**Notes for Reviewer**
- [trade-offs]
- [known limitations]
```
