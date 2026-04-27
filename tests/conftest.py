"""Shared pytest fixtures for Zenflow tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from zenflow.init import make_env


@pytest.fixture(scope="session")
def repo_root() -> str:
    """Return the repository root directory.

    Returns:
        Absolute path to the repo root.
    """
    return str(Path(__file__).parent.parent)


@pytest.fixture()
def tmp_target(tmp_path: Path) -> Path:
    """Return a temporary target directory for deployment tests.

    Args:
        tmp_path: pytest built-in temporary directory fixture.

    Returns:
        Path to the temporary target directory.
    """
    return tmp_path


@pytest.fixture(scope="session")
def backend_env(repo_root: str):
    """Return a Jinja2 Environment scoped to the backend agent.

    Args:
        repo_root: Repository root path.

    Returns:
        Configured Jinja2 Environment with backend skill override path.
    """
    return make_env(repo_root, agent_name="backend")


@pytest.fixture(scope="session")
def frontend_env(repo_root: str):
    """Return a Jinja2 Environment scoped to the frontend agent.

    Args:
        repo_root: Repository root path.

    Returns:
        Configured Jinja2 Environment with frontend skill override path.
    """
    return make_env(repo_root, agent_name="frontend")


@pytest.fixture(scope="session")
def reviewer_env(repo_root: str):
    """Return a Jinja2 Environment scoped to the reviewer agent.

    Args:
        repo_root: Repository root path.

    Returns:
        Configured Jinja2 Environment with reviewer skill override path.
    """
    return make_env(repo_root, agent_name="reviewer")


@pytest.fixture(scope="session")
def base_env(repo_root: str):
    """Return a base Jinja2 Environment with no agent-specific overrides.

    Args:
        repo_root: Repository root path.

    Returns:
        Configured Jinja2 Environment.
    """
    return make_env(repo_root)
