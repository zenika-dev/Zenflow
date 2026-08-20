"""FastAPI application entry point for the Zenflow API.

Interactive docs (Swagger UI) are served at /docs, ReDoc at /redoc, and the raw
OpenAPI schema at /openapi.json — all provided automatically by FastAPI.
"""

from __future__ import annotations

from fastapi import FastAPI

from zenflow.routers import init, stacks

app = FastAPI(
    title="Zenflow API",
    description="Programmatic access to Zenflow project initialization.",
    version="0.1.0",
)

app.include_router(init.router, tags=["init"])
app.include_router(stacks.router, tags=["stacks"])


def main() -> None:
    """Run the Zenflow API locally with uvicorn (development entry point)."""
    import uvicorn

    uvicorn.run("zenflow.routers.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
