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


## How To Use
See README.md at project root for deployment via script.

To modify the script logic, you can update `src/zenflow/init.py`, for example, to add a language option to the initialisation process.

## Notes

- Keep template files generic enough to reuse across projects.
- After cloning, modify files in `.github/guidelines` or `skills/<skill name>/references` as necessary for the project's requirements.
