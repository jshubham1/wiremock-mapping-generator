# WireMock Mapping Generator

A comprehensive tool for generating WireMock mappings and Java integration code from OpenAPI specifications. Features both CLI and modern web interface with improved project structure.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker (for WireMock service)
- Docker Compose (optional, for full stack)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd wiremock-mapping-generator

# Setup the project
make setup
```

## 📖 Usage

### 🖥️ CLI Usage

Generate mappings for all specs in a directory:

```bash
# Generate only JSON mappings
./wiremock-generator --spec-dir ./examples --output-dir ./output

# Generate mappings + Java code
./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
```

### 🌐 Web UI

The modern web interface provides drag-and-drop functionality:

```bash
# Start web UI (development mode)
./wiremock-web

# Or using Docker
make web-ui

# Interactive demo
make demo
```

**Features:**
- ✨ Drag-and-drop file upload
- 📁 Multi-file processing
- ☕ Optional Java code generation
- 📦 ZIP download of generated files
- 📱 Fully responsive design
- 🔒 Session-based isolation

### 🔧 Make Commands

```bash
# Setup
make setup          # Complete project setup
make install        # Install dependencies only
make dev-setup      # Setup development environment

# Generation (CLI)
make generate       # Generate mappings only
make generate-java  # Generate mappings + Java code

# Web Interface
make web-ui         # Start web UI (Docker)
make web-dev        # Start web UI (local Python)
make demo           # Interactive demo

# WireMock Service
make start          # Start WireMock with generated mappings
make stop           # Stop all services
make restart        # Restart services

# Testing & Validation
make test           # Test generated endpoints
make test-scenarios # Test error scenarios
make full-cycle     # Complete workflow test

# Utilities
make clean          # Clean generated files
make show-mappings  # List generated mappings
make validate-spec  # Validate OpenAPI specs
make help           # Show all commands
```

## 📁 Project Structure

```
wiremock-mapping-generator/
├── 🚀 Entry Points
│   ├── wiremock-generator          # CLI entry point
│   ├── wiremock-web               # Web UI entry point
│   └── Makefile                   # Build automation
│
├── 📦 Source Code
│   ├── src/
│   │   ├── core/                  # Core generation logic
│   │   │   ├── __init__.py
│   │   │   └── multi_spec_wiremock_generator.py
│   │   ├── cli/                   # CLI scripts and tools
│   │   │   ├── __init__.py
│   │   │   ├── demo-web-ui.sh
│   │   │   ├── start-web-dev.sh
│   │   │   ├── start-web-ui.sh
│   │   │   ├── quick-start.sh
│   │   │   └── test-scenarios.sh
│   │   └── web/                   # Web application
│   │       ├── __init__.py
│   │       ├── app.py             # Flask application factory
│   │       ├── routes/            # Web routes
│   │       │   ├── main_routes.py
│   │       │   └── api_routes.py
│   │       ├── services/          # Business logic
│   │       │   ├── file_service.py
│   │       │   └── generation_service.py
│   │       ├── templates/         # HTML templates
│   │       └── static/            # Static assets
│   │
├── 🔧 Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── docker-compose.yml         # Service orchestration
│   └── .gitignore                # VCS ignore rules
│
├── 📚 Documentation & Examples
│   ├── docs/                     # Documentation
│   │   ├── README.md
│   │   └── LICENSE
│   └── examples/                 # Example OpenAPI specs
│       ├── open-api-spec.yaml
│       ├── products-api.yaml
│       └── users-api.yaml
│
├── 🧪 Testing
│   ├── tests/
│   │   ├── test_core/            # Core logic tests
│   │   ├── test_cli/             # CLI tests
│   │   ├── test_web/             # Web application tests
│   │   └── fixtures/             # Test data
│   │       ├── sample-specs/
│   │       └── expected-outputs/
│
├── 🚢 Deployment
│   ├── deploy/
│   │   ├── docker/               # Docker configurations
│   │   │   └── docker-compose.yml
│   │   ├── k8s/                  # Kubernetes manifests
│   │   └── helm/                 # Helm charts
│   │       └── wiremock-generator/
│
└── 📁 Output
    └── output/                   # Generated files
        ├── mappings/             # WireMock JSON mappings
        ├── stubs/               # Response files (__files)
        └── java/                # Java integration code
