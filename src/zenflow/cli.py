"""CLI entry point and interactive wizard for Zenflow initialization."""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys

from zenflow.deployment import (
    deploy_agents,
    deploy_guidelines_to_github,
    deploy_guidelines_to_skills,
)


def get_dirs(repo_root: str) -> tuple[str, str, str]:
    """Return key source directories derived from repo_root.

    Args:
        repo_root: Repository root path.

    Returns:
        Tuple of (agents_src_dir, instructions_src_dir, guidelines_src_dir).
    """
    return (
        os.path.join(repo_root, "templates", "agents"),
        os.path.join(repo_root, "templates", "instructions"),
        os.path.join(repo_root, "templates", "guidelines"),
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


def _choose_stack(label: str, options: dict[str, tuple[str, str]]) -> tuple[str, str]:
    """Prompt user to choose a stack from a numbered list.

    Args:
        label: Human-readable name for the stack type (e.g. 'backend').
        options: Mapping of choice key to (arch_filename, doc_filename).

    Returns:
        Tuple of (arch_filename, doc_filename) — doc_filename may be empty string.
    """
    print()
    print(f"Choose {label} stack:")
    for key, (arch, _) in options.items():
        print(f"  {key}) {arch.removesuffix('.md.j2')}")
    choice = input(f"Enter choice [1-{len(options)}]: ").strip()
    if choice not in options:
        print(f"Error: invalid {label} choice '{choice}'.", file=sys.stderr)
        sys.exit(1)
    return options[choice]


def choose_backend_stack() -> tuple[str, str]:
    """Prompt user to choose backend stack.

    Returns:
        Tuple of (arch_filename, doc_filename) — doc_filename may be empty string.
    """
    return _choose_stack(
        "backend",
        {
            "1": ("java-spring-boot.md.j2", "java-spring-boot.md.j2"),
            "2": ("golang-gin.md.j2", ""),
            "3": ("python-fastapi.md.j2", ""),
        },
    )


def choose_frontend_stack() -> tuple[str, str]:
    """Prompt user to choose frontend stack.

    Returns:
        Tuple of (arch_filename, doc_filename) — doc_filename may be empty string.
    """
    return _choose_stack(
        "frontend",
        {
            "1": ("react-typescript.md.j2", "react-typescript.md.j2"),
            "2": ("nextjs-app-router.md.j2", ""),
        },
    )


def main() -> None:
    """Run the Zenflow initialization wizard."""
    parser = argparse.ArgumentParser(
        prog="zenflow-init",
        description="Initializes Zenflow scaffolding in a target directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # src/zenflow/cli.py -> repo root is three levels up
    repo_root = os.path.dirname(os.path.dirname(script_dir))

    agents_src_dir, instructions_src_dir, guidelines_src_dir = get_dirs(repo_root)
    validate_dirs(agents_src_dir, instructions_src_dir, guidelines_src_dir)

    # --- User configuration ---
    default_target_path = os.path.join(repo_root, "target")
    target_path_input = input(f"Target path [{default_target_path}]: ").strip()
    target_path = target_path_input or default_target_path

    deploy_copilot = input("Set up GitHub Copilot (VS Code)? [Y/N]: ").strip().lower() == "y"
    deploy_opencode = input("Set up OpenCode? [Y/N]: ").strip().lower() == "y"
    deploy_claude = input("Set up Claude Code? [Y/N]: ").strip().lower() == "y"

    if not any((deploy_copilot, deploy_opencode, deploy_claude)):
        print("Error: at least one tool must be selected.", file=sys.stderr)
        sys.exit(1)

    print("Zenflow initialization")
    print(f"Target path: {target_path}")
    print("Tools:")
    if deploy_copilot:
        print("  ✓ GitHub Copilot (VS Code)")
    if deploy_opencode:
        print("  ✓ OpenCode")
    if deploy_claude:
        print("  ✓ Claude Code")
    print()
    print("The following will be generated:")
    if deploy_copilot:
        print("  - .github/agents/        (agent definitions)")
        print("  - .github/instructions/  (instruction files)")
        print("  - .github/guidelines/    (architecture, review, and conventions)")
    if deploy_opencode:
        print("  - .opencode/skills/      (OpenCode skill definitions + references/)")
    if deploy_claude:
        print("  - .claude/skills/        (Claude Code skill definitions + references/)")
    print()
    input("Press any key to continue...")
    print()

    include_backend = input("Include backend guidelines? [Y/N]: ").strip().lower() == "y"
    include_frontend = input("Include frontend guidelines? [Y/N]: ").strip().lower() == "y"

    backend_arch_file, backend_doc_file = choose_backend_stack() if include_backend else ("", "")
    frontend_arch_file, frontend_doc_file = choose_frontend_stack() if include_frontend else ("", "")

    print()
    include_conventions = input("Include git conventions template? [Y/N]: ").strip().lower() != "n"
    conventions_msg = "Included conventions" if include_conventions else "Skipped conventions"

    backend_doc_msg = (
        "Included backend documentation template"
        if backend_doc_file
        else ("Skipped backend documentation template" if include_backend else None)
    )
    frontend_doc_msg = (
        "Included frontend documentation template"
        if frontend_doc_file
        else ("Skipped frontend documentation template" if include_frontend else None)
    )

    print()

    # --- Deploy GitHub Copilot ---
    if deploy_copilot:
        print("Deploying GitHub Copilot (VS Code) setup...")
        target_github_dir = os.path.join(target_path, ".github")
        target_agents_dir = os.path.join(target_github_dir, "agents")
        target_instructions_dir = os.path.join(target_github_dir, "instructions")
        target_guidelines_dir = os.path.join(target_github_dir, "guidelines")
        os.makedirs(target_agents_dir, exist_ok=True)
        os.makedirs(target_instructions_dir, exist_ok=True)
        os.makedirs(target_guidelines_dir, exist_ok=True)

        print("Copying agents...")
        deploy_agents(
            agents_src_dir,
            target_agents_dir,
            repo_root,
            tool="copilot",
            skill_mode=False,
        )

        print("Copying instructions...")
        for f in glob.glob(os.path.join(instructions_src_dir, "*.md")):
            shutil.copy(f, target_instructions_dir)

        print("Copying selected guideline templates...")
        deploy_guidelines_to_github(
            target_guidelines_dir,
            repo_root,
            backend_arch_file,
            frontend_arch_file,
            backend_doc_file,
            frontend_doc_file,
            include_conventions,
        )

    # --- Deploy OpenCode ---
    if deploy_opencode:
        print("Deploying OpenCode setup...")
        target_opencode_dir = os.path.join(target_path, ".opencode", "skills")
        deploy_agents(
            agents_src_dir,
            target_opencode_dir,
            repo_root,
            tool="opencode",
            skill_mode=True,
        )
        deploy_guidelines_to_skills(
            target_opencode_dir,
            repo_root,
            backend_arch_file,
            frontend_arch_file,
            backend_doc_file,
            frontend_doc_file,
            include_conventions,
            tool="opencode",
        )
        print(f"Copied skills to {target_opencode_dir}")

    # --- Deploy Claude Code ---
    if deploy_claude:
        print("Deploying Claude Code setup...")
        target_claude_dir = os.path.join(target_path, ".claude", "skills")
        deploy_agents(agents_src_dir, target_claude_dir, repo_root, tool="claude", skill_mode=True)
        deploy_guidelines_to_skills(
            target_claude_dir,
            repo_root,
            backend_arch_file,
            frontend_arch_file,
            backend_doc_file,
            frontend_doc_file,
            include_conventions,
            tool="claude",
        )
        print(f"Copied skills to {target_claude_dir}")

    print()
    print("Initialization complete.")
    print(f"Target: {target_path}")
    if deploy_copilot:
        print("✓ GitHub Copilot (VS Code): .github/agents, instructions, and guidelines")
    if deploy_opencode:
        print("✓ OpenCode: .opencode/skills/ (with references/)")
    if deploy_claude:
        print("✓ Claude Code: .claude/skills/ (with references/)")
    if backend_doc_msg:
        print(f"- {backend_doc_msg}")
    if frontend_doc_msg:
        print(f"- {frontend_doc_msg}")
    print(f"- {conventions_msg}")


if __name__ == "__main__":
    main()
