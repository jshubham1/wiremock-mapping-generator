#!/bin/bash

# WireMock Web UI Demo Script
set -e

echo "🎬 WireMock Mapping Generator Web UI Demo"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}Welcome to the WireMock Mapping Generator Web UI Demo!${NC}"
echo ""
echo -e "${CYAN}This demo will show you how to use the modern web interface to:${NC}"
echo "• 📤 Upload OpenAPI specification files via drag & drop"
echo "• ⚙️  Configure generation options (JSON only or JSON + Java)"
echo "• 🎯 Generate comprehensive WireMock mappings"
echo "• 📦 Download complete packages as ZIP files"
echo ""

echo -e "${YELLOW}📋 Features Showcase:${NC}"
echo ""
echo -e "${GREEN}🎨 Modern Interface:${NC}"
echo "  ✓ Responsive design (works on desktop, tablet, mobile)"
echo "  ✓ Drag & drop file upload with visual feedback"
echo "  ✓ Real-time progress tracking during generation"
echo "  ✓ Instant download of generated packages"
echo ""

echo -e "${GREEN}📁 File Support:${NC}"
echo "  ✓ YAML files (.yaml, .yml)"
echo "  ✓ JSON files (.json)"
echo "  ✓ Multiple files simultaneously"
echo "  ✓ File validation and size checking (max 16MB)"
echo ""

echo -e "${GREEN}⚙️  Generation Options:${NC}"
echo "  ✓ JSON Only: WireMock mappings for immediate use"
echo "  ✓ JSON + Java: Include Spring Boot & JUnit integration"
echo "  ✓ Custom Java package names"
echo "  ✓ Comprehensive error scenario coverage"
echo ""

echo -e "${GREEN}📦 Output Package:${NC}"
echo "  ✓ ZIP archive with organized structure"
echo "  ✓ Complete documentation included"
echo "  ✓ Ready-to-use mapping files"
echo "  ✓ Optional Java integration code"
echo ""

echo -e "${BLUE}🚀 Starting the Web UI...${NC}"
echo ""

# Check if we're in the correct directory
if [ ! -d "web-app" ]; then
    echo -e "${RED}❌ Please run this script from the project root directory${NC}"
    exit 1
fi

# Start the web UI in development mode
echo -e "${YELLOW}Starting in development mode for best demo experience...${NC}"
echo ""

# Start in background for demo
./scripts/start-web-dev.sh &
WEB_UI_PID=$!

# Wait for startup
echo -e "${CYAN}⏳ Waiting for web UI to start...${NC}"
sleep 10

# Check if it's running
if curl -s http://localhost:5000/health > /dev/null; then
    echo -e "${GREEN}✅ Web UI is running successfully!${NC}"
    echo ""
    
    echo -e "${BLUE}🌐 Demo Instructions:${NC}"
    echo ""
    echo -e "${YELLOW}1. Open your browser to:${NC} ${CYAN}http://localhost:5000${NC}"
    echo ""
    echo -e "${YELLOW}2. Try the demo with sample files:${NC}"
    echo "   • Use the existing files in the spec/ directory:"
    find spec/ -name "*.yaml" -o -name "*.yml" -o -name "*.json" 2>/dev/null | head -3 | sed 's/^/     - /'
    echo ""
    echo -e "${YELLOW}3. Upload Process:${NC}"
    echo "   • Drag files onto the upload area (or click to browse)"
    echo "   • Choose 'JSON Only' or 'JSON + Java' generation"
    echo "   • Click 'Generate WireMock Mappings'"
    echo "   • Watch real-time progress"
    echo "   • Download the ZIP package when complete"
    echo ""
    echo -e "${YELLOW}4. Explore Generated Content:${NC}"
    echo "   • Extract the ZIP file"
    echo "   • Review the organized mapping structure"
    echo "   • Check the included documentation"
    echo "   • Use with WireMock server"
    echo ""
    
    echo -e "${GREEN}🎯 What You'll See:${NC}"
    echo "• Modern, responsive interface with WireMock branding"
    echo "• Drag & drop area with visual feedback"
    echo "• Generation options with clear descriptions"
    echo "• Progress modal with animated loading"
    echo "• Success modal with generation summary"
    echo "• Download button for ZIP package"
    echo ""
    
    echo -e "${BLUE}📊 Expected Results:${NC}"
    echo "• Comprehensive WireMock mappings (JSON files)"
    echo "• Realistic response files for all scenarios"
    echo "• Optional Java Spring Boot integration code"
    echo "• Complete documentation and usage instructions"
    echo "• Organized directory structure for easy integration"
    echo ""
    
    echo -e "${CYAN}🔗 Quick Links:${NC}"
    echo "• Web UI: http://localhost:5000"
    echo "• Health Check: http://localhost:5000/health"
    echo ""
    
    echo -e "${YELLOW}Press any key to stop the demo...${NC}"
    read -n 1 -s
    
    # Clean shutdown
    echo ""
    echo -e "${BLUE}🛑 Stopping demo...${NC}"
    kill $WEB_UI_PID 2>/dev/null || true
    wait $WEB_UI_PID 2>/dev/null || true
    
    echo -e "${GREEN}✅ Demo completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "• Use 'make web-dev' for development"
    echo "• Use 'make web-ui' for Docker deployment"
    echo "• Check web-app/README.md for detailed documentation"
    echo "• Explore the generated mappings with WireMock"
    
else
    echo -e "${RED}❌ Failed to start web UI. Please check the logs above.${NC}"
    kill $WEB_UI_PID 2>/dev/null || true
    exit 1
fi
