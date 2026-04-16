# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. Each workflow is implemented as a team of collaborating AI agents, demonstrating patterns that teams can study, adapt, and build upon.

---

## Workflows

### 1. Fullstack Application — New Feature

This workflow delivers a complete feature end-to-end, from branch creation to a merged pull request. A top-level **Orchestrator** agent checks for `zenflow.config.yaml`, resolves the workflow paths it needs when the file is present, and delegates each task to a specialist sub-agent in sequence.

This workflow can optionally use [`zenflow.config.yaml`](/Users/martin/Desktop/Workspace/Zenflow/zenflow.config.yaml) for workflow-specific paths and defaults. Other workflows may use a different config file shape, or no config file at all.

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

#### Workflow Configuration

This workflow can use [`zenflow.config.yaml`](/Users/martin/Desktop/Workspace/Zenflow/zenflow.config.yaml) as an optional, workflow-specific configuration file.

Its purpose is to keep file locations and workflow settings for this workflow in one place so agents do not hardcode assumptions in their prompts. The intended pattern is:

1. The **Orchestrator** checks for `zenflow.config.yaml` first.
2. If the file exists, the Orchestrator resolves the concrete paths needed for this workflow from the repository root.
3. The Orchestrator passes only those resolved values to sub-agents.

For this workflow, plan files must be written only under the repository-root directory resolved from `paths.plans_dir` in `zenflow.config.yaml`. A fallback directory such as `plans/`, or a nested `<subdirectory>/<plans_dir>/` directory, is invalid.

This keeps the config small, reduces prompt duplication, and makes it easier to move guideline files or change plan locations later without rewriting every agent.

#### When This Workflow Needs It

Use `zenflow.config.yaml` for this workflow when it needs explicit configuration such as:

- where plans should be stored
- where backend or frontend guideline files live
- how plan filenames should be generated

Do not require `zenflow.config.yaml` for every workflow. If a workflow has no workflow-specific settings, the file can be omitted.

#### Configuration Sections

##### `paths`

Repository paths used by this workflow.

- `plans_dir`: Directory where workflow plans should be stored.
- `readme`: Path to the main project README that the Documentation agent should update.
- `guidelines.backend`: Path to the backend guideline document.
- `guidelines.frontend`: Path to the frontend guideline document.
- `guidelines.documentation`: Optional documentation context file for the Documentation agent.

##### `plan_files`

Plan filename templates for this workflow.

- `backend`: Naming template for the backend plan file.
- `frontend`: Naming template for the frontend plan file.

#### Why This Exists

Using `zenflow.config.yaml` in this workflow helps Zenflow:

- avoid hardcoded path assumptions across agent prompts
- keep workflow defaults in one place
- reduce hallucination risk by making agents resolve real file paths before acting
- allow workflow-specific config only when this workflow actually needs it

For a detailed flow diagram, see [docs/diagrams/fullstack-newfeature.md](docs/diagrams/fullstack-newfeature.md).

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
