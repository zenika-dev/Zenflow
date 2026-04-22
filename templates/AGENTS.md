# Project Rules

This file guides OpenCode for this project.

## Architecture Guidelines

Consult these files before making any changes:

- **Backend**: See `.github/guidelines/architecture-backend.md` for backend structure, patterns, and conventions
- **Frontend**: See `.github/guidelines/architecture-frontend.md` for frontend structure, patterns, and conventions
- **Review Checklist**: See `.github/guidelines/review-backend.md` and `.github/guidelines/review-frontend.md` for review standards

## Skills

OpenCode can use custom skills in `.opencode/skills/` when they are relevant to the task:

- `backend-expert`: Backend implementation guidance
- `frontend-expert`: Frontend implementation guidance
- `reviewer`: Code review and quality standards
- `documentation`: Documentation updates
- `git`: Git workflow guidance
- `orchestrator`: Guidance for coordinating multi-step workflows

## External File Loading

Read guideline files on demand when they are relevant to the current task. Treat the referenced files as project instructions.

## Before You Start

1. Always check the architecture guidelines relevant to your task.
2. Follow existing codebase patterns and conventions.
3. For features spanning backend and frontend, use the orchestrator guidance when available.
