#!/usr/bin/env python3
"""Redirect shim — the init script has moved to src/zenflow/init.py.

Run via uv:
    uv run zenflow-init
"""

import subprocess
import sys

print(
    "Note: scripts/init.py is a compatibility shim. "
    "Run 'uv run zenflow-init' instead.",
    file=sys.stderr,
)
result = subprocess.run(
    [sys.executable, "-m", "zenflow.init", *sys.argv[1:]],
    check=False,
)
sys.exit(result.returncode)
