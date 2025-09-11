#!/bin/bash

# Multi-Spec WireMock Scenario Testing Script
# Tests all generated scenarios for any APIs in the spec directory

set -e

WIREMOCK_URL="http://localhost:8080"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Multi-Spec WireMock Scenario Testing${NC}"
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

# Auto-discover endpoints from generated mappings
echo "Discovering generated API endpoints..."
ENDPOINTS=()

# Look for mapping files and extract endpoints
if [ -d "wiremock/mappings" ]; then
    for api_dir in wiremock/mappings/*/; do
        if [ -d "$api_dir" ]; then
            api_name=$(basename "$api_dir")
            echo "Found API: $api_name"
            
            # Look for common endpoints in the API
            if [ -f "$api_dir/get_${api_name}_mappings.json" ]; then
                # Extract URLs from the mapping files
                endpoint=$(jq -r '.mappings[0].request.urlPathPattern // .mappings[0].request.urlPath // .mappings[0].request.url' "$api_dir/get_${api_name}_mappings.json" 2>/dev/null | head -1)
                if [ "$endpoint" != "null" ] && [ "$endpoint" != "" ]; then
                    ENDPOINTS+=("$endpoint")
                    echo "  - Endpoint: $endpoint"
                fi
            fi
        fi
    done
fi

if [ ${#ENDPOINTS[@]} -eq 0 ]; then
    echo -e "${YELLOW}No endpoints auto-discovered. Using default products endpoint for demo.${NC}"
    ENDPOINTS=("/products")
fi

echo ""

# Test each discovered endpoint
for endpoint in "${ENDPOINTS[@]}"; do
    echo -e "${BLUE}Testing endpoint: $endpoint${NC}"
    echo ""
    
    # Sample request body for POST/PUT requests
    REQUEST_BODY='{
      "name": "Test Item",
      "description": "Test description",
      "scenario": "happy_path"
    }'

    # Test 1: Success Scenario (GET)
    test_scenario \
        "GET Success - List items" \
        "200" \
        "curl -s -X GET '$WIREMOCK_URL$endpoint'"

    # Test 2: Success Scenario (POST)  
    test_scenario \
        "POST Success - Create item" \
        "201" \
        "curl -s -X POST '$WIREMOCK_URL$endpoint' \
            -H 'Content-Type: application/json' \
            -d '$REQUEST_BODY'"

    # Test 3: Unauthorized (401)
    test_scenario \
        "Unauthorized - Invalid scenario" \
        "401" \
        "curl -s -X POST '$WIREMOCK_URL$endpoint' \
            -H 'Content-Type: application/json' \
            -d '{\"name\": \"Test\", \"scenario\": \"unauthorized_access\"}'"

    # Test 4: Forbidden (403)
    test_scenario \
        "Forbidden - Forbidden scenario" \
        "403" \
        "curl -s -X POST '$WIREMOCK_URL$endpoint' \
            -H 'Content-Type: application/json' \
            -d '{\"name\": \"Test\", \"scenario\": \"forbidden_request\"}'"

    # Test 5: Not Found (404)
    test_scenario \
        "Not Found - Query parameter" \
        "404" \
        "curl -s -X GET '$WIREMOCK_URL$endpoint?simulate=not_found'"

    # Test 6: Internal Server Error (500)
    test_scenario \
        "Internal Server Error" \
        "500" \
        "curl -s -X GET '$WIREMOCK_URL$endpoint?simulate=server_error'"

    # Test 7: Bad Gateway (502)
    test_scenario \
        "Bad Gateway" \
        "502" \
        "curl -s -X GET '$WIREMOCK_URL$endpoint?simulate=bad_gateway'"

    # Test 8: Service Unavailable (503)
    test_scenario \
        "Service Unavailable" \
        "503" \
        "curl -s -X GET '$WIREMOCK_URL$endpoint?simulate=service_unavailable'"

    echo -e "${BLUE}Completed testing for $endpoint${NC}"
    echo ""
done

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
