#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

AGENTS_SRC_DIR="${REPO_ROOT}/.github/agents"
INSTRUCTIONS_SRC_DIR="${REPO_ROOT}/.github/instructions"
TEMPLATES_DIR="${REPO_ROOT}/templates/guidelines"

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

DEFAULT_TARGET_PATH="${REPO_ROOT}/target"
read -r -p "Target path [${DEFAULT_TARGET_PATH}]: " TARGET_PATH_INPUT
TARGET_PATH="${TARGET_PATH_INPUT:-${DEFAULT_TARGET_PATH}}"

echo "Zenflow initialization"
echo "The following will be generated inside the target folder (${TARGET_PATH}):"
echo "  - .github/agents/        (agent definitions)"
echo "  - .github/instructions/  (instruction files)"
echo "  - .github/guidelines/    (architecture, review, and conventions templates)"
echo
read -r -n 1 -s -p "Press any key to continue..."
echo

TARGET_GITHUB_DIR="${TARGET_PATH}/.github"
TARGET_AGENTS_DIR="${TARGET_GITHUB_DIR}/agents"
TARGET_INSTRUCTIONS_DIR="${TARGET_GITHUB_DIR}/instructions"
TARGET_GUIDELINES_DIR="${TARGET_GITHUB_DIR}/guidelines"

mkdir -p "${TARGET_AGENTS_DIR}"
mkdir -p "${TARGET_INSTRUCTIONS_DIR}"
mkdir -p "${TARGET_GUIDELINES_DIR}"

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
      ;;
    2)
      BACKEND_ARCH_FILE="golang-gin.md"
      ;;
    3)
      BACKEND_ARCH_FILE="python-fastapi.md"
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
      ;;
    2)
      FRONTEND_ARCH_FILE="nextjs-app-router.md"
      ;;
    *)
      echo "Error: invalid frontend choice '${frontend_choice}'." >&2
      exit 1
      ;;
  esac
}

choose_backend_stack
choose_frontend_stack

echo
read -r -p "Include git conventions template as .github/guidelines/conventions.md? [Y/n]: " INCLUDE_CONVENTIONS
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

echo
echo "Copying agents..."
cp "${AGENTS_SRC_DIR}"/*.md "${TARGET_AGENTS_DIR}/"

echo "Copying instructions..."
cp "${INSTRUCTIONS_SRC_DIR}"/*.md "${TARGET_INSTRUCTIONS_DIR}/"

echo "Copying selected guideline templates..."
copy_file "${TEMPLATES_DIR}/backend/${BACKEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-backend.md"
copy_file "${TEMPLATES_DIR}/frontend/${FRONTEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-frontend.md"
copy_file "${TEMPLATES_DIR}/review/backend.md" "${TARGET_GUIDELINES_DIR}/review-backend.md"
copy_file "${TEMPLATES_DIR}/review/frontend.md" "${TARGET_GUIDELINES_DIR}/review-frontend.md"

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

echo
echo "Initialization complete."
echo "Target: ${TARGET_PATH}"
echo "- Copied agents to ${TARGET_AGENTS_DIR}"
echo "- Copied instructions to ${TARGET_INSTRUCTIONS_DIR}"
echo "- Copied architecture/review guidelines to ${TARGET_GUIDELINES_DIR}"
echo "- ${CONVENTIONS_MSG}"
