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

This is a mandatory bootstrap step before using the workflow agents.

1. Choose one backend template and one frontend template.
2. Copy the selected architecture templates and both review protocol templates into `.github/guidelines/`.
3. Rename them to match the files expected by agents:
   - backend architecture -> `.github/guidelines/architecture-backend.md`
   - frontend architecture -> `.github/guidelines/architecture-frontend.md`
   - backend review -> `.github/guidelines/review-backend.md`
   - frontend review -> `.github/guidelines/review-frontend.md`
   - conventions -> `.github/guidelines/conventions.md`
4. Edit each copied file with project-specific details.

Minimum required files for successful orchestration:
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
