# Backend Architecture Guidelines (Java + Spring Boot)

Purpose: backend single source of truth for architecture, implementation order, testing, and backend handover format.

## Stack Profile

- Language: Java 17+
- Framework: Spring Boot
- Build: Maven or Gradle
- Data: Spring Data JPA (or project standard)

## Project Structure Expectations

- Keep API entry points in `controller` packages.
- Keep business logic in `service` packages.
- Keep persistence logic in `repository` packages.
- Keep DTOs, entities, and mappers separated by responsibility.
- Use DTOs at API boundaries; do not replace persistence entities with DTOs in repository layer.

## API and Validation Conventions

- Controllers stay thin and delegate to services.
- Use `@RestController` with consistent `@RequestMapping` conventions.
- Avoid `ResponseEntity` by default; use it only when status/header control is required.
- Validate request DTOs using Bean Validation annotations.
- Return stable response shapes for success and error cases.
- Use `@ControllerAdvice` (or project equivalent) for centralized exception handling.

## Persistence and Data Rules

- Model persisted domain changes with JPA entities first.
- Use Spring Data JPA repositories; do not add `@Repository` when using repository interfaces.
- No raw SQL string concatenation with untrusted input.
- Use migrations for schema changes (Flyway/Liquibase/project standard).
- Keep transaction boundaries explicit in service layer.

## Implementation Order (Mandatory)

Implement backend changes in this order unless the approved plan explicitly says otherwise:

1. Entity
2. Repository
3. Service
4. Controller
5. Tests

This order keeps schema and business logic stable before exposing HTTP endpoints.

Entity-first does not conflict with DTO usage: entities model persistence, while DTOs shape request/response contracts.

## Testing Strategy (Mandatory)

- Prefer service-layer tests as the default verification layer.
- For straightforward rules, use integration-style service tests against in-memory DB where appropriate.
- For complex business branching, use unit tests with mocks at service layer.
- Do not create repository tests by default.
- Add repository tests only when explicitly requested by the user or required by the approved plan.
- Do not create controller tests by default.
- Add controller tests only when explicitly requested by the user or required by the approved plan.

**Planning constraint:** When generating a feature plan, do not include repository tests or controller tests in the testing plan unless the user explicitly requested them. The "required by the approved plan" clause applies only during implementation — it does not allow the planner to self-approve excluded test types.

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
- Backend tests to add/update: [list — must follow Testing Strategy defaults; do not add controller or repository tests unless the user explicitly requested them]
- Integration points to verify: [list]

### Risks and unknowns
- [list]
```

## Backend Implementation Checklist

- [ ] Read this file before coding
- [ ] Entity: create/update JPA entities when data model changes are required
- [ ] Repository: create/update Spring Data JPA repository interfaces (no `@Repository` needed for interfaces)
- [ ] Service: implement business logic with `@Service` and `@Transactional` where needed
- [ ] Controller: expose endpoints via `@RestController`; keep controllers thin
- [ ] Tests: follow the Testing Strategy section; do not add controller tests by default
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
| src/path/to/file | Created or Modified with short reason |

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
