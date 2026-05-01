# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.3
ARG BUILD_ENV=development
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh

WORKDIR /app

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

# COPY ./src/ .
COPY ./pyproject.toml .
COPY ./uv.lock .


# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv
RUN if [ "$BUILD_ENV" = "production" ]; then \
    uv sync --no-group=dev; \
else \
    uv sync;\
fi
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync


FROM python:${PYTHON_VERSION}-slim-bookworm AS base

# Copy the installed Python packages from the builder stage
COPY --from=builder /app/.venv/ /app/.venv/

COPY ./src ./app/src

EXPOSE 8000


# Development stage
FROM base AS development

ARG USER_UID
ARG USER_GID

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONPATH="/app/src"

RUN addgroup --gid "${USER_GID}" appgroup && \
    adduser \
        --disabled-password \
        --gecos "" \
        --home "/nonexistent" \
        --shell "/usr/sbin/nologin" \
        --no-create-home \
        --uid "${USER_UID}" \
        --gid "${USER_GID}" \
        appuser

# Give ownership of /app to appuser
RUN chown -R appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

COPY --chown=appuser:appuser ./tests/ ./app/tests
COPY --chown=appuser:appuser ./.coveragerc ./app
COPY --chown=appuser:appuser ./pyproject.toml ./app

WORKDIR /app/src

CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]


# Production ready stage
FROM base AS production

ENV PATH="/app/.venv/bin:{$PATH}"

WORKDIR /app/src

CMD ["uvicorn", "main:app","--workers","4", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
