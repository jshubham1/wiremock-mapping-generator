# Multi-Spec WireMock Mapping Generator

## Overview

The Multi-Spec WireMock Mapping Generator is an enhanced version of the OpenAPI to WireMock converter that supports processing multiple API specifications simultaneously and generates consolidated mapping files organized by API and HTTP method.

## Features

- **Multi-API Support**: Process multiple OpenAPI specifications from a single directory
- **Consolidated Mappings**: Group mappings by API name and HTTP method (GET, POST, PUT, DELETE, etc.)
- **Organized File Structure**: Creates clean folder hierarchy for easy navigation
- **Comprehensive Scenarios**: Generates mappings for all common HTTP status codes (200, 201, 401, 403, 404, 500, 502, 503)
- **Spec-Compliant Responses**: Uses actual examples from OpenAPI specifications
- **Smart Request Matching**: Advanced request matching with scenario-based routing

## Directory Structure

After generation, your WireMock directory will look like this:

```
wiremock/
├── mappings/
│   ├── products/
│   │   ├── get_products_mappings.json      # All GET operations for products
│   │   ├── create_products_mappings.json   # All POST operations for products
│   │   ├── update_products_mappings.json   # All PUT operations for products
│   │   └── delete_products_mappings.json   # All DELETE operations for products
│   ├── users/
│   │   ├── get_users_mappings.json         # All GET operations for users
│   │   ├── create_users_mappings.json      # All POST operations for users
│   │   ├── update_users_mappings.json      # All PUT operations for users
│   │   └── delete_users_mappings.json      # All DELETE operations for users
│   └── orders/
│       ├── get_orders_mappings.json
│       ├── create_orders_mappings.json
│       └── ...
└── __files/
    ├── products/
    │   ├── get_getProducts_200_response.json
    │   ├── post_createProduct_201_response.json
    │   ├── get_getProducts_401_error.json
    │   └── ...
    ├── users/
    │   ├── get_getUsers_200_response.json
    │   ├── post_createUser_201_response.json
    │   └── ...
    └── orders/
        └── ...
```

## Usage

### 1. Prepare API Specifications

Place all your OpenAPI specification files in the `spec/` directory:

```
spec/
├── products-api.yaml
├── users-api.yaml
├── orders-api.yaml
├── payments-api.json
└── notifications-api.yaml
```

Supported formats:
- YAML (.yaml, .yml)
- JSON (.json)

### 2. Generate Mappings

Run the multi-spec generator:

```bash
# Using Make (recommended)
make generate-multi-spec

# Or run directly with Python
python scripts/multi_spec_wiremock_generator.py spec wiremock
```

### 3. Start WireMock

```bash
make start
```

## API Naming Convention

The generator automatically extracts API names from:

1. **Filename**: `products-api.yaml` → `products`
2. **OpenAPI Title**: Uses `info.title` field if filename is generic
3. **Sanitization**: Converts spaces and special characters to underscores

Examples:
- `products-api.yaml` → `products`
- `user-management-api.yaml` → `user_management`
- `Payment Processing API.json` → `payment_processing_api`

## Mapping File Structure

Each consolidated mapping file contains multiple scenarios for the same HTTP method:

```json
{
  "mappings": [
    {
      "id": "unique-id-1",
      "request": {
        "method": "POST",
        "urlPathPattern": "/products",
        "bodyPatterns": [
          {
            "matchesJsonPath": "$[?(@..* =~ /.*happy_path.*/i)]"
          }
        ],
        "headers": {
          "Accept": {"contains": "json"}
        }
      },
      "response": {
        "status": 201,
        "bodyFileName": "products/post_createProduct_201_response.json",
        "headers": {"Content-Type": "application/json"}
      },
      "metadata": {
        "scenario": "created",
        "operation_id": "createProduct",
        "api_name": "products"
      }
    },
    {
      "id": "unique-id-2",
      "request": {
        "method": "POST",
        "urlPathPattern": "/products",
        "bodyPatterns": [
          {
            "matchesJsonPath": "$[?(@..* =~ /.*unauthorized_access.*/i)]"
          }
        ],
        "headers": {
          "Accept": {"contains": "json"}
        }
      },
      "response": {
        "status": 401,
        "bodyFileName": "products/post_createProduct_401_error.json",
        "headers": {"Content-Type": "application/json"}
      },
      "metadata": {
        "scenario": "unauthorized",
        "operation_id": "createProduct",
        "api_name": "products"
      }
    }
    // ... more scenarios
  ]
}
```

