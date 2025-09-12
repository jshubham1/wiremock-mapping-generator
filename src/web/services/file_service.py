"""File handling service for the web application"""

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {'yaml', 'yml', 'json'}

class FileService:
    def __init__(self, upload_folder: str, temp_folder: str):
        self.upload_folder = upload_folder
        self.temp_folder = temp_folder
    
    def allowed_file(self, filename: str) -> bool:
        """Check if file has allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def cleanup_session_files(self, session_id: str):
        """Clean up files for a specific session"""
        session_upload_dir = os.path.join(self.upload_folder, session_id)
        session_temp_dir = os.path.join(self.temp_folder, session_id)
        
        for directory in [session_upload_dir, session_temp_dir]:
            if os.path.exists(directory):
                try:
                    shutil.rmtree(directory)
                except Exception as e:
                    print(f"Warning: Could not clean up {directory}: {e}")
    
    def cleanup_old_sessions(self):
        """Clean up sessions older than 1 hour"""
        current_time = datetime.now()
        cutoff_time = current_time.timestamp() - 3600  # 1 hour ago
        
        for folder in [self.upload_folder, self.temp_folder]:
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
    
    def save_uploaded_files(self, files, session_id: str) -> List[Dict[str, Any]]:
        """Save uploaded files and return file info"""
        session_upload_dir = os.path.join(self.upload_folder, session_id)
        os.makedirs(session_upload_dir, exist_ok=True)
        
        uploaded_files = []
        for file in files:
            if file and file.filename and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if filename:
                    filepath = os.path.join(session_upload_dir, filename)
                    file.save(filepath)
                    uploaded_files.append({
                        'name': filename,
                        'size': os.path.getsize(filepath)
                    })
        
        return uploaded_files
    
    def get_session_spec_files(self, session_id: str) -> List[str]:
        """Get list of spec files for a session"""
        session_upload_dir = os.path.join(self.upload_folder, session_id)
        if not os.path.exists(session_upload_dir):
            return []
        
        spec_files = []
        for filename in os.listdir(session_upload_dir):
            if self.allowed_file(filename):
                spec_files.append(os.path.join(session_upload_dir, filename))
        
        return spec_files
