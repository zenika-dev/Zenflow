"""Unit tests for CLI stack selection helpers and data classes."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from zenflow.cli import (
    GuidelineSelection,
    ToolSelection,
    _choose_language_then_framework,
    _choose_stack,
)
from zenflow.stack import BACKEND, FRONTEND

OPTIONS: list[tuple[str, str, str]] = [
    ("Option A", "a.md.j2", ""),
    ("Option B", "b.md.j2", "b-doc.md.j2"),
    ("Option C", "c.md.j2", ""),
]


# ---------------------------------------------------------------------------
# ToolSelection
# ---------------------------------------------------------------------------


def test_tool_selection_any_selected_true() -> None:
    assert ToolSelection(copilot=True, opencode=False, claude=False).any_selected()


def test_tool_selection_any_selected_false() -> None:
    assert not ToolSelection(copilot=False, opencode=False, claude=False).any_selected()


@pytest.mark.parametrize(
    "copilot, opencode, claude",
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, True),
    ],
)
def test_tool_selection_any_selected_combinations(copilot: bool, opencode: bool, claude: bool) -> None:
    assert ToolSelection(copilot=copilot, opencode=opencode, claude=claude).any_selected()


# ---------------------------------------------------------------------------
# GuidelineSelection
# ---------------------------------------------------------------------------


def test_guideline_selection_fields() -> None:
    g = GuidelineSelection(
        backend_arch_file="python.md.j2",
        backend_doc_file="",
        frontend_arch_file="react-typescript.md.j2",
        frontend_doc_file="react-typescript.md.j2",
        include_conventions=True,
    )
    assert g.backend_arch_file == "python.md.j2"
    assert g.backend_doc_file == ""
    assert g.frontend_arch_file == "react-typescript.md.j2"
    assert g.frontend_doc_file == "react-typescript.md.j2"
    assert g.include_conventions is True


# ---------------------------------------------------------------------------
# _choose_stack
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "choice, expected",
    [
        ("1", ("Option A", "a.md.j2", "")),
        ("2", ("Option B", "b.md.j2", "b-doc.md.j2")),
        ("3", ("Option C", "c.md.j2", "")),
    ],
)
def test_choose_stack_valid(choice: str, expected: tuple[str, str, str]) -> None:
    with patch("builtins.input", return_value=choice):
        assert _choose_stack("test", OPTIONS) == expected


@pytest.mark.parametrize("choice", ["0", "9", "abc", "", " "])
def test_choose_stack_invalid_exits(choice: str, capsys: pytest.CaptureFixture) -> None:
    with patch("builtins.input", return_value=choice):
        with pytest.raises(SystemExit):
            _choose_stack("test", OPTIONS)
    if choice not in ("0", " "):
        assert "invalid" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# _choose_language_then_framework
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "lang_choice, fw_choice, expected_arch, expected_doc",
    [
        ("1", "1", "python.md.j2", ""),
        ("1", "2", "python-fastapi.md.j2", ""),
        ("2", "1", "java.md.j2", ""),
        ("2", "2", "java-spring-boot.md.j2", "java-spring-boot.md.j2"),
        ("3", "1", "golang.md.j2", ""),
        ("3", "2", "golang-gin.md.j2", ""),
    ],
)
def test_choose_backend(
    lang_choice: str,
    fw_choice: str,
    expected_arch: str,
    expected_doc: str,
) -> None:
    with patch("builtins.input", side_effect=[lang_choice, fw_choice]):
        arch, doc = _choose_language_then_framework("backend", BACKEND)
    assert arch == expected_arch
    assert doc == expected_doc


@pytest.mark.parametrize(
    "lang_choice, fw_choice, expected_arch, expected_doc",
    [
        ("1", "1", "typescript.md.j2", ""),
        ("1", "2", "react-typescript.md.j2", "react-typescript.md.j2"),
        ("1", "3", "nextjs-app-router.md.j2", ""),
    ],
)
def test_choose_frontend(
    lang_choice: str,
    fw_choice: str,
    expected_arch: str,
    expected_doc: str,
) -> None:
    with patch("builtins.input", side_effect=[lang_choice, fw_choice]):
        arch, doc = _choose_language_then_framework("frontend", FRONTEND)
    assert arch == expected_arch
    assert doc == expected_doc
