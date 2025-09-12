# WireMock OpenAPI Mapping Generator
# Enhanced Makefile for comprehensive mapping generation with Web UI

.PHONY: help build start stop restart clean generate generate-java logs status test test-scenarios full-cycle wait-for-wiremock web-ui start-web stop-web setup install dev-setup

# Default target
help:
	@echo "WireMock Multi-Spec Mapping Generator"
	@echo "===================================="
	@echo ""
	@echo "Setup commands:"
	@echo "  make setup               - Install dependencies and setup project"
	@echo "  make install             - Install Python dependencies"
	@echo "  make dev-setup           - Setup development environment"
	@echo ""
	@echo "CLI commands:"
	@echo "  make generate            - Generate consolidated mappings for multiple APIs"
	@echo "  make generate-java       - Generate mappings + Java Spring Boot code"
	@echo ""
	@echo "Web UI commands:"
	@echo "  make web-ui              - Start Web UI for drag & drop mapping generation"
	@echo "  make web-dev             - Start Web UI in development mode (local Python)"
	@echo "  make demo                - Interactive demo of the Web UI features"
	@echo "  make start-web           - Start complete stack with Web UI"
	@echo "  make stop-web            - Stop Web UI services"
	@echo ""
	@echo "WireMock service commands:"
	@echo "  make start               - Start WireMock with generated mappings"
	@echo "  make stop                - Stop all services"
	@echo "  make restart             - Restart all services"
	@echo "  make logs                - Show service logs"
	@echo "  make status              - Show service status"
	@echo ""
	@echo "Testing commands:"
	@echo "  make test                - Test all generated endpoints dynamically"
	@echo "  make test-scenarios      - Test all error scenarios across APIs"
	@echo "  make full-cycle          - Complete workflow: clean→generate+Java→start→wait→test"
	@echo ""
	@echo "Utility commands:"
	@echo "  make clean               - Clean generated files and containers"
	@echo "  make show-mappings       - List generated mapping files"
	@echo "  make validate-spec       - Validate OpenAPI specifications"
	@echo "  make help                - Show this help message"

# Setup Commands
setup: install
	@echo "✅ Project setup complete!"
	@echo "You can now use:"
	@echo "  ./wiremock-generator --help  (CLI)"
	@echo "  ./wiremock-web              (Web UI)"
	@echo "  make web-ui                 (Docker Web UI)"

install:
	@echo "📦 Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

dev-setup: install
	@echo "🔧 Setting up development environment..."
	@if [ ! -d "venv" ]; then \
		python3 -m venv venv; \
		echo "📁 Virtual environment created"; \
	fi
	@echo "🔧 To activate virtual environment run: source venv/bin/activate"
	@echo "✅ Development environment ready!"

# Web UI Commands
web-ui:
	@echo "🌐 Starting WireMock Mapping Generator Web UI..."
	@echo "This will start a modern web interface for generating mappings"
	@echo ""
	./src/cli/start-web-ui.sh

web-dev:
	@echo "🌐 Starting WireMock Mapping Generator Web UI (Development Mode)..."
	@echo "This will start the web interface using local Python environment"
	@echo ""
	./wiremock-web

demo:
	@echo "🎬 Starting Interactive Web UI Demo..."
	@echo "This will showcase all the features of the modern web interface"
	@echo ""
	./src/cli/demo-web-ui.sh

start-web:
	@echo "🚀 Starting complete stack with Web UI..."
	docker-compose up --build -d
	@echo ""
	@echo "🌐 Web UI: http://localhost:5000"
	@echo "⚙️  WireMock Admin: http://localhost:8080/__admin"

stop-web:
	@echo "🛑 Stopping Web UI services..."
	docker-compose down

# Start all services (generate mappings and start WireMock)
start:
	@echo "Starting WireMock with OpenAPI-generated mappings..."
	docker-compose up -d
	@echo "Services started! WireMock is available at http://localhost:8080"
	@echo "Admin UI: http://localhost:8080/__admin"

# Stop all services
stop:
	@echo "Stopping all services..."
	docker-compose down

# Restart all services
restart: stop start

# Generate consolidated mappings for multiple API specs
generate:
	@echo "Generating consolidated WireMock mappings for multiple API specifications..."
	@echo "This will process all specs in ./examples/ and create organized mappings by API and HTTP method"
	./wiremock-generator --spec-dir ./examples --output-dir ./output --verbose
	@echo "Multi-spec mappings generated successfully!"
	@echo "Check ./output/mappings/ for consolidated mapping files"
	@echo "Check ./output/__files/ for response files"

