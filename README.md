# Multi-Spec WireMock Mapping Generator

**🎯 Goal: Drop any OpenAPI spec (YAML/JSON) file into `/spec` directory → Automatic WireMock mapping and stub generation!**

This project automatically discovers and processes ALL OpenAPI specifications in the `/spec` directory, generating comprehensive WireMock stubs and mappings with zero configuration. Simply place your API specs in the folder and run the generator - everything else is handled automatically.

## ✨ Key Features

- ✅ **Zero Configuration Required**: Drop any OpenAPI spec file (YAML/JSON) into `/spec` → automatic discovery and processing
- ✅ **Multi-API Specification Support**: Unlimited OpenAPI specs processed simultaneously from the `/spec` directory
- ✅ **Automatic API Discovery**: Scans `/spec` folder and generates mappings for ALL found specifications
- ✅ **Universal Format Support**: Works with both JSON and YAML OpenAPI specifications
- ✅ **Consolidated Mapping Files**: Groups all scenarios for the same HTTP method into single files
- ✅ **Organized File Structure**: Clean folder hierarchy by API name and method for easy navigation
- ✅ **Spec-Compliant Response Generation**: Uses actual examples and schemas from OpenAPI specifications
- ✅ **Comprehensive Scenario Generation**: Creates mappings for all HTTP status codes (200, 201, 401, 403, 404, 500, 502, 503)
- ✅ **Enhanced Request Matching**: Smart scenario-based routing with JSON Path and header matching
- ✅ **Realistic Response Bodies**: Generates actual response structures matching your API specifications
- ✅ **Professional Error Responses**: Uses industry-standard error format with traceId, timestamps, and detailed messages
- ✅ **Intelligent API Discovery**: Automatically detects and processes all API specs in the spec directory
- ✅ **Docker-based**: Easy deployment with Docker Compose
- ✅ **Configurable**: Environment-based configuration
- ✅ **Exportable**: Portable setup that can be shared across teams
- ✅ **Multiple Formats**: Supports both JSON and YAML OpenAPI specs

## Project Structure

```
wiremock-mapping-generator/
├── spec/                           # 🎯 DROP YOUR API SPECS HERE
│   ├── any-api-spec-1.yaml         # ← Any OpenAPI spec file (auto-discovered)
│   ├── any-api-spec-2.yaml         # ← Another API spec (auto-discovered)
│   ├── products-api.yaml           # ← Example: Products API 
│   ├── users-api.yaml              # ← Example: Users API
│   ├── orders-api.json             # ← JSON format also supported
│   └── payments-api.yaml           # ← Add unlimited APIs - all auto-processed
├── wiremock/                       # 🚀 AUTO-GENERATED MAPPINGS & STUBS
│   ├── mappings/                   # ← Organized by API name (auto-created)
│   │   ├── any_api_spec_1/         # ← Folder created from filename
│   │   │   ├── get_any_api_spec_1_mappings.json     # All GET operations
│   │   │   ├── create_any_api_spec_1_mappings.json  # All POST operations  
│   │   │   ├── update_any_api_spec_1_mappings.json  # All PUT operations
│   │   │   └── delete_any_api_spec_1_mappings.json  # All DELETE operations
│   │   ├── products/               # ← From products-api.yaml
│   │   ├── users/                  # ← From users-api.yaml  
│   │   ├── orders/                 # ← From orders-api.json
│   │   └── payments/               # ← From payments-api.yaml
│   └── __files/                    # ← Response files (auto-generated)
│       ├── any_api_spec_1/         # ← Realistic response data
│       ├── products/               # ← Spec-compliant responses
│       ├── users/                  # ← Enhanced error responses
│       └── ...                     # ← All APIs get response files
├── scripts/
│   └── multi_spec_wiremock_generator.py # Consolidated multi-spec generator with enhanced logic
├── docker-compose.yml              # Docker Compose configuration
├── .env                            # Environment variables
├── .env.enhanced                   # Enhanced configuration
├── Makefile                        # Easy-to-use commands
├── test-multi-spec.sh              # Multi-API test script
├── MULTI_SPEC_GUIDE.md             # Comprehensive multi-spec documentation
└── README.md                       # This file
```

## Quick Start - Zero Configuration Setup

### Prerequisites

