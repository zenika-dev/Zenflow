# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. Each workflow is implemented as a team of collaborating AI agents, demonstrating patterns that teams can study, adapt, and build upon.

---

## Workflows

### 1. Fullstack Application — New Feature

This workflow delivers a complete feature end-to-end, from branch creation to a merged pull request. A top-level **Orchestrator** agent breaks the feature request into tasks and delegates each one to a specialist sub-agent in sequence.

| Step | Agent | Responsibility |
|------|-------|----------------|
| 0 | Git | Creates and checks out a feature branch |
| 1 | Orchestrator | Produces the Feature Plan |
| 2 | Discovery | Explores the codebase and maps relevant files |
| 3 | Backend | Implements API endpoints and business logic |
| 4 | Frontend | Builds UI components and wires up API calls |
| 5 | Reviewer | Performs security and quality review |
| 6 | Playwright | Generates E2E tests |
| 7 | Documentation | Updates docs and changelogs |
| 8 | Git | Commits changes and opens a pull request |

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

