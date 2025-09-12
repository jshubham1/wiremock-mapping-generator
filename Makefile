# WireMock Mapping Generator
# Streamlined Makefile for mapping generation and web interface

.PHONY: help setup install generate generate-java web-dev start stop restart clean test status

# Default target
help:
	@echo "WireMock Mapping Generator"
	@echo "========================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup       - Install dependencies and setup project"
	@echo "  make install     - Install Python dependencies only"
	@echo ""
	@echo "Generation:"
	@echo "  make generate    - Generate WireMock mappings from examples/"
	@echo "  make generate-java - Generate mappings + Java integration code"
	@echo ""
	@echo "Web Interface:"
	@echo "  make web-dev     - Start Web UI in development mode"
	@echo ""
	@echo "WireMock Server:"
	@echo "  make start       - Start WireMock server with Docker"
	@echo "  make stop        - Stop all Docker services"
	@echo "  make restart     - Restart Docker services"
	@echo "  make status      - Show service status"
	@echo ""
	@echo "Utilities:"
	@echo "  make test        - Test generated endpoints"
	@echo "  make clean       - Clean generated files and containers"
	@echo "  make help        - Show this help message"

# Setup Commands
setup: install
	@echo "✅ Project setup complete!"
	@echo "Usage:"
	@echo "  ./wiremock-generator --help    # CLI tool"
	@echo "  ./wiremock-web                 # Web UI"
	@echo "  make start                     # WireMock server"

install:
	@echo "📦 Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Generation Commands
generate:
	@echo "🔧 Generating WireMock mappings..."
	./wiremock-generator --spec-dir ./examples --output-dir ./output --verbose
	@echo "✅ Mappings generated in ./output/"

generate-java:
	@echo "🔧 Generating WireMock mappings + Java code..."
	./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
	@echo "✅ Mappings + Java code generated in ./output/"

# Web Interface  
web-dev:
	@echo "🌐 Starting Web UI in development mode..."
	@echo "Visit: http://localhost:5001"
	./wiremock-web

# WireMock Server Management
start:
	@echo "🚀 Starting WireMock server..."
	docker-compose up -d wiremock
	@echo "WireMock available at: http://localhost:8080"
	@echo "Admin dashboard: http://localhost:8080/__admin"

stop:
	@echo "🛑 Stopping services..."
	docker-compose down

restart: stop start

status:
	@echo "📊 Service status:"
	docker-compose ps

# Testing
test:
	@echo "🧪 Testing generated endpoints..."
	@if [ ! -d "./output/mappings" ]; then \
		echo "❌ No mappings found. Run 'make generate' first"; \
		exit 1; \
	fi
	./test-scenarios.sh

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v --remove-orphans 2>/dev/null || true
	rm -rf ./output/mappings/* ./output/__files/* 2>/dev/null || true
	@echo "✅ Cleanup complete"
