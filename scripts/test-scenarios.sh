#!/bin/bash

# Enhanced WireMock Scenario Testing Script
# This script demonstrates all the generated scenarios

set -e

WIREMOCK_URL="http://localhost:8080"
ENDPOINT="/credit-transfer-order-requests"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Sample request body
REQUEST_BODY='{
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

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Enhanced WireMock Scenario Testing${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to make API call and display result
test_scenario() {
    local scenario_name="$1"
    local expected_status="$2"
    local curl_command="$3"
    
    echo -e "${YELLOW}Testing: $scenario_name${NC}"
    echo -e "Expected Status: $expected_status"
    echo "Command: $curl_command"
    echo ""
    
    # Execute the curl command and capture response
    response=$(eval "$curl_command" 2>/dev/null || true)
    status_code=$(eval "$curl_command" -w "%{http_code}" -o /dev/null -s 2>/dev/null || echo "000")
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ SUCCESS: Got expected status $status_code${NC}"
    else
        echo -e "${RED}✗ FAILED: Expected $expected_status, got $status_code${NC}"
    fi
    
    echo "Response:"
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
    echo ""
    echo "---"
    echo ""
}

# Check if WireMock is running
echo "Checking WireMock availability..."
if ! curl -s "$WIREMOCK_URL/__admin/health" > /dev/null; then
    echo -e "${RED}ERROR: WireMock is not running at $WIREMOCK_URL${NC}"
    echo "Please run: make start"
    exit 1
fi
echo -e "${GREEN}✓ WireMock is running${NC}"
echo ""

# Test 1: Success Scenario (200/201)
test_scenario \
    "Success - Valid Request" \
    "201" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer valid-token' \
        -d '$REQUEST_BODY'"

# Test 2: Unauthorized (401)
test_scenario \
    "Unauthorized - Missing Authorization Header" \
    "401" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT' \
        -H 'Content-Type: application/json' \
        -d '$REQUEST_BODY'"

# Test 3: Forbidden (403)
test_scenario \
    "Forbidden - Invalid Authorization Header" \
    "403" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer invalid-token' \
        -d '$REQUEST_BODY'"

# Test 4: Internal Server Error (500)
test_scenario \
    "Internal Server Error - Simulated" \
    "500" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT?simulate=server_error' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer valid-token' \
        -d '$REQUEST_BODY'"

# Test 5: Bad Gateway (502)
test_scenario \
    "Bad Gateway - Simulated" \
    "502" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT?simulate=bad_gateway' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer valid-token' \
        -d '$REQUEST_BODY'"

# Test 6: Service Unavailable (503)
test_scenario \
    "Service Unavailable - Simulated" \
    "503" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT?simulate=service_unavailable' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer valid-token' \
        -d '$REQUEST_BODY'"

# Test 7: Not Found (404) - This one might need different URL or parameter
test_scenario \
    "Not Found - Default Priority" \
    "404" \
    "curl -s -X POST '$WIREMOCK_URL$ENDPOINT?simulate=not_found' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer valid-token' \
        -d '$REQUEST_BODY'"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Testing Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Additional Resources:${NC}"
echo "• WireMock Admin UI: $WIREMOCK_URL/__admin"
echo "• View all mappings: $WIREMOCK_URL/__admin/mappings"
echo "• View request history: $WIREMOCK_URL/__admin/requests"
echo "• Generated documentation: ./wiremock/mappings/MAPPINGS_DOCUMENTATION.md"
echo ""
