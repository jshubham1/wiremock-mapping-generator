# Project Structure Documentation

## Overview

This document provides a comprehensive overview of the new project structure for the WireMock Mapping Generator.

## Directory Structure

### Root Level Files

| File | Purpose | Description |
|------|---------|-------------|
| `wiremock-generator` | CLI Entry Point | Executable script for command-line usage |
| `wiremock-web` | Web UI Entry Point | Executable script for web interface |
| `Makefile` | Build Automation | Enhanced makefile with 20+ commands |
| `requirements.txt` | Dependencies | Python package requirements |
| `docker-compose.yml` | Container Orchestration | Multi-service Docker setup |
| `README.md` | Documentation | Main project documentation |
| `.gitignore` | VCS Configuration | Git ignore rules for new structure |

### Source Code (`src/`)

#### Core Logic (`src/core/`)
Contains the fundamental business logic for WireMock generation.

| File | Purpose |
|------|---------|
| `__init__.py` | Package initialization with exports |
| `multi_spec_wiremock_generator.py` | Main generator classes |

**Classes:**
- `MultiSpecWireMockGenerator`: Processes multiple OpenAPI specs
- `JavaWireMockGenerator`: Generates Java integration code

**Recent Improvements:**
- Enhanced error handling and logging
- Support for WireMock 3.13.1
- Optimized mapping generation performance

#### CLI Tools (`src/cli/`)
Command-line interface utilities and scripts.

| File | Purpose |
|------|---------|
| `__init__.py` | Package initialization |

**Note:** Legacy scripts have been cleaned up and consolidated. The main CLI functionality is now available through the root-level `wiremock-generator` executable.

#### Web Application (`src/web/`)
Modern Flask web application with clean architecture.

| Directory/File | Purpose |
|----------------|---------|
| `__init__.py` | Package initialization |
| `app.py` | Flask application factory |
| `routes/` | HTTP route handlers |
| `services/` | Business logic services |
| `templates/` | HTML templates |
| `static/` | Static assets (CSS, JS, images) |
| `uploads/` | Temporary upload storage |
| `temp/` | Temporary generation files |

##### Routes (`src/web/routes/`)
| File | Purpose |
|------|---------|
| `main_routes.py` | Main page and health endpoints |
| `api_routes.py` | REST API endpoints for file operations |

##### Services (`src/web/services/`)
| File | Purpose |
|------|---------|
| `file_service.py` | File upload/download/cleanup operations |
| `generation_service.py` | WireMock mapping generation logic |

### Examples (`examples/`)
Sample OpenAPI specifications for testing and demonstration.

| File | Purpose |
|------|---------|
| `open-api-spec.yaml` | Generic OpenAPI example |
| `products-api.yaml` | Products API specification |
| `users-api.yaml` | Users API specification |

### Documentation (`docs/`)
Centralized documentation and resources.

| File | Purpose |
|------|---------|
| `README.md` | Detailed project documentation |
| `LICENSE` | MIT license file |

### Testing (`tests/`)
Comprehensive testing structure.

| Directory | Purpose |
|-----------|---------|
| `test_core/` | Tests for core generation logic |
| `test_cli/` | Tests for CLI functionality |
| `test_web/` | Tests for web application |
| `fixtures/` | Test data and expected outputs |

### Deployment (`deploy/`)
Production deployment configurations.

| Directory | Purpose |
|-----------|---------|
| `docker/` | Docker configurations |
| `k8s/` | Kubernetes manifests |
| `helm/` | Helm chart templates |

### Output (`output/`)
Generated files from the mapping generation process.

| Directory | Purpose |
|-----------|---------|
| `mappings/` | WireMock JSON mapping files |
| `stubs/` | Response files (__files) |
| `java/` | Generated Java integration code |

## Recent Improvements (v2.0)

### 🧹 Codebase Cleanup
As part of the recent optimization effort, the following improvements were made:

#### Removed Components
- **Legacy Scripts**: Removed redundant scripts from `scripts/` directory
- **Duplicate Templates**: Consolidated `index.html` and kept `index_new.html` as the main template
- **Redundant JavaScript**: Merged `ui.js` functionality into `upload.js`
- **Debug Code**: Removed 20+ console.log statements for production optimization
- **Empty Files**: Cleaned up placeholder files and documentation

#### Enhanced Components
- **Modern Web UI**: Tabbed modal interface with drag & drop functionality
- **Live Testing**: Integrated endpoint testing within the web interface
- **Session Management**: UUID-based session handling for multi-user support
- **WireMock Integration**: Real-time health monitoring and admin access
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS

