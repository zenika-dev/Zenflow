# Zenflow Template Library

This directory contains reusable guideline templates for different backend and frontend stacks.

Purpose:
- keep core agents stable and stack-agnostic
- move stack-specific behavior into copyable guideline files
- make repository bootstrapping predictable for new teams

To extend Zenflow with team specific guidelines, you can fork the repository, update the templates with additional guidelines, or include other templates. Then, team members cloning from your repository will be able to bootstrap their tools with team specific guidelines.

## Single Source of Truth

Architecture templates (backend and frontend) contain **all rules** for planning, implementation, and review. They are the single source of truth.

Review templates are **process documents only** — they define the review scope and instruct the reviewer to audit against the architecture guideline. They do not contain substantive stack related rules. This ensures rules are never duplicated and cannot drift between implementation and review.

## How To Use
See README.md at project root for deployment via script.

### Manual Setup (if not using init script)

1. Choose one backend template and one frontend template.
2. Copy the selected architecture templates and both review protocol templates into `.github/guidelines/`.
3. Rename them to match the expected file structure:
   - backend architecture → `.github/guidelines/architecture-backend.md`
   - frontend architecture → `.github/guidelines/architecture-frontend.md`
   - backend review → `.github/guidelines/review-backend.md`
   - frontend review → `.github/guidelines/review-frontend.md`
   - (optional) conventions → `.github/guidelines/conventions.md`
   - (opitonal) stack specific documentation → `.github/guidelines/documentation-backend.md` (or frontend)
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

Documentation:
- `guidelines/documentation/java-spring-boot.md`
- `guidelines/documentation/react-typescript.md`

## Notes

- Keep template files generic enough to reuse across projects.
- Keep project-specific decisions in `.github/guidelines/`, not in templates.
