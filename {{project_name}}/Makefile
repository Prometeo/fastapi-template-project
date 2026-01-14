SHELL := /bin/bash
# =============================================================================
# Variables
MMSG =
# =============================================================================

.DEFAULT_GOAL:=help
.ONESHELL:
.EXPORT_ALL_VARIABLES:

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


# =============================================================================
# Developer Utils
# =============================================================================


.PHONY: up
up:                                                 ## Start containers
	@docker compose up -d


.PHONY: install
install:											## Install dependencies
	@uv sync


.PHONY: clean
clean:												## Cleanup temporary build artifacts
	@echo "=> Cleaning working directory"
	@rm -rf .pytest_cache .ruff_cache .hypothesis build/ -rf dist/ .eggs/
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -type f -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '.ipynb_checkpoints' -exec rm -rf {} +
	@rm -rf .coverage coverage.xml coverage.json htmlcov/ .pytest_cache tests/.pytest_cache tests/**/.pytest_cache .mypy_cache

.PHONY: migrations
migrations:											## Make migrations
	@docker compose exec api alembic revision --autogenerate -m $(MMSG)


.PHONY: migrate
migrate:                                            ## Apply migrations (E.g: make migrations MMSG=test migration)
	@docker compose exec api alembic upgrade head

.PHONY: tests
tests:                                               ## Run tests
	@docker compose exec --workdir /app api pytest --cov --cov-report=term-missing
