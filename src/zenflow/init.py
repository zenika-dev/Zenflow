#!/usr/bin/env python3
"""Zenflow initialization script."""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


# ---------------------------------------------------------------------------
# Jinja2 environment
# ---------------------------------------------------------------------------

def make_env(repo_root: str, agent_name: str | None = None) -> Environment:
    """Return a Jinja2 Environment with template search paths.

    Search order:
    1. templates/skills/<agent_name>/  (tool-specific overrides, if agent_name given)
    2. templates/                      (canonical templates and partials)
    """
    search_paths: list[str] = []
    if agent_name:
        override_dir = os.path.join(repo_root, "templates", "skills", agent_name)
        if os.path.isdir(override_dir):
            search_paths.append(override_dir)
    search_paths.append(os.path.join(repo_root, "templates"))

    return Environment(
        loader=FileSystemLoader(search_paths),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


# ---------------------------------------------------------------------------
# Guidelines context per tool
# ---------------------------------------------------------------------------

def guidelines_context(tool: str) -> dict[str, str]:
    """Return the guidelines file paths for a given tool.

    Args:
        tool: One of 'copilot', 'opencode', 'claude'.

    Returns:
        A dict mapping guideline keys to their file paths for that tool.
    """
    if tool == "copilot":
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
    if tool == "opencode":
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
    if tool == "claude":
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


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def render_template(
    env: Environment,
    template_path: str,
    context: dict,
) -> str:
    """Render a Jinja2 template file with the given context.

    Args:
        env: Configured Jinja2 Environment.
        template_path: Path relative to the loader's search root.
        context: Template variables.

    Returns:
        Rendered string content.
    """
    tmpl = env.get_template(template_path)
    return tmpl.render(**context)


def write_rendered(content: str, dst_path: str) -> None:
    """Write rendered content to dst_path, creating parent dirs as needed.

    Args:
        content: Rendered file content.
        dst_path: Absolute destination path.
    """
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    Path(dst_path).write_text(content, encoding="utf-8")


def assemble_agent(
    src_template: str,
    dst_path: str,
    env: Environment,
    context: dict,
    *,
    skill_mode: bool = False,
) -> None:
    """Render an agent template and write to dst_path.

    Args:
        src_template: Template path relative to loader root (e.g. 'agents/backend.agent.md.j2').
        dst_path: Absolute output path.
        env: Configured Jinja2 Environment.
        context: Template variables.
        skill_mode: Passed into the template as a variable — controls handoffs block and Next Steps footer.
    """
    rendered = render_template(env, src_template, {**context, "skill_mode": skill_mode})
    write_rendered(rendered, dst_path)


def assemble_guideline(
    src_template: str,
    dst_path: str,
    env: Environment,
    context: dict,
) -> None:
    """Render a guideline template and write to dst_path.

    Args:
        src_template: Template path relative to loader root.
        dst_path: Absolute output path.
        env: Configured Jinja2 Environment.
        context: Template variables (guidelines context not needed for guideline files).
    """
    rendered = render_template(env, src_template, context)
    write_rendered(rendered, dst_path)


# ---------------------------------------------------------------------------
# Deployment helpers
# ---------------------------------------------------------------------------

def deploy_agents(
    agents_src_dir: str,
    target_agents_dir: str,
    repo_root: str,
    tool: str,
    *,
    skill_mode: bool = False,
) -> None:
    """Render and deploy all agent templates.

    Args:
        agents_src_dir: Directory containing *.agent.md.j2 source files.
        target_agents_dir: Destination directory.
        repo_root: Repository root path.
        tool: Tool name for guidelines context ('copilot', 'opencode', 'claude').
        skill_mode: If True, strips handoffs and appends Next Steps block.
    """
    os.makedirs(target_agents_dir, exist_ok=True)
    context = {"guidelines": guidelines_context(tool)}

    for agent_file in glob.glob(os.path.join(agents_src_dir, "*.md.j2")):
        agent_name = re.sub(
            r"\.agent$", "", os.path.splitext(os.path.splitext(os.path.basename(agent_file))[0])[0]
        )
        env = make_env(repo_root, agent_name=agent_name)
        template_path = f"agents/{os.path.basename(agent_file)}"

        if skill_mode:
            skill_dir = os.path.join(target_agents_dir, agent_name)
            dst = os.path.join(skill_dir, "SKILL.md")
        else:
            # Strip .j2 suffix for output filename
            out_name = os.path.basename(agent_file)[:-len(".j2")]
            dst = os.path.join(target_agents_dir, out_name)

        assemble_agent(template_path, dst, env, context, skill_mode=skill_mode)


def deploy_guidelines_to_github(
    templates_dir: str,
    target_guidelines_dir: str,
    repo_root: str,
    backend_arch_file: str,
    frontend_arch_file: str,
    backend_doc_file: str,
    frontend_doc_file: str,
    include_conventions: bool,
) -> None:
    """Deploy guideline files to .github/guidelines/ (GitHub Copilot).

    Args:
        templates_dir: Path to templates/guidelines/.
        target_guidelines_dir: Destination .github/guidelines/ path.
        repo_root: Repository root path.
        backend_arch_file: Selected backend architecture template filename.
        frontend_arch_file: Selected frontend architecture template filename.
        backend_doc_file: Selected backend documentation template filename (may be empty).
        frontend_doc_file: Selected frontend documentation template filename (may be empty).
        include_conventions: Whether to include git conventions.
    """
    env = make_env(repo_root)
    ctx = {"guidelines": guidelines_context("copilot")}

    def deploy(src_subdir: str, src_filename: str, dst_filename: str) -> None:
        src_template = f"guidelines/{src_subdir}/{src_filename}"
        dst = os.path.join(target_guidelines_dir, dst_filename)
        assemble_guideline(src_template, dst, env, ctx)

    if backend_arch_file:
        deploy("backend", backend_arch_file, "architecture-backend.md")
        deploy("review", "backend.md.j2", "review-backend.md")
    if frontend_arch_file:
        deploy("frontend", frontend_arch_file, "architecture-frontend.md")
        deploy("review", "frontend.md.j2", "review-frontend.md")

    if backend_doc_file:
        deploy("documentation", backend_doc_file, "documentation-backend.md")
    if frontend_doc_file:
        deploy("documentation", frontend_doc_file, "documentation-frontend.md")
    if include_conventions:
        deploy("git-conventions", "default.md.j2", "conventions.md")


def deploy_guidelines_to_skills(
    templates_dir: str,
    target_skills_dir: str,
    repo_root: str,
    backend_arch_file: str,
    frontend_arch_file: str,
    backend_doc_file: str,
    frontend_doc_file: str,
    include_conventions: bool,
    tool: str,
) -> None:
    """Deploy guideline files into skill references/ subdirs (OpenCode / Claude Code).

    Mapping:
      backend/<arch>.md.j2         -> backend/references/architecture.md
      frontend/<arch>.md.j2        -> frontend/references/architecture.md
      review/backend.md.j2         -> reviewer/references/review-backend.md
      review/frontend.md.j2        -> reviewer/references/review-frontend.md
      documentation/<doc>.md.j2    -> documentation/references/documentation-backend.md (optional)
      documentation/<doc>.md.j2    -> documentation/references/documentation-frontend.md (optional)
      git-conventions/default.md.j2 -> git/references/conventions.md (optional)

    Args:
        templates_dir: Path to templates/guidelines/.
        target_skills_dir: Root skills directory (e.g. .opencode/skills/).
        repo_root: Repository root path.
        backend_arch_file: Selected backend architecture template filename.
        frontend_arch_file: Selected frontend architecture template filename.
        backend_doc_file: Selected backend documentation template filename (may be empty).
        frontend_doc_file: Selected frontend documentation template filename (may be empty).
        include_conventions: Whether to include git conventions.
        tool: Tool name ('opencode' or 'claude') for guidelines context.
    """
    env = make_env(repo_root)
    ctx = {"guidelines": guidelines_context(tool)}

    def deploy(src_subdir: str, src_filename: str, skill_name: str, dst_filename: str) -> None:
        src_template = f"guidelines/{src_subdir}/{src_filename}"
        dst = os.path.join(target_skills_dir, skill_name, "references", dst_filename)
        assemble_guideline(src_template, dst, env, ctx)

    if backend_arch_file:
        deploy("backend", backend_arch_file, "backend", "architecture.md")
        deploy("review", "backend.md.j2", "reviewer", "review-backend.md")
    if frontend_arch_file:
        deploy("frontend", frontend_arch_file, "frontend", "architecture.md")
        deploy("review", "frontend.md.j2", "reviewer", "review-frontend.md")

    if backend_doc_file:
        deploy("documentation", backend_doc_file, "documentation", "documentation-backend.md")
    if frontend_doc_file:
        deploy("documentation", frontend_doc_file, "documentation", "documentation-frontend.md")
    if include_conventions:
        deploy("git-conventions", "default.md.j2", "git", "conventions.md")


# ---------------------------------------------------------------------------
# Directory / path helpers
# ---------------------------------------------------------------------------

def get_dirs(repo_root: str) -> tuple[str, str, str]:
    """Return key source directories derived from repo_root.

    Args:
        repo_root: Repository root path.

    Returns:
        Tuple of (agents_src_dir, instructions_src_dir, templates_dir).
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


def choose_backend_stack() -> tuple[str, str]:
    """Prompt user to choose backend stack.

    Returns:
        Tuple of (arch_filename, doc_filename) — doc_filename may be empty string.
    """
    print()
    print("Choose backend stack:")
    print("  1) java-spring-boot")
    print("  2) golang-gin")
    print("  3) python-fastapi")
    choice = input("Enter choice [1-3]: ").strip()
    options: dict[str, tuple[str, str]] = {
        "1": ("java-spring-boot.md.j2", "java-spring-boot.md.j2"),
        "2": ("golang-gin.md.j2", ""),
        "3": ("python-fastapi.md.j2", ""),
    }
    if choice not in options:
        print(f"Error: invalid backend choice '{choice}'.", file=sys.stderr)
        sys.exit(1)
    return options[choice]


def choose_frontend_stack() -> tuple[str, str]:
    """Prompt user to choose frontend stack.

    Returns:
        Tuple of (arch_filename, doc_filename) — doc_filename may be empty string.
    """
    print()
    print("Choose frontend stack:")
    print("  1) react-typescript")
    print("  2) nextjs-app-router")
    choice = input("Enter choice [1-2]: ").strip()
    options: dict[str, tuple[str, str]] = {
        "1": ("react-typescript.md.j2", "react-typescript.md.j2"),
        "2": ("nextjs-app-router.md.j2", ""),
    }
    if choice not in options:
        print(f"Error: invalid frontend choice '{choice}'.", file=sys.stderr)
        sys.exit(1)
    return options[choice]


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
    # src/zenflow/init.py -> repo root is three levels up
    repo_root = os.path.dirname(os.path.dirname(script_dir))

    agents_src_dir, instructions_src_dir, templates_dir = get_dirs(repo_root)
    validate_dirs(agents_src_dir, instructions_src_dir, templates_dir)

    # --- User configuration ---
    default_target_path = os.path.join(repo_root, "target")
    target_path_input = input(f"Target path [{default_target_path}]: ").strip()
    target_path = target_path_input or default_target_path

    deploy_copilot = input("Set up GitHub Copilot (VS Code)? [Y/N]: ").strip().lower() == "y"
    deploy_opencode = input("Set up OpenCode? [Y/N]: ").strip().lower() == "y"
    deploy_claude = input("Set up Claude Code? [Y/N]: ").strip().lower() == "y"

    if not any([deploy_copilot, deploy_opencode, deploy_claude]):
        print("Error: at least one tool must be selected.", file=sys.stderr)
        sys.exit(1)

    print("Zenflow initialization")
    print(f"Target path: {target_path}")
    print("Tools:")
    if deploy_copilot:
        print("  \u2713 GitHub Copilot (VS Code)")
    if deploy_opencode:
        print("  \u2713 OpenCode")
    if deploy_claude:
        print("  \u2713 Claude Code")
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
    include_conventions_input = (
        input("Include git conventions template? [Y/N]: ").strip()
        or "Y"
    )

    if include_conventions_input.lower() in ("y", ""):
        include_conventions = True
        conventions_msg = "Included conventions"
    elif include_conventions_input.lower() == "n":
        include_conventions = False
        conventions_msg = "Skipped conventions"
    else:
        print(
            f"Error: invalid conventions choice '{include_conventions_input}'. Use Y or N.",
            file=sys.stderr,
        )
        sys.exit(1)

    backend_doc_msg = "Included backend documentation template" if backend_doc_file else ("Skipped backend documentation template" if include_backend else None)
    frontend_doc_msg = "Included frontend documentation template" if frontend_doc_file else ("Skipped frontend documentation template" if include_frontend else None)

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
        deploy_agents(agents_src_dir, target_agents_dir, repo_root, tool="copilot", skill_mode=False)

        print("Copying instructions...")
        for f in glob.glob(os.path.join(instructions_src_dir, "*.md")):
            shutil.copy(f, target_instructions_dir)

        print("Copying selected guideline templates...")
        deploy_guidelines_to_github(
            templates_dir, target_guidelines_dir, repo_root,
            backend_arch_file, frontend_arch_file,
            backend_doc_file, frontend_doc_file,
            include_conventions,
        )

    # --- Deploy OpenCode ---
    if deploy_opencode:
        print("Deploying OpenCode setup...")
        target_opencode_dir = os.path.join(target_path, ".opencode", "skills")
        deploy_agents(agents_src_dir, target_opencode_dir, repo_root, tool="opencode", skill_mode=True)
        deploy_guidelines_to_skills(
            templates_dir, target_opencode_dir, repo_root,
            backend_arch_file, frontend_arch_file,
            backend_doc_file, frontend_doc_file,
            include_conventions,
            tool="opencode",
        )
        print(f"Copied skills to {target_opencode_dir}")

        agents_template = os.path.join(repo_root, "templates", "AGENTS.md")
        agents_target = os.path.join(target_path, "AGENTS.md")
        if os.path.isfile(agents_template):
            shutil.copy(agents_template, agents_target)
            print(f"Copied AGENTS.md to {target_path}")
        else:
            print(f"Warning: AGENTS.md template not found at {agents_template}", file=sys.stderr)

    # --- Deploy Claude Code ---
    if deploy_claude:
        print("Deploying Claude Code setup...")
        target_claude_dir = os.path.join(target_path, ".claude", "skills")
        deploy_agents(agents_src_dir, target_claude_dir, repo_root, tool="claude", skill_mode=True)
        deploy_guidelines_to_skills(
            templates_dir, target_claude_dir, repo_root,
            backend_arch_file, frontend_arch_file,
            backend_doc_file, frontend_doc_file,
            include_conventions,
            tool="claude",
        )
        print(f"Copied skills to {target_claude_dir}")

        claude_template = os.path.join(repo_root, "templates", "AGENTS.md")
        claude_target = os.path.join(target_path, "CLAUDE.md")
        if os.path.isfile(claude_template):
            shutil.copy(claude_template, claude_target)
            print(f"Copied AGENTS.md to {target_path}")
        else:
            print(f"Warning: AGENTS.md template not found at {claude_template}", file=sys.stderr)

    print()
    print("Initialization complete.")
    print(f"Target: {target_path}")
    if deploy_copilot:
        print("\u2713 GitHub Copilot (VS Code): .github/agents, instructions, and guidelines")
    if deploy_opencode:
        print("\u2713 OpenCode: .opencode/skills/ (with references/) and AGENTS.md")
    if deploy_claude:
        print("\u2713 Claude Code: .claude/skills/ (with references/) and CLAUDE.md")
    if backend_doc_msg:
        print(f"- {backend_doc_msg}")
    if frontend_doc_msg:
        print(f"- {frontend_doc_msg}")
    print(f"- {conventions_msg}")


if __name__ == "__main__":
    main()