#### Performance Improvements
- **Reduced Bundle Size**: Consolidated JavaScript files (~1,400 lines removed)
- **Optimized Loading**: Removed unnecessary console logging
- **Clean Architecture**: Improved separation of concerns
- **Docker Optimization**: Updated to WireMock 3.13.1 with better performance

## Architecture Patterns

### 1. Application Factory Pattern
The web application uses Flask's application factory pattern for better testability and configuration management.

```python
# src/web/app.py
def create_app():
    app = Flask(__name__)
    # Configuration
    # Blueprint registration
    return app
```

### 2. Blueprint Organization
Routes are organized into logical blueprints:
- `main_routes`: Main pages and health checks
- `api_routes`: REST API endpoints

### 3. Service Layer
Business logic is separated into service classes:
- `FileService`: File operations
- `GenerationService`: Mapping generation

### 4. Clean Separation of Concerns
- **Core**: Pure business logic, no dependencies on web or CLI
- **CLI**: Command-line interface, imports from core
- **Web**: Web interface, imports from core through services

## Entry Points

### CLI Entry Point (`wiremock-generator`)
```bash
# Direct execution
./wiremock-generator --spec-dir ./examples --output-dir ./output

# With options
./wiremock-generator --spec-dir ./examples --output-dir ./output --include-java --verbose
```

### Web Entry Point (`wiremock-web`)
```bash
# Start web server
./wiremock-web

# Available at http://localhost:5001
```

## Configuration Management

### Environment Variables
The application supports configuration through environment variables:
- `FLASK_ENV`: Development/production mode
- `UPLOAD_FOLDER`: Custom upload directory
- `TEMP_FOLDER`: Custom temporary directory

### Application Configuration
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = './src/web/uploads'
app.config['TEMP_FOLDER'] = './src/web/temp'
```

## Import Strategy

### Core Imports
```python
from src.core.multi_spec_wiremock_generator import MultiSpecWireMockGenerator
```

### Web Service Imports
```python
from src.web.services.file_service import FileService
from src.web.services.generation_service import GenerationService
```

### Route Imports
```python
from src.web.routes.main_routes import create_main_blueprint
from src.web.routes.api_routes import create_api_blueprint
```

## Development Workflow

### 1. Setup
```bash
make setup          # Install dependencies and setup
```

### 2. Development
```bash
make dev-setup      # Setup development environment
source venv/bin/activate  # Optional: activate virtual environment
```

### 3. Testing
```bash
make test           # Run all tests
```

### 4. Local Development
```bash
make web-dev        # Start web UI locally
./wiremock-generator --help  # Test CLI
```

## Deployment Options

### Local Development
```bash
./wiremock-web      # Direct Python execution
```

### Docker Development
```bash
make web-ui         # Docker-based web UI
```

### Production
```bash
docker-compose up -d  # Full stack deployment
```

## Security Considerations

### File Upload Security
- Filename sanitization with `secure_filename()`
- File type validation (YAML/JSON only)
- Size limits (16MB maximum)
- Session-based isolation

### Session Management
- UUID-based session IDs
- Automatic cleanup after 1 hour
- Isolated temporary directories per session

### Error Handling
- Comprehensive exception handling
- Secure error messages (no sensitive data)
- Proper HTTP status codes

## Performance Considerations

### File Handling
- Streaming file uploads for large files
- Efficient ZIP creation for downloads
- Background cleanup of old sessions

### Memory Management
- Session-based temporary storage
- Automatic cleanup mechanisms
- Configurable upload limits

### Scalability
- Stateless application design
- External storage ready (S3, etc.)
- Horizontal scaling support

## Monitoring and Observability

### Health Checks
```
GET /health
```
Returns service status and version information.

### Logging
- Structured logging for debugging
- Error tracking for production monitoring
- Performance metrics collection ready

### Metrics
- Session creation/cleanup statistics
- Generation success/failure rates
- Response time tracking

## Best Practices

### Code Organization
1. Keep core logic framework-agnostic
2. Use dependency injection for services
3. Separate business logic from presentation
4. Maintain clear import hierarchies

### Testing
1. Unit tests for core logic
2. Integration tests for services
3. End-to-end tests for web flows
4. Fixture-based test data

### Documentation
1. Inline code documentation
2. API documentation for web endpoints
3. Usage examples in README
4. Architecture decision records

### Security
1. Input validation at all entry points
2. Secure file handling practices
3. Regular dependency updates
4. Security-focused code reviews

This structure provides a solid foundation for continued development and maintenance of the WireMock Mapping Generator project.