- Docker and Docker Compose installed
- OpenAPI specification files (JSON or YAML format)

### 🎯 The Goal: Drop & Generate

**Step 1:** Place ANY OpenAPI spec files in the `/spec` directory
```bash
# Copy your API specifications to the spec directory
cp your-api-spec.yaml spec/
cp another-api.json spec/
cp third-api.yaml spec/
# Add as many as you want - all will be auto-discovered!
```

**Step 2:** Generate mappings for ALL specs automatically
```bash
# One command processes ALL API specs in /spec directory
make generate
```

**Step 3:** Start WireMock with all generated mappings
```bash
# Start WireMock with ALL generated mappings loaded
make start
```

### 🚀 That's it! No configuration needed!

```bash
# Generate consolidated mappings for all API specs in spec/ directory
make generate

# Start WireMock with generated mappings
make start
```

This will:
- Process all OpenAPI specs in the `spec/` directory
- Create organized mappings by API name and HTTP method
- Generate consolidated mapping files (e.g., `get_products_mappings.json`, `create_users_mappings.json`)
- Use actual examples from OpenAPI specifications

```bash
# Generate comprehensive mappings with all scenarios and start WireMock
make clean && make generate-enhanced && make start

# Or using Docker Compose directly (basic mappings)
docker-compose up -d
```

### 3. Access WireMock

- **WireMock Server**: http://localhost:8080
- **Admin Interface**: http://localhost:8080/__admin
- **Health Check**: http://localhost:8080/__admin/health
- **Mappings Documentation**: `./wiremock/mappings/MAPPINGS_DOCUMENTATION.md`

### 4. Test Different Scenarios

#### Comprehensive Multi-API Testing

```bash
# Test all APIs and scenarios with comprehensive test suite
./test-multi-spec.sh

# Or test specific APIs:
./test-multi-spec.sh --products    # Test only Products API
./test-multi-spec.sh --users       # Test only Users API
./test-multi-spec.sh --credit      # Test only Credit Transfer API
```

#### Manual API Testing

```bash
# Test using make command
make test-scenarios

# Or test individual scenarios manually:

# Success scenario (201 Created)
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": 100}'

# Unauthorized scenario (401)
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'

# Forbidden scenario (403)
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-token" \
  -d '{"amount": 100}'
```

#### Multi-Spec Scenario Testing Examples

```bash
# Products API - Success scenarios
curl -X GET http://localhost:8080/products
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product created_success", "category": "electronics", "price": 99.99}'

# Products API - Error scenarios  
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product unauthorized_access", "category": "electronics", "price": 99.99}'

# Users API - Success scenarios
curl -X GET http://localhost:8080/users
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser_created_success", "email": "user@example.com", "password": "pass123", "role": "user"}'

# Users API - Error scenarios
curl -X GET http://localhost:8080/users -H "X-Test-Scenario: forbidden_access"
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser_server_error", "email": "error@example.com", "password": "pass123", "role": "user"}'
```

# Server error scenario (500)
curl -X POST "http://localhost:8080/credit-transfer-order-requests?simulate=server_error" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": 100}'

# Service unavailable scenario (503)
curl -X POST "http://localhost:8080/credit-transfer-order-requests?simulate=service_unavailable" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": 100}'
```

## Available Commands

Use the Makefile for easy project management:

```bash
make help                    # Show available commands
make start                   # Start WireMock with generated mappings
make stop                    # Stop all services
make restart                 # Restart all services
make generate                # Generate consolidated mappings for multiple APIs
make logs                    # Show service logs
make status                  # Show service status
make clean                   # Clean generated files and containers
make test                    # Test the generated endpoints
make test-scenarios          # Test all error scenarios across APIs
make show-mappings           # List generated mapping files
make validate-spec           # Validate all OpenAPI specifications
```

## Multi-API Specification Support

### Overview

The multi-spec generator processes multiple OpenAPI specifications and creates organized, consolidated mapping files. This is ideal for:

- **Microservices Architecture**: Mock multiple services from a single WireMock instance
- **Integration Testing**: Test complex workflows across multiple APIs
- **Team Collaboration**: Organized structure for different API teams
- **Consolidated Testing**: Single test suite for all your APIs

### Key Features

1. **Automatic API Discovery**: Scans `spec/` directory for all `.yaml`, `.yml`, and `.json` files
2. **Intelligent Naming**: Extracts API names from filenames or OpenAPI titles
3. **Consolidated Mappings**: Groups all scenarios for the same HTTP method into single files
4. **Organized Structure**: Creates clean folder hierarchy by API name

### File Organization

```
# Before (individual mappings)
wiremock/mappings/
├── mapping_001_get_products_200.json
├── mapping_002_get_products_401.json
├── mapping_003_post_products_201.json
└── ... (100+ individual files)

