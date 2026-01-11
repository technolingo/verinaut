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

.PHONY: help api api-migrate api-migrations api-test api-test-cov \
        web web-build web-install web-preview web-clean \
        web-lint web-lint-fix web-format web-format-check web-typecheck web-check \
        agent-test vectordb-test install dev

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
	@echo "    make web              - Start Vite dev server"
	@echo "    make web-build        - Build for production"
	@echo "    make web-preview      - Preview production build"
	@echo "    make web-install      - Install dependencies"
	@echo "    make web-clean        - Remove build artifacts and cache"
	@echo "    make web-lint         - Run ESLint"
	@echo "    make web-lint-fix     - Run ESLint with auto-fix"
	@echo "    make web-format       - Format code with Prettier"
	@echo "    make web-format-check - Check code formatting"
	@echo "    make web-typecheck    - Run TypeScript type checking"
	@echo "    make web-check        - Run all checks (type + lint + format)"
	@echo ""
	@echo "  Agent (packages/agent):"
	@echo "    make agent-test       - Run agent tests"
	@echo ""
	@echo "  Combined:"
	@echo "    make install          - Install all dependencies"
	@echo "    make dev              - Instructions to run dev servers"

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
	cd $(WEB_DIR) && bun run dev

web-build:
	cd $(WEB_DIR) && bun run build

web-preview:
	cd $(WEB_DIR) && bun run preview

web-install:
	cd $(WEB_DIR) && bun install

web-clean:
	rm -rf $(WEB_DIR)/dist $(WEB_DIR)/node_modules/.vite

web-lint:
	cd $(WEB_DIR) && bun eslint .

web-lint-fix:
	cd $(WEB_DIR) && bun eslint . --fix

web-format:
	cd $(WEB_DIR) && bun prettier --write "src/**/*.{ts,tsx,css}"

web-format-check:
	cd $(WEB_DIR) && bun prettier --check "src/**/*.{ts,tsx,css}"

web-typecheck:
	cd $(WEB_DIR) && bun tsc --noEmit

web-check:
	cd $(WEB_DIR) && bun tsc --noEmit && bun run lint && bun prettier --check "src/**/*.{ts,tsx,css}"

# ==================== AGENT ====================

agent-test:
	cd $(AGENT_DIR) && uv run pytest


# ==================== VECTORDB ====================

vectordb-test:
	cd $(VECTORDB_DIR) && uv run pytest

# ==================== COMBINED ====================

# Install all dependencies
install:
	cd $(API_DIR) && uv sync
	cd $(WEB_DIR) && bun install

# Run both API and Web (requires terminal multiplexer or run in separate terminals)
dev:
	@echo "Run these in separate terminals:"
	@echo "  make api"
	@echo "  make web"
