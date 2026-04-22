# Zenflow Template Library

This directory contains reusable guideline templates for different backend and frontend stacks.

Purpose:
- keep core agents stable and stack-agnostic
- move stack-specific behavior into copyable guideline files
- make repository bootstrapping predictable for new teams

## Single Source of Truth

Architecture templates (backend and frontend) contain **all rules** for planning, implementation, and review. They are the single source of truth.

Review templates are **process documents only** — they define the review scope and instruct the reviewer to audit against the architecture guideline. They do not contain substantive rules. This ensures rules are never duplicated and cannot drift between implementation and review.

## How To Use

Use `./scripts/init.sh` (bash) or `./scripts/init.ps1` (PowerShell) to bootstrap a target repository.

The script always deploys the full GitHub Copilot (VS Code) setup. OpenCode and Claude Code are optional add-ons.

1. **Always deployed**: Agents, instructions, and selected guideline templates to `.github/`
2. **Optional add-ons**: OpenCode (`.opencode/skills/`) and/or Claude Code (`.claude/skills/` + `CLAUDE.md`)
3. All tools reference `.github/guidelines/` as the single source of truth

### Example

```bash
./scripts/init.sh
# → Enter target repository path
# → Also set up OpenCode? [y/N]
# → Also set up Claude Code? [y/N]
# → Choose backend stack (java-spring-boot, golang-gin, python-fastapi)
# → Choose frontend stack (react-typescript, nextjs-app-router)
# → Include conventions? [Y/n]
# → Press key to continue
# → Scaffolding complete!
```

### Manual Setup (if not using init script)

1. Choose one backend template and one frontend template.
2. Copy the selected architecture templates and both review protocol templates into `.github/guidelines/`.
3. Rename them to match the expected file structure:
   - backend architecture → `.github/guidelines/architecture-backend.md`
   - frontend architecture → `.github/guidelines/architecture-frontend.md`
   - backend review → `.github/guidelines/review-backend.md`
   - frontend review → `.github/guidelines/review-frontend.md`
   - (optional) conventions → `.github/guidelines/conventions.md`
4. Edit each copied file with project-specific details.

**Minimum required files:**
- `.github/guidelines/architecture-backend.md`
- `.github/guidelines/architecture-frontend.md`
- `.github/guidelines/review-backend.md`
- `.github/guidelines/review-frontend.md`

## Structure

- `guidelines/backend/`
  - stack-specific backend architecture templates
- `guidelines/frontend/`
  - stack-specific frontend architecture templates
- `guidelines/review/`
  - stack-agnostic review protocol templates (scope and process only; rules live in architecture templates)
- `guidelines/git-conventions/`
  - branch and commit conventions templates

## Available Templates

Backend architecture:
- `guidelines/backend/java-spring-boot.md`
- `guidelines/backend/golang-gin.md`
- `guidelines/backend/python-fastapi.md`

Frontend architecture:
- `guidelines/frontend/react-typescript.md`
- `guidelines/frontend/nextjs-app-router.md`

Review protocol templates:
- `guidelines/review/backend.md`
- `guidelines/review/frontend.md`

Conventions:
- `guidelines/git-conventions/default.md`

## Notes

- Keep template files generic enough to reuse across projects.
- Keep project-specific decisions in `.github/guidelines/`, not in templates.
