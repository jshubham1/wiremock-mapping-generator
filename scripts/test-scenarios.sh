#!/bin/bash

# Dynamic WireMock Test Script
# Tests all generated endpoints based on actual mapping files

set -e

WIREMOCK_URL="http://localhost:8080"
TIMEOUT=5
MAPPINGS_DIR="./generated/wiremock/mappings"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Dynamic WireMock Test Suite${NC}"
echo -e "${BLUE}=================================${NC}"
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

# Extract test cases from mapping files
extract_test_cases() {
    local mappings_file="$1"
    local api_name="$2"
    
    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}❌ jq is required but not installed. Please install jq to run tests.${NC}"
        return 1
    fi
    
    # Extract mappings using jq - also extract header requirements
    jq -r '.mappings[] | "\(.request.method)|\(.request.urlPathPattern // .request.urlPath)|\(.response.status)|\(.metadata.scenario // "default")|\(.metadata.operation_id // "unknown")|\(.request.headers."X-Test-Scenario".equalTo // "")"' "$mappings_file" 2>/dev/null | while IFS='|' read -r method url_pattern status scenario operation_id test_header; do
        if [ -n "$method" ] && [ -n "$url_pattern" ] && [ -n "$status" ]; then
            echo "$api_name|$method|$url_pattern|$status|$scenario|$operation_id|$test_header"
        fi
    done
}

# Convert URL pattern to actual URL for testing
convert_url_pattern() {
    local pattern="$1"
    local method="$2"
    local scenario="$3"
    
    # Convert regex patterns to actual test URLs
    # Replace [^/]+ with sample values
    local url="$pattern"
    url=$(echo "$url" | sed 's|\[\\?\^/\]\\?+|123|g')  # Replace [^/]+ or [^/]+ with 123
    url=$(echo "$url" | sed 's|\[\^/\]+|123|g')        # Replace [^/]+ with 123
    url=$(echo "$url" | sed 's|{[^}]*}|123|g')         # Replace {id} with 123
    
    echo "$url"
}

# Generate test payload based on scenario and method
generate_test_payload() {
    local method="$1"
    local scenario="$2"
    local operation_id="$3"
    
    case "$method" in
        "POST"|"PUT"|"PATCH")
            # Generate JSON payload with scenario identifier that matches bodyPatterns
            # Map scenarios to the identifiers expected by bodyPatterns
            local scenario_identifier=""
            case "$scenario" in
                "success")
                    scenario_identifier="happy_path"
                    ;;
                "created")
                    scenario_identifier="created_success"
                    ;;
                "unauthorized")
                    scenario_identifier="unauthorized_access"
                    ;;
                "forbidden")
                    scenario_identifier="forbidden_access"
                    ;;
                "not_found")
                    scenario_identifier="not_found_error"
                    ;;
                "server_error")
                    scenario_identifier="server_error"
                    ;;
                "bad_gateway")
                    scenario_identifier="bad_gateway"
                    ;;
                "service_unavailable")
                    scenario_identifier="service_unavailable"
                    ;;
                *)
                    scenario_identifier="$scenario"
                    ;;
            esac
            
            # Generate appropriate payload based on operation
            case "$operation_id" in
                *user*|*User*)
                    echo "{\"name\": \"$scenario_identifier\", \"email\": \"test@example.com\", \"role\": \"user\"}"
                    ;;
                *product*|*Product*)
                    echo "{\"name\": \"$scenario_identifier\", \"price\": 99.99, \"category\": \"test\"}"
                    ;;
                *)
                    echo "{\"test_scenario\": \"$scenario_identifier\", \"data\": \"test\"}"
                    ;;
            esac
            ;;
        *)
            echo ""
            ;;
    esac
}