# Generate mappings + Java code for Spring Boot integration
generate-java:
	@echo "Generating WireMock mappings + Java Spring Boot integration code..."
	@echo "This will process all specs in ./examples/ and create:"
	@echo "  - Organized JSON mappings by API and HTTP method"
	@echo "  - Spring Boot configuration classes"
	@echo "  - JUnit test base classes"
	@echo "  - Maven/Gradle build files"
	./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
	@echo "✅ Multi-spec mappings + Java code generated successfully!"
	@echo "📁 JSON mappings: ./output/mappings/"
	@echo "📁 Response files: ./output/__files/"
	@echo "🔥 Java code: ./output/java/"
	@echo "📖 Java usage guide: ./output/java/README.md"

# Show logs
logs:
	docker-compose logs -f

# Show service status
status:
	docker-compose ps

# Clean generated files and containers
clean:
	@echo "Cleaning up..."
	docker-compose down -v --remove-orphans
	docker-compose rm -f
	rm -rf ./generated/wiremock/mappings/*
	rm -rf ./generated/wiremock/__files/*
	rm -rf ./generated/wiremock/java/src/main/java/com/
	rm -rf ./generated/wiremock/java/src/test/java/com/
	@echo "Cleanup completed!"

# Test the generated endpoints with different scenarios
test:
	@echo "Testing generated WireMock endpoints..."
	@echo ""
	@if [ ! -d "./generated/wiremock/mappings" ] || [ -z "$$(find ./generated/wiremock/mappings -name '*.json' -type f)" ]; then \
		echo "No mappings found. Please run 'make generate' first."; \
		exit 1; \
	fi
	@./scripts/test-scenarios.sh
	@echo ""
	@echo "WireMock Admin Interface:"
	@echo "http://localhost:8080/__admin"

# Test all error scenarios across multiple APIs
test-scenarios:
	@echo "Testing all scenarios across multiple APIs..."
	@echo ""
	@echo "Running comprehensive multi-API test suite..."
	./scripts/test-scenarios.sh
	@echo ""
	@echo "WireMock Admin Interface:"
	@echo "http://localhost:8080/__admin"

# Build custom image (if needed)
build:
	@echo "Building custom images..."
	docker-compose build

# Show generated mappings
show-mappings:
	@echo "Generated WireMock mappings:"
	@ls -la ./generated/wiremock/mappings/ 2>/dev/null || echo "No mappings found. Run 'make generate' first."
	@echo ""
	@echo "Generated response files:"
	@ls -la ./generated/wiremock/__files/ 2>/dev/null || echo "No response files found. Run 'make generate' first."

# Validate OpenAPI specifications (all specs in directory)
validate-spec:
	@echo "Validating all OpenAPI specifications..."
	@for spec in ./spec/*.yaml ./spec/*.yml ./spec/*.json; do \
		if [ -f "$$spec" ]; then \
			echo "Validating $$spec..."; \
			docker run --rm -v $(PWD)/spec:/spec openapitools/openapi-generator-cli:v7.1.0 \
				validate -i "/spec/$$(basename $$spec)" || echo "Validation failed for $$spec"; \
		fi; \
	done

# Complete workflow: clean, generate with Java code, start, wait for startup, validate and test
full-cycle: clean validate-spec generate-java start wait-for-wiremock test
	@echo ""
	@echo -e "\033[0;32m🎉 Full cycle completed successfully!\033[0m"
	@echo "✅ Cleaned old artifacts"
	@echo "✅ Validated OpenAPI specifications" 
	@echo "✅ Generated new mappings + Java code"
	@echo "✅ Started WireMock server"
	@echo "✅ Waited for WireMock to be ready"
	@echo "✅ Tested all endpoints"
	@echo ""
	@echo "🔗 WireMock server: http://localhost:8080"
	@echo "⚙️  Admin interface: http://localhost:8080/__admin"

# Wait for WireMock to be ready
wait-for-wiremock:
	@echo "⏳ Waiting for WireMock to start..."
	@for i in $$(seq 1 30); do \
		if curl -s -f http://localhost:8080/__admin/mappings >/dev/null 2>&1; then \
			echo "✅ WireMock is ready!"; \
			sleep 2; \
			break; \
		fi; \
		echo "   Attempt $$i/30: WireMock not ready yet, waiting 2 seconds..."; \
		sleep 2; \
		if [ $$i -eq 30 ]; then \
			echo "❌ WireMock failed to start within 60 seconds"; \
			exit 1; \
		fi; \
	done
