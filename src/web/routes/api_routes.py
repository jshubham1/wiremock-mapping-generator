"""API routes for the web application"""

import os
import uuid
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.exceptions import RequestEntityTooLarge
from src.web.services.file_service import FileService
from src.web.services.generation_service import GenerationService

def create_api_blueprint():
    """Create the API routes blueprint"""
    bp = Blueprint('api', __name__)
    
    @bp.route('/upload', methods=['POST'])
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
            
            # Initialize file service
            file_service = FileService(
                current_app.config['UPLOAD_FOLDER'],
                current_app.config['TEMP_FOLDER']
            )
            
            uploaded_files = file_service.save_uploaded_files(files, session_id)
            
            if not uploaded_files:
                file_service.cleanup_session_files(session_id)
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
    
    @bp.route('/generate', methods=['POST'])
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
            
            # Initialize services
            file_service = FileService(
                current_app.config['UPLOAD_FOLDER'],
                current_app.config['TEMP_FOLDER']
            )
            generation_service = GenerationService(current_app.config['TEMP_FOLDER'])
            
            # Get spec files
            spec_files = file_service.get_session_spec_files(session_id)
            if not spec_files:
                return jsonify({'error': 'No valid spec files found'}), 400
            
            # Generate mappings
            result = generation_service.generate_mappings(session_id, spec_files, include_java)
            
            return jsonify({
                'message': 'Generation completed',
                **result
            })
            
        except Exception as e:
            return jsonify({'error': f'Generation failed: {str(e)}'}), 500
    
    @bp.route('/download/<session_id>')
    def download_package(session_id):
        """Download generated mappings as ZIP"""
        try:
            # Validate session ID format
            try:
                uuid.UUID(session_id)
            except ValueError:
                return jsonify({'error': 'Invalid session ID format'}), 400
            
            session_temp_dir = os.path.join(current_app.config['TEMP_FOLDER'], session_id)
            if not os.path.exists(session_temp_dir):
                return jsonify({'error': 'Session not found or expired'}), 404
            
            # Initialize services
            generation_service = GenerationService(current_app.config['TEMP_FOLDER'])
            file_service = FileService(
                current_app.config['UPLOAD_FOLDER'],
                current_app.config['TEMP_FOLDER']
            )
            
            # Create ZIP package
            zip_path = generation_service.create_download_package(session_id)
            if not zip_path:
                return jsonify({'error': 'No files to download'}), 404
            
            zip_filename = f'wiremock-mappings-{session_id[:8]}.zip'
            
            def remove_file():
                """Clean up the session after download"""
                try:
                    file_service.cleanup_session_files(session_id)
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
    
    @bp.errorhandler(413)
    def too_large(e):
        """Handle file too large error"""
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

    @bp.errorhandler(404)
    def not_found(e):
        """Handle not found error"""
        return jsonify({'error': 'Endpoint not found'}), 404

    @bp.errorhandler(500)
    def internal_error(e):
        """Handle internal server error"""
        return jsonify({'error': 'Internal server error'}), 500
    
    return bp