# Test a specific endpoint
test_endpoint() {
    local api_name="$1"
    local method="$2"
    local url_pattern="$3"
    local expected_status="$4"
    local scenario="$5"
    local operation_id="$6"
    local test_header="$7"
    
    local url=$(convert_url_pattern "$url_pattern" "$method" "$scenario")
    local payload=$(generate_test_payload "$method" "$scenario" "$operation_id")
    
    echo -e "${YELLOW}🧪 Testing: $api_name - $method $url ($scenario)${NC}"
    
    # Build curl command
    local curl_cmd="curl -s -w 'HTTP_STATUS:%{http_code}' --max-time $TIMEOUT"
    curl_cmd="$curl_cmd -X $method"
    curl_cmd="$curl_cmd -H 'Accept: application/json'"
    
    # Add scenario-specific headers or body based on method
    case "$method" in
        "GET"|"DELETE")
            # For GET/DELETE, use X-Test-Scenario header if specified
            if [ -n "$test_header" ]; then
                curl_cmd="$curl_cmd -H 'X-Test-Scenario: $test_header'"
            fi
            ;;
        "POST"|"PUT"|"PATCH")
            # For POST/PUT/PATCH, use JSON body with scenario identifier
            if [ -n "$payload" ]; then
                curl_cmd="$curl_cmd -H 'Content-Type: application/json'"
                curl_cmd="$curl_cmd -d '$payload'"
            fi
            ;;
    esac
    
    curl_cmd="$curl_cmd '$WIREMOCK_URL$url'"
    
    # Execute request
    local response
    response=$(eval $curl_cmd 2>/dev/null) || {
        echo -e "${RED}   ❌ Request failed (network error)${NC}"
        return 1
    }
    
    # Extract status code
    local actual_status
    actual_status=$(echo "$response" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)
    
    # Extract body
    local body
    body=$(echo "$response" | sed 's/HTTP_STATUS:[0-9]*$//')
    
    # Check status code
    if [ "$actual_status" = "$expected_status" ]; then
        echo -e "${GREEN}   ✅ Status: $actual_status (Expected: $expected_status)${NC}"
        
        # Pretty print JSON response if it's JSON and not too long
        if echo "$body" | jq . > /dev/null 2>&1; then
            local formatted_body
            formatted_body=$(echo "$body" | jq -c .)
            if [ ${#formatted_body} -lt 200 ]; then
                echo -e "${GREEN}   📄 Response: $formatted_body${NC}"
            else
                echo -e "${GREEN}   📄 Response: [JSON Response - ${#formatted_body} characters]${NC}"
            fi
        else
            if [ ${#body} -lt 100 ]; then
                echo -e "${GREEN}   📄 Response: $body${NC}"
            else
                echo -e "${GREEN}   📄 Response: [Response - ${#body} characters]${NC}"
            fi
        fi
        return 0
    else
        echo -e "${RED}   ❌ Status: $actual_status (Expected: $expected_status)${NC}"
        if [ ${#body} -lt 200 ]; then
            echo -e "${RED}   📄 Response: $body${NC}"
        else
            echo -e "${RED}   📄 Response: [Error Response - ${#body} characters]${NC}"
        fi
        return 1
    fi
}

# Test all APIs
test_all_apis() {
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    echo -e "${BLUE}🔍 Discovering test cases from mapping files...${NC}"
    
    # Find all mapping files
    local test_cases_file=$(mktemp)
    
    for api_dir in "$MAPPINGS_DIR"/*; do
        if [ -d "$api_dir" ]; then
            local api_name=$(basename "$api_dir")
            echo -e "${BLUE}📁 Processing API: $api_name${NC}"
            
            for mapping_file in "$api_dir"/*.json; do
                if [ -f "$mapping_file" ]; then
                    extract_test_cases "$mapping_file" "$api_name" >> "$test_cases_file"
                fi
            done
        fi
    done
    
    # Count total test cases
    total_tests=$(wc -l < "$test_cases_file")
    
    if [ "$total_tests" -eq 0 ]; then
        echo -e "${RED}❌ No test cases found in mapping files${NC}"
        rm -f "$test_cases_file"
        return 1
    fi
    
    echo -e "${BLUE}🎯 Found $total_tests test cases to execute${NC}"
    echo ""
    
    # Execute each test case
    while IFS='|' read -r api_name method url_pattern status scenario operation_id test_header; do
        if test_endpoint "$api_name" "$method" "$url_pattern" "$status" "$scenario" "$operation_id" "$test_header"; then
            ((passed_tests++))
        else
            ((failed_tests++))
        fi
        echo ""
    done < "$test_cases_file"
    
    # Clean up
    rm -f "$test_cases_file"
    
    # Print summary
    echo -e "${BLUE}📊 Test Summary${NC}"
    echo -e "${BLUE}===============${NC}"
    echo -e "Total Tests: $total_tests"
    echo -e "${GREEN}Passed: $passed_tests${NC}"
    echo -e "${RED}Failed: $failed_tests${NC}"
    
    if [ "$failed_tests" -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}❌ Some tests failed${NC}"
        return 1
    fi
}

# Main execution
main() {
    if ! check_wiremock; then
        exit 1
    fi
    
    echo ""
    
    if ! test_all_apis; then
        exit 1
    fi
}

main "$@"
