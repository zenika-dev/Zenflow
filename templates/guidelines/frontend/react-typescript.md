# Frontend Architecture Guidelines (React + TypeScript)

Purpose: frontend single source of truth for architecture, implementation checklist, and frontend handover format.

## Stack Profile

- Framework: React
- Language: TypeScript
- Testing: React Testing Library + project test runner

## Project Structure Expectations

- Keep API calls in service/client modules, not components.
- Keep presentational and stateful concerns separated where practical.
- Keep shared UI primitives and feature-level components organized by project conventions.

## Frontend Conventions

- Type all props and external data contracts.
- Use explicit loading, error, and success states.
- Follow existing routing and state-management patterns.
- Follow existing styling approach; do not introduce alternatives without approval.
- Use CSS variables for design tokens (colors, spacing, radius, typography, z-index) instead of hardcoded values in component styles.
- Meet baseline accessibility expectations for labels, keyboard access, and semantic structure.

## Styling Token Rules (CSS Variables)

- Define shared tokens in a global stylesheet scope (for example, `:root`).
- Prefer semantic token names (for example, `--color-surface`, `--color-text-primary`) over raw palette names.
- Keep component styles consuming tokens, not redefining them.
- For theming, override existing tokens by theme scope instead of creating parallel style systems.
- Avoid hardcoded hex/rgb values in component-level styles unless there is a documented exception.

## Required Workflow Contract (Frontend)

Use this file as the source of truth for:
- frontend plan format
- frontend implementation checklist
- frontend handover format

## Frontend Plan Format

```markdown
## Frontend Plan: [Feature Name]

### What we are building
[1 short paragraph in plain language]

### UI scope
- New components/screens: [list]
- Modified components/screens: [list]

### API integration scope
- Endpoints consumed: [list]
- Data contracts used: [list]

### State and UX
- Loading states: [list]
- Error states: [list]
- Success states: [list]

### Routing impact
- New routes: [list or none]
- Modified routes: [list or none]

### Testing plan
- Frontend tests to add/update: [list]

### Risks and unknowns
- [list]
```

## Frontend Implementation Checklist

- [ ] Read this file before coding
- [ ] Define or update request/response types
- [ ] Implement or update service/API client calls
- [ ] Implement or update UI components
- [ ] Implement loading, error, and success states
- [ ] Mirror backend validation rules in UI
- [ ] Use existing CSS variables (or add new semantic tokens) for visual styling changes
- [ ] Apply accessibility rules from this architecture
- [ ] Add or update tests following this architecture
- [ ] Run project frontend test command

## Frontend Handover Format

```markdown
### Frontend Handover

**Components Created / Modified**
| Component | File Path | Purpose |
|-----------|-----------|---------|
| ExampleComponent | src/path/to/component | Short purpose |

**API Integration**
- Endpoint consumed: [method path]
- Client/service location: [file path]
- Auth headers: [none or details]
- Error handling strategy: [short summary]

**Files Changed**
| File | Change |
|------|--------|
| src/path/to/file | Created or Modified with short reason |

**Test Result**
- Status: PASS or FAIL
- Command: [exact command]
- Notes: [summary or failure excerpt]

**Notes for Reviewer**
- [edge cases handled]
- [known limitations]

**Notes for Documentation**
- [props/options]
- [usage notes]
- [env requirements]
```