# After (consolidated mappings)
wiremock/mappings/
├── products/
│   ├── get_products_mappings.json      # All GET scenarios in one file
│   ├── create_products_mappings.json   # All POST scenarios in one file
│   └── update_products_mappings.json   # All PUT scenarios in one file
├── users/
│   ├── get_users_mappings.json
│   ├── create_users_mappings.json
│   └── update_users_mappings.json
└── orders/
    └── ...
```

### Scenario Identifiers

Each status code uses specific identifiers for request matching:

| Status Code | Scenario ID | Trigger Method |
|-------------|-------------|----------------|
| 200 | `happy_path` | Include in request body/field |
| 201 | `created_success` | Include in request body/field |
| 401 | `unauthorized_access` | Include in request body or use header |
| 403 | `forbidden_access` | Include in request body or use header |
| 404 | `not_found_error` | Include in request body or use header |
| 500 | `server_error` | Include in request body or use header |
| 502 | `bad_gateway` | Include in request body or use header |
| 503 | `service_unavailable` | Include in request body or use header |

For detailed multi-spec documentation, see [MULTI_SPEC_GUIDE.md](MULTI_SPEC_GUIDE.md).

## Enhanced Mapping Generation

The enhanced generator creates comprehensive mappings for each OpenAPI operation with multiple scenarios:

### Generated Status Codes

For each endpoint operation, the following status codes are generated:

- **200 (Success)**: Default success response
- **201 (Created)**: Resource creation success  
- **401 (Unauthorized)**: Missing or invalid authentication
- **403 (Forbidden)**: Valid authentication but insufficient permissions
- **404 (Not Found)**: Resource not found
- **500 (Internal Server Error)**: Server-side error
- **502 (Bad Gateway)**: Upstream server error
- **503 (Service Unavailable)**: Service temporarily unavailable

### Request Matching Logic

The enhanced generator uses intelligent request matching:

- **Success scenarios**: Match requests with proper authentication
- **Unauthorized (401)**: Triggered when `Authorization` header is missing
- **Forbidden (403)**: Triggered when `Authorization` header contains "invalid"
- **Server errors (500/502/503)**: Triggered by query parameter `?simulate={error_type}`

### Response Structure

**Success responses** use the actual OpenAPI specification structure:

```json
{
  "creditTransferOrderRequestId": "EPT000000000RF60",
  "signObjectId": "54803246cdf641c78f601a638064dba6",
  "transactionType": "SCT",
  "messages": {
    "messages": [
      {
        "messageKey": "PAI_CHARACTERS_FLIPPED_001",
        "messageType": "INFO",
        "messageText": "Unable to retrieve the available balance"
      }
    ]
  },
  "extraVerificationAction": "NOT_REQUIRED"
}
```

**Error responses** follow the ABN AMRO API specification format:

```json
{
  "errors": [
    {
      "code": "SUBJECT_UNAUTHENTICATED",
      "message": "Subject Token is invalid. Create a new token.",
      "traceId": "f1b554d8-406a-4301-b549-d539a5e885ae",
      "status": 401
    }
  ]
}
```

### Priority System

- **Success mappings** (200, 201): Priority 1 (highest)
- **Error mappings** (4xx, 5xx): Priority 5 (lower)

This ensures that valid requests are handled by success scenarios unless specific error conditions are met.

## Configuration

### Environment Variables

Edit the `.env` file to customize the setup:

```bash
# WireMock Configuration
WIREMOCK_PORT=8080                              # Port for WireMock server
WIREMOCK_OPTIONS=--global-response-templating   # Additional WireMock options

# OpenAPI Spec Configuration
OPENAPI_SPEC_FILE=open-api-spec.yaml            # Name of your OpenAPI spec file

# Output Configuration
MAPPINGS_DIR=./wiremock/mappings                 # Directory for mapping files
FILES_DIR=./wiremock/__files                     # Directory for response files

