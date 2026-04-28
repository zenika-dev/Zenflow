# Zenflow Template Library

This directory contains reusable guideline templates for different agents and skills.

Purpose:
- keep agents/skills stable, stack-agnostic and tool-agnostic
- keep stack-specific behaviour in copyable guideline files
- adapt agents/skills contents to tool-specific syntax
- make repository bootstrapping predictable for new teams

## Folders
1. Agents

These templates will be initialized as either Agents for Copilot or Skills for Claude/Open Code.

In general there is no need to change these files, as they determine primarily the workflow and will redirect the tool to refer to the guideline files (next section) for the rules that the agent/skill should follow.

2. Guidelines

Based on the stack chosen by the user when running the init command, the relevant files will be copied to:
* `.github/guidelines` for Copilot
* each skill's `references` folder for Claude/Open Code

Guideline logic:
- **architecture-backend.md**: Backend framework conventions, package structure, patterns, validation rules, database expectations, and testing strategy.
- **architecture-frontend.md**: Frontend framework conventions, component structure, API client patterns, routing, styling, accessibility, and testing strategy.
- **review-backend.md** and **review-frontend.md**: Review scope and audit checklist against the architecture guidelines. They reference the above two architecture documents to review what is implemented and do not contain substantive stack related rules.
- **conventions.md** (optional): Git branch and commit conventions.

The more explicit these files are, the more consistently all tools can follow your standards.

These are the files to be edited with the architectural guidelines your team agrees on.

If there are extra languages or stacks to be configured, the initialisation functions `choose_backend_stack` and `choose_frontend_stack` in `cli.py` will have to be extended as well.

3. Instructions

This is only used by Copilot to configure how questions are asked to the user and does not need to be customised.

4. Partials

Partial templates are shared across different stacks and involve formatting of output, checklists, and handover. You can define your own partials that can be loaded automatically by the init script into the actual agents/skills templates. See files in `guidelines/backend/` for an example at the end of each file.


## AGENTS.md
For Claude Code and Open Code, this will be copied to either CLAUDE or AGENTS.md. As this file will be loaded for every session, it is deliberately lightweight. Since skills are handled natively by both tools, there is no need to specify where to load the skills from.

Editing this file will configure what is loaded into your team's tool **every session**.


## Jinja Templates

**Agent and guideline source files** are [Jinja2](https://jinja.palletsprojects.com/) templates (`.md.j2`). At init time, each template will be rendered with a tool-specific context, and assembled files will be written to the target.

For agent source files, each tool gets its own `guidelines` context so file references resolve to the correct location:

| Variable | Copilot | OpenCode | Claude Code |
|---|---|---|---|
| `{{ guidelines.backend_arch }}` | `.github/guidelines/architecture-backend.md` | `.opencode/skills/backend/references/architecture.md` | `.claude/skills/backend/references/architecture.md` |
| `{{ guidelines.review_backend }}` | `.github/guidelines/review-backend.md` | `.opencode/skills/reviewer/references/review-backend.md` | `.claude/skills/reviewer/references/review-backend.md` |
| `{{ guidelines.conventions }}` | `.github/guidelines/conventions.md` | `.opencode/skills/git/references/conventions.md` | `.claude/skills/git/references/conventions.md` |

**Partials** will be included in source files using standard Jinja2 syntax:

```
{% include 'partials/backend-handover.md.j2' %}
```

The entire templates folder is provided to the Jinja2 environment when rendering the files, so any filepath within templates can be referenced directly.

Other partials can be included similarly according to the team's needs. 

## Notes

- Keep template files generic enough to reuse across projects.
- After cloning into a project for use, modify files in `.github/guidelines` or `skills/<skill name>/references` as necessary for the project's requirements.
