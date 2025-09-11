# Multi-Spec WireMock Mapping Generator

**🎯 Goal: Drop any OpenAPI spec (YAML/JSON) file into `/spec` directory → Automatic WireMock mapping and stub generation!**

This project automatically discovers and processes ALL OpenAPI specifications in the `/spec` directory, generating comprehensive WireMock stubs and mappings with zero configuration. Simply place your API specs in the folder and run the generator - everything else is handled automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🌟 Features

- ✅ **Zero Configuration**: Drop OpenAPI specs in `/spec` → automatic processing
- ✅ **Multi-API Support**: Process unlimited APIs simultaneously
- ✅ **Auto-Discovery**: Scans for `*.yaml`, `*.yml`, `*.json` files
- ✅ **Consolidated Mappings**: Groups HTTP methods into single files
- ✅ **Organized Structure**: API-specific folders auto-created
- ✅ **Spec-Compliant Responses**: Uses actual OpenAPI examples
- ✅ **Comprehensive Scenarios**: All status codes (200, 201, 401, 403, 404, 500, 502, 503)
- ✅ **Smart Request Matching**: JSON Path and header-based routing
- ✅ **Docker-Ready**: Easy deployment with Docker Compose
- ✅ **Team-Friendly**: Shareable setup across development teams

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OpenAPI       │    │   Generator     │    │   WireMock      │
│   Specs         │───▶│   Engine        │───▶│   Server        │
│   (spec/)       │    │   (Python)      │    │   (Docker)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ • products.yaml │    │ • Auto Discovery│    │ • HTTP Mocks    │
│ • users.yaml    │    │ • Consolidation │    │ • Admin UI      │
│ • orders.json   │    │ • Validation    │    │ • Health Check  │
│ • *.yaml/*.json │    │ • Generation    │    │ • JSON Matching │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** installed ([Get Docker](https://docs.docker.com/get-docker/))
- **OpenAPI 3.0+** specification files (YAML or JSON)

### 🎯 Three Simple Steps

**1. Drop API Specs**
```bash
# Copy your OpenAPI specifications to the spec directory
cp your-api-spec.yaml spec/
cp another-api.json spec/
cp third-api.yaml spec/
# Add unlimited APIs - all auto-discovered!
```

**2. Generate Mappings**
```bash
# One command processes ALL specs in /spec directory
make generate
```

**3. Start WireMock**
```bash
# Start WireMock with ALL generated mappings
make start
```

### ✅ That's it! Zero configuration needed.

## 📁 Project Structure

```
wiremock-mapping-generator/
├── spec/                           # 🎯 DROP YOUR API SPECS HERE
│   ├── products-api.yaml           # ← Any OpenAPI spec (auto-discovered)
│   ├── users-api.yaml              # ← Another API spec
│   ├── orders-api.json             # ← JSON format supported
│   └── any-name.yaml               # ← Unlimited APIs supported
├── wiremock/                       # 🚀 AUTO-GENERATED OUTPUT
│   ├── mappings/                   # ← Organized by API name
│   │   ├── products/               # ← Auto-created from products-api.yaml
│   │   │   ├── get_products_mappings.json      # All GET operations
│   │   │   ├── create_products_mappings.json   # All POST operations
│   │   │   ├── update_products_mappings.json   # All PUT operations
│   │   │   └── delete_products_mappings.json   # All DELETE operations
│   │   ├── users/                  # ← Auto-created from users-api.yaml
│   │   │   ├── get_users_mappings.json
│   │   │   ├── create_users_mappings.json
│   │   │   └── ...
│   │   └── orders/                 # ← Auto-created from orders-api.json
│   └── __files/                    # ← Response files (realistic data)
│       ├── products/               # ← Spec-compliant responses
│       ├── users/                  # ← Enhanced error responses
│       └── orders/                 # ← Auto-generated for each API
├── scripts/
│   └── multi_spec_wiremock_generator.py    # Core generator engine
├── docker-compose.yml              # Docker configuration
├── Makefile                        # Easy commands
└── .env.example                    # Configuration template
```

## 🛠️ Available Commands

```bash
# Core Commands
make help                    # Show all available commands
make generate               # Generate mappings for all APIs in /spec
make start                  # Start WireMock with generated mappings
make stop                   # Stop WireMock server
make restart                # Restart WireMock server

# Development Commands
make clean                  # Clean generated files
make logs                   # Show WireMock logs
make status                 # Check service status
make test                   # Test generated endpoints
make test-scenarios         # Test all error scenarios

# Validation Commands
make validate-spec          # Validate all OpenAPI specs
make show-mappings          # List generated mapping files
```

## 🎯 How It Works

### 1. **Auto-Discovery**
```bash
✓ Scans /spec for *.yaml, *.yml, *.json files
✓ Extracts API names from filenames or OpenAPI titles
✓ No manual configuration required
```

### 2. **Consolidation**
```bash
✓ Groups HTTP methods: GET → get_api_mappings.json
✓ Multiple scenarios per file (8 status codes each)
✓ Organized folder structure by API name
```

### 3. **Generation**
```bash
✓ Spec-compliant success responses (200, 201)
✓ Professional error responses (401, 403, 404, 500, 502, 503)
✓ Smart request matching with JSON Path patterns
✓ Realistic data using OpenAPI examples
```

## 📋 Generated Content

### Mapping Files Structure
Each API gets consolidated mapping files:
```json
{
  "mappings": [
    {
      "request": {
        "method": "POST",
        "urlPathPattern": "/products",
        "bodyPatterns": [
          {"matchesJsonPath": "$[?(@..* =~ /.*happy_path.*/i)]"}
        ]
      },
      "response": {
        "status": 201,
        "bodyFileName": "products/post_createProduct_201_response.json"
      }
    }
    // ... 7 more scenarios for different status codes
  ]
}
```

### Response Files
Realistic response data matching your OpenAPI specifications:
```json
// Success Response (from OpenAPI examples)
{
  "id": "prod-789",
  "name": "Smart Watch",
  "category": "electronics", 
  "price": 299.99,
  "stock": 50,
  "createdAt": "2024-01-01T12:00:00Z"
}

