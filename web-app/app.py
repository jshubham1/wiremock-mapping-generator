#!/usr/bin/env python3
"""
WireMock Mapping Generator Web UI
Modern web interface for generating WireMock mappings from OpenAPI specifications
"""

import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
import sys
import subprocess
import json
import uuid
from typing import List, Dict, Any
import mimetypes

from flask import Flask, request, render_template, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Add the scripts directory to the path so we can import our generator
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))

try:
    from multi_spec_wiremock_generator import MultiSpecWireMockGenerator, JavaWireMockGenerator
except ImportError as e:
    print(f"Error importing generator modules: {e}")
    print("Please ensure you're running from the correct directory")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'wiremock-generator-secret-key-' + str(uuid.uuid4())

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['TEMP_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

# Ensure upload and temp directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'yaml', 'yml', 'json'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_session_files(session_id: str):
    """Clean up files for a specific session"""
    session_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    session_temp_dir = os.path.join(app.config['TEMP_FOLDER'], session_id)
    
    for directory in [session_upload_dir, session_temp_dir]:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
            except Exception as e:
                print(f"Warning: Could not clean up {directory}: {e}")

def cleanup_old_sessions():
    """Clean up sessions older than 1 hour"""
    current_time = datetime.now()
    cutoff_time = current_time.timestamp() - 3600  # 1 hour ago
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['TEMP_FOLDER']]:
        if not os.path.exists(folder):
            continue
            
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isdir(item_path):
                try:
                    # Check if it's a UUID (session directory)
                    uuid.UUID(item)
                    if os.path.getctime(item_path) < cutoff_time:
                        shutil.rmtree(item_path)
                        print(f"Cleaned up old session: {item}")
                except (ValueError, OSError):
                    # Not a valid UUID or couldn't access, skip
                    continue

@app.route('/')
def index():
    """Main page"""
    # Clean up old sessions
    cleanup_old_sessions()
    
    # Generate new session ID
    session_id = str(uuid.uuid4())
    return render_template('index.html', session_id=session_id)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'wiremock-mapping-generator-web-ui',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload"""
    try:
        session_id = request.form.get('session_id')
        if not session_id:
            return jsonify({'error': 'No session ID provided'}), 400
        
        # Validate session ID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            return jsonify({'error': 'Invalid session ID format'}), 400
        
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({'error': 'No files selected'}), 400
        
        # Create session directory
        session_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_upload_dir, exist_ok=True)
        
        uploaded_files = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if filename:
                    filepath = os.path.join(session_upload_dir, filename)
                    file.save(filepath)
                    uploaded_files.append({
                        'name': filename,
                        'size': os.path.getsize(filepath)
                    })
        
        if not uploaded_files:
            cleanup_session_files(session_id)
            return jsonify({'error': 'No valid OpenAPI files uploaded. Please upload YAML or JSON files.'}), 400
        
        return jsonify({
            'message': 'Files uploaded successfully',
            'files': uploaded_files,
            'session_id': session_id
        })
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
def generate_mappings():
    """Generate WireMock mappings"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        include_java = data.get('include_java', False)
        
        if not session_id:
            return jsonify({'error': 'No session ID provided'}), 400
        
        # Validate session ID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            return jsonify({'error': 'Invalid session ID format'}), 400
        
        session_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        if not os.path.exists(session_upload_dir):
            return jsonify({'error': 'Session not found or expired'}), 404
        
        # Find uploaded spec files
        spec_files = []
        for filename in os.listdir(session_upload_dir):
            if allowed_file(filename):
                spec_files.append(os.path.join(session_upload_dir, filename))
        
        if not spec_files:
            return jsonify({'error': 'No valid spec files found'}), 400
        
        # Create session temp directory
        session_temp_dir = os.path.join(app.config['TEMP_FOLDER'], session_id)
        os.makedirs(session_temp_dir, exist_ok=True)
        
        # Generate mappings for all specs
        # The MultiSpecWireMockGenerator expects spec_dir and output_dir
        generator = MultiSpecWireMockGenerator(session_upload_dir, session_temp_dir)
        generator.generate_all_mappings()
        
        # Count generated mappings by checking the mappings directory
        mappings_dir = os.path.join(session_temp_dir, 'mappings')
        mapping_count = 0
        if os.path.exists(mappings_dir):
            mapping_count = len([f for f in os.listdir(mappings_dir) if f.endswith('.json')])
        
        # Prepare results
        results = []
        for spec_file in spec_files:
            spec_name = Path(spec_file).stem
            result = {
                'spec_file': os.path.basename(spec_file),
                'spec_name': spec_name,
                'mappings_generated': mapping_count // len(spec_files) if len(spec_files) > 0 else 0,
                'output_dir': session_temp_dir
            }
            results.append(result)
        
        # Generate Java code if requested
        if include_java:
            try:
                # Discover specs using the generator's method
                specs = generator.discover_specs()
                if specs:
                    java_generator = JavaWireMockGenerator()
                    java_generator.generate_java_code_for_apis(specs, session_temp_dir)
                    
                    # Update results to indicate Java generation
                    for result in results:
                        result['java_generated'] = True
            except Exception as e:
                print(f"Warning: Java generation failed: {e}")
                # Continue without Java generation
        
        return jsonify({
            'message': 'Generation completed',
            'results': results,
            'session_id': session_id,
            'include_java': include_java
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/download/<session_id>')
def download_package(session_id):
    """Download generated mappings as ZIP"""
    try:
        # Validate session ID format
        try:
            uuid.UUID(session_id)
        except ValueError:
            return jsonify({'error': 'Invalid session ID format'}), 400
        
        session_temp_dir = os.path.join(app.config['TEMP_FOLDER'], session_id)
        if not os.path.exists(session_temp_dir):
            return jsonify({'error': 'Session not found or expired'}), 404
        
        # Create ZIP file
        zip_filename = f'wiremock-mappings-{session_id[:8]}.zip'
        zip_path = os.path.join(session_temp_dir, zip_filename)
        
        created_zip = create_download_package(session_temp_dir, zip_path)
        if not created_zip:
            return jsonify({'error': 'No files to download'}), 404
        
        def remove_file():
            """Clean up the session after download"""
            try:
                cleanup_session_files(session_id)
            except Exception as e:
                print(f"Warning: Could not clean up session {session_id}: {e}")
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

def create_download_package(temp_dir: str, zip_path: str) -> bool:
    """Create a ZIP package of all generated files"""
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            file_count = 0
            
            for root, dirs, files in os.walk(temp_dir):
                # Skip the zip file itself
                if zip_path in [os.path.join(root, f) for f in files]:
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    # Create relative path for ZIP
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
                    file_count += 1
            
            return file_count > 0
            
    except Exception as e:
        print(f"Error creating ZIP package: {e}")
        return False

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle not found error"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting WireMock Mapping Generator Web UI...")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🔧 Temp folder: {app.config['TEMP_FOLDER']}")
    print("🌐 Server will be available at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
