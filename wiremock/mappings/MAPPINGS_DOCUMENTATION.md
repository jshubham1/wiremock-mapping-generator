# Generated WireMock Mappings Documentation

This document describes the generated WireMock mappings and how to test different scenarios.

## 🎯 How Scenarios Work

Each API endpoint generates **8 different scenarios** covering all common HTTP status codes:

| Scenario | Status Code | Description | How to Trigger |
|----------|-------------|-------------|----------------|
| success | 200 | Successful operation | `"scenario": "happy_path"` in request body |
| created | 201 | Resource created successfully | `"scenario": "happy_path"` in request body |
| unauthorized | 401 | Authentication required | `"scenario": "unauthorized_access"` in request body |
| forbidden | 403 | Access denied | `"scenario": "forbidden_request"` in request body |
| not_found | 404 | Resource not found | `?simulate=not_found` query parameter |
| server_error | 500 | Internal server error | `?simulate=server_error` query parameter |
| bad_gateway | 502 | Bad gateway | `?simulate=bad_gateway` query parameter |
| service_unavailable | 503 | Service unavailable | `?simulate=service_unavailable` query parameter |

## 🧪 Testing Examples

### Success Scenarios (POST/PUT)
```bash
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "scenario": "happy_path"}'
```

### Error Scenarios (POST/PUT)  
```bash
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "scenario": "unauthorized_access"}'
```

### Query Parameter Scenarios (GET/DELETE)
```bash
curl "http://localhost:8080/products?simulate=server_error"
curl "http://localhost:8080/products/123?simulate=not_found"
```

## 📁 File Organization

Generated mappings are organized by API and HTTP method:

```
mappings/
├── {api_name}/
│   ├── get_{api_name}_mappings.json      # All GET operations  
│   ├── create_{api_name}_mappings.json   # All POST operations
│   ├── update_{api_name}_mappings.json   # All PUT operations
│   └── delete_{api_name}_mappings.json   # All DELETE operations
```

Each mapping file contains **consolidated scenarios** with multiple status codes in a single file.

## 🔍 Understanding Request Matching

### JSON Body Matching (POST/PUT/PATCH)
```json
{
  "bodyPatterns": [
    {"matchesJsonPath": "$[?(@..* =~ /.*happy_path.*/i)]"}
  ]
}
```

### Query Parameter Matching (GET/DELETE)  
```json
{
  "queryParameters": {
    "simulate": {"equalTo": "server_error"}
  }
}
```

### Header Matching
```json
{
  "headers": {
    "X-Test-Scenario": {"equalTo": "not_found"}
  }
}
```

## 📊 Response Files

Response files are organized in the `__files/` directory:

```
__files/
├── {api_name}/
│   ├── get_{operation}_200_response.json     # Success responses
│   ├── post_{operation}_201_response.json    # Created responses  
│   ├── get_{operation}_401_error.json        # Error responses
│   └── ...                                   # All status codes
```

## 🚀 Generated Content

- **Spec-Compliant Responses**: Uses actual examples from your OpenAPI specifications
- **Professional Error Formats**: Industry-standard error responses with traceId and timestamps
- **Realistic Data**: Generated using OpenAPI schemas and examples
- **Comprehensive Coverage**: All common HTTP status codes included

---

*This documentation is auto-generated when you run `make generate`*

## get_products__productId

| Scenario | Status Code | Description | Request Condition |
|----------|-------------|-------------|-----------------|
| success | 200 | Get product by ID - Success | Invalid Authorization header |
| created | 201 | Get product by ID - Created | Invalid Authorization header |
| unauthorized | 401 | Get product by ID - Unauthorized | No Authorization header |
| forbidden | 403 | Get product by ID - Forbidden | Invalid Authorization header |
| not_found | 404 | Get product by ID - Not Found | ?simulate=not_found |
| server_error | 500 | Get product by ID - Internal Server Error | ?simulate=server_error |
| bad_gateway | 502 | Get product by ID - Bad Gateway | ?simulate=bad_gateway |
| service_unavailable | 503 | Get product by ID - Service Unavailable | ?simulate=service_unavailable |

## put_products__productId

| Scenario | Status Code | Description | Request Condition |
|----------|-------------|-------------|-----------------|
| success | 200 | Update product by ID - Success | Invalid Authorization header |
| created | 201 | Update product by ID - Created | Invalid Authorization header |
| unauthorized | 401 | Update product by ID - Unauthorized | No Authorization header |
| forbidden | 403 | Update product by ID - Forbidden | Invalid Authorization header |
| not_found | 404 | Update product by ID - Not Found | ?simulate=not_found |
| server_error | 500 | Update product by ID - Internal Server Error | ?simulate=server_error |
| bad_gateway | 502 | Update product by ID - Bad Gateway | ?simulate=bad_gateway |
| service_unavailable | 503 | Update product by ID - Service Unavailable | ?simulate=service_unavailable |

## delete_products__productId

| Scenario | Status Code | Description | Request Condition |
|----------|-------------|-------------|-----------------|
| success | 200 | Delete product by ID - Success | Invalid Authorization header |
| created | 201 | Delete product by ID - Created | Invalid Authorization header |
| unauthorized | 401 | Delete product by ID - Unauthorized | No Authorization header |
| forbidden | 403 | Delete product by ID - Forbidden | Invalid Authorization header |
| not_found | 404 | Delete product by ID - Not Found | ?simulate=not_found |
| server_error | 500 | Delete product by ID - Internal Server Error | ?simulate=server_error |
| bad_gateway | 502 | Delete product by ID - Bad Gateway | ?simulate=bad_gateway |
| service_unavailable | 503 | Delete product by ID - Service Unavailable | ?simulate=service_unavailable |


## Testing Examples

```bash
# Success scenario
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": 100}'

# Unauthorized scenario
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'

# Server error scenario
curl -X POST http://localhost:8080/credit-transfer-order-requests?simulate=server_error \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": 100}'
```
