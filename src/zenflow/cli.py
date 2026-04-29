"""CLI entry point and interactive wizard for Zenflow initialization."""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys
from dataclasses import dataclass

from zenflow.deployment import (
    deploy_agents,
    deploy_guidelines_to_github,
    deploy_guidelines_to_skills,
)
from zenflow.stack import BACKEND, FRONTEND

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceDirs:
    """Key source directories derived from the repository root.

    Attributes:
        agents: Path to the agents templates directory.
        instructions: Path to the instructions templates directory.
        guidelines: Path to the guidelines templates directory.
    """

    agents: str
    instructions: str
    guidelines: str


@dataclass(frozen=True)
class ToolSelection:
    """Which AI tools the user wants to set up.

    Attributes:
        copilot: Whether to deploy GitHub Copilot (VS Code) setup.
        opencode: Whether to deploy OpenCode setup.
        claude: Whether to deploy Claude Code setup.
    """

    copilot: bool
    opencode: bool
    claude: bool

    def any_selected(self) -> bool:
        """Return True if at least one tool is selected."""
        return any((self.copilot, self.opencode, self.claude))


@dataclass(frozen=True)
class GuidelineSelection:
    """User's guideline file choices.

    Attributes:
        backend_arch_file: Arch template filename for backend, or empty string.
        backend_doc_file: Doc template filename for backend, or empty string.
        frontend_arch_file: Arch template filename for frontend, or empty string.
        frontend_doc_file: Doc template filename for frontend, or empty string.
        include_conventions: Whether to include git conventions template.
    """

    backend_arch_file: str
    backend_doc_file: str
    frontend_arch_file: str
    frontend_doc_file: str
    include_conventions: bool


# ---------------------------------------------------------------------------
# Directory helpers
# ---------------------------------------------------------------------------


def get_dirs(repo_root: str) -> SourceDirs:
    """Return key source directories derived from repo_root.

    Args:
        repo_root: Repository root path.

    Returns:
        SourceDirs with agents, instructions, and guidelines paths.
    """
    return SourceDirs(
        agents=os.path.join(repo_root, "templates", "agents"),
        instructions=os.path.join(repo_root, "templates", "instructions"),
        guidelines=os.path.join(repo_root, "templates", "guidelines"),
    )


def validate_dirs(*dirs: str) -> None:
    """Exit with error if any of the given directories do not exist.

    Args:
        *dirs: Directory paths to validate.
    """
    for d in dirs:
        if not os.path.isdir(d):
            print(f"Error: missing source directory: {d}", file=sys.stderr)
            sys.exit(1)


# ---------------------------------------------------------------------------
# Stack selection
# ---------------------------------------------------------------------------


