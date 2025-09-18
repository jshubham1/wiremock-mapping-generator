# WireMock Mapping Generator

🚀 **Modern tool for generating WireMock mappings from OpenAPI specifications**

Transform your OpenAPI specs into ready-to-use WireMock mappings with both CLI and elegant web interface.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.13.1-blue.svg)](http://wiremock.org/)

## ✨ Features

- 🔄 **Multi-spec processing** - Generate mappings from multiple OpenAPI specs
- 🎯 **Smart mapping generation** - Comprehensive HTTP status codes (200, 401, 403, 404, 500, 502, 503)
- 🌐 **Modern web interface** - Drag-and-drop file upload with tabbed modals and live testing
- ⚡ **CLI tool** - Perfect for automation and CI/CD pipelines
- 🐳 **Docker ready** - Full Docker Compose setup with WireMock 3.13.1
- ☕ **Java integration** - Optional Java client code generation
- 🧪 **Live testing** - Test generated endpoints directly from web UI
- 📦 **Smart packaging** - Download all generated files as ZIP

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (optional, for WireMock server)

### Installation

```bash
git clone <repository-url>
cd wiremock-mapping-generator
make setup
```

## 📖 Usage

### 🖥️ CLI Tool

```bash
# Generate mappings for all specs
./wiremock-generator --spec-dir ./examples --output-dir ./output

# Include Java code generation
./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
```

### 🌐 Web Interface

```bash
# Start the web UI
./wiremock-web
# Open http://localhost:5001
```

**Web UI Features:**
- 🎨 **Modern interface** - Clean, responsive design with Tailwind CSS
- 📁 **Drag & drop** - Upload multiple OpenAPI spec files
- 📊 **Real-time progress** - Live generation status with progress bars
- 📦 **Smart download** - Download all generated files as ZIP
- 🧪 **Live testing** - Test endpoints directly from the interface
- 🔗 **WireMock integration** - Direct connection testing and management
### 🐳 Docker & WireMock Server

```bash
# Start everything (Web UI + WireMock server)
docker-compose up -d

# Access services:
# Web UI: http://localhost:5001
# WireMock: http://localhost:8080
# WireMock Admin: http://localhost:8080/__admin
```

## 🔧 Available Commands

```bash
# Setup
make setup          # Complete project setup
make install        # Install dependencies

# Generation  
make generate       # Generate mappings using CLI
make generate-java  # Generate mappings + Java code

# Development Environment
make dev-hybrid     # Start WireMock in Docker + Web UI locally
make web-dev        # Start web UI locally only

# Full Docker Environment  
make start          # Start all services (Web UI + WireMock)
make stop           # Stop all services
make restart        # Restart all services

# Health & Monitoring
make health         # Check service health
make logs           # View service logs
make status         # Show container status

# Testing & Cleanup
make test           # Test generated endpoints
make clean          # Clean up all containers and files
```
## 📁 Project Structure

```
wiremock-mapping-generator/
├── 🚀 Entry Points
│   ├── wiremock-generator        # CLI tool
│   ├── wiremock-web             # Web UI launcher
│   └── Makefile                 # Build automation
│
├── 📦 Source Code
│   ├── src/core/                # Core generation logic
│   ├── src/cli/                 # CLI utilities  
│   └── src/web/                 # Web application
│       ├── routes/              # API routes
│       ├── services/            # Business logic
│       └── templates/           # Web UI
│
├── 📚 Resources
│   ├── examples/                # Sample OpenAPI specs
│   ├── docs/                   # Documentation
│   └── output/                 # Generated files
│
└── 🧪 Testing
    └── tests/                   # Test structure
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [`README.md`](README.md) | Main project documentation |
| [`QUICKSTART.md`](QUICKSTART.md) | Quick start guide and common commands |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Detailed architecture and project structure |

## 🔄 Recent Updates (v2.0)

### ✨ What's New
- **🎨 Enhanced Web UI** - Modern tabbed interface with live testing
- **🚀 WireMock 3.13.1** - Latest WireMock version with improved performance  
- **🧹 Codebase Cleanup** - Removed 1,400+ lines of redundant code
- **⚡ Performance** - Optimized JavaScript and removed debug logging
- **🔧 Hybrid Development** - Mix Docker and local development modes
- **📱 Responsive Design** - Mobile-friendly interface

### 🗑️ Cleanup Results
- Removed legacy `scripts/` directory
- Consolidated JavaScript files (ui.js → upload.js)
- Removed redundant templates and debug code
- Streamlined project structure
- Enhanced documentation

## 🎯 Generated Output

After running the generator, you'll find:

```
output/
├── mappings/           # WireMock JSON mapping files
│   ├── get_products_mappings.json
│   ├── create_products_mappings.json
│   └── ...
├── __files/           # Response body files  
│   ├── get_products_200_response.json
│   └── ...
└── java/              # Java integration code (optional)
    ├── src/main/java/
    ├── README.md
    └── pom.xml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make test`
5. Submit a pull request

## 📄 License
