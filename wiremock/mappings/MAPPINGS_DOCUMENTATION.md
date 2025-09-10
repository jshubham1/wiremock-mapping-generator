# WireMock Mappings Documentation

This document describes the generated WireMock mappings and how to use them.

## get_products

| Scenario | Status Code | Description | Request Condition |
|----------|-------------|-------------|-----------------|
| success | 200 | Get all products - Success | Invalid Authorization header |
| created | 201 | Get all products - Created | Invalid Authorization header |
| unauthorized | 401 | Get all products - Unauthorized | No Authorization header |
| forbidden | 403 | Get all products - Forbidden | Invalid Authorization header |
| not_found | 404 | Get all products - Not Found | ?simulate=not_found |
| server_error | 500 | Get all products - Internal Server Error | ?simulate=server_error |
| bad_gateway | 502 | Get all products - Bad Gateway | ?simulate=bad_gateway |
| service_unavailable | 503 | Get all products - Service Unavailable | ?simulate=service_unavailable |

## post_products

| Scenario | Status Code | Description | Request Condition |
|----------|-------------|-------------|-----------------|
| success | 200 | Create a new product - Success | Invalid Authorization header |
| created | 201 | Create a new product - Created | Invalid Authorization header |
| unauthorized | 401 | Create a new product - Unauthorized | No Authorization header |
| forbidden | 403 | Create a new product - Forbidden | Invalid Authorization header |
| not_found | 404 | Create a new product - Not Found | ?simulate=not_found |
| server_error | 500 | Create a new product - Internal Server Error | ?simulate=server_error |
| bad_gateway | 502 | Create a new product - Bad Gateway | ?simulate=bad_gateway |
| service_unavailable | 503 | Create a new product - Service Unavailable | ?simulate=service_unavailable |

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