// Error Response (enhanced professional format)
{
  "errors": [
    {
      "code": "UNAUTHORIZED",
      "message": "Authentication required",
      "traceId": "uuid-trace-id",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## 🧪 Testing Your Mocks

### Access Points
- **API Base**: http://localhost:8080
- **Admin UI**: http://localhost:8080/__admin  
- **Health Check**: http://localhost:8080/__admin/health

### Test Different Scenarios
```bash
# Success scenarios
curl -X GET http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"scenario": "happy_path"}'

# Error scenarios  
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -d '{"scenario": "unauthorized_access"}'

# Query parameter scenarios
curl "http://localhost:8080/products?simulate=server_error"
```

### Request Matching Patterns

| Scenario | Status | Request Pattern |
|----------|--------|----------------|
| Success | 200/201 | `"scenario": "happy_path"` in body |
| Unauthorized | 401 | `"scenario": "unauthorized_access"` in body |
| Forbidden | 403 | `"scenario": "forbidden_request"` in body |
| Not Found | 404 | `?simulate=not_found` query param |
| Server Error | 500 | `?simulate=server_error` query param |
| Bad Gateway | 502 | `?simulate=bad_gateway` query param |
| Service Unavailable | 503 | `?simulate=service_unavailable` query param |

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and customize:
```bash
# WireMock Configuration
WIREMOCK_PORT=8080
WIREMOCK_VERBOSE=true
WIREMOCK_ENABLE_BROWSER_PROXYING=false

# Generator Configuration  
SPEC_DIRECTORY=./spec
OUTPUT_DIRECTORY=./wiremock
```

### API Naming
The generator extracts API names automatically:
- **From filename**: `products-api.yaml` → `products`
- **From OpenAPI title**: Uses `info.title` if filename is generic
- **Sanitization**: Converts spaces and special characters to underscores

Examples:
- `products-api.yaml` → `products`
- `user-management.yaml` → `user_management`  
- `Payment Processing API.json` → `payment_processing_api`

## 🌍 Real-World Use Cases

### Microservices Development
```bash
# Team with 6 microservices
spec/
├── user-service.yaml
├── product-service.yaml
├── order-service.yaml  
├── payment-service.yaml
├── inventory-service.yaml
└── notification-service.yaml

# One command mocks all services
make generate && make start
```

### External API Integration
```bash
# Mock third-party APIs locally
spec/
├── stripe-api.yaml        # Payment provider
├── sendgrid-api.yaml      # Email service  
├── twilio-api.yaml        # SMS service
└── our-api.yaml           # Internal API

# Test without external dependencies
make generate && make start
```

### CI/CD Pipeline Integration
```bash
# In your CI pipeline
- name: Setup API Mocks
  run: |
    make generate
    make start
    make test-scenarios
```

## 🤝 Contributing

We welcome contributions! This project is open source under the MIT License.

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/wiremock-mapping-generator.git
cd wiremock-mapping-generator

# Add your OpenAPI specs
cp your-spec.yaml spec/

# Test the generator
make generate
make start
make test
```

### Areas for Contribution
- ✅ Support for more OpenAPI features
- ✅ Additional response formats
- ✅ Enhanced error scenarios
- ✅ Performance improvements
- ✅ Documentation improvements
- ✅ Integration examples

## 📚 Advanced Usage

### Custom Docker Setup
```bash
# Use custom WireMock version
docker-compose run --rm wiremock-generator sh -c \
  "python3 /scripts/multi_spec_wiremock_generator.py /spec /output"

# Run generator directly
python scripts/multi_spec_wiremock_generator.py spec wiremock
```

### Integration with Existing Projects
```bash
# Add to existing Docker Compose
services:
  wiremock:
    image: wiremock/wiremock:3.3.1
    ports:
      - "8080:8080"
    volumes:
      - ./wiremock:/home/wiremock
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: No mappings generated
```bash
# Check spec files are valid
make validate-spec

# Check file permissions
ls -la spec/
```

**Issue**: WireMock not starting  
```bash
# Check Docker is running
docker ps

# Check logs
make logs
```

**Issue**: Invalid OpenAPI spec
```bash
# Validate your spec online
# https://editor.swagger.io/

# Check generator output
make generate 2>&1 | grep ERROR
```

### Getting Help
- 📖 **Documentation**: Check this README
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Open an issue with enhancement label
- 🤝 **Community**: Contribute via Pull Requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WireMock](http://wiremock.org/) - Powerful HTTP mocking framework
- [OpenAPI](https://swagger.io/specification/) - API specification standard
- [Docker](https://www.docker.com/) - Containerization platform

---

**⭐ Star this repository if it helps your project!**

**🤝 Contributions welcome - Help make this tool even better!**
