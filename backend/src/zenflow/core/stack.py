"""Stack and framework constants for Zenflow CLI."""

from __future__ import annotations

# Each framework entry: (label, arch_file, doc_file)
# Dict keys are the language labels; numbers are inferred from position in cli.py.

BACKEND: dict[str, list[tuple[str, str, str]]] = {
    "Python": [
        ("None (plain Python)", "python.md.j2", ""),
        ("FastAPI", "python-fastapi.md.j2", ""),
    ],
    "Java": [
        ("None (plain Java)", "java.md.j2", ""),
        ("Spring Boot", "java-spring-boot.md.j2", "java-spring-boot.md.j2"),
    ],
    "Go": [
        ("None (plain Go)", "golang.md.j2", ""),
        ("Gin", "golang-gin.md.j2", ""),
    ],
}

FRONTEND: dict[str, list[tuple[str, str, str]]] = {
    "TypeScript": [
        ("None (plain TypeScript)", "typescript.md.j2", ""),
        ("React", "react-typescript.md.j2", "react-typescript.md.j2"),
        ("Next.js (App Router)", "nextjs-app-router.md.j2", ""),
    ],
}
