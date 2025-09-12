#!/bin/bash

# WireMock Web UI Startup Script
set -e

echo "🌐 Starting WireMock Mapping Generator Web UI..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if required directories exist
if [ ! -d "web-app" ]; then
    echo -e "${RED}❌ web-app directory not found. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Building and starting services...${NC}"
echo ""

# Start the complete stack with web UI
docker-compose up --build -d

echo ""
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 10

# Check if services are running
if docker-compose ps | grep -q "wiremock-web-ui"; then
    echo -e "${GREEN}✅ Web UI started successfully!${NC}"
    echo ""
    echo -e "${BLUE}🌐 Access the WireMock Mapping Generator Web UI:${NC}"
    echo "   📱 http://localhost:5000"
    echo ""
    echo -e "${BLUE}🔧 WireMock Server Admin Interface:${NC}"
    echo "   ⚙️  http://localhost:8080/__admin"
    echo ""
    echo -e "${YELLOW}📋 Available services:${NC}"
    docker-compose ps
    echo ""
    echo -e "${GREEN}🎉 All services are ready!${NC}"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    echo "1. 📂 Open http://localhost:5000 in your browser"
    echo "2. 📤 Upload your OpenAPI specification files"
    echo "3. ⚙️  Choose generation options (JSON only or JSON + Java)"
    echo "4. 🎯 Generate and download your WireMock mappings"
    echo "5. 🚀 Use the generated files with WireMock server"
else
    echo -e "${RED}❌ Failed to start web UI. Check Docker logs:${NC}"
    docker-compose logs wiremock-web-ui
    exit 1
fi