def _choose_stack(label: str, options: list[tuple[str, str, str]]) -> tuple[str, str, str]:
    """Prompt user to choose a stack from a numbered list.

    Args:
        label: Human-readable name for the stack type (e.g. 'backend').
        options: List of (label, arch_filename, doc_filename) entries.

    Returns:
        The chosen (label, arch_filename, doc_filename) tuple.
    """
    print()
    print(f"Choose {label}:")
    for i, (name, _, _) in enumerate(options, start=1):
        print(f"  {i}) {name}")
    choice = input(f"Enter choice [1-{len(options)}]: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(options):
        print(f"Error: invalid {label} choice '{choice}'.", file=sys.stderr)
        sys.exit(1)
    return options[int(choice) - 1]


def _choose_language_then_framework(
    domain: str,
    stacks: dict[str, list[tuple[str, str, str]]],
) -> tuple[str, str]:
    """Prompt user to choose a language then a framework.

    Args:
        domain: Human-readable domain name (e.g. 'backend').
        stacks: Dict of language label to list of (label, arch_file, doc_file) framework entries.

    Returns:
        Tuple of (arch_filename, doc_filename).
    """
    languages = [(lang, lang, "") for lang in stacks]
    _, language, _ = _choose_stack(f"{domain} language", languages)
    _, arch_file, doc_file = _choose_stack(f"{domain} framework", stacks[language])
    return arch_file, doc_file


# ---------------------------------------------------------------------------
# User prompts
# ---------------------------------------------------------------------------


def _prompt_tool_selection() -> ToolSelection:
    """Prompt user to select which AI tools to set up.

    Returns:
        ToolSelection with the user's choices.
    """
    return ToolSelection(
        copilot=input("Set up GitHub Copilot (VS Code)? [Y/N]: ").strip().lower() == "y",
        opencode=input("Set up OpenCode? [Y/N]: ").strip().lower() == "y",
        claude=input("Set up Claude Code? [Y/N]: ").strip().lower() == "y",
    )


def _prompt_guideline_selection() -> GuidelineSelection:
    """Prompt user to select backend, frontend, and conventions guidelines.

    Returns:
        GuidelineSelection with the user's file choices.
    """
    include_backend = input("Include backend guidelines? [Y/N]: ").strip().lower() == "y"
    include_frontend = input("Include frontend guidelines? [Y/N]: ").strip().lower() == "y"

    backend_arch_file, backend_doc_file = (
        _choose_language_then_framework("backend", BACKEND) if include_backend else ("", "")
    )
    frontend_arch_file, frontend_doc_file = (
        _choose_language_then_framework("frontend", FRONTEND) if include_frontend else ("", "")
    )

    print()
    include_conventions = input("Include git conventions template? [Y/N]: ").strip().lower() != "n"

    return GuidelineSelection(
        backend_arch_file=backend_arch_file,
        backend_doc_file=backend_doc_file,
        frontend_arch_file=frontend_arch_file,
        frontend_doc_file=frontend_doc_file,
        include_conventions=include_conventions,
    )


def _print_plan(target_path: str, tools: ToolSelection) -> None:
    """Print a summary of what will be generated before deployment.

    Args:
        target_path: Resolved target directory path.
        tools: Selected AI tools.
    """
    print("Zenflow initialization")
    print(f"Target path: {target_path}")
    print("Tools:")
    if tools.copilot:
        print("  ✓ GitHub Copilot (VS Code)")
    if tools.opencode:
        print("  ✓ OpenCode")
    if tools.claude:
        print("  ✓ Claude Code")
    print()
    print("The following will be generated:")
    if tools.copilot:
        print("  - .github/agents/        (agent definitions)")
        print("  - .github/instructions/  (instruction files)")
        print("  - .github/guidelines/    (architecture, review, and conventions)")
    if tools.opencode:
        print("  - .opencode/skills/      (OpenCode skill definitions + references/)")
    if tools.claude:
        print("  - .claude/skills/        (Claude Code skill definitions + references/)")
    print()
    input("Press any key to continue...")
    print()


# ---------------------------------------------------------------------------
# Deployment
# ---------------------------------------------------------------------------


def _deploy_copilot(
    target_path: str,
    src: SourceDirs,
    repo_root: str,
    guidelines: GuidelineSelection,
) -> None:
    """Deploy GitHub Copilot (VS Code) setup to target_path.

    Args:
        target_path: Root target directory.
        src: Source directory paths.
        repo_root: Repository root path.
        guidelines: User's guideline file choices.
    """
    print("Deploying GitHub Copilot (VS Code) setup...")
    target_github_dir = os.path.join(target_path, ".github")
    agents_dir = os.path.join(target_github_dir, "agents")
    instructions_dir = os.path.join(target_github_dir, "instructions")
    guidelines_dir = os.path.join(target_github_dir, "guidelines")
    os.makedirs(agents_dir, exist_ok=True)
    os.makedirs(instructions_dir, exist_ok=True)
    os.makedirs(guidelines_dir, exist_ok=True)

    print("Copying agents...")
    deploy_agents(src.agents, agents_dir, repo_root, tool="copilot", skill_mode=False)

    print("Copying instructions...")
    for f in glob.glob(os.path.join(src.instructions, "*.md")):
        shutil.copy(f, instructions_dir)

    print("Copying selected guideline templates...")
    deploy_guidelines_to_github(
        guidelines_dir,
        repo_root,
        guidelines.backend_arch_file,
        guidelines.frontend_arch_file,
        guidelines.backend_doc_file,
        guidelines.frontend_doc_file,
        guidelines.include_conventions,
    )


def _deploy_skills_tool(
    target_path: str,
    tool_subdir: str,
    tool: str,
    src: SourceDirs,
    repo_root: str,
    guidelines: GuidelineSelection,
) -> None:
    """Deploy a skills-based tool (OpenCode or Claude Code) to target_path.

    Args:
        target_path: Root target directory.
        tool_subdir: Subdirectory under target_path (e.g. '.opencode/skills').
        tool: Tool identifier passed to deployment functions (e.g. 'opencode').
        src: Source directory paths.
        repo_root: Repository root path.
        guidelines: User's guideline file choices.
    """
    skills_dir = os.path.join(target_path, tool_subdir)
    deploy_agents(src.agents, skills_dir, repo_root, tool=tool, skill_mode=True)
    deploy_guidelines_to_skills(
        skills_dir,
        repo_root,
        guidelines.backend_arch_file,
        guidelines.frontend_arch_file,
        guidelines.backend_doc_file,
        guidelines.frontend_doc_file,
        guidelines.include_conventions,
        tool=tool,
    )
    print(f"Copied skills to {skills_dir}")


def _print_summary(
    target_path: str,
    tools: ToolSelection,
    guidelines: GuidelineSelection,
    include_backend: bool,
    include_frontend: bool,
) -> None:
    """Print post-deployment summary.

    Args:
        target_path: Resolved target directory path.
        tools: Selected AI tools.
        guidelines: User's guideline file choices.
        include_backend: Whether backend guidelines were included.
        include_frontend: Whether frontend guidelines were included.
    """
    backend_doc_msg: str | None = (
        "Included backend documentation template"
        if guidelines.backend_doc_file
        else ("Skipped backend documentation template" if include_backend else None)
    )
    frontend_doc_msg: str | None = (
        "Included frontend documentation template"
        if guidelines.frontend_doc_file
        else ("Skipped frontend documentation template" if include_frontend else None)
    )
    conventions_msg = "Included conventions" if guidelines.include_conventions else "Skipped conventions"

    print()
    print("Initialization complete.")
    print(f"Target: {target_path}")
    if tools.copilot:
        print("✓ GitHub Copilot (VS Code): .github/agents, instructions, and guidelines")
    if tools.opencode:
        print("✓ OpenCode: .opencode/skills/ (with references/)")
    if tools.claude:
        print("✓ Claude Code: .claude/skills/ (with references/)")
    if backend_doc_msg:
        print(f"- {backend_doc_msg}")
    if frontend_doc_msg:
        print(f"- {frontend_doc_msg}")
    print(f"- {conventions_msg}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the Zenflow initialization wizard."""
    parser = argparse.ArgumentParser(
        prog="zenflow-init",
        description="Initializes Zenflow scaffolding in a target directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))

    src = get_dirs(repo_root)
    validate_dirs(src.agents, src.instructions, src.guidelines)

    default_target_path = os.path.join(repo_root, "target")
    target_path_input = input(f"Target path [{default_target_path}]: ").strip()
    target_path = target_path_input or default_target_path

    tools = _prompt_tool_selection()
    if not tools.any_selected():
        print("Error: at least one tool must be selected.", file=sys.stderr)
        sys.exit(1)

    _print_plan(target_path, tools)

    guidelines = _prompt_guideline_selection()
    include_backend = bool(guidelines.backend_arch_file)
    include_frontend = bool(guidelines.frontend_arch_file)

    print()

    if tools.copilot:
        _deploy_copilot(target_path, src, repo_root, guidelines)
    if tools.opencode:
        print("Deploying OpenCode setup...")
        _deploy_skills_tool(target_path, ".opencode/skills", "opencode", src, repo_root, guidelines)
    if tools.claude:
        print("Deploying Claude Code setup...")
        _deploy_skills_tool(target_path, ".claude/skills", "claude", src, repo_root, guidelines)

    _print_summary(target_path, tools, guidelines, include_backend, include_frontend)


if __name__ == "__main__":
    main()
