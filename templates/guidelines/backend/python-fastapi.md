# Backend Architecture Guidelines (Python + FastAPI)

Purpose: backend single source of truth for architecture, implementation order, testing, and backend handover format.

## Stack Profile

- Language: Python 3.11+
- Framework: FastAPI
- Data: SQLAlchemy/SQLModel/project standard

## Project Structure Expectations

- Keep API routers thin and focused on HTTP concerns.
- Keep business logic in service modules.
- Keep persistence logic in repository/data modules.
- Keep Pydantic schemas explicit for input/output contracts.
- Follow project conventions for module layout and naming.

## API and Validation Conventions

- Use Pydantic validation for all external inputs.
- Keep response models explicit and stable.
- Handle exceptions centrally and return consistent error shapes.
- Do not expose internal stack traces or sensitive internals.
- Keep dependency injection patterns consistent with project style.
- Do not hardcode secrets, tokens, or passwords in source files.
- Do not log sensitive data.

## Persistence and Data Rules

- Do not compose raw SQL with untrusted input.
- Use migrations for schema evolution.
- Keep transaction boundaries explicit.

## Testing Strategy (Mandatory)

- Prefer TestClient integration tests (FastAPI standard).
- Use `app.dependency_overrides` to mock database or external service dependencies.
- For complex business logic, add unit tests with mocks at service layer.
- Cover edge cases including invalid input, not found, and constraint violations.
- Tests should verify behavior, not private internals.
- Test names should clearly describe the behavior or test case.
- Repository/data access layer testing is not standard in FastAPI; test via TestClient with mocked dependencies.

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
| app/path/to/file.py | Created or Modified with short reason |

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