# Generator Configuration
GENERATE_RESPONSES=true                          # Generate response bodies
RESPONSE_TEMPLATING=true                         # Enable response templating
DEFAULT_RESPONSE_STATUS=200                      # Default response status
```

### Custom OpenAPI Spec

To use a different OpenAPI specification:

1. Place your spec file in the `spec/` directory
2. Update the `OPENAPI_SPEC_FILE` in `.env`
3. Restart the services: `make restart`

## How It Works

1. **OpenAPI Parsing**: The Python script (`openapi_to_wiremock.py`) parses your OpenAPI specification
2. **Mapping Generation**: For each endpoint, it creates a corresponding WireMock mapping with:
   - HTTP method and URL path matching
   - Response status codes
   - Response headers
   - Response bodies (from examples or generated from schemas)
3. **File Organization**: Mappings are saved as JSON files in `wiremock/mappings/`, response bodies in `wiremock/__files/`
4. **WireMock Startup**: WireMock loads the generated mappings and serves mock responses

## Generated Mappings

Each OpenAPI operation generates a WireMock mapping with:

- **Request Matching**: HTTP method and URL path
- **Response**: Status code, headers, and body
- **Unique ID**: Based on operationId or generated from method/path
- **Response Files**: Large response bodies are stored as separate files

Example generated mapping:
```json
{
  "id": "listVersionsv2",
  "name": "List API versions",
  "request": {
    "method": "GET",
    "urlPath": "/"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "bodyFileName": "listVersionsv2_response.json"
  }
}
```

## Customization

### Adding Custom Mappings

You can add custom WireMock mappings by:

1. Creating JSON files in `wiremock/mappings/`
2. Following the [WireMock mapping format](http://wiremock.org/docs/stubbing/)
3. Restarting WireMock: `make restart`

### Modifying Response Bodies

Response files in `wiremock/__files/` can be edited directly. Changes take effect immediately without restarting WireMock.

### Advanced WireMock Configuration

Modify the `docker-compose.yml` file to add WireMock command-line options:

```yaml
command: >
  --port 8080
  --root-dir /home/wiremock
  --global-response-templating
  --verbose
  --enable-browser-proxying
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change `WIREMOCK_PORT` in `.env`
2. **OpenAPI spec not found**: Ensure the file is in `spec/` directory
3. **Invalid OpenAPI spec**: Use `make validate-spec` to check your specification
4. **No mappings generated**: Check logs with `make logs`

### Debugging

```bash
# Check service status
make status

# View logs
make logs

# Restart services
make restart

# Clean and restart
make clean && make start
```

### Logs

View detailed logs for troubleshooting:

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f wiremock
docker-compose logs -f wiremock-generator
```

## Export and Sharing

This project is designed to be portable and shareable:

1. **Version Control**: Add everything except generated files to your repository
2. **Git Ignore**: The `.gitignore` excludes generated mappings and response files
3. **Team Sharing**: Share the entire directory structure
4. **CI/CD**: Use `make generate && make start` in your automation pipelines

### Recommended .gitignore

```gitignore
# Generated WireMock files
wiremock/mappings/*
wiremock/__files/*

# Keep directory structure
!wiremock/mappings/.gitkeep
!wiremock/__files/.gitkeep

# Docker
.env.local
docker-compose.override.yml

# Logs
*.log
```

## Advanced Usage

### Response Templating

WireMock supports response templating for dynamic responses. Enable it by adding `--global-response-templating` to WireMock options (already enabled by default).

### Request Matching

Customize request matching by editing generated mappings in `wiremock/mappings/`:

```json
{
  "request": {
    "method": "GET",
    "urlPathPattern": "/api/users/.*",
    "queryParameters": {
      "active": {
        "equalTo": "true"
      }
    }
  }
}
```

### HTTPS Support

To enable HTTPS:

1. Add certificates to a `certs/` directory
2. Mount the directory in docker-compose.yml
3. Add HTTPS options to WireMock command

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your OpenAPI specifications
5. Submit a pull request

## License

This project is open source. Modify and distribute as needed for your organization.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review WireMock documentation: http://wiremock.org/docs/
3. Validate your OpenAPI spec: https://editor.swagger.io/
4. Check Docker logs: `make logs`
