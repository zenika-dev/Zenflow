# Zenflow Template Library

This directory contains reusable guideline templates for different agents and skills.

Purpose:
- keep core agents/skills stable, stack-agnostic and tool-agnostic
- keep stack-specific behavior into copyable guideline files
- make repository bootstrapping predictable for new teams

## Folders
1. Agents

These templates will be initialized as either Agents for Copilot or Skills for Claude/Open Code.

2. Guidelines

These files are copied to `.github/guidelines` for Copilot and in each skill's `references` folder for Claude/Open Code.

Architecture templates backend/frontend in `guidelines` contain **all rules** for planning, implementation, and review. They are the single source of truth.

Review templates are **process documents only** — they define the review scope and instruct the reviewer to audit against the architecture guideline. They do not contain substantive stack related rules. This ensures rules are never duplicated and cannot drift between implementation and review.

3. Instructions

This is only used by Copilot.

4. Partials

Partial templates are shared across different stacks and involve formatting of output, checklists, and handover. You can define your own partials that can be loaded automatically by the init script into the actual agents/skills templates. See files in `guidelines/backend/` for an example at the end of each file.

## AGENTS.md
For Claude Code and Open Code, this will be copied to either CLAUDE or AGENTS.md. As this file will be loaded for every session, it is deliberately lightweight. Since skills are handled natively by both tools, there is no need to specify where to load the skills from.

Editing this file will allow your team's tool to have these instructions for **every session**.


## Partial System

Agent and guideline source files are [Jinja2](https://jinja.palletsprojects.com/) templates (`.md.j2`). At init time, `src/zenflow/init.py` renders each template with a tool-specific context before writing assembled files to the target.

**Guideline path variables** — each tool gets its own `guidelines` context so file references resolve to the correct location:

| Variable | Copilot | OpenCode | Claude Code |
|---|---|---|---|
| `{{ guidelines.backend_arch }}` | `.github/guidelines/architecture-backend.md` | `.opencode/skills/backend/references/architecture.md` | `.claude/skills/backend/references/architecture.md` |
| `{{ guidelines.review_backend }}` | `.github/guidelines/review-backend.md` | `.opencode/skills/reviewer/references/review-backend.md` | `.claude/skills/reviewer/references/review-backend.md` |
| `{{ guidelines.conventions }}` | `.github/guidelines/conventions.md` | `.opencode/skills/git/references/conventions.md` | `.claude/skills/git/references/conventions.md` |

**Partial includes** use standard Jinja2 syntax:

```
{% include 'partials/backend-handover.md.j2' %}
```

**Tool-specific partial overrides** — place a file at `templates/skills/<agent-name>/<partial-filename>` to override a partial for skill output only. Jinja2's `FileSystemLoader` checks the agent override directory before falling back to the canonical partial:

```
templates/skills/reviewer/review-report.md.j2   ← used in skill output
templates/partials/review-report.md.j2           ← canonical fallback
```

## Notes

- Keep template files generic enough to reuse across projects.
- After cloning into a project for use, modify files in `.github/guidelines` or `skills/<skill name>/references` as necessary for the project's requirements.
