#!/bin/bash

# WireMock Web UI Development Startup Script
set -e

echo "🌐 Starting WireMock Mapping Generator Web UI (Development Mode)..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to web-app directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
WEB_APP_DIR="$PROJECT_ROOT/web-app"

if [ ! -d "$WEB_APP_DIR" ]; then
    echo -e "${RED}❌ web-app directory not found at $WEB_APP_DIR${NC}"
    echo "Please run this script from the project root."
    exit 1
fi

cd "$WEB_APP_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -d "web-app" ]; then
    echo -e "${RED}❌ web-app directory not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Navigate to web-app directory
cd web-app

echo -e "${BLUE}📦 Installing Python dependencies...${NC}"

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

echo ""
echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"
echo ""

# Set environment variables
export FLASK_ENV=development
export FLASK_APP=app.py
export PYTHONPATH="$(pwd):$(pwd)/.."

echo -e "${BLUE}🚀 Starting Web UI in development mode...${NC}"
echo ""
echo -e "${GREEN}🌐 Web UI will be available at: http://localhost:5001${NC}"
echo ""
echo -e "${YELLOW}📋 Features available:${NC}"
echo "• 📤 Drag & drop OpenAPI file upload"
echo "• 🔧 JSON and Java code generation options"
echo "• 📦 ZIP download of generated mappings"
echo "• 📱 Mobile-responsive interface"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the Flask application
python app.py
