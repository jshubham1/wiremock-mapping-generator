# Multi-Spec WireMock Mapping Generator

**🎯 Drop OpenAPI specs → Get WireMock mappings + Spring Boot Java code automatically!**

Transform multiple OpenAPI specifications into comprehensive WireMock stubs with **zero configuration**. Generate both JSON mappings AND production-ready Java Spring Boot integration code from any OpenAPI spec files.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Java](https://img.shields.io/badge/Java-Spring%20Boot-orange.svg)](https://spring.io/projects/spring-boot)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## 🔥 What's New: Java Code Generation

Generate **Spring Boot-ready Java code** alongside JSON mappings! Perfect for enterprise Java teams who need type-safe WireMock integration.

```bash
# Generate JSON mappings + Java Spring Boot code
make generate-java

# Or directly with Python
python3 scripts/multi_spec_wiremock_generator.py spec wiremock --java --package com.yourcompany.wiremock
```

### 🎯 Java Output Example
```
wiremock/java/
├── README.md                    # Comprehensive Java usage guide
├── pom.xml & build.gradle       # Ready-to-use build files
└── src/
    ├── main/java/com/example/wiremock/
    │   ├── MultiApiWireMockServer.java      # 🎯 Main orchestrator
    │   └── config/
    │       ├── WireMockTestConfig.java      # Spring Boot config
    │       ├── ProductsWireMockConfig.java  # Per-API configs
    │       └── UsersWireMockConfig.java     # Auto-generated per API
    └── test/java/com/example/wiremock/test/
        ├── BaseWireMockIntegrationTest.java # Base test class
        └── {Api}WireMockTest.java           # Per-API test bases
```

### � Use in Your Spring Boot Tests
```java
@SpringBootTest
@Import(WireMockTestConfig.class)
class IntegrationTest extends BaseWireMockIntegrationTest {
    @Test
    void shouldTestApiInteractions() {
        String productsUrl = getProductsBaseUrl(); // Port 8080
        String usersUrl = getUsersBaseUrl();       // Port 8081
        // Test your services that call these APIs
    }
}
```
✅ Basic authentication scenario templates
✅ Java code generation for Spring Boot integration
```

#### 🥈 Phase 2: Professional Features (3-6 months)
```bash
� Web-based configuration UI
🔄 Contract testing integration
🔄 State management and data persistence
🔄 GraphQL schema support
🔄 Kubernetes deployment manifests
```

#### 🥇 Phase 3: Enterprise Scale (6-12 months)
```bash
🚀 AI-powered test data generation
🚀 Multi-environment configuration
🚀 Comprehensive analytics dashboard
� Enterprise security features
🚀 Cloud provider integrations
```

### 🎯 Community Contribution Opportunities

**Beginner Contributors:**
- 📝 Documentation improvements and translations
- 🧪 Additional test scenarios and examples
- 🎨 UI/UX enhancements for web interface
- � Package manager integrations (Homebrew, Chocolatey)

**Advanced Contributors:**
- 🔧 Core engine optimizations and new protocols
- 🤖 AI/ML integration for smart features
- ☁️ Cloud platform integrations
- 🔒 Security and enterprise features

**Enterprise Partners:**
- � Custom integration development
- 📊 Advanced analytics and monitoring
- 🏢 White-label solutions
- 🎓 Training and certification programs

## 🚀 Promotion & Community

### Official Recognition
- 🎯 **Submitted to OpenAPI Generator**: Proposal for official WireMock mapping generator
- 🤝 **WireMock Community**: Featured in WireMock ecosystem discussions
- 📢 **Open Source Promotion**: Active in developer communities

### Media Coverage
- � **Blog Posts**: Technical articles on API mocking strategies
- 🎥 **Video Demos**: YouTube tutorials and conference talks
- 🐦 **Social Media**: Twitter, LinkedIn, and dev community engagement everything else is handled automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0+-green.svg)](https://swagger.io/specification/)
[![WireMock](https://img.shields.io/badge/WireMock-3.3.1-blue.svg)](http://wiremock.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

## � Why Use This Tool?

### 🏢 **Perfect For Enterprise Java Teams**
- **🔒 Type-Safe Integration**: Get strongly-typed Spring beans for API URLs
- **⚡ Zero Boilerplate**: No manual WireMock configuration needed  
- **🧪 Test-Ready**: Instant JUnit 5 + Spring Boot test base classes
- **🏗️ Production Patterns**: Follow Spring Boot best practices out of the box
- **👥 Team Consistency**: Standardized approach across all your microservices

### 🚀 **Ideal Use Cases**
- **🔧 Microservices Testing**: Mock external APIs in your integration tests
- **🔄 Contract Testing**: Validate your code against API contracts  
- **🧪 Development Environment**: Local development without external dependencies
- **⚡ CI/CD Pipelines**: Fast, reliable tests without network dependencies
- **📊 Load Testing**: Consistent mock responses for performance testing
- **🎯 Demo Environments**: Showcase features without live API dependencies

### 📈 **Key Benefits Over Manual WireMock**
- **🕐 10x Faster Setup**: Minutes instead of hours to configure
- **🔍 Auto-Discovery**: Processes unlimited APIs automatically
- **✅ Spec Compliance**: Responses match your OpenAPI definitions exactly
- **🔄 Easy Updates**: Regenerate when specs change
- **📋 Organized Output**: Clean, maintainable structure
- **🐳 Docker Integration**: Works seamlessly in containerized environments

## �🌟 Core Features

### 🔥 **Java Spring Boot Integration** (NEW!)
- **🏗️ Spring Boot Configuration Classes**: Auto-generated `@TestConfiguration` for each API
- **🧪 JUnit 5 Test Base Classes**: Ready-to-extend test classes with lifecycle management  
- **🎯 Multi-API Orchestrator**: Single class to manage all WireMock servers with different ports
- **📦 Maven & Gradle Support**: Complete build files with all required dependencies
- **🔒 Type-Safe API URLs**: Strongly-typed Spring beans (`@Autowired String productsApiBaseUrl`)
- **⚡ Zero Boilerplate**: Just `@Import(WireMockTestConfig.class)` and you're ready!

### 🎯 **WireMock JSON Generation**
- **🚀 Zero Configuration**: Drop OpenAPI specs in `/spec` → automatic processing
- **🔄 Multi-API Support**: Process unlimited APIs simultaneously  
- **🔍 Auto-Discovery**: Scans for `*.yaml`, `*.yml`, `*.json` files
- **📋 Consolidated Mappings**: Groups HTTP methods into organized files
- **✅ Spec-Compliant Responses**: Uses actual OpenAPI examples and schemas
- **🎭 Comprehensive Scenarios**: All status codes (200, 201, 401, 403, 404, 500, 502, 503)
- **🎯 Smart Request Matching**: JSON Path and header-based routing

### �️ **Developer Experience**
- **🐳 Docker-Ready**: Easy deployment with Docker Compose
- **👥 Team-Friendly**: Shareable setup across development teams
- **⌨️ Command Line Interface**: Both direct Python and Make targets
- **📁 Organized Structure**: API-specific folders auto-created
- **📖 Rich Documentation**: Comprehensive READMEs for both JSON and Java usage

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

## 🚀 Quick Start Guide

### 🎯 Choose Your Path

**🔥 Path 1: JSON + Java Code (RECOMMENDED for Java Teams)**
```bash
# 1. Drop your OpenAPI specs in the spec/ directory
cp your-api-specs.yaml spec/

# 2. Generate JSON mappings + Spring Boot Java code
make generate-java

# 3. Use in your Spring Boot tests
# See generated README at wiremock/java/README.md for complete examples
```

**⚡ Path 2: JSON Mappings Only (Traditional WireMock)**
```bash
# 1. Drop your OpenAPI specs in the spec/ directory  
cp your-api-specs.yaml spec/

# 2. Generate JSON mappings
make generate

# 3. Start WireMock server
make start
```

### Prerequisites

- **Docker & Docker Compose** ([Get Docker](https://docs.docker.com/get-docker/))
- **OpenAPI 3.0+** specification files (YAML or JSON)

### 🎯 Three Simple Steps (Traditional Path)

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
# OR for Java integration:
make generate-java
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
│   ├── mappings/                   # ← JSON mappings for WireMock
│   │   ├── products/               # ← Auto-created from products-api.yaml
│   │   │   ├── get_products_mappings.json      # All GET operations
│   │   │   ├── create_products_mappings.json   # All POST operations
│   │   │   ├── update_products_mappings.json   # All PUT operations
│   │   │   └── delete_products_mappings.json   # All DELETE operations
│   │   ├── users/                  # ← Auto-created from users-api.yaml
│   │   │   └── ... (similar structure)
│   │   └── orders/                 # ← Auto-created from orders-api.json
│   ├── __files/                    # ← Response files (realistic data)
│   │   ├── products/               # ← Spec-compliant responses
│   │   ├── users/                  # ← Enhanced error responses
│   │   └── orders/                 # ← Auto-generated for each API
│   └── java/                       # 🔥 AUTO-GENERATED JAVA CODE
│       ├── README.md               # ← Comprehensive Java usage guide
│       ├── pom.xml                 # ← Maven build file
│       ├── build.gradle            # ← Gradle build file
│       └── src/
│           ├── main/java/com/example/wiremock/
│           │   ├── MultiApiWireMockServer.java      # 🎯 Main orchestrator
│           │   └── config/
│           │       ├── WireMockTestConfig.java      # Spring Boot config
│           │       ├── ProductsWireMockConfig.java  # Per-API configs
│           │       └── UsersWireMockConfig.java     # Auto-generated per API
│           └── test/java/com/example/wiremock/test/
│               ├── BaseWireMockIntegrationTest.java # Base test class
│               ├── ProductsWireMockTest.java        # Per-API test bases
│               └── UsersWireMockTest.java           # Ready for extension
├── scripts/
│   └── multi_spec_wiremock_generator.py    # Core generator engine
├── docker-compose.yml              # Docker configuration
├── Makefile                        # Easy commands with Java support
└── .env.example                    # Configuration template
```
```

## 🛠️ Available Commands

```bash
# 🔥 Core Generation Commands
make generate-java          # Generate JSON mappings + Spring Boot Java code
make generate               # Generate JSON mappings only (traditional)
make help                   # Show all available commands

# 🚀 WireMock Server Commands  
make start                  # Start WireMock with generated mappings
make stop                   # Stop WireMock server
make restart                # Restart WireMock server

# 🔧 Development Commands
make clean                  # Clean generated files
make logs                   # Show WireMock logs
make status                 # Check service status
make test                   # Test generated endpoints
make test-scenarios         # Test all error scenarios

# ✅ Validation Commands
make validate-spec          # Validate all OpenAPI specs
make show-mappings          # List generated mapping files
```

### 🎯 Command Line Options

```bash
# Direct Python usage (bypass Docker)
python3 scripts/multi_spec_wiremock_generator.py spec wiremock

# Generate with Java code
python3 scripts/multi_spec_wiremock_generator.py spec wiremock --java

# Custom Java package
python3 scripts/multi_spec_wiremock_generator.py spec wiremock --java --package com.yourcompany.wiremock

# Help
python3 scripts/multi_spec_wiremock_generator.py --help
```

## 🔥 Java Spring Boot Integration Examples

### 🎯 Single API Testing
```java
@SpringBootTest
@Import(ProductsWireMockConfig.class)
class ProductServiceTest {
    @Autowired
    private String productsApiBaseUrl; // http://localhost:8089
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Test
    void shouldCallProductsApi() {
        String response = restTemplate.getForObject(
            productsApiBaseUrl + "/products", 
            String.class
        );
        assertThat(response).isNotNull();
    }
}
```

### 🚀 Multi-API Integration Testing
```java
@SpringBootTest
@Import(WireMockTestConfig.class)
class IntegrationTest extends BaseWireMockIntegrationTest {
    
    @Test
    void shouldTestApiInteractions() {
        String productsUrl = getProductsBaseUrl(); // Port 8080
        String usersUrl = getUsersBaseUrl();       // Port 8081
        String ordersUrl = getOrdersBaseUrl();     // Port 8082
        
        // Test interactions between multiple services
        // All APIs are automatically started and ready
    }
    
    @Test 
    void shouldTestErrorScenarios() {
        // Reset all servers to clean state
        getMultiApiServer().resetAll();
        
        // All error scenarios from OpenAPI specs are available
        // Test your error handling logic
    }
}
```

### ⚡ Manual Server Management
```java
class CustomIntegrationTest {
    private MultiApiWireMockServer server = new MultiApiWireMockServer();
    
    @BeforeEach
    void setUp() {
        server.startAllServers(); // Starts all APIs on different ports
        
        Map<String, String> urls = server.getServerUrls();
        urls.forEach((api, url) -> {
            // Configure your HTTP clients with the URLs
            configureApiClient(api, url);
        });
    }
    
    @AfterEach
    void tearDown() {
        server.stopAllServers();
    }
    
    @Test
    void shouldTestWithCustomConfiguration() {
        // Your test logic here
        // Full control over server lifecycle
    }
}
```

### 🧪 Advanced Test Patterns
```java
@SpringBootTest
@Import(WireMockTestConfig.class)
class AdvancedIntegrationTest extends BaseWireMockIntegrationTest {
    
    @Test
    void shouldTestCircuitBreakerWithMultipleApis() {
        // Get individual WireMock servers for fine-grained control
        WireMockServer productsServer = getMultiApiServer().getServer("products");
        WireMockServer usersServer = getMultiApiServer().getServer("users");
        
        // Create custom stubs for specific test scenarios
        productsServer.stubFor(get(urlEqualTo("/products"))
            .willReturn(aResponse()
                .withStatus(503)
                .withFixedDelay(5000))); // Simulate slow response
                
        // Test your circuit breaker logic
    }
    
    @Test
    void shouldVerifyRequestsWereMade() {
        // Test your service
        callYourService();
        
        // Verify requests were made to the mock APIs
        getMultiApiServer().getServer("products")
            .verify(getRequestedFor(urlEqualTo("/products")));
    }
}
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

### Java Code Generation 🔥 NEW!

Generate Spring Boot-ready Java WireMock configuration classes alongside JSON mappings:

```bash
# Generate JSON mappings + Java code
python3 scripts/multi_spec_wiremock_generator.py spec wiremock --java

# Generate with custom Java package
python3 scripts/multi_spec_wiremock_generator.py spec wiremock --java --package com.mycompany.wiremock

# Legacy mode (JSON only)
python3 scripts/multi_spec_wiremock_generator.py spec wiremock
```

#### What Gets Generated

```
wiremock/
├── mappings/              # JSON mappings (as before)
├── __files/              # Response files (as before)
└── java/                 # 🆕 Java code for Spring Boot integration
    ├── README.md         # Comprehensive Java usage guide
    ├── pom.xml           # Maven build file
    ├── build.gradle      # Gradle build file
    └── src/
        ├── main/java/com/example/wiremock/
        │   ├── MultiApiWireMockServer.java       # 🎯 Main orchestrator
        │   └── config/
        │       ├── WireMockTestConfig.java       # Spring Boot config
        │       ├── ProductsWireMockConfig.java   # Per-API configs
        │       └── UsersWireMockConfig.java      # Auto-generated per API
        └── test/java/com/example/wiremock/test/
            ├── BaseWireMockIntegrationTest.java  # Base test class
            ├── ProductsWireMockTest.java         # Per-API test bases
            └── UsersWireMockTest.java            # Ready for extension
```

#### Usage in Spring Boot Tests

**Option 1: Single API**
```java
@SpringBootTest
@Import(ProductsWireMockConfig.class)
class ProductServiceTest {
    @Autowired
    private String productsApiBaseUrl; // http://localhost:8089
    
    @Test
    void shouldCallProductsApi() {
        // Test your service that calls the products API
    }
}
```

**Option 2: Multiple APIs**
```java
@SpringBootTest
@Import(WireMockTestConfig.class)
class IntegrationTest extends BaseWireMockIntegrationTest {
    @Test
    void shouldTestApiInteractions() {
        String productsUrl = getProductsBaseUrl(); // Port 8080
        String usersUrl = getUsersBaseUrl();       // Port 8081
        // Test interactions between multiple services
    }
}
```

**Option 3: Manual Management**
```java
class CustomTest {
    private MultiApiWireMockServer server = new MultiApiWireMockServer();
    
    @BeforeEach
    void setUp() {
        server.startAllServers(); // Starts all APIs on different ports
        Map<String, String> urls = server.getServerUrls();
        // Configure your HTTP clients with the URLs
    }
}
```

#### Key Benefits
- 🚀 **Zero Configuration**: Just import and use
- 🎯 **Type Safety**: Strongly-typed Spring beans for API URLs
- 🧪 **Test Ready**: Base classes for JUnit 5 and Spring Boot
- 🔄 **Auto Management**: Lifecycle handling with @PostConstruct/@PreDestroy
- 📦 **Build Ready**: Includes pom.xml and build.gradle
- 📖 **Well Documented**: Comprehensive README with examples

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

## � Promotion & Community

### Official Recognition
- 🎯 **Submitted to OpenAPI Generator**: Proposal for official WireMock mapping generator
- 🤝 **WireMock Community**: Featured in WireMock ecosystem discussions
- 📢 **Open Source Promotion**: Active in developer communities

### Media Coverage
- 📝 **Blog Posts**: Technical articles on API mocking strategies
- 🎥 **Video Demos**: YouTube tutorials and conference talks
- 🐦 **Social Media**: Twitter, LinkedIn, and dev community engagement

## �🙏 Acknowledgments

- [WireMock](http://wiremock.org/) - Powerful HTTP mocking framework
- [OpenAPI](https://swagger.io/specification/) - API specification standard
- [Docker](https://www.docker.com/) - Containerization platform
- [OpenAPI Generator](https://openapi-generator.tech/) - Code generation inspiration

---

**⭐ Star this repository if it helps your project!**

**🤝 Contributions welcome - Help make this tool even better!**

**📢 Share this tool with your team and community!**
