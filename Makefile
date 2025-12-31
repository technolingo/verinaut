# Varinaut Monorepo Makefile
# Run all commands from project root

# Directory paths
API_DIR := apps/api
WEB_DIR := apps/web
AGENT_DIR := packages/agent
EVALS_DIR := packages/evals
VECTORDB_DIR := packages/vectordb

# Default target
.DEFAULT_GOAL := help

.PHONY: help api api-migrate api-migrations api-test api-test-cov web web-build agent-test

help:
	@echo "Varinaut Commands:"
	@echo ""
	@echo "  API (apps/api):"
	@echo "    make api              - Start FastAPI dev server"
	@echo "    make api-migrate      - Run database migrations"
	@echo "    make api-migrations   - Generate new migration (MSG=description)"
	@echo "    make api-test         - Run integration tests"
	@echo "    make api-test-cov     - Run tests with coverage"
	@echo ""
	@echo "  Web (apps/web):"
	@echo "    make web              - Start React dev server"
	@echo "    make web-build        - Build for production"
	@echo ""
	@echo "  Agent (packages/agent):"
	@echo "    make agent-test       - Run agent tests"

# ==================== API ====================

api:
	cd $(API_DIR) && uv run uvicorn src.main:app --reload --port 8000

api-migrate:
	cd $(API_DIR) && uv run alembic upgrade head

api-migrations:
ifndef MSG
	$(error MSG is required. Usage: make api-migrations MSG="Your migration message")
endif
	cd $(API_DIR) && uv run alembic revision --autogenerate -m "$(MSG)"

api-test:
	cd $(API_DIR) && uv run pytest -v tests/

api-test-cov:
	cd $(API_DIR) && uv run pytest --cov=src --cov-report=html

# ==================== WEB ====================

web:
	cd $(WEB_DIR) && npm run dev

web-build:
	cd $(WEB_DIR) && npm run build

web-install:
	cd $(WEB_DIR) && npm install

# ==================== AGENT ====================

agent-test:
	cd $(AGENT_DIR) && uv run pytest


# ==================== VECTORDB ====================

vectordb-test:
	cd $(VECTORDB_DIR) && uv run pytest

# ==================== COMBINED ====================

# Install all dependencies
install:
	uv sync
	cd $(WEB_DIR) && npm install

# Run both API and Web (requires terminal multiplexer or run in separate terminals)
dev:
	@echo "Run these in separate terminals:"
	@echo "  make api"
	@echo "  make web"
