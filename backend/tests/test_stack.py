"""Unit tests for stack constants."""

from __future__ import annotations

import pytest

from zenflow.core.stack import BACKEND, FRONTEND


@pytest.mark.parametrize("stacks", [BACKEND, FRONTEND], ids=["backend", "frontend"])
def test_has_entries(stacks: dict) -> None:
    assert len(stacks) > 0


@pytest.mark.parametrize("stacks", [BACKEND, FRONTEND], ids=["backend", "frontend"])
def test_frameworks_are_non_empty(stacks: dict) -> None:
    for language, frameworks in stacks.items():
        assert len(frameworks) > 0, f"No frameworks for language '{language}'"


@pytest.mark.parametrize(
    "language, frameworks",
    [*BACKEND.items(), *FRONTEND.items()],
)
def test_entries_are_three_tuples(language: str, frameworks: list) -> None:
    for entry in frameworks:
        assert len(entry) == 3, f"Expected 3-tuple in '{language}', got {entry}"


@pytest.mark.parametrize(
    "language, frameworks",
    [*BACKEND.items(), *FRONTEND.items()],
)
def test_arch_files_end_with_md_j2(language: str, frameworks: list) -> None:
    for label, arch_file, _ in frameworks:
        assert arch_file.endswith(".md.j2"), f"'{language}' / '{label}': arch_file '{arch_file}' must end with .md.j2"


@pytest.mark.parametrize(
    "language, frameworks",
    [*BACKEND.items(), *FRONTEND.items()],
)
def test_doc_files_end_with_md_j2_or_empty(language: str, frameworks: list) -> None:
    for label, _, doc_file in frameworks:
        assert doc_file == "" or doc_file.endswith(".md.j2"), (
            f"'{language}' / '{label}': doc_file '{doc_file}' must be empty or .md.j2"
        )
