# Multi-Spec WireMock Mapping Generator

Automatically generate WireMock mappings from multiple OpenAPI specifications with zero configuration. Drop your API specs into a directory and get comprehensive mock servers with realistic responses.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## Features

- **Zero Configuration**: Drop OpenAPI specs in `/spec` directory and run
- **Multi-API Support**: Process unlimited APIs simultaneously  
- **Comprehensive Coverage**: 8 HTTP status codes per endpoint (200, 201, 401, 403, 404, 500, 502, 503)
- **Docker Ready**: Full containerization with Docker Compose
- **Organized Output**: API-specific folders with consolidated mappings
- **Realistic Responses**: Spec-compliant JSON responses with examples

## Quick Start

```bash
# 1. Add your OpenAPI specs
cp your-api-spec.yaml spec/

# 2. Generate mappings
make generate

# 3. Start WireMock
make start

# Your APIs are now mocked at http://localhost:8080
```

## Project Structure

```
spec/                           # Your OpenAPI specifications
├── products-api.yaml           # API specs (auto-discovered)
├── users-api.yaml              # YAML and JSON supported
└── orders-api.json             # Unlimited APIs

wiremock/                       # Generated output
├── mappings/                   # Organized by API
│   ├── products/               # Consolidated by HTTP method
│   │   ├── get_products_mappings.json
│   │   ├── create_products_mappings.json
│   │   └── ...
│   └── users/
└── __files/                    # Response files
    ├── products/               # Realistic JSON responses
    └── users/
```

## Usage

### Available Commands

```bash
make generate    # Process all specs and generate mappings
make start       # Start WireMock server
make stop        # Stop WireMock server
make clean       # Remove generated files
make test        # Test endpoints
```

### Testing Endpoints

```bash
# Success scenarios
curl -X GET http://localhost:8080/products \
  -H "Accept: application/json" \
  -d '{"scenario": "happy_path"}'

# Error scenarios  
curl -X GET http://localhost:8080/products \
  -H "Accept: application/json" \
  -d '{"scenario": "server_error"}'  # Returns 500
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
