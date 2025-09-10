# Enhanced WireMock Mapping Generator - Usage Guide

## Quick Start

1. **Clean and Generate Enhanced Mappings**:
   ```bash
   make clean && make generate-enhanced
   ```

2. **Start WireMock Server**:
   ```bash
   make start
   ```

3. **Test All Scenarios**:
   ```bash
   make test-scenarios
   ```

## Generated Files Overview

### Mapping Files
- Located in `./wiremock/mappings/`
- Named with pattern: `mapping_{number}_{operationId}_{scenario}_{statusCode}.json`
- Examples:
  - `mapping_001_createCreditTransferOrderRequest_success_200.json`
  - `mapping_003_createCreditTransferOrderRequest_unauthorized_401.json`
  - `mapping_006_createCreditTransferOrderRequest_server_error_500.json`

### Response Files
- Located in `./wiremock/__files/`
- Named with pattern: `{operationId}_{scenario}_response.json`
- Examples:
  - `createCreditTransferOrderRequest_success_response.json`
  - `createCreditTransferOrderRequest_unauthorized_response.json`

### Documentation
- `./wiremock/mappings/MAPPINGS_DOCUMENTATION.md` - Complete mapping documentation

## Testing Different Scenarios

### 1. Success Scenarios (200/201)

```bash
# POST request with valid authentication
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{
    "amount": {
      "value": "100.00",
      "currency": "EUR"
    },
    "creditorAccount": {
      "iban": "NL91ABNA0417164300"
    },
    "debtor": {
      "name": "John Doe"
    }
  }'
```

### 2. Authentication Errors

#### Unauthorized (401) - Missing Authorization Header
```bash
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -d '{"amount": {"value": "100.00", "currency": "EUR"}}'
```

#### Forbidden (403) - Invalid Authorization Header
```bash
curl -X POST http://localhost:8080/credit-transfer-order-requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid-token" \
  -d '{"amount": {"value": "100.00", "currency": "EUR"}}'
```

### 3. Server Error Simulation

#### Internal Server Error (500)
```bash
curl -X POST "http://localhost:8080/credit-transfer-order-requests?simulate=server_error" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": {"value": "100.00", "currency": "EUR"}}'
```

#### Bad Gateway (502)
```bash
curl -X POST "http://localhost:8080/credit-transfer-order-requests?simulate=bad_gateway" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": {"value": "100.00", "currency": "EUR"}}'
```

#### Service Unavailable (503)
```bash
curl -X POST "http://localhost:8080/credit-transfer-order-requests?simulate=service_unavailable" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-token" \
  -d '{"amount": {"value": "100.00", "currency": "EUR"}}'
```

## Available Operations

Based on your OpenAPI spec, the following operations are available:

1. **createCreditTransferOrderRequest** - `POST /credit-transfer-order-requests`
2. **updateCreditTransferOrderRequest** - `PUT /credit-transfer-order-requests/{id}`
3. **deleteCreditTransferOrderRequest** - `POST /credit-transfer-order-requests-deletion`
4. **cancelCreditTransferOrderRequest** - `POST /credit-transfer-order-requests-cancellation`
5. **postCreditTransferOrderRequestPaymentSetInclusion** - `POST /credit-transfer-order-requests/{id}/payment-set-inclusion`
6. **postCreditTransferOrderRequestPaymentSetExclusion** - `POST /credit-transfer-order-requests/{id}/payment-set-exclusion`
7. **verifyCreditTransferOrderRequest** - `POST /credit-transfer-order-requests-verification`

Each operation has all 8 status code scenarios (200, 201, 401, 403, 404, 500, 502, 503).

## Response Examples

### Success Response (201)
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

### Error Response (401)
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

### Error Response (500)
```json
{
  "errors": [
    {
      "code": "INTERNAL_SERVER_ERROR", 
      "message": "Server error occured while processing the request.",
      "traceId": "f1b554d8-406a-4301-b549-d539a5e885ae",
      "status": 500
    }
  ]
}
```

## Advanced Usage

### Custom Mapping Modifications

You can modify the generated mappings in `./wiremock/mappings/` to customize:

1. **Request matching criteria**
2. **Response content**
3. **Response delays** (add `"fixedDelayMilliseconds": 2000`)
4. **Response headers**

### Adding Custom Scenarios

Create additional JSON files in `./wiremock/mappings/` following the WireMock format:

```json
{
  "id": "custom-scenario",
  "name": "Custom Scenario",
  "request": {
    "method": "POST",
    "urlPath": "/credit-transfer-order-requests",
    "queryParameters": {
      "test": {"equalTo": "custom"}
    }
  },
  "response": {
    "status": 422,
    "headers": {"Content-Type": "application/json"},
    "body": "{\"error\": \"Custom validation error\"}"
  }
}
```

### Monitoring and Debugging

1. **View all mappings**: Visit http://localhost:8080/__admin/mappings
2. **View requests**: Visit http://localhost:8080/__admin/requests
3. **Reset mappings**: `curl -X POST http://localhost:8080/__admin/mappings/reset`
4. **Check logs**: `make logs`

## Troubleshooting

### All Requests Return 201 (Success)
This happens when WireMock doesn't match your error scenarios. Check:
1. **Authorization header**: Use exact format in examples
2. **Query parameters**: Include `?simulate=error_type` for server errors
3. **Request content-type**: Ensure it's `application/json`

### Mappings Not Loading
1. **Restart WireMock**: `make restart`
2. **Check mapping syntax**: Validate JSON files
3. **Check logs**: `make logs`

### Response File Not Found
1. **Regenerate mappings**: `make clean && make generate-enhanced`
2. **Check file permissions**: Ensure Docker can read files
3. **Verify file names**: Check that bodyFileName matches actual file

## Performance Considerations

- **56 mappings** generated for 7 operations × 8 scenarios
- **Priority-based matching** ensures optimal performance
- **Static response files** for fast response times
- **No external dependencies** for reliability
