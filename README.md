# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. Each workflow is implemented as a team of collaborating AI agents, demonstrating patterns that teams can study, adapt, and build upon.

**Zenflow supports GitHub Copilot (VS Code), OpenCode, and Claude Code.** Each tool is optional — you can install any combination.

To extend Zenflow with team specific guidelines for your own use:
1. Fork the repository
2. Update the templates with additional guidelines, or include other templates
3. Team members cloning from your repository will be able to bootstrap their tools with team specific guidelines.

For more details on how to extend Zenflow, refer to the relevant section below.


## Quick Start

To install Zenflow in an existing repository, install dependencies with [uv](https://docs.astral.sh/uv/) and run the init script:

```bash
uv sync
uv run zenflow-init
```

Or without installing (uv will resolve on the fly):

```bash
uv run --with jinja2 python src/zenflow/init.py
```

! Note: if you have an existing Agent or Skill with the same name configured globally or locally in your project directory, it will be overloaded in the project directory when running this script.

Follow the prompts to:
1. Enter the target repository folder path.
2. Choose which tools to set up (GitHub Copilot, OpenCode, Claude Code — any combination).
3. Choose backend stack (Java/Spring Boot, Go/Gin, Python/FastAPI).
4. Choose frontend stack (React, Next.js App Router).
5. Optionally include git conventions.

### What the script installs
After running the script, the target repository will have:

- **.github/agents/**, **.github/instructions/**, **.github/guidelines/** (if GitHub Copilot selected): Agents and guideline files, instructions to configure agents.
- **.opencode/skills/** and **AGENTS.md** (if OpenCode selected): Skills, guideline files embedded in each skill's `references/` subfolder
- **.claude/skills/** and **CLAUDE.md** (if Claude Code selected): Skills, guideline files embedded in each skill's `references/` subfolder

### Recommended Supporting Files
For best results, ensure the target project provides additional context:

- **README.md**: The Documentation agent updates the README, so it helps if the project already has a clear structure and an API or usage section to extend.
- **docs/plans/**: The Backend and Frontend agents save planning artifacts here for user review before implementation. Create this directory up front to keep outputs consistent.
- **.github/copilot-instructions.md** (for Copilot only): The Documentation agent will load this if it exists. It can be useful for project-specific context, terminology, and documentation expectations.


## Workflows

### 1. Fullstack Application — New Feature

This workflow delivers a complete feature end-to-end, from branch creation to a merged pull request. 

When using GitHub Copilot, a top-level **Orchestrator** agent breaks the feature request into tasks. Then, the agent delegates each one to a specialist sub-agent in sequence. Subagents can also be loaded directly if preferable.

When using OpenCode or ClaudeCode, each agent below is loaded as a Skill instead. Suggested workflow will be included at the end of the task performed by each skill.

| Step | Agent | Responsibility |
|------|-------|----------------|
| 0 | Git | Creates and checks out a feature branch |
| 1 | Backend | Produces feature plan (saved to `docs/plans/`) for user approval |
| 2 | Backend | Implements API endpoints and business logic |
| 3 | Frontend | Produces frontend plan for user approval |
| 4 | Frontend | Builds UI components and wires up API calls |
| 5 | Reviewer | Performs security and quality review |
| 6 | Documentation | Updates README and other documentation where applicable. |
| 7 | Git | Stages changes, writes a conventional commit, and prepares a PR description |
| 8 | Orchestrator | Presents a final summary of what was built, files changed, and outstanding items |

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

## Extending and Customising Zenflow
### How the Guidelines Work

For GitHub Copilot, the generated `.github/guidelines/` directory contains all rules. For OpenCode and Claude Code, the same content is placed inside each skill's `references/` subfolder so agents can load it without crossing tool boundaries:

- **architecture-backend.md**: Backend framework conventions, package structure, patterns, validation rules, database expectations, and testing strategy.
- **architecture-frontend.md**: Frontend framework conventions, component structure, API client patterns, routing, styling, accessibility, and testing strategy.
- **review-backend.md** and **review-frontend.md**: Review scope and audit checklist against the architecture guidelines.
- **conventions.md** (optional): Git branch and commit conventions.

The more explicit these files are, the more consistently all tools can follow your standards.

### Template Library

Zenflow includes a stack template library under `templates/`.

See [templates/README.md](templates/README.md) for available templates and structure, as well as how to extend this for your own use.


## Project Structure

```
Zenflow/
├── docs/             # Explanation of Zenflow orchestration
├── src/              # Setup script (Jinja2-based rendering)
├── templates/        # Reusable templates
```


## License

This project is licensed under the [Apache License 2.0](LICENSE).
