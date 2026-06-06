# ═══════════════════════════════════════════════════════════════════
# Interleet — Makefile
# Development shortcuts for the judge engine
# ═══════════════════════════════════════════════════════════════════

.PHONY: help dev build-sandboxes build-python build-node build-typescript \
        build-go build-cpp build-rust build-java \
        run-worker install clean logs

# Default target
help:
	@echo ""
	@echo "  ╔══════════════════════════════════════════════════╗"
	@echo "  ║        Interleet Judge Engine — Makefile         ║"
	@echo "  ╚══════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Setup:"
	@echo "    make install           Install Python dependencies"
	@echo "    make build-sandboxes   Build all 7 language Docker images"
	@echo ""
	@echo "  Development:"
	@echo "    make dev               Start FastAPI dev server (with workers)"
	@echo "    make run-worker        Run the execution worker separately"
	@echo ""
	@echo "  Individual sandbox builds:"
	@echo "    make build-python"
	@echo "    make build-node"
	@echo "    make build-typescript"
	@echo "    make build-go"
	@echo "    make build-cpp"
	@echo "    make build-rust"
	@echo "    make build-java"
	@echo ""
	@echo "  Docker Compose:"
	@echo "    make up                Start full stack"
	@echo "    make down              Stop full stack"
	@echo "    make logs              Tail logs"
	@echo ""

# ─── Setup ──────────────────────────────────────────────────────────

install:
	@echo "📦 Installing Python dependencies..."
	cd backend && pip install -r requirements.txt

# ─── Sandbox Image Builds ────────────────────────────────────────────

build-python:
	@echo "🐍 Building Python sandbox..."
	docker build -t interleet-python:latest sandboxes/python/

build-node:
	@echo "🟢 Building Node.js sandbox..."
	docker build -t interleet-node:latest sandboxes/node/

build-typescript:
	@echo "🔷 Building TypeScript sandbox..."
	docker build -t interleet-typescript:latest sandboxes/typescript/

build-go:
	@echo "🐹 Building Go sandbox..."
	docker build -t interleet-go:latest sandboxes/go/

build-cpp:
	@echo "⚙️  Building C++ sandbox..."
	docker build -t interleet-cpp:latest sandboxes/cpp/

build-rust:
	@echo "🦀 Building Rust sandbox..."
	docker build -t interleet-rust:latest sandboxes/rust/

build-java:
	@echo "☕ Building Java sandbox..."
	docker build -t interleet-java:latest sandboxes/java/

build-sandboxes: build-python build-node build-typescript build-go build-cpp build-rust build-java
	@echo ""
	@echo "✅ All sandbox images built successfully!"
	@docker images | grep "interleet-" | awk '{printf "   %-30s %s\n", $$1, $$7}'
	@echo ""

# ─── Development ────────────────────────────────────────────────────

dev:
	@echo "🚀 Starting Interleet API (dev mode)..."
	cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run-worker:
	@echo "⚙️  Starting standalone execution worker..."
	cd backend && python -m app.engine.workers.main

# ─── Docker Compose ─────────────────────────────────────────────────

up:
	@echo "🐳 Starting full Interleet stack..."
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f api worker

clean:
	@echo "🧹 Removing sandbox images..."
	-docker rmi interleet-python:latest interleet-node:latest \
	            interleet-typescript:latest interleet-go:latest \
	            interleet-cpp:latest interleet-rust:latest \
	            interleet-java:latest 2>/dev/null || true
	@echo "🧹 Cleaning workspaces..."
	-rm -rf /tmp/interleet_workspaces
	@echo "Done."
