# WireMock OpenAPI Mapping Generator
# Enhanced Makefile for comprehensive mapping generation

.PHONY: help build start stop restart clean generate logs status test test-scenarios

# Default target
help:
	@echo "WireMock Multi-Spec Mapping Generator"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make start               - Start WireMock with generated mappings"
	@echo "  make stop                - Stop all services"
	@echo "  make restart             - Restart all services"
	@echo "  make generate            - Generate consolidated mappings for multiple APIs"
	@echo "  make logs                - Show service logs"
	@echo "  make status              - Show service status"
	@echo "  make clean               - Clean generated files and containers"
	@echo "  make test                - Test the generated endpoints"
	@echo "  make test-scenarios      - Test all error scenarios across APIs"
	@echo "  make show-mappings       - List generated mapping files"
	@echo "  make validate-spec       - Validate OpenAPI specifications"
	@echo "  make help                - Show this help message"

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
	@echo "This will process all specs in ./spec/ and create organized mappings by API and HTTP method"
	docker-compose run --rm wiremock-generator sh -c "python3 /scripts/multi_spec_wiremock_generator.py /spec /output"
	@echo "Multi-spec mappings generated successfully!"
	@echo "Check ./wiremock/mappings/{api_name}/ for consolidated mapping files"
	@echo "Check ./wiremock/__files/{api_name}/ for response files"

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
	rm -rf ./wiremock/mappings/*
	rm -rf ./wiremock/__files/*
	@echo "Cleanup completed!"

# Test the generated endpoints with different scenarios
test:
	@echo "Testing generated WireMock endpoints..."
	@echo ""
	@echo "Testing POST /credit-transfer-order-requests (Success scenario)"
	@curl -s -w "\nStatus: %{http_code}\n" -X POST http://localhost:8080/credit-transfer-order-requests \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer valid-token" \
		-d '{"amount": 100}' || echo "Service not running"
	@echo ""
	@echo "WireMock Admin Interface:"
	@echo "http://localhost:8080/__admin"

# Test all error scenarios across multiple APIs
test-scenarios:
	@echo "Testing all scenarios across multiple APIs..."
	@echo ""
	@echo "Running comprehensive multi-API test suite..."
	./test-multi-spec.sh
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
	@ls -la ./wiremock/mappings/ 2>/dev/null || echo "No mappings found. Run 'make generate' first."
	@echo ""
	@echo "Generated response files:"
	@ls -la ./wiremock/__files/ 2>/dev/null || echo "No response files found. Run 'make generate' first."

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
