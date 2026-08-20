"""Jinja2 environment construction and rendering helpers."""

from __future__ import annotations

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def make_env(repo_root: str) -> Environment:
    """Return a Jinja2 Environment with template search paths.

    Args:
        repo_root: Repository root path.

    Returns:
        Configured Jinja2 Environment.
    """
    search_paths: list[str] = [os.path.join(repo_root, "templates")]

    return Environment(
        loader=FileSystemLoader(search_paths),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_template(
    env: Environment,
    template_path: str,
    context: dict[str, object],
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
    context: dict[str, object],
    *,
    skill_mode: bool = False,
) -> None:
    """Render a template and write to dst_path.

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
    context: dict[str, object],
) -> None:
    """Render a guideline template and write to dst_path.

    Args:
        src_template: Template path relative to loader root.
        dst_path: Absolute output path.
        env: Configured Jinja2 Environment.
        context: Template variables.
    """
    assemble_agent(src_template, dst_path, env, context)
