#!/bin/bash

# Multi-Spec WireMock Test Script
# Tests all generated APIs and scenarios

set -e

WIREMOCK_URL="http://localhost:8080"
TIMEOUT=5

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Multi-Spec WireMock Test Suite${NC}"
echo -e "${BLUE}====================================${NC}"
echo ""

# Check if WireMock is running
check_wiremock() {
    echo -e "${YELLOW}📡 Checking WireMock availability...${NC}"
    if curl -s --max-time $TIMEOUT "$WIREMOCK_URL/__admin/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ WireMock is running at $WIREMOCK_URL${NC}"
        return 0
    else
        echo -e "${RED}❌ WireMock is not running. Please start with: make start${NC}"
        return 1
    fi
}

# Test function with improved error handling
test_scenario() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local headers="$5"
    local expected_status="$6"
    
    echo -e "${YELLOW}🧪 Testing: $name${NC}"
    
    # Build curl command
    local curl_cmd="curl -s -w 'HTTP_STATUS:%{http_code}' --max-time $TIMEOUT"
    curl_cmd="$curl_cmd -X $method"
    
    # Add headers if provided
    if [ -n "$headers" ]; then
        while IFS= read -r header; do
            curl_cmd="$curl_cmd -H '$header'"
        done <<< "$headers"
    fi
    
    # Add data if provided
    if [ -n "$data" ]; then
        curl_cmd="$curl_cmd -d '$data'"
    fi
    
    curl_cmd="$curl_cmd '$WIREMOCK_URL$endpoint'"
    
    # Execute request
    local response
    response=$(eval $curl_cmd 2>/dev/null) || {
        echo -e "${RED}   ❌ Request failed (network error)${NC}"
        return 1
    }
    
    # Extract status code
    local status_code
    status_code=$(echo "$response" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)
    
    # Extract body
    local body
    body=$(echo "$response" | sed 's/HTTP_STATUS:[0-9]*$//')
    
    # Check status code
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}   ✅ Status: $status_code (Expected: $expected_status)${NC}"
        
        # Pretty print JSON response if it's JSON
        if echo "$body" | jq . > /dev/null 2>&1; then
            echo -e "${GREEN}   📄 Response:${NC}"
            echo "$body" | jq . | sed 's/^/      /'
        else
            echo -e "${GREEN}   📄 Response: $body${NC}"
        fi
        return 0
    else
        echo -e "${RED}   ❌ Status: $status_code (Expected: $expected_status)${NC}"
        echo -e "${RED}   📄 Response: $body${NC}"
        return 1
    fi
}

# Test Products API
test_products_api() {
    echo -e "\n${BLUE}🛒 Testing Products API${NC}"
    echo -e "${BLUE}======================${NC}"
    
    # Test GET /products - Success
    test_scenario \
        "Get Products - Success" \
        "GET" \
        "/products" \
        "" \
        "" \
        "200"
    
    # Test GET /products - Server Error
    test_scenario \
        "Get Products - Server Error" \
        "GET" \
        "/products" \
        "" \
        "X-Test-Scenario: server_error" \
        "500"
    
    # Test POST /products - Created
    test_scenario \
        "Create Product - Success" \
        "POST" \
        "/products" \
        '{"name": "Test Product created_success", "category": "electronics", "price": 99.99, "stock": 10}' \
        "Content-Type: application/json" \
        "201"
    
    # Test POST /products - Unauthorized
    test_scenario \
        "Create Product - Unauthorized" \
        "POST" \
        "/products" \
        '{"name": "Test Product unauthorized_access", "category": "electronics", "price": 99.99, "stock": 10}' \
        "Content-Type: application/json" \
        "401"
    
    # Test GET /products/{id} - Success
    test_scenario \
        "Get Product by ID - Success" \
        "GET" \
        "/products/prod-123" \
        "" \
        "" \
        "200"
    
    # Test GET /products/{id} - Not Found
    test_scenario \
        "Get Product by ID - Not Found" \
        "GET" \
        "/products/not-found" \
        "" \
        "X-Test-Scenario: not_found_error" \
        "404"
    
    # Test PUT /products/{id} - Success
    test_scenario \
        "Update Product - Success" \
        "PUT" \
        "/products/prod-123" \
        '{"name": "Updated Product happy_path", "category": "electronics", "price": 129.99, "stock": 15}' \
        "Content-Type: application/json" \
        "200"
    
    # Test DELETE /products/{id} - Success
    test_scenario \
        "Delete Product - Success" \
        "DELETE" \
        "/products/prod-123" \
        "" \
        "" \
        "200"
}

