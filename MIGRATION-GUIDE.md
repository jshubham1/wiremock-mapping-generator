# Project Structure Migration Guide

This document outlines the migration from the old flat structure to the new organized structure.

## Migration Overview

### Old Structure (Flat)
```
wiremock-mapping-generator/
├── scripts/
│   ├── multi_spec_wiremock_generator.py
│   ├── demo-web-ui.sh
│   ├── start-web-*.sh
│   └── ...
├── web-app/
│   ├── app.py
│   ├── templates/
│   └── ...
├── spec/
├── wiremock/
├── Makefile
└── ...
```

### New Structure (Organized)
```
wiremock-mapping-generator/
├── 🚀 Entry Points
│   ├── wiremock-generator          # NEW: CLI entry point
│   ├── wiremock-web               # NEW: Web UI entry point
│   └── Makefile                   # UPDATED: Enhanced commands
│
├── 📦 Source Code
│   ├── src/
│   │   ├── core/                  # MOVED: From scripts/
│   │   ├── cli/                   # MOVED: From scripts/
│   │   └── web/                   # MOVED: From web-app/
│   │       ├── routes/            # NEW: Separated routes
│   │       └── services/          # NEW: Business logic
│
├── 📚 Documentation & Examples
│   ├── docs/                     # NEW: Centralized docs
│   └── examples/                 # MOVED: From spec/
│
├── 🧪 Testing
│   └── tests/                    # NEW: Organized testing
│
├── 🚢 Deployment
│   └── deploy/                   # NEW: Deployment configs
│
└── 📁 Output
    └── output/                   # NEW: Clean output directory
```

## Key Changes

### 1. Entry Points
- **NEW**: `./wiremock-generator` - Unified CLI entry point
- **NEW**: `./wiremock-web` - Web UI entry point
- **BENEFIT**: Clear, executable entry points at project root

### 2. Source Organization
- **MOVED**: `scripts/multi_spec_wiremock_generator.py` → `src/core/`
- **MOVED**: CLI scripts → `src/cli/`
- **MOVED**: `web-app/` → `src/web/`
- **NEW**: Separated routes and services in web app
- **BENEFIT**: Clear separation of concerns

### 3. Examples & Documentation
- **MOVED**: `spec/` → `examples/`
- **NEW**: `docs/` directory for documentation
- **BENEFIT**: Better organization of learning materials

### 4. Output Structure
- **NEW**: `output/` directory for all generated files
- **REMOVED**: `generated/` and `wiremock/` directories
- **BENEFIT**: Clean, predictable output location

### 5. Testing Structure
- **NEW**: `tests/` with organized subdirectories
- **NEW**: `fixtures/` for test data
- **BENEFIT**: Comprehensive testing support

## Migration Commands

### Automated Setup
```bash
# The new structure is already in place
# Just run setup to install dependencies
make setup
```

### Manual Cleanup (Optional)
```bash
# Remove old directories if needed
rm -rf scripts/ web-app/ spec/ generated/ wiremock/

# Clean up old virtual environments
rm -rf venv/ web-app/venv/
```

## Updated Commands

### CLI Usage
```bash
# OLD
python3 scripts/multi_spec_wiremock_generator.py /spec /output

# NEW
./wiremock-generator --spec-dir ./examples --output-dir ./output
```

### Web UI
```bash
# OLD
cd web-app && python app.py

# NEW
./wiremock-web
# OR
make web-dev
```

### Make Commands
```bash
# NEW setup commands
make setup          # Complete project setup
make install        # Install dependencies
make dev-setup      # Development environment

# UPDATED generation commands
make generate       # Uses new CLI entry point
make generate-java  # Uses new CLI entry point

# UPDATED web commands
make web-dev        # Uses new entry point
```

## Benefits of New Structure

### 1. Professional Organization
- Clear separation between core logic, CLI, and web components
- Standard Python package structure with proper `__init__.py` files
- Intuitive directory names and hierarchy

### 2. Better Development Experience
- Dedicated entry points reduce confusion
- Modular architecture makes testing easier
- Clear import paths improve code maintainability

### 3. Deployment Ready
- Organized deployment configurations
- Docker support with proper structure
- Kubernetes and Helm templates ready

### 4. Scalability
- Easy to add new features in appropriate directories
- Testing infrastructure supports growth
- Documentation structure scales with project

### 5. Industry Standards
- Follows Python packaging best practices
- Flask application factory pattern
- Clean architecture principles

## Import Changes

### Old Imports
```python
# OLD
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from multi_spec_wiremock_generator import MultiSpecWireMockGenerator
```

### New Imports
```python
# NEW
from src.core.multi_spec_wiremock_generator import MultiSpecWireMockGenerator
```

## Configuration Updates

### Makefile
- Enhanced with setup commands
- Updated paths to use new entry points
- Better command organization

### Docker Compose
- Updated to work with new structure
- Proper volume mappings for new directories

### Requirements
- Consolidated into single `requirements.txt`
- Added development dependencies
- Better dependency organization

## Testing the Migration

### Verify CLI Works
```bash
./wiremock-generator --spec-dir ./examples --output-dir ./output --verbose
```

### Verify Web UI Works
```bash
./wiremock-web
# Open http://localhost:5001
```

### Verify Make Commands
```bash
make setup
make generate
make web-dev
```

## Rollback Plan

If needed, the old structure can be restored from git history:
```bash
# Check git history for old structure
git log --oneline
git checkout <commit-before-migration>
```

## Next Steps

1. **Test thoroughly**: Verify all functionality works
2. **Update documentation**: Ensure all docs reflect new structure
3. **Team training**: Ensure team understands new structure
4. **CI/CD updates**: Update build scripts for new structure
5. **Cleanup**: Remove old files after verification
