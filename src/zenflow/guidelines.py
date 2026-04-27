"""Guidelines context per supported AI tool."""

from __future__ import annotations

from enum import StrEnum


class Tool(StrEnum):
    """Supported AI coding tools."""

    COPILOT = "copilot"
    OPENCODE = "opencode"
    CLAUDE = "claude"


def guidelines_context(tool: str) -> dict[str, str]:
    """Return the guidelines file paths for a given tool.

    Args:
        tool: One of 'copilot', 'opencode', 'claude'.

    Returns:
        A dict mapping guideline keys to their file paths for that tool.

    Raises:
        ValueError: If the tool is not recognised.
    """
    if tool == Tool.COPILOT:
        base = "@.github/guidelines"
        return {
            "backend_arch": f"{base}/architecture-backend.md",
            "frontend_arch": f"{base}/architecture-frontend.md",
            "review_backend": f"{base}/review-backend.md",
            "review_frontend": f"{base}/review-frontend.md",
            "documentation_backend": f"{base}/documentation-backend.md",
            "documentation_frontend": f"{base}/documentation-frontend.md",
            "conventions": f"{base}/conventions.md",
            "project_context": "@.github/copilot-instructions.md",
        }
    if tool == Tool.OPENCODE:
        base = ".opencode/skills"
        return {
            "backend_arch": f"{base}/backend/references/architecture.md",
            "frontend_arch": f"{base}/frontend/references/architecture.md",
            "review_backend": f"{base}/reviewer/references/review-backend.md",
            "review_frontend": f"{base}/reviewer/references/review-frontend.md",
            "documentation_backend": f"{base}/documentation/references/documentation-backend.md",
            "documentation_frontend": f"{base}/documentation/references/documentation-frontend.md",
            "conventions": f"{base}/git/references/conventions.md",
            "project_context": "AGENTS.md",
        }
    if tool == Tool.CLAUDE:
        base = ".claude/skills"
        return {
            "backend_arch": f"{base}/backend/references/architecture.md",
            "frontend_arch": f"{base}/frontend/references/architecture.md",
            "review_backend": f"{base}/reviewer/references/review-backend.md",
            "review_frontend": f"{base}/reviewer/references/review-frontend.md",
            "documentation_backend": f"{base}/documentation/references/documentation-backend.md",
            "documentation_frontend": f"{base}/documentation/references/documentation-frontend.md",
            "conventions": f"{base}/git/references/conventions.md",
            "project_context": "CLAUDE.md",
        }
    msg = f"Unknown tool: {tool}"
    raise ValueError(msg)
