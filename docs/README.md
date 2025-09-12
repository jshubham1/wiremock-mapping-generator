# Multi-Spec WireMock Mapping Generator

Automatically generate WireMock mappings from multiple OpenAPI specifications with zero configuration. Drop your API specs into a directory and get comprehensive mock servers with realistic responses.

**🌐 NEW: Web UI Available!** - Modern drag-and-drop interface at `make web-ui`

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## Features

- **🌐 Modern Web UI**: Drag-and-drop interface with real-time progress and ZIP downloads
- **Zero Configuration**: Drop OpenAPI specs in `/spec` directory and run
- **Multi-API Support**: Process unlimited APIs simultaneously  
- **Comprehensive Coverage**: 8 HTTP status codes per endpoint (200, 201, 401, 403, 404, 500, 502, 503)
- **Docker Ready**: Full containerization with Docker Compose
- **Organized Output**: API-specific folders with consolidated mappings
- **Realistic Responses**: Spec-compliant JSON responses with examples
- **Java Integration**: Optional Spring Boot & JUnit code generation

## Quick Start

### Option 1: Web UI (Recommended)
```bash
# Start the modern web interface
make web-ui

# Open http://localhost:5000 in your browser
# Drag & drop your OpenAPI files
# Generate and download mappings
```

### Option 2: Command Line
```bash
# 1. Add your OpenAPI specs
cp your-api-spec.yaml spec/

# 2. Generate mappings
make generate

# 3. Start WireMock
make start

# Your APIs are now mocked at http://localhost:8080

# Or run the complete workflow in one command:
make full-cycle
```

## Project Structure

```
spec/                           # Your OpenAPI specifications
├── products-api.yaml           # API specs (auto-discovered)
├── users-api.yaml              # YAML and JSON supported
└── orders-api.json             # Unlimited APIs

scripts/                        # Shell scripts and generators
├── test-scenarios.sh           # Dynamic test suite
├── quick-start.sh              # Quick setup script
└── multi_spec_wiremock_generator.py

generated/                      # All generated content
└── wiremock/                   # WireMock artifacts
    ├── mappings/               # Organized by API
    │   ├── products/           # Consolidated by HTTP method
    │   │   ├── get_products_mappings.json
    │   │   ├── create_products_mappings.json
    │   │   └── ...
    │   └── users/
    ├── __files/                # Response files
    │   ├── products/           # Realistic JSON responses
    │   └── users/
    └── java/                   # Generated Java code (optional)
        ├── src/main/java/      # Spring Boot configuration
        ├── src/test/java/      # JUnit test bases
        ├── pom.xml             # Maven build file
        └── build.gradle        # Gradle build file

web-app/                        # Modern Web UI
├── app.py                      # Flask application
├── templates/index.html        # Responsive web interface
├── Dockerfile                  # Container configuration
└── README.md                   # Web UI documentation
```

## Web UI Features

### 🎨 Modern Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Drag & Drop**: Simply drag OpenAPI files onto the interface
- **Real-time Progress**: Visual feedback during generation
- **Instant Downloads**: Get ZIP packages immediately

### 📁 File Management
- **Multi-format Support**: YAML (.yaml, .yml) and JSON files
- **Batch Upload**: Process multiple API specs simultaneously
- **File Validation**: Automatic type and size checking (max 16MB)
- **Smart Organization**: Generated files organized by API

### ⚙️ Generation Options
- **JSON Only**: WireMock mappings for immediate use
- **JSON + Java**: Include Spring Boot & JUnit integration
- **Custom Packages**: Specify Java package names
- **Download Packages**: Complete ZIP with documentation

### 🔧 Technical Features
- **Session Management**: Unique sessions for concurrent users
- **Auto Cleanup**: Temporary files cleaned automatically
- **Health Monitoring**: Built-in health checks
- **Error Handling**: Comprehensive error reporting
```
    └── users/
```

## Usage

### Web UI Interface

```bash
# Start the modern web interface
make web-ui

# Access at http://localhost:5000
# Features:
# - Drag & drop OpenAPI files
# - Choose JSON only or JSON + Java generation
# - Real-time progress tracking
# - Download ZIP packages
# - Mobile-responsive design
```

### Available Commands

```bash
make web-ui          # Start Web UI for drag & drop generation
make start-web       # Start complete stack with Web UI
make stop-web        # Stop Web UI services
make generate        # Generate mappings (CLI)
make start           # Start WireMock server
make stop            # Stop WireMock server
make clean           # Remove generated files (including Java code)
make test            # Test all generated endpoints dynamically
make full-cycle      # Complete workflow: clean→generate→start→validate→test
```

### Testing Endpoints

The project now includes dynamic testing that automatically discovers and tests all generated endpoints:

```bash
# Test all generated endpoints automatically
make test

# Or run the test script directly
./scripts/test-scenarios.sh
```

The test suite will:
- 🔍 **Auto-discover** all generated mapping files
- 🧪 **Test each scenario** with appropriate payloads  
- ✅ **Validate responses** against expected status codes
- 📊 **Provide summary** of passed/failed tests

**Requirements**: `jq` must be installed for JSON processing
```bash
# Install jq (macOS)
brew install jq

# Install jq (Ubuntu/Debian)
sudo apt-get install jq
```

### Manual Testing Examples

```bash
# Success scenarios
curl -X PUT http://localhost:8080/users/123 \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name": "happy_path", "email": "test@example.com"}'

# Error scenarios  
curl -X PUT http://localhost:8080/users/123 \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"name": "server_error", "email": "test@example.com"}'  # Returns 500
```

### Scenario Types

Each endpoint supports 8 scenarios triggered by JSON body content:

- `happy_path` → 200/201 Success
- `unauthorized_access` → 401 Unauthorized
- `forbidden_access` → 403 Forbidden  
- `not_found_error` → 404 Not Found
- `server_error` → 500 Internal Server Error
- `bad_gateway` → 502 Bad Gateway
- `service_unavailable` → 503 Service Unavailable

## Requirements

- Docker and Docker Compose
- OpenAPI 3.0+ specifications (YAML or JSON)

## Configuration

### Environment Variables

```bash
WIREMOCK_PORT=8080          # Server port (default: 8080)
SPEC_DIRECTORY=./spec       # Input directory  
OUTPUT_DIRECTORY=./wiremock # Output directory
```

### Docker Compose Override

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  wiremock-server:
    ports:
      - "9090:8080"  # Custom port
    environment:
      - WIREMOCK_VERBOSE=true
```

## Advanced Usage

### Direct Python Script

```bash
# Install dependencies
pip install pyyaml

# Run generator directly
python scripts/multi_spec_wiremock_generator.py spec wiremock
```

### CI/CD Integration

```yaml
# .github/workflows/api-mocks.yml
- name: Generate API Mocks
  run: |
    make generate
    make start
    make test
```

## Troubleshooting

### Common Issues

**No mappings generated**
```bash
# Check spec files exist and are valid
ls -la spec/
make validate
```

**WireMock won't start**
```bash
# Check Docker is running
docker ps

# Check logs for errors
make logs
```

**Endpoints return 404**
```bash
# Verify mappings are loaded
curl http://localhost:8080/__admin/mappings

# Check request format matches expected pattern
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [WireMock](http://wiremock.org/) - HTTP service virtualization
- [OpenAPI](https://swagger.io/specification/) - API specification standard
- [Docker](https://www.docker.com/) - Containerization platform
