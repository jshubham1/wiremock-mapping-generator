# WireMock Mapping Generator Web UI

A modern, responsive web interface for generating WireMock mappings from OpenAPI specifications. Built with Flask and featuring drag-and-drop file upload, real-time generation progress, and downloadable ZIP packages.

## Features

### 🌐 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Drag & Drop Upload**: Simply drag your OpenAPI files or click to browse
- **Real-time Progress**: Visual feedback during mapping generation
- **Instant Download**: Get your generated mappings as a ZIP file

### 📁 File Support
- **Multiple Formats**: YAML (.yaml, .yml) and JSON (.json) OpenAPI specifications
- **Batch Processing**: Upload and process multiple API specs simultaneously
- **File Validation**: Automatic validation of file types and sizes (max 16MB per file)
- **Smart Organization**: Generated mappings organized by API and HTTP method

### ⚙️ Generation Options
- **JSON Only**: Generate WireMock JSON mappings for immediate use
- **JSON + Java**: Include Spring Boot configuration and JUnit test classes
- **Custom Packages**: Specify Java package names for generated classes
- **Comprehensive Coverage**: 8 HTTP status codes per endpoint (200, 201, 401, 403, 404, 500, 502, 503)

### 📦 Download Package
- **ZIP Archive**: Complete package with all generated files
- **Documentation**: Included README with usage instructions
- **Organized Structure**: Clear directory layout for easy integration
- **Size Optimization**: Compressed files for faster downloads

## Quick Start

### Option 1: Using Make (Recommended)
```bash
# Start the complete stack with Web UI
make web-ui

# Or start services individually
make start-web
```

### Option 2: Using Docker Compose
```bash
# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps
```

### Option 3: Local Development
```bash
# Navigate to web-app directory
cd web-app

# Install dependencies
pip install -r requirements.txt

# Start the Flask app
python app.py
```

## Usage

1. **Access the Web UI**
   - Open your browser to: http://localhost:5000

2. **Upload OpenAPI Specifications**
   - Drag and drop your `.yaml`, `.yml`, or `.json` files
   - Or click the upload area to browse files
   - Multiple files can be uploaded simultaneously

3. **Configure Generation Options**
   - Choose **JSON Only** for WireMock mappings only
   - Choose **JSON + Java** to include Spring Boot integration code
   - Specify Java package name if generating Java code

4. **Generate and Download**
   - Click "Generate WireMock Mappings"
   - Monitor progress in real-time
   - Download the ZIP package when complete

## Architecture

```
web-app/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── templates/
│   └── index.html        # Web UI template
├── static/               # Static assets (if needed)
├── uploads/              # Temporary file uploads
└── temp/                 # Generated packages (auto-cleaned)
```

## API Endpoints

### GET /
Main web interface for file upload and generation.

### POST /upload
Handle file upload and mapping generation.

**Parameters:**
- `files`: OpenAPI specification files (multipart/form-data)
- `generateJava`: Boolean flag for Java code generation
- `javaPackage`: Java package name (when generateJava=true)

**Response:**
```json
{
  "success": true,
  "sessionId": "uuid",
  "summary": {
    "uploadedFiles": ["api1.yaml", "api2.json"],
    "generatedMappings": 24,
    "responseFiles": 48,
    "javaFiles": 12,
    "includeJava": true,
    "zipSize": 156789
  },
  "downloadUrl": "/download/uuid"
}
```

### GET /download/<session_id>
Download generated ZIP package.

### GET /health
Health check endpoint for monitoring.

## Configuration

### Environment Variables
```bash
FLASK_ENV=production          # Flask environment
FLASK_APP=app.py             # Flask application
PYTHONPATH=/app              # Python path for imports
```

### Docker Configuration
The web UI is configured to work seamlessly with the existing WireMock infrastructure:

```yaml
services:
  wiremock-web-ui:
    build: ./web-app
    ports:
      - "5000:5000"
    volumes:
      - ./scripts:/app/scripts:ro
      - ./generated:/app/generated
    depends_on:
      - wiremock
```

## Development

### Local Setup
```bash
# Clone and navigate
cd web-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
export FLASK_ENV=development
python app.py
```

### Adding Features
1. **Frontend**: Modify `templates/index.html` for UI changes
2. **Backend**: Update `app.py` for new endpoints or functionality
3. **Styling**: Use Tailwind CSS classes (included via CDN)
4. **Icons**: FontAwesome icons available throughout

### Testing
```bash
# Test file upload
curl -X POST http://localhost:5000/upload \
  -F "files=@your-api-spec.yaml" \
  -F "generateJava=true" \
  -F "javaPackage=com.example.test"

# Health check
curl http://localhost:5000/health
```

## Security Considerations

### File Upload Security
- **File Type Validation**: Only YAML and JSON files accepted
- **Size Limits**: 16MB maximum per file
- **Secure Filenames**: Werkzeug's secure_filename() for safety
- **Temporary Storage**: Files auto-cleaned after 1 hour

### Production Deployment
- **HTTPS**: Use reverse proxy (nginx) with SSL certificates
- **Authentication**: Add authentication middleware if needed
- **Rate Limiting**: Implement request rate limiting
- **File Scanning**: Consider virus scanning for uploaded files

## Troubleshooting

### Common Issues

**Web UI not accessible**
```bash
# Check if services are running
docker-compose ps

# Check logs
docker-compose logs wiremock-web-ui
```

**Upload fails**
- Verify file format (YAML/JSON only)
- Check file size (max 16MB)
- Ensure valid OpenAPI 3.0+ specification

**Generation errors**
- Validate OpenAPI spec syntax
- Check Docker container logs
- Ensure sufficient disk space

**Download issues**
- Files expire after 1 hour
- Regenerate if session expired
- Check browser download settings

### Logs and Monitoring
```bash
# View web UI logs
docker-compose logs -f wiremock-web-ui

# View all service logs
docker-compose logs -f

# Monitor container health
docker-compose ps
curl http://localhost:5000/health
```

## Integration with Existing Workflow

The Web UI seamlessly integrates with the existing command-line tools:

### CLI to Web UI Migration
```bash
# Old CLI approach
make generate
make start
make test

# New Web UI approach
make web-ui
# Use browser interface
# Download and use generated files
```

### Hybrid Usage
- Use Web UI for one-off generations
- Use CLI/Makefile for CI/CD pipelines
- Both approaches generate identical output

## License

MIT License - see [LICENSE](../LICENSE) file for details.

## Support

For issues and feature requests:
- 📖 Documentation: See main project README
- 🐛 Issues: GitHub Issues tracker
- 💬 Discussions: GitHub Discussions
