"""GET /stacks — expose the backend/frontend framework catalog used to build an init request."""

from __future__ import annotations

from fastapi import APIRouter

from zenflow.core.stack import BACKEND, FRONTEND
from zenflow.routers.schemas import FrameworkOption, StackCatalog

router = APIRouter()


def _catalog(stacks: dict[str, list[tuple[str, str, str]]]) -> dict[str, list[FrameworkOption]]:
    """Convert a stack.py dict of (label, arch_file, doc_file) tuples into FrameworkOption models."""
    return {
        language: [FrameworkOption(label=label, arch_file=arch, doc_file=doc) for label, arch, doc in frameworks]
        for language, frameworks in stacks.items()
    }


@router.get("/stacks", response_model=StackCatalog)
def get_stacks() -> StackCatalog:
    """Return the available backend/frontend languages and frameworks.

    Returns:
        StackCatalog with backend and frontend options.
    """
    return StackCatalog(backend=_catalog(BACKEND), frontend=_catalog(FRONTEND))
