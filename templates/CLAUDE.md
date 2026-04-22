# Claude Code Configuration

This file guides Claude Code for this project.

## Architecture Guidelines

Consult these files before making any changes:

- **Backend**: See `.github/guidelines/architecture-backend.md` for backend structure, patterns, and conventions
- **Frontend**: See `.github/guidelines/architecture-frontend.md` for frontend structure, patterns, and conventions
- **Review Checklist**: See `.github/guidelines/review-backend.md` and `.github/guidelines/review-frontend.md` for review standards

## Skills

Claude Code will automatically discover and use custom skills in `.claude/skills/` based on your requests:

- `backend-expert`: Backend implementation guidance
- `frontend-expert`: Frontend implementation guidance
- `reviewer`: Code review and quality standards
- `documentation`: Documentation updates
- `git`: Git workflow guidance
- `orchestrator`: Guidance for coordinating multi-step workflows

## Before You Start

1. Always check the architecture guidelines relevant to your task
2. Follow existing codebase patterns — never introduce new frameworks without discussion
3. For features spanning backend + frontend, see the orchestrator skill guidance