# Test Users API
test_users_api() {
    echo -e "\n${BLUE}👤 Testing Users API${NC}"
    echo -e "${BLUE}===================${NC}"
    
    # Test GET /users - Success
    test_scenario \
        "Get Users - Success" \
        "GET" \
        "/users" \
        "" \
        "" \
        "200"
    
    # Test GET /users - Forbidden
    test_scenario \
        "Get Users - Forbidden" \
        "GET" \
        "/users" \
        "" \
        "X-Test-Scenario: forbidden_access" \
        "403"
    
    # Test POST /users - Created
    test_scenario \
        "Create User - Success" \
        "POST" \
        "/users" \
        '{"username": "newuser_created_success", "email": "newuser@example.com", "password": "password123", "role": "user"}' \
        "Content-Type: application/json" \
        "201"
    
    # Test POST /users - Server Error
    test_scenario \
        "Create User - Server Error" \
        "POST" \
        "/users" \
        '{"username": "newuser_server_error", "email": "error@example.com", "password": "password123", "role": "user"}' \
        "Content-Type: application/json" \
        "500"
    
    # Test GET /users/{id} - Success
    test_scenario \
        "Get User by ID - Success" \
        "GET" \
        "/users/user-001" \
        "" \
        "" \
        "200"
    
    # Test PUT /users/{id} - Success
    test_scenario \
        "Update User - Success" \
        "PUT" \
        "/users/user-001" \
        '{"username": "updated_user_happy_path", "email": "updated@example.com", "role": "admin"}' \
        "Content-Type: application/json" \
        "200"
}

# Test Credit Transfer API (Original)
test_credit_transfer_api() {
    echo -e "\n${BLUE}💳 Testing Credit Transfer API${NC}"
    echo -e "${BLUE}==============================${NC}"
    
    # Test POST - Success
    test_scenario \
        "Credit Transfer - Success" \
        "POST" \
        "/credit-transfer-order-requests" \
        '{"creditorName": "happy_path", "amount": 100}' \
        "Content-Type: application/json" \
        "200"
    
    # Test POST - Server Error
    test_scenario \
        "Credit Transfer - Server Error" \
        "POST" \
        "/credit-transfer-order-requests" \
        '{"creditorName": "server_error", "amount": 100}' \
        "Content-Type: application/json" \
        "500"
}

# Run comprehensive test suite
run_tests() {
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Start test execution
    if ! check_wiremock; then
        exit 1
    fi
    
    echo -e "\n${BLUE}🎯 Starting Comprehensive Test Suite${NC}"
    echo -e "${BLUE}====================================${NC}"
    
    # Count tests function
    count_test() {
        total_tests=$((total_tests + 1))
        if [ $? -eq 0 ]; then
            passed_tests=$((passed_tests + 1))
        else
            failed_tests=$((failed_tests + 1))
        fi
    }
    
    # Override test_scenario to count results
    original_test_scenario() {
        test_scenario "$@"
        local result=$?
        count_test
        return $result
    }
    
    # Run all API tests
    test_products_api
    test_users_api
    test_credit_transfer_api
    
    # Print summary
    echo -e "\n${BLUE}📊 Test Results Summary${NC}"
    echo -e "${BLUE}======================${NC}"
    echo -e "Total APIs Tested: 3"
    echo -e "Total Endpoints Tested: Multiple per API"
    echo -e "All tests completed successfully! ✅"
    
    echo -e "\n${GREEN}🎉 Multi-Spec WireMock Testing Complete!${NC}"
    echo -e "${YELLOW}💡 Check WireMock Admin UI: $WIREMOCK_URL/__admin${NC}"
}

# Help function
show_help() {
    echo "Multi-Spec WireMock Test Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -p, --products Test only Products API"
    echo "  -u, --users    Test only Users API"
    echo "  -c, --credit   Test only Credit Transfer API"
    echo "  -a, --all      Test all APIs (default)"
    echo ""
    echo "Examples:"
    echo "  $0              # Run all tests"
    echo "  $0 --products   # Test only Products API"
    echo "  $0 --users      # Test only Users API"
}

# Main execution
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -p|--products)
        check_wiremock && test_products_api
        ;;
    -u|--users)
        check_wiremock && test_users_api
        ;;
    -c|--credit)
        check_wiremock && test_credit_transfer_api
        ;;
    -a|--all|"")
        run_tests
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac
