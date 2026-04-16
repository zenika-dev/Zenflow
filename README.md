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

#### Project Setup

To get the best results from this workflow, the target project should provide a few files and conventions up front. The agents are designed to follow project-specific guidance instead of inventing patterns on their own, so these inputs help keep the workflow more reliable and reduce hallucination.

##### Required Guidance Files

The current workflow expects these files to exist in the target repository:

- `.github/guidelines/architecture-backend.md`
- `.github/guidelines/architecture-frontend.md`

These files act as the main source of truth for how the Backend and Frontend agents should work inside your project.

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

##### Recommended Supporting Files

- `README.md`
  The Documentation agent updates the README, so it helps if the project already has a clear structure and an API or usage section to extend.
- `.github/copilot-instructions.md`
  The Documentation agent will load this if it exists. It can be useful for project-specific context, terminology, and documentation expectations.
- `docs/plans/`
  The Backend and Frontend agents save planning artifacts here for user review before implementation. Creating this directory up front helps keep plan outputs consistent.

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