```

## 🎯 Features

### Core Capabilities
- 🔄 **Multi-Spec Processing**: Process multiple OpenAPI specifications simultaneously
- 📊 **Comprehensive Mapping**: Generate complete WireMock mappings for all HTTP methods
- ☕ **Java Integration**: Generate Spring Boot integration code with test utilities
- 🎯 **Error Scenarios**: Support for 4xx and 5xx error response mappings
- 📱 **Response Files**: Generate realistic response data from schema examples

### Web Interface
- 🖱️ **Drag & Drop**: Intuitive file upload with visual feedback
- 📁 **Multi-File Support**: Process multiple API specifications at once
- ⚡ **Real-Time Progress**: Live updates during generation process
- 📦 **ZIP Downloads**: Convenient packaging of generated files
- 🔒 **Session Isolation**: Secure, isolated sessions with auto-cleanup
- 📱 **Responsive Design**: Works perfectly on desktop and mobile

### CLI Tools
- 🚀 **Fast Generation**: Optimized command-line interface for automation
- 📝 **Verbose Logging**: Detailed output for debugging and monitoring
- 🔧 **Flexible Options**: Configurable output directories and generation options
- 🎯 **Batch Processing**: Process entire directories of specifications

## 🔧 Development

### Setting up Development Environment

```bash
# Setup development environment
make dev-setup

# Activate virtual environment (optional)
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
make test
```

### Project Architecture

The project follows a clean architecture pattern:

- **`src/core/`**: Domain logic for WireMock generation
- **`src/cli/`**: Command-line interface and scripts
- **`src/web/`**: Web application with Flask
  - **`routes/`**: HTTP route handlers
  - **`services/`**: Business logic services
  - **`static/`**: Frontend assets
  - **`templates/`**: HTML templates

## 📋 Requirements

### Python Dependencies
- `PyYAML>=6.0` - YAML processing
- `Flask>=3.1.0` - Web framework
- `Werkzeug>=3.0.0` - WSGI utilities
- `requests>=2.28.0` - HTTP client

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=22.0.0` - Code formatting
- `flake8>=5.0.0` - Linting

## 🐳 Docker Support

### Development
```bash
# Start web UI with Docker
make web-ui

# Start full stack
make start-web
```

### Production
```bash
# Build production image
docker build -t wiremock-generator .

# Run with docker-compose
docker-compose up -d
```

## 📖 API Documentation

### CLI Options
```bash
./wiremock-generator --help
```

### Web API Endpoints
- `GET /` - Main interface
- `POST /api/upload` - File upload
- `POST /api/generate` - Generate mappings
- `GET /api/download/<session_id>` - Download ZIP
- `GET /health` - Health check

## 🆕 What's New in This Version

### Improved Project Structure
- **Organized Source Code**: Clear separation between core, CLI, and web components
- **Clean Entry Points**: Dedicated executables for CLI (`wiremock-generator`) and web (`wiremock-web`)
- **Modular Design**: Services and routes properly separated for maintainability
- **Better Documentation**: Comprehensive docs with clear examples

### Enhanced Developer Experience
- **Setup Automation**: `make setup` for one-command installation
- **Development Mode**: Local development with `make dev-setup`
- **Comprehensive Testing**: Organized test structure with fixtures
- **Modern Python**: Application factory pattern with Flask blueprints

### Production Ready
- **Docker Support**: Multi-stage builds with health checks
- **Deployment Configs**: Kubernetes and Helm chart templates
- **Session Management**: UUID-based sessions with auto-cleanup
- **Error Handling**: Comprehensive error handling and logging

## 🤝 Support

For issues, questions, or contributions:

1. Check existing issues
2. Create a new issue with detailed description
3. Include example specifications and expected output
4. For urgent issues, include logs and environment details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.
