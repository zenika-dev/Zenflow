# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. Each workflow is implemented as a team of collaborating AI agents, demonstrating patterns that teams can study, adapt, and build upon.

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

To use this workflow in an existing repository:

```bash
./scripts/init.sh
```

Follow the prompts to:
1. Enter the target repository folder path (local directory).
2. Choose backend stack (Java/Spring Boot, Go/Gin, Python/FastAPI).
3. Choose frontend stack (React, Next.js App Router).
4. Optionally include git conventions.

The script copies `.github/agents/` and guideline templates into the target repository, ready for use.

**Note:** This setup is currently temporary and will be replaced with a more streamlined approach in future phases.

#### Project Setup

To get the best results from this workflow, the target project should provide a few files and conventions up front. The agents are designed to follow project-specific guidance instead of inventing patterns on their own, so these inputs help keep the workflow more reliable and reduce hallucination.

##### Required Guidance Files

For a fully working orchestration flow, you must add these files under `.github/guidelines/` before running agents:

- `architecture-backend.md`
- `architecture-frontend.md`
- `review-backend.md`
- `review-frontend.md`

Use the Quick Start section above to set up a new repository with these files.

The architecture files are the main source of truth for Backend and Frontend implementation behavior.
The review files are the source of truth for Reviewer checklists.

`architecture-backend.md` should ideally describe things like:

- backend framework and language conventions
- package and folder structure
- controller, service, repository, and entity patterns
- validation rules and error-handling conventions
- database and migration expectations
- testing strategy, including when to write service, repository, or controller tests

`architecture-frontend.md` should ideally describe things like:

- frontend framework and language conventions
- component and service structure
- API client patterns
- routing conventions
- styling approach
- accessibility expectations
- testing strategy and preferred test patterns

The more explicit these files are, the more consistently the agents can follow your standards.

For Git branch and commit conventions, you can also provide:

- `.github/guidelines/conventions.md`

If present, the Git agent will use it for branch naming and commit formatting.

##### Recommended Supporting Files

- `README.md`
  The Documentation agent updates the README, so it helps if the project already has a clear structure and an API or usage section to extend.
- `.github/copilot-instructions.md`
  The Documentation agent will load this if it exists. It can be useful for project-specific context, terminology, and documentation expectations.
- `docs/plans/`
  The Backend and Frontend agents save planning artifacts here for user review before implementation. Creating this directory up front helps keep plan outputs consistent.

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

### Template Library

Zenflow includes a stack template library under `templates/`.

The templates exist to keep core agent behavior stable while moving stack-specific architecture and review conventions into reusable files.

See [templates/README.md](templates/README.md) for available templates and structure.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
