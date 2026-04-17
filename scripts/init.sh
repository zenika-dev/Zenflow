#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

AGENTS_SRC_DIR="${REPO_ROOT}/.github/agents"
TEMPLATES_DIR="${REPO_ROOT}/templates/guidelines"

if [[ ! -d "${AGENTS_SRC_DIR}" ]]; then
  echo "Error: missing agents source directory: ${AGENTS_SRC_DIR}" >&2
  exit 1
fi

if [[ ! -d "${TEMPLATES_DIR}" ]]; then
  echo "Error: missing templates source directory: ${TEMPLATES_DIR}" >&2
  exit 1
fi

echo "Zenflow initialization"
echo "This script copies .github/agents and selected guideline templates into a target folder."
echo

read -r -p "Target local repository folder path: " TARGET_PATH
if [[ -z "${TARGET_PATH}" ]]; then
  echo "Error: target path is required." >&2
  exit 1
fi

if [[ ! -d "${TARGET_PATH}" ]]; then
  echo "Error: target folder does not exist: ${TARGET_PATH}" >&2
  exit 1
fi

TARGET_GITHUB_DIR="${TARGET_PATH}/.github"
TARGET_AGENTS_DIR="${TARGET_GITHUB_DIR}/agents"
TARGET_GUIDELINES_DIR="${TARGET_GITHUB_DIR}/guidelines"

mkdir -p "${TARGET_AGENTS_DIR}"
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
      BACKEND_REVIEW_FILE="backend-java.md"
      ;;
    2)
      BACKEND_ARCH_FILE="golang-gin.md"
      BACKEND_REVIEW_FILE="backend-golang.md"
      ;;
    3)
      BACKEND_ARCH_FILE="python-fastapi.md"
      BACKEND_REVIEW_FILE="backend-python-fastapi.md"
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
      FRONTEND_REVIEW_FILE="frontend-react.md"
      ;;
    2)
      FRONTEND_ARCH_FILE="nextjs-app-router.md"
      FRONTEND_REVIEW_FILE="frontend-nextjs-app-router.md"
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

echo "Copying selected guideline templates..."
copy_file "${TEMPLATES_DIR}/backend/${BACKEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-backend.md"
copy_file "${TEMPLATES_DIR}/frontend/${FRONTEND_ARCH_FILE}" "${TARGET_GUIDELINES_DIR}/architecture-frontend.md"
copy_file "${TEMPLATES_DIR}/review/${BACKEND_REVIEW_FILE}" "${TARGET_GUIDELINES_DIR}/review-backend.md"
copy_file "${TEMPLATES_DIR}/review/${FRONTEND_REVIEW_FILE}" "${TARGET_GUIDELINES_DIR}/review-frontend.md"

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
echo "- Copied architecture/review guidelines to ${TARGET_GUIDELINES_DIR}"
echo "- ${CONVENTIONS_MSG}"
