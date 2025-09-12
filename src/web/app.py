#!/usr/bin/env python3
"""
WireMock Mapping Generator Web UI
Modern web interface for generating WireMock mappings from OpenAPI specifications
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.web.services.file_service import FileService
from src.web.services.generation_service import GenerationService
from src.web.routes.main_routes import create_main_blueprint
from src.web.routes.api_routes import create_api_blueprint

from flask import Flask
import uuid

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.secret_key = 'wiremock-generator-secret-key-' + str(uuid.uuid4())

    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['TEMP_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

    # Ensure upload and temp directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

    # Register blueprints
    app.register_blueprint(create_main_blueprint())
    app.register_blueprint(create_api_blueprint(), url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting WireMock Mapping Generator Web UI...")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🔧 Temp folder: {app.config['TEMP_FOLDER']}")
    print("🌐 Server will be available at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
