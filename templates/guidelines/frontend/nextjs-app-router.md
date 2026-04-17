# Frontend Architecture Guidelines (Next.js App Router)

Purpose: frontend single source of truth for architecture, implementation checklist, and frontend handover format.

## Stack Profile

- Framework: Next.js (App Router)
- Language: TypeScript
- Rendering: server and client components according to feature needs

## Project Structure Expectations

- Keep route segments under `app/` following project conventions.
- Keep data fetching strategy explicit (server fetch, route handlers, or client calls).
- Keep reusable UI in shared component directories.

## Frontend Conventions

- Choose server vs client components intentionally and document the reason.
- Keep API/network access in dedicated modules when possible.
- Define loading and error boundaries where user experience requires them.
- Follow existing styling and design system conventions.
- Use CSS variables for design tokens (colors, spacing, radius, typography, z-index) instead of hardcoded values in component styles.
- Meet accessibility baseline for interactive elements and form controls.

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
| ExampleComponent | app/path/to/component | Short purpose |

**API Integration**
- Endpoint consumed: [method path]
- Client/service location: [file path]
- Auth headers: [none or details]
- Error handling strategy: [short summary]

**Files Changed**
| File | Change |
|------|--------|
| app/path/to/file | Created or Modified with short reason |

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
