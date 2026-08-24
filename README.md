# Zenflow

Zenflow is an **open-source project** that showcases the most common agentic workflows for AI-driven software development. It ships as a Python CLI/API and, going forward, a companion web frontend.

This is a monorepo with two projects:

- **[backend/](backend/README.md)** — the Zenflow Python package: `zenflow-init` CLI wizard and the `zenflow-api` FastAPI service (Swagger UI at `/docs`). See [backend/README.md](backend/README.md) for setup, usage, and the full workflow documentation.
- **[frontend/](frontend/README.md)** — a Next.js app that talks to the backend API.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
