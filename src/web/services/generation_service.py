"""Generation service for WireMock mappings and Java code"""

import os
import sys
import zipfile
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.multi_spec_wiremock_generator import MultiSpecWireMockGenerator, JavaWireMockGenerator

class GenerationService:
    def __init__(self, temp_folder: str):
        self.temp_folder = temp_folder
    
    def generate_mappings(self, session_id: str, spec_files: List[str], include_java: bool = False) -> Dict[str, Any]:
        """Generate WireMock mappings and optionally Java code"""
        session_upload_dir = os.path.dirname(spec_files[0]) if spec_files else ""
        session_temp_dir = os.path.join(self.temp_folder, session_id)
        os.makedirs(session_temp_dir, exist_ok=True)
        
        # Generate mappings for all specs
        generator = MultiSpecWireMockGenerator(session_upload_dir, session_temp_dir)
        generator.generate_all_mappings()
        
        # Count generated mappings
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
                specs = generator.discover_specs()
                if specs:
                    java_generator = JavaWireMockGenerator()
                    java_generator.generate_java_code_for_apis(specs, session_temp_dir)
                    
                    for result in results:
                        result['java_generated'] = True
            except Exception as e:
                print(f"Warning: Java generation failed: {e}")
        
        return {
            'results': results,
            'session_id': session_id,
            'include_java': include_java
        }
    
    def create_download_package(self, session_id: str) -> str:
        """Create a ZIP package of all generated files"""
        session_temp_dir = os.path.join(self.temp_folder, session_id)
        zip_filename = f'wiremock-mappings-{session_id[:8]}.zip'
        zip_path = os.path.join(session_temp_dir, zip_filename)
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                
                for root, dirs, files in os.walk(session_temp_dir):
                    # Skip the zip file itself
                    if zip_path in [os.path.join(root, f) for f in files]:
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Create relative path for ZIP
                        arcname = os.path.relpath(file_path, session_temp_dir)
                        zipf.write(file_path, arcname)
                        file_count += 1
                
                if file_count > 0:
                    return zip_path
                else:
                    return None
                    
        except Exception as e:
            print(f"Error creating ZIP package: {e}")
            return None
