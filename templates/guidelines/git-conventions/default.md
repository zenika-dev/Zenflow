# Git Conventions Template

Purpose: define default branch naming and conventional commit rules used by the Git agent.

## Branch Naming

Use this format unless your project defines a stricter pattern:

`<type>/<ticket-or-scope>-<short-kebab-description>`

Examples:
- `feature/PROJ-123-user-feedback-endpoint`
- `fix/PROJ-456-null-pointer-check`
- `chore/review-guidelines-cleanup`

Recommended branch types:
- `feature`
- `fix`
- `chore`
- `refactor`
- `docs`
- `test`

## Conventional Commit Rules

Use:

`<type>(<scope>): <short summary>`

Examples:
- `feat(auth): add refresh token endpoint`
- `fix(frontend): handle loading state in settings page`
- `docs(workflow): clarify handover contract`

Recommended commit types:
- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `chore`

Recommended scopes:
- `backend`
- `frontend`
- `review`
- `docs`
- `workflow`
- `agent`

## Pull Request Title

Use this format:

`[<type>] <ticket-or-scope>: <summary>`

Examples:
- `[feature] PROJ-123: add user feedback API and form`
- `[chore] workflow: split stack templates from core agents`
