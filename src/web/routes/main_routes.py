"""Main routes for the web application"""

import uuid
from datetime import datetime
from flask import Blueprint, render_template, current_app
from src.web.services.file_service import FileService

def create_main_blueprint():
    """Create the main routes blueprint"""
    bp = Blueprint('main', __name__)
    
    @bp.route('/')
    def index():
        """Main page"""
        # Initialize file service
        file_service = FileService(
            current_app.config['UPLOAD_FOLDER'],
            current_app.config['TEMP_FOLDER']
        )
        
        # Clean up old sessions
        file_service.cleanup_old_sessions()
        
        # Generate new session ID
        session_id = str(uuid.uuid4())
        return render_template('index_new.html', session_id=session_id)
    
    @bp.route('/health')
    def health_check():
        """Health check endpoint"""
        from flask import jsonify
        return jsonify({
            'status': 'healthy',
            'service': 'wiremock-mapping-generator-web-ui',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    return bp
