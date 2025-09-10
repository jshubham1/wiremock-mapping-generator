#!/bin/bash

# WireMock OpenAPI Setup Script
set -e

echo "=== WireMock OpenAPI Mapping Generator Setup ==="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if spec file exists
if [ ! -f "spec/open-api-spec.json" ] && [ ! -f "spec/open-api-spec.yaml" ]; then
    echo -e "${RED}Error: OpenAPI spec file not found!${NC}"
    echo "Please place your OpenAPI specification in the spec/ directory as:"
    echo "  - open-api-spec.json (recommended)"
    echo "  - open-api-spec.yaml"
    exit 1
fi

# Determine spec file
SPEC_FILE=""
if [ -f "spec/open-api-spec.json" ]; then
    SPEC_FILE="open-api-spec.json"
elif [ -f "spec/open-api-spec.yaml" ]; then
    SPEC_FILE="open-api-spec.yaml"
fi

echo -e "${BLUE}Found OpenAPI spec: spec/${SPEC_FILE}${NC}"

# Generate mappings
echo -e "${YELLOW}Step 1: Generating WireMock mappings...${NC}"
python3 scripts/openapi_to_wiremock.py "spec/${SPEC_FILE}" wiremock/mappings wiremock/__files

# Start WireMock
echo -e "${YELLOW}Step 2: Starting WireMock server...${NC}"
docker-compose up -d wiremock

# Wait a moment for startup
sleep 3

# Check status
echo -e "${YELLOW}Step 3: Checking server status...${NC}"
if curl -sf http://localhost:8080/__admin/health > /dev/null; then
    echo -e "${GREEN}✓ WireMock server is running successfully!${NC}"
    echo ""
    echo -e "${GREEN}🚀 Your mock API is ready:${NC}"
    echo -e "  API Base URL:     ${BLUE}http://localhost:8080${NC}"
    echo -e "  Admin Interface:  ${BLUE}http://localhost:8080/__admin${NC}"
    echo -e "  Health Check:     ${BLUE}http://localhost:8080/__admin/health${NC}"
    echo ""
    echo -e "${GREEN}📊 Available endpoints:${NC}"
    echo -e "  GET ${BLUE}http://localhost:8080/${NC}     - List API versions"
    echo -e "  GET ${BLUE}http://localhost:8080/v2${NC}   - Show API version details"
    echo ""
    echo -e "${YELLOW}Quick commands:${NC}"
    echo "  make test      - Test all endpoints"
    echo "  make logs      - View server logs"
    echo "  make stop      - Stop the server"
    echo "  make restart   - Restart the server"
else
    echo -e "${RED}✗ WireMock server failed to start${NC}"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
