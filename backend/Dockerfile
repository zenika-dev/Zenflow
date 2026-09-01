FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src
COPY templates ./templates

RUN uv sync --frozen --extra api --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

# Cloud Run injects $PORT; default to 8080 for local `docker run`.
CMD ["sh", "-c", "uvicorn zenflow.routers.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
