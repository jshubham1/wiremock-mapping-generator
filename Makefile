# WireMock Mapping Generator
# Comprehensive Makefile for full application stack management

.PHONY: help setup install dev start stop restart status logs clean test health check-deps

# Default target
help:
	@echo "🚀 WireMock Mapping Generator"
	@echo "============================="
	@echo ""
	@echo "📦 Setup:"
	@echo "  make setup       - Complete project setup (dependencies + Docker)"
	@echo "  make install     - Install Python dependencies only"
	@echo "  make check-deps  - Check system dependencies"
	@echo ""
	@echo "🚀 Application Management:"
	@echo "  make dev         - Start full development environment (Web UI + WireMock)"
	@echo "  make dev-hybrid  - Start WireMock in Docker + Web UI locally (recommended)"
	@echo "  make start       - Start all services in background"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make status      - Show service status"
	@echo "  make logs        - Show live logs from all services"
	@echo ""
	@echo "🔧 Individual Services:"
	@echo "  make web-local   - Start Web UI locally (no SSL issues, faster)"
	@echo "  make web         - Start Web UI in Docker"
	@echo "  make wiremock    - Start only WireMock server"
	@echo ""
	@echo "📋 Generation (Legacy CLI):"
	@echo "  make generate    - Generate mappings from examples/ (CLI mode)"
	@echo "  make generate-java - Generate mappings + Java code (CLI mode)"
	@echo ""
	@echo "🧪 Testing & Health:"
	@echo "  make test        - Test generated endpoints"
	@echo "  make health      - Check health of all services"
	@echo ""
	@echo "🧹 Utilities:"
	@echo "  make clean       - Clean generated files and containers"
	@echo "  make help        - Show this help message"
	@echo ""
	@echo "🌐 URLs:"
	@echo "  Web UI:          http://localhost:5001"
	@echo "  WireMock API:    http://localhost:8080"
	@echo "  WireMock Admin:  http://localhost:8080/__admin"

# Setup Commands
setup: check-deps install
	@echo "🐳 Setting up Docker environment..."
	@docker-compose pull
	@echo "✅ Project setup complete!"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make dev    # Start development environment"
	@echo "  make logs   # Watch logs"

check-deps:
	@echo "🔍 Checking dependencies..."
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Please install Docker."; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
	@echo "✅ All dependencies found!"

install:
	@echo "📦 Installing Python dependencies..."
	@pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Application Management Commands
dev:
	@echo "🚀 Starting development environment..."
	@echo "This will start:"
	@echo "  - Web UI on http://localhost:5001"
	@echo "  - WireMock server on http://localhost:8080"
	@echo ""
	@docker-compose up --build
	@echo ""
	@echo "✅ Development environment started!"

dev-hybrid:
	@echo "🚀 Starting hybrid development environment..."
	@echo "This will start:"
	@echo "  - WireMock server in Docker on http://localhost:8080"
	@echo "  - Web UI locally on http://localhost:5001"
	@echo ""
	@echo "🔧 Starting WireMock server in background..."
	@docker-compose up -d wiremock
	@echo "⏳ Waiting for WireMock to be ready..."
	@sleep 5
	@echo "🌐 Starting Web UI locally..."
	@echo "Visit: http://localhost:5001"
	@echo ""
	python3 wiremock-web

start:
	@echo "🚀 Starting all services in background..."
	@docker-compose up -d --build
	@echo ""
	@echo "✅ Services started!"
	@echo "  Web UI:         http://localhost:5001"
	@echo "  WireMock API:   http://localhost:8080"
	@echo "  WireMock Admin: http://localhost:8080/__admin"
	@echo ""
	@echo "💡 Use 'make logs' to watch logs or 'make status' to check health"

stop:
	@echo "🛑 Stopping all services..."
	@docker-compose down
	@echo "✅ All services stopped!"

restart: stop start

status:
	@echo "📊 Service Status:"
	@echo "=================="
	@docker-compose ps
	@echo ""
	@echo "🏥 Health Status:"
	@echo "=================="
	@make health --no-print-directory

logs:
	@echo "📋 Live logs from all services (Ctrl+C to exit):"
	@echo "================================================"
	@docker-compose logs -f

# Individual Service Commands
web-local:
	@echo "🌐 Starting Web UI locally (better performance, no Docker SSL issues)..."
	@echo "Note: Make sure WireMock is running with 'make wiremock' first"
	python3 wiremock-web

web:
	@echo "🌐 Starting Web UI in Docker..."
	@docker-compose up wiremock-web-ui

wiremock:
	@echo "🔧 Starting WireMock server only..."
	@docker-compose up wiremock

# Legacy CLI Generation Commands (for backward compatibility)
generate:
	@echo "🔧 Generating WireMock mappings (CLI mode)..."
	@mkdir -p ./output/mappings ./output/__files
	./wiremock-generator --spec-dir ./examples --output-dir ./output --verbose
	@echo "✅ Mappings generated in ./output/"

generate-java:
	@echo "🔧 Generating WireMock mappings + Java code (CLI mode)..."
	@mkdir -p ./output/mappings ./output/__files
	./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
	@echo "✅ Mappings + Java code generated in ./output/"

# Health Check Commands
health:
	@echo "� Checking service health..."
	@echo ""
	@echo "Web UI (http://localhost:5001):"
	@curl -s -f http://localhost:5001/health >/dev/null 2>&1 && echo "  ✅ Healthy" || echo "  ❌ Unhealthy or not running"
	@echo ""
	@echo "WireMock (http://localhost:8080):"
	@curl -s -f http://localhost:8080/__admin/health >/dev/null 2>&1 && echo "  ✅ Healthy" || echo "  ❌ Unhealthy or not running"
	@echo ""

# Testing Commands
test:
	@echo "🧪 Testing WireMock endpoints..."
	@if [ ! -d "./output/mappings" ] || [ -z "$$(ls -A ./output/mappings)" ]; then \
		echo "❌ No mappings found. Please:"; \
		echo "  1. Start the app: make dev"; \
		echo "  2. Upload API specs via Web UI: http://localhost:5001"; \
		echo "  3. Or generate via CLI: make generate"; \
		exit 1; \
	fi
	@echo "📡 Testing WireMock health endpoint..."
	@curl -s http://localhost:8080/__admin/health | jq . 2>/dev/null || curl -s http://localhost:8080/__admin/health
	@echo ""
	@echo "📋 Available mappings:"
	@curl -s http://localhost:8080/__admin/mappings | jq '.mappings | length' 2>/dev/null || echo "Could not fetch mappings count"

# Cleanup Commands  
clean:
	@echo "🧹 Cleaning up..."
	@echo "Stopping and removing containers..."
	@docker-compose down -v --remove-orphans 2>/dev/null || true
	@echo "Cleaning generated files..."
	@rm -rf ./output/mappings/* ./output/__files/* 2>/dev/null || true
	@echo "Removing unused Docker images..."
	@docker image prune -f >/dev/null 2>&1 || true
	@echo "✅ Cleanup complete!"
	@echo ""
	@echo "💡 Run 'make setup' to reinstall if needed"
