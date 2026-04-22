# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. Each workflow is implemented as a team of collaborating AI agents, demonstrating patterns that teams can study, adapt, and build upon.

**Zenflow supports GitHub Copilot (VS Code), OpenCode, and Claude Code.** GitHub Copilot is always deployed as the baseline. OpenCode and Claude Code are optional add-ons.

---

## Workflows

### 1. Fullstack Application — New Feature

This workflow delivers a complete feature end-to-end, from branch creation to a merged pull request. A top-level **Orchestrator** agent breaks the feature request into tasks and delegates each one to a specialist sub-agent in sequence.

| Step | Agent | Responsibility |
|------|-------|----------------|
| 0 | Git | Creates and checks out a feature branch |
| 1 | Backend | Produces feature plan (saved to `docs/plans/`) for user approval |
| 2 | Backend | Implements API endpoints and business logic |
| 3 | Frontend | Produces frontend plan for user approval |
| 4 | Frontend | Builds UI components and wires up API calls |
| 5 | Reviewer | Performs security and quality review |
| 6 | Documentation | Updates README, JavaDoc, and TSDoc |
| 7 | Git | Stages changes, writes a conventional commit, and prepares a PR description |

#### Quick Start

To use this workflow in an existing repository, run the init script:

```bash
# bash (Linux/macOS)
./scripts/init.sh

# PowerShell (Windows)
.\scripts\init.ps1
```

Follow the prompts to:
1. Enter the target repository folder path.
2. Optionally add OpenCode and/or Claude Code on top of Copilot.
3. Choose backend stack (Java/Spring Boot, Go/Gin, Python/FastAPI).
4. Choose frontend stack (React, Next.js App Router).
5. Optionally include git conventions.

The script always deploys:
- **GitHub Copilot (VS Code)**: Agents, instructions, and guidelines to `.github/`

Optionally also deploys:
- **OpenCode**: Wraps agents as skills in `.opencode/skills/`
- **Claude Code**: Wraps agents as skills in `.claude/skills/` and copies `CLAUDE.md` to the repository root

All tools reference `.github/guidelines/` as their single source of truth.

#### Project Setup

The init script always deploys the full GitHub Copilot setup. After running the script, the target repository will have:

- **.github/agents/**: Agent definitions for Copilot
- **.github/instructions/**: Shared cross-agent behavior rules
- **.github/guidelines/**: Stack-specific architecture, review, and conventions — the single source of truth used by all tools
- **.opencode/skills/** (if OpenCode selected): Skills mirroring the agent structure, referencing `.github/guidelines/`
- **.claude/skills/** and **CLAUDE.md** (if Claude Code selected): Skills and entry point for Claude Code, referencing `.github/guidelines/`

For best results, ensure the target project provides additional context:

##### Recommended Supporting Files

- **README.md**: The Documentation agent updates the README, so it helps if the project already has a clear structure and an API or usage section to extend.
- **docs/plans/**: The Backend and Frontend agents save planning artifacts here for user review before implementation. Create this directory up front to keep outputs consistent.
- **.github/copilot-instructions.md**: The Documentation agent will load this if it exists. It can be useful for project-specific context, terminology, and documentation expectations.

##### How the Guidelines Work

The generated `.github/guidelines/` directory contains **all rules** for planning, implementation, and review. All tools reference this location directly:

- **architecture-backend.md**: Backend framework conventions, package structure, patterns, validation rules, database expectations, and testing strategy.
- **architecture-frontend.md**: Frontend framework conventions, component structure, API client patterns, routing, styling, accessibility, and testing strategy.
- **review-backend.md** and **review-frontend.md**: Review scope and audit checklist against the architecture guidelines.
- **conventions.md** (optional): Git branch and commit conventions.

The more explicit these files are, the more consistently all tools can follow your standards.

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

### Template Library

Zenflow includes a stack template library under `templates/`.

The templates exist to keep core agent behavior stable while moving stack-specific architecture and review conventions into reusable files.

See [templates/README.md](templates/README.md) for available templates and structure.

---

## Project Structure

```
Zenflow/
├── .github/
│   ├── agents/               # Stack-agnostic agent definitions
│   │   ├── backend.agent.md
│   │   ├── frontend.agent.md
│   │   ├── orchestrator.agent.md
│   │   ├── reviewer.agent.md
│   │   ├── documentation.agent.md
│   │   └── git.agent.md
│   └── instructions/         # Shared cross-agent behavior rules
│       └── agent-questions.instructions.md
├── templates/
│   └── guidelines/           # Reusable stack-specific templates
│       ├── backend/
│       ├── frontend/
│       ├── review/
│       └── git-conventions/
├── scripts/
│   ├── init.sh               # Setup script (bash)
│   └── init.ps1              # Setup script (PowerShell)
├── CLAUDE.md             # Claude Code entry point template
├── README.md
└── LICENSE
```

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