## Request Matching Strategies

The generator uses different matching strategies for different scenarios:

### POST/PUT/PATCH Requests
Uses JSON Path matching on request body:
- **Success scenarios**: Match fields containing scenario identifiers
- **Error scenarios**: Match specific error trigger fields

### GET/DELETE Requests
Uses header-based matching:
- **Error scenarios**: Uses `X-Test-Scenario` header
- **Success scenarios**: Default matching without special headers

## Scenario Identifiers

Each status code has a unique scenario identifier used in request matching:

| Status Code | Scenario ID | Description |
|-------------|-------------|-------------|
| 200 | `happy_path` | Success response |
| 201 | `created_success` | Resource created |
| 401 | `unauthorized_access` | Authentication required |
| 403 | `forbidden_access` | Access denied |
| 404 | `not_found_error` | Resource not found |
| 500 | `server_error` | Internal server error |
| 502 | `bad_gateway` | Bad gateway |
| 503 | `service_unavailable` | Service unavailable |

## Testing Different Scenarios

### Success Scenarios (200/201)
```bash
# For POST requests - include scenario identifier in request body
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product happy_path", "category": "electronics", "price": 99.99}'

curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product created_success", "category": "electronics", "price": 99.99}'
```

### Error Scenarios
```bash
# 401 Unauthorized
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product unauthorized_access", "category": "electronics", "price": 99.99}'

# 500 Server Error
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product server_error", "category": "electronics", "price": 99.99}'

# For GET requests - use headers
curl -X GET http://localhost:8080/products \
  -H "X-Test-Scenario: server_error"
```

## Response Types

### Success Responses
- Use actual examples from OpenAPI specifications
- Include realistic data structures and values
- Saved as separate JSON files for reusability

### Error Responses
- Standardized error format with:
  - Error code and message
  - Timestamp
  - Trace ID for debugging
- Consistent across all APIs

## Advanced Configuration

### Environment Variables (.env.enhanced)

The generator supports various configuration options:

```bash
# Status codes to generate
STATUS_CODES=200,201,401,403,404,500,502,503

# Response configuration
USE_SCHEMA_EXAMPLES=true
INCLUDE_HEADERS=true
PRETTY_PRINT_JSON=true

# Error response configuration
INCLUDE_TRACE_ID=true
INCLUDE_TIMESTAMP=true
```

## Benefits

### For Development Teams
1. **Organized Structure**: Easy to find and manage mappings by API and method
2. **Comprehensive Coverage**: All error scenarios covered out of the box
3. **Realistic Responses**: Uses actual OpenAPI examples
4. **Easy Testing**: Clear scenario identifiers for testing different paths

### For QA Teams
1. **Complete Test Coverage**: Test all error scenarios systematically
2. **Predictable Responses**: Consistent error response formats
3. **Easy Scenario Switching**: Simple request modifications to trigger different responses

### For Integration Testing
1. **Multi-API Support**: Test complex workflows across multiple services
2. **Realistic Data**: Actual examples from specifications
3. **Stable Endpoints**: Consistent mock behavior across test runs

## Migration from Single Spec Generator

If you're migrating from the single-spec generator:

1. **Backup existing mappings**: `cp -r wiremock/mappings wiremock/mappings.backup`
2. **Clean directory**: `make clean`
3. **Generate new mappings**: `make generate-multi-spec`
4. **Update test scripts**: Use new file structure and scenario identifiers

## Troubleshooting

### Common Issues

1. **No mappings generated**
   - Check if spec files are valid YAML/JSON
   - Ensure spec files contain `paths` section
   - Verify Python dependencies are installed

2. **Invalid JSON Path errors**
   - Check request body structure in tests
   - Ensure scenario identifiers are included in request data

3. **Wrong responses returned**
   - Verify request matches the expected pattern
   - Check WireMock logs: `make logs`
   - Use WireMock admin UI: `http://localhost:8080/__admin`

### Debug Mode

Enable verbose logging by setting environment variable:
```bash
export WIREMOCK_VERBOSE=true
make generate-multi-spec
```

## Examples

See the `examples/` directory for complete working examples of:
- Multi-API specifications
- Test scripts for all scenarios
- Integration test examples

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.
