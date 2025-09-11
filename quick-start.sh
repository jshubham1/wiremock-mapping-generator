#!/bin/bash

# WireMock Multi-Spec OpenAPI Setup Script
set -e

echo "=== WireMock Multi-Spec Mapping Generator Setup ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if any spec files exist
if [ ! "$(ls -A spec/*.{yaml,yml,json} 2>/dev/null)" ]; then
    echo -e "${RED}Error: No OpenAPI spec files found in spec/ directory!${NC}"
    echo "Please place your OpenAPI specifications in the spec/ directory as:"
    echo "  - any-name.yaml"
    echo "  - any-name.yml" 
    echo "  - any-name.json"
    echo ""
    echo "🎯 Goal: Drop any OpenAPI spec → automatic mapping generation!"
    exit 1
fi

# Count spec files
SPEC_COUNT=$(find spec/ -name "*.yaml" -o -name "*.yml" -o -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

echo -e "${BLUE}Found ${SPEC_COUNT} OpenAPI specification(s) in spec/ directory:${NC}"
find spec/ -name "*.yaml" -o -name "*.yml" -o -name "*.json" 2>/dev/null | sed 's/^/  - /'
echo ""

# Generate mappings using multi-spec generator
echo -e "${YELLOW}Step 1: Generating consolidated WireMock mappings for all APIs...${NC}"
make generate

# Start WireMock
echo -e "${YELLOW}Step 2: Starting WireMock server...${NC}"
make start

# Wait a moment for startup
sleep 5

# Check status
echo -e "${YELLOW}Step 3: Checking server status...${NC}"
if curl -sf http://localhost:8080/__admin/health > /dev/null; then
    echo -e "${GREEN}✓ WireMock server is running successfully!${NC}"
    echo ""
    echo -e "${GREEN}🚀 Your multi-spec mock API is ready:${NC}"
    echo -e "  API Base URL:     ${BLUE}http://localhost:8080${NC}"
    echo -e "  Admin Interface:  ${BLUE}http://localhost:8080/__admin${NC}"
    echo -e "  Health Check:     ${BLUE}http://localhost:8080/__admin/health${NC}"
    echo ""
    echo -e "${GREEN}📊 Generated mappings:${NC}"
    echo -e "  Total APIs:       ${BLUE}${SPEC_COUNT}${NC}"
    
    # Count mapping files
    MAPPING_COUNT=$(find wiremock/mappings -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  Mapping files:    ${BLUE}${MAPPING_COUNT}${NC}"
    
    # Show API directories
    if [ -d "wiremock/mappings" ]; then
        echo -e "  API directories:${NC}"
        find wiremock/mappings -type d -mindepth 1 -maxdepth 1 2>/dev/null | sed 's/.*\///g' | sed 's/^/    - /'
    fi
    
    echo ""
    echo -e "${YELLOW}🎯 Goal achieved: All OpenAPI specs automatically processed!${NC}"
    echo ""
    echo -e "${YELLOW}Quick commands:${NC}"
    echo "  make test              - Test all endpoints"
    echo "  make test-scenarios    - Test all error scenarios"
    echo "  make logs              - View server logs"
    echo "  make stop              - Stop the server"
    echo "  make restart           - Restart the server"
    echo "  make show-mappings     - List all generated mappings"
else
    echo -e "${RED}✗ WireMock server failed to start${NC}"
    echo "Check logs with: make logs"
    exit 1
fi
