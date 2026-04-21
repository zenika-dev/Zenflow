#!/usr/bin/env bash
set -euo pipefail


# Setup directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

AGENTS_SRC_DIR="${REPO_ROOT}/.github/agents"
INSTRUCTIONS_SRC_DIR="${REPO_ROOT}/.github/instructions"
TEMPLATES_DIR="${REPO_ROOT}/templates/guidelines"
DOCUMENTATION_TEMPLATES_DIR="${TEMPLATES_DIR}/documentation"

if [[ ! -d "${AGENTS_SRC_DIR}" ]]; then
  echo "Error: missing agents source directory: ${AGENTS_SRC_DIR}" >&2
  exit 1
fi

if [[ ! -d "${INSTRUCTIONS_SRC_DIR}" ]]; then
  echo "Error: missing instructions source directory: ${INSTRUCTIONS_SRC_DIR}" >&2
  exit 1
fi

if [[ ! -d "${TEMPLATES_DIR}" ]]; then
  echo "Error: missing templates source directory: ${TEMPLATES_DIR}" >&2
  exit 1
fi

# Help message
show_help() {
  cat <<EOF
Usage: $(basename "$0") [--help|-h]

Initializes Zenflow target scaffolding by copying:
  - .github/agents
  - .github/instructions
  - selected templates under .github/guidelines

Options:
  -h, --help    Show this help message and exit
EOF
}

for arg in "$@"; do
  case "${arg}" in
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Error: unknown argument '${arg}'. Use --help for usage." >&2
      exit 1
      ;;
  esac
done

# User configurations
# 1. Target directory
DEFAULT_TARGET_PATH="${REPO_ROOT}/target"
read -r -p "Target path [${DEFAULT_TARGET_PATH}]: " TARGET_PATH_INPUT
TARGET_PATH="${TARGET_PATH_INPUT:-${DEFAULT_TARGET_PATH}}"

# 2. Optional add-on tools (Copilot/VS Code is always deployed)
read -r -p "Also set up OpenCode? [Y/N]: " opencode_input
DEPLOY_OPENCODE=false
[[ "${opencode_input}" =~ ^[Yy]$ ]] && DEPLOY_OPENCODE=true

read -r -p "Also set up Claude Code? [Y/N]: " claude_input
DEPLOY_CLAUDE=false
[[ "${claude_input}" =~ ^[Yy]$ ]] && DEPLOY_CLAUDE=true

echo "Zenflow initialization"
echo "Target path: ${TARGET_PATH}"
echo "Tools:"
echo "  ✓ GitHub Copilot (VS Code) — always installed"
[[ "${DEPLOY_OPENCODE}" == "true" ]] && echo "  ✓ OpenCode"
[[ "${DEPLOY_CLAUDE}" == "true" ]] && echo "  ✓ Claude Code"
echo
echo "The following will be generated:"
echo "  - .github/agents/        (agent definitions)"
echo "  - .github/instructions/  (instruction files)"
echo "  - .github/guidelines/    (architecture, review, and conventions)"
[[ "${DEPLOY_OPENCODE}" == "true" ]] && echo "  - .opencode/skills/      (OpenCode skill definitions)"
[[ "${DEPLOY_CLAUDE}" == "true" ]] && echo "  - .claude/skills/        (Claude Code skill definitions)"
echo
read -r -n 1 -s -p "Press any key to continue..."
echo

TARGET_GITHUB_DIR="${TARGET_PATH}/.github"
TARGET_AGENTS_DIR="${TARGET_GITHUB_DIR}/agents"
TARGET_INSTRUCTIONS_DIR="${TARGET_GITHUB_DIR}/instructions"
TARGET_GUIDELINES_DIR="${TARGET_GITHUB_DIR}/guidelines"

# Always create .github directories (Copilot/VS Code is always deployed)
mkdir -p "${TARGET_AGENTS_DIR}"
mkdir -p "${TARGET_INSTRUCTIONS_DIR}"
mkdir -p "${TARGET_GUIDELINES_DIR}"


# 3. Stack choices for guidelines
choose_backend_stack() {
  echo
  echo "Choose backend stack:"
  echo "  1) java-spring-boot"
  echo "  2) golang-gin"
  echo "  3) python-fastapi"
  read -r -p "Enter choice [1-3]: " backend_choice

  case "${backend_choice}" in
    1)
      BACKEND_ARCH_FILE="java-spring-boot.md"
      BACKEND_DOC_FILE="java-spring-boot.md"
      ;;
    2)
      BACKEND_ARCH_FILE="golang-gin.md"
      BACKEND_DOC_FILE=""
      ;;
    3)
      BACKEND_ARCH_FILE="python-fastapi.md"
      BACKEND_DOC_FILE=""
      ;;
    *)
      echo "Error: invalid backend choice '${backend_choice}'." >&2
      exit 1
      ;;
  esac
}

choose_frontend_stack() {
  echo
  echo "Choose frontend stack:"
  echo "  1) react-typescript"
  echo "  2) nextjs-app-router"
  read -r -p "Enter choice [1-2]: " frontend_choice

  case "${frontend_choice}" in
    1)
      FRONTEND_ARCH_FILE="react-typescript.md"
      FRONTEND_DOC_FILE="react-typescript.md"
      ;;
    2)
      FRONTEND_ARCH_FILE="nextjs-app-router.md"
      FRONTEND_DOC_FILE=""
      ;;
    *)
      echo "Error: invalid frontend choice '${frontend_choice}'." >&2
      exit 1
      ;;
  esac
}

# 3. Stack choices
choose_backend_stack
choose_frontend_stack

echo
read -r -p "Include git conventions template as .github/guidelines/conventions.md? [Y/N]: " INCLUDE_CONVENTIONS
INCLUDE_CONVENTIONS="${INCLUDE_CONVENTIONS:-Y}"

copy_file() {
  local src="$1"
  local dst="$2"
  if [[ ! -f "${src}" ]]; then
    echo "Error: source file not found: ${src}" >&2
    exit 1
  fi
  cp "${src}" "${dst}"
}

copy_agents_as_skills() {
  local target_dir="$1"

  mkdir -p "${target_dir}"

  for agent_file in "${AGENTS_SRC_DIR}"/*.md; do
    agent_name=$(basename "$agent_file" .md | sed 's/\.agent//')
    skill_dir="${target_dir}/${agent_name}"
    mkdir -p "$skill_dir"
    cp "$agent_file" "${skill_dir}/SKILL.md"
  done
}

echo

# Deploy Copilot/VS Code (always)
echo "Deploying GitHub Copilot (VS Code) setup..."
echo "Copying agents..."
cp "${AGENTS_SRC_DIR}"/*.md "${TARGET_AGENTS_DIR}/"

echo "Copying instructions..."
cp "${INSTRUCTIONS_SRC_DIR}"/*.md "${TARGET_INSTRUCTIONS_DIR}/"

echo "Copying selected guideline templates..."
copy_file "${TEMPLATES_DIR}/backend/${BACKEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-backend.md"
copy_file "${TEMPLATES_DIR}/frontend/${FRONTEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-frontend.md"
copy_file "${TEMPLATES_DIR}/review/backend.md" "${TARGET_GUIDELINES_DIR}/review-backend.md"
copy_file "${TEMPLATES_DIR}/review/frontend.md" "${TARGET_GUIDELINES_DIR}/review-frontend.md"

if [[ -n "${BACKEND_DOC_FILE}" ]]; then
  copy_file "${DOCUMENTATION_TEMPLATES_DIR}/${BACKEND_DOC_FILE}" "${TARGET_GUIDELINES_DIR}/documentation-backend.md"
  BACKEND_DOC_MSG="Included backend documentation template"
else
  BACKEND_DOC_MSG="Skipped backend documentation template"
fi

if [[ -n "${FRONTEND_DOC_FILE}" ]]; then
  copy_file "${DOCUMENTATION_TEMPLATES_DIR}/${FRONTEND_DOC_FILE}" "${TARGET_GUIDELINES_DIR}/documentation-frontend.md"
  FRONTEND_DOC_MSG="Included frontend documentation template"
else
  FRONTEND_DOC_MSG="Skipped frontend documentation template"
fi

case "${INCLUDE_CONVENTIONS}" in
  Y|y|"")
    copy_file "${TEMPLATES_DIR}/git-conventions/default.md" "${TARGET_GUIDELINES_DIR}/conventions.md"
    CONVENTIONS_MSG="Included conventions.md"
    ;;
  N|n)
    CONVENTIONS_MSG="Skipped conventions.md"
    ;;
  *)
    echo "Error: invalid conventions choice '${INCLUDE_CONVENTIONS}'. Use Y or n." >&2
    exit 1
    ;;
esac

# Deploy OpenCode
if [[ "${DEPLOY_OPENCODE}" == "true" ]]; then
  echo "Deploying OpenCode setup..."
  TARGET_OPENCODE_DIR="${TARGET_PATH}/.opencode/skills"

  # Create OpenCode skills from agent templates
  copy_agents_as_skills "${TARGET_OPENCODE_DIR}"
  echo "Copied skills to ${TARGET_OPENCODE_DIR}"

  # Copy AGENTS.md from template to target
  AGENTS_TEMPLATE="${REPO_ROOT}/templates/AGENTS.md"
  AGENTS_TARGET="${TARGET_PATH}/AGENTS.md"
  if [[ -f "${AGENTS_TEMPLATE}" ]]; then
    cp "${AGENTS_TEMPLATE}" "${AGENTS_TARGET}"
    echo "Copied AGENTS.md to ${TARGET_PATH}"
  else
    echo "Warning: AGENTS.md template not found at ${AGENTS_TEMPLATE}" >&2
  fi
fi

# Deploy Claude Code
if [[ "${DEPLOY_CLAUDE}" == "true" ]]; then
  echo "Deploying Claude Code setup..."
  TARGET_CLAUDE_DIR="${TARGET_PATH}/.claude/skills"

  # Create Claude skills from agent templates
  copy_agents_as_skills "${TARGET_CLAUDE_DIR}"
  echo "Copied skills to ${TARGET_CLAUDE_DIR}"

  # Copy CLAUDE.md from template to target
  CLAUDE_TEMPLATE="${REPO_ROOT}/templates/CLAUDE.md"
  CLAUDE_TARGET="${TARGET_PATH}/CLAUDE.md"
  if [[ -f "${CLAUDE_TEMPLATE}" ]]; then
    cp "${CLAUDE_TEMPLATE}" "${CLAUDE_TARGET}"
    echo "Copied CLAUDE.md to ${TARGET_PATH}"
  else
    echo "Warning: CLAUDE.md template not found at ${CLAUDE_TEMPLATE}" >&2
  fi
fi

echo
echo "Initialization complete."
echo "Target: ${TARGET_PATH}"
echo "✓ GitHub Copilot (VS Code): .github/agents, instructions, and guidelines"
[[ "${DEPLOY_OPENCODE}" == "true" ]] && echo "✓ OpenCode: .opencode/skills/ and AGENTS.md"
[[ "${DEPLOY_CLAUDE}" == "true" ]] && echo "✓ Claude Code: .claude/skills/ and CLAUDE.md"

echo "- ${BACKEND_DOC_MSG}"
echo "- ${FRONTEND_DOC_MSG}"
echo "- ${CONVENTIONS_MSG}"
