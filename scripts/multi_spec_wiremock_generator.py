#!/usr/bin/env python3
"""
Multi-Spec WireMock Mapping Generator
Converts multiple OpenAPI specifications to consolidated WireMock stub mappings organized by API and HTTP method
"""

import json
import sys
import os
import re
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
import glob

# Try to import yaml, but make it optional
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class MultiSpecWireMockGenerator:
    def __init__(self, spec_dir: str, output_dir: str):
        self.spec_dir = spec_dir
        self.output_dir = output_dir
        self.mappings_dir = os.path.join(output_dir, 'mappings')
        self.files_dir = os.path.join(output_dir, '__files')
        
        # Define comprehensive status codes with scenarios
        self.status_codes = {
            200: {"name": "Success", "scenario": "success"},
            201: {"name": "Created", "scenario": "created"},
            401: {"name": "Unauthorized", "scenario": "unauthorized"},
            403: {"name": "Forbidden", "scenario": "forbidden"},
            404: {"name": "Not Found", "scenario": "not_found"},
            500: {"name": "Internal Server Error", "scenario": "server_error"},
            502: {"name": "Bad Gateway", "scenario": "bad_gateway"},
            503: {"name": "Service Unavailable", "scenario": "service_unavailable"}
        }
        
        # Mapping configuration
        self.scenario_identifiers = {
            200: "happy_path",
            201: "created_success", 
            401: "unauthorized_access",
            403: "forbidden_access",
            404: "not_found_error",
            500: "server_error",
            502: "bad_gateway",
            503: "service_unavailable"
        }
        
    def discover_specs(self) -> List[Dict[str, str]]:
        """Discover all OpenAPI spec files in the spec directory"""
        specs = []
        
        # Look for common spec file patterns
        patterns = ['*.yaml', '*.yml', '*.json']
        
        for pattern in patterns:
            for spec_file in glob.glob(os.path.join(self.spec_dir, pattern)):
                api_name = self.extract_api_name(spec_file)
                specs.append({
                    'file': spec_file,
                    'api_name': api_name,
                    'filename': os.path.basename(spec_file)
                })
                
        print(f"✓ Discovered {len(specs)} API specifications")
        for spec in specs:
            print(f"  - {spec['api_name']}: {spec['filename']}")
            
        return specs
    
    def extract_api_name(self, spec_file: str) -> str:
        """Extract API name from spec file name or content"""
        filename = os.path.basename(spec_file)
        
        # Remove common spec file suffixes
        api_name = re.sub(r'[-_](api|spec|openapi|swagger)\.(yaml|yml|json)$', '', filename, flags=re.IGNORECASE)
        api_name = re.sub(r'\.(yaml|yml|json)$', '', api_name)
        
        # Convert to clean format
        api_name = re.sub(r'[-_]+', '_', api_name)
        api_name = api_name.strip('_').lower()
        
        # If still generic, try to extract from file content
        if api_name in ['api', 'spec', 'openapi', 'swagger', '']:
            try:
                spec_content = self.load_spec_file(spec_file)
                if 'info' in spec_content and 'title' in spec_content['info']:
                    title = spec_content['info']['title']
                    api_name = self.sanitize_filename(title).lower()
            except:
                pass
                
        return api_name or 'unknown_api'
    
    def load_spec_file(self, spec_file: str) -> Dict[str, Any]:
        """Load OpenAPI specification from file"""
        try:
            with open(spec_file, 'r') as f:
                content = f.read()
                # Try JSON first, then YAML if available
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    if HAS_YAML:
                        return yaml.safe_load(content)
                    else:
                        raise Exception("File is not valid JSON and YAML module is not available")
        except Exception as e:
            raise Exception(f"Failed to load OpenAPI spec {spec_file}: {e}")
    
    def sanitize_filename(self, text: str) -> str:
        """Convert text to valid filename"""
        return re.sub(r'[^a-zA-Z0-9_]', '_', text).strip('_')
    
    def generate_from_schema(self, schema: Dict[str, Any], depth: int = 0, property_name: str = None) -> Any:
        """Generate example data from JSON schema with enhanced spec awareness"""
        if depth > 5:  # Prevent infinite recursion
            return {}
            
        # Handle references first
        if '$ref' in schema:
            ref_path = schema['$ref']
            if ref_path.startswith('#/components/schemas/'):
                schema_name = ref_path.split('/')[-1]
                referenced_schema = self.get_schema_definition(schema_name)
                if referenced_schema:
                    return self.generate_from_schema(referenced_schema, depth + 1, property_name)
            
        schema_type = schema.get('type', 'object')
        
        # Check for explicit examples first
        if 'example' in schema:
            return schema['example']
        elif 'examples' in schema and schema['examples']:
            return list(schema['examples'].values())[0]
        
        # Property-specific examples for common API patterns
        if property_name:
            if property_name in ['id', 'creditTransferOrderRequestId']:
                return f"EPT{str(uuid.uuid4()).replace('-', '')[:12].upper()}"
            elif property_name == 'signObjectId':
                return str(uuid.uuid4()).replace('-', '')
            elif property_name == 'transactionType':
                return "SCT"
            elif property_name == 'extraVerificationAction':
                return "NOT_REQUIRED"
            elif property_name in ['messageKey', 'code']:
                return f"API_ERROR_{property_name.upper()}"
            elif property_name in ['messageType', 'type']:
                return "INFO"
            elif property_name in ['messageText', 'message']:
                return f"Example message for {property_name}"
            elif property_name in ['traceId', 'trackingId']:
                return str(uuid.uuid4())
            elif property_name == 'timestamp':
                return "2024-01-01T12:00:00Z"
            elif property_name in ['email']:
                return "user@example.com"
            elif property_name in ['username', 'name']:
                return f"example_{property_name}"
            elif property_name in ['price', 'amount']:
                return 99.99
            elif property_name in ['stock', 'quantity']:
                return 10
        
        # Generate based on schema type
        if schema_type == 'object':
            obj = {}
            properties = schema.get('properties', {})
            for prop_name, prop_schema in properties.items():
                obj[prop_name] = self.generate_from_schema(prop_schema, depth + 1, prop_name)
            return obj
        elif schema_type == 'array':
            items_schema = schema.get('items', {})
            # Generate 1-2 items for arrays
            return [self.generate_from_schema(items_schema, depth + 1, property_name)]
        elif schema_type == 'string':
            if 'enum' in schema:
                return schema['enum'][0]
            format_type = schema.get('format', 'string')
            if format_type == 'email':
                return "user@example.com"
            elif format_type == 'date-time':
                return "2024-01-01T12:00:00Z"
            elif format_type == 'date':
                return "2024-01-01"
            elif format_type == 'uuid':
                return str(uuid.uuid4())
            return f"example_{format_type}"
        elif schema_type == 'integer':
            minimum = schema.get('minimum', 1)
            maximum = schema.get('maximum', 1000)
            return min(maximum, max(minimum, 123))
        elif schema_type == 'number':
            minimum = schema.get('minimum', 1.0)
            maximum = schema.get('maximum', 1000.0)
            return min(maximum, max(minimum, 123.45))
        elif schema_type == 'boolean':
            return True
        else:
            return None
    
    def get_schema_definition(self, schema_name: str) -> Dict[str, Any]:
        """Get schema definition from current OpenAPI spec"""
        if hasattr(self, 'current_spec') and self.current_spec:
            components = self.current_spec.get('components', {})
            schemas = components.get('schemas', {})
            return schemas.get(schema_name, {})
        return {}
    
    def extract_response_example(self, operation: Dict[str, Any], status_code: int) -> Optional[Dict[str, Any]]:
        """Extract response example from OpenAPI spec with enhanced logic"""
        responses = operation.get('responses', {})
        response_spec = responses.get(str(status_code), {})
        
        if response_spec:
            content = response_spec.get('content', {})
            json_content = content.get('application/json', {})
            
            # Use example from spec if available
            if 'example' in json_content:
                return json_content['example']
            
            # Try examples (plural)
            if 'examples' in json_content:
                examples = json_content['examples']
                if examples:
                    # Get first example
                    first_example = list(examples.values())[0]
                    if 'value' in first_example:
                        return first_example['value']
                        
            # Generate from schema if available
            schema = json_content.get('schema', {})
            if schema:
                return self.generate_from_schema(schema)
        
        # Try to get from global responses
        if hasattr(self, 'current_spec') and self.current_spec:
            components = self.current_spec.get('components', {})
            responses_comp = components.get('responses', {})
            
            # Look for common response patterns
            status_name_map = {
                401: ['Unauthorized', 'unauthorized'],
                403: ['Forbidden', 'forbidden'], 
                404: ['NotFound', 'not_found', 'NotFoundError'],
                500: ['InternalServerError', 'internal_server_error', 'ServerError']
            }
            
            if status_code in status_name_map:
                for response_name in status_name_map[status_code]:
                    if response_name in responses_comp:
                        response_def = responses_comp[response_name]
                        content = response_def.get('content', {})
                        json_content = content.get('application/json', {})
                        if 'example' in json_content:
                            return json_content['example']
                        schema = json_content.get('schema', {})
                        if schema:
                            return self.generate_from_schema(schema)
                            
        return None
    
    def create_scenario_request_matcher(self, method: str, path: str, status_code: int, scenario_id: str) -> Dict[str, Any]:
        """Create request matcher for specific scenario"""
        matcher = {
            "method": method.upper(),
            "urlPathPattern": path
        }
        
        # Add headers for scenario identification
        headers = {
            "Accept": {"contains": "json"}
        }
        
        # Add scenario-specific matchers based on status code
        if method.upper() in ['POST', 'PUT', 'PATCH']:
            # Use body patterns for request differentiation
            body_patterns = []
            
            if status_code == 200 or status_code == 201:
                body_patterns.append({
                    "matchesJsonPath": f"$[?(@..* =~ /.*{self.scenario_identifiers[status_code]}.*/i)]"
                })
            else:
                # For error scenarios, use specific field matching
                body_patterns.append({
                    "matchesJsonPath": f"$[?(@..* =~ /.*{self.scenario_identifiers[status_code]}.*/i)]"
                })
            
            if body_patterns:
                matcher["bodyPatterns"] = body_patterns
        else:
            # For GET requests, use query parameters or headers
            if status_code != 200:
                headers[f"X-Test-Scenario"] = {"equalTo": self.scenario_identifiers[status_code]}
        
        matcher["headers"] = headers
        return matcher
    
    def generate_error_response(self, status_code: int, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate error response based on status code with enhanced logic"""
        
        # First try to get error response from the spec
        if hasattr(self, 'current_spec') and self.current_spec:
            spec_response = self.extract_response_example(operation, status_code)
            if spec_response:
                return spec_response
        
        # Generate realistic error response based on status code
        error_details = {
            401: {
                "code": "UNAUTHORIZED",
                "message": "Authentication credentials were not provided or are invalid",
                "details": "Please provide a valid authorization token"
            },
            403: {
                "code": "FORBIDDEN", 
                "message": "You do not have permission to access this resource",
                "details": "Insufficient privileges for this operation"
            },
            404: {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found",
                "details": "Resource does not exist or has been removed"
            },
            500: {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": "Please try again later or contact support"
            },
            502: {
                "code": "BAD_GATEWAY",
                "message": "Invalid response from upstream server",
                "details": "The server received an invalid response from an upstream server"
            },
            503: {
                "code": "SERVICE_UNAVAILABLE", 
                "message": "Service is temporarily unavailable",
                "details": "The service is currently undergoing maintenance or experiencing high load"
            }
        }
        
        error_info = error_details.get(status_code, {
            "code": f"ERROR_{status_code}",
            "message": self.status_codes[status_code]["name"],
            "details": f"Test scenario for {status_code} status code"
        })
        
        # Create comprehensive error response
        error_response = {
            "errors": [error_info],
            "timestamp": "2024-01-01T12:00:00Z",
            "traceId": str(uuid.uuid4()),
            "status": status_code,
            "path": operation.get('summary', 'Unknown operation')
        }
        
        return error_response
    
    def create_mapping_entry(self, operation_id: str, method: str, path: str, operation: Dict[str, Any], status_code: int, api_name: str) -> Dict[str, Any]:
        """Create a single mapping entry for a specific scenario"""
        scenario_id = f"{operation_id}_{status_code}"
        
        # Create request matcher
        request_matcher = self.create_scenario_request_matcher(method, path, status_code, scenario_id)
        
        # Create response
        response = {
            "status": status_code,
            "headers": {
                "Content-Type": "application/json"
            }
        }
        
        # Generate response body
        if status_code in [200, 201]:
            # Success response - use spec example or generate
            response_example = self.extract_response_example(operation, status_code)
            if response_example:
                # Save to file
                response_filename = f"{api_name}/{method.lower()}_{operation_id}_{status_code}_response.json"
                response_file_path = os.path.join(self.files_dir, response_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(response_file_path), exist_ok=True)
                
                with open(response_file_path, 'w') as f:
                    json.dump(response_example, f, indent=2)
                
                response["bodyFileName"] = response_filename
            else:
                response["body"] = json.dumps({"message": "Success"})
        else:
            # Error response
            error_response = self.generate_error_response(status_code, operation)
            response_filename = f"{api_name}/{method.lower()}_{operation_id}_{status_code}_error.json"
            response_file_path = os.path.join(self.files_dir, response_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(response_file_path), exist_ok=True)
            
            with open(response_file_path, 'w') as f:
                json.dump(error_response, f, indent=2)
            
            response["bodyFileName"] = response_filename
        
        return {
            "id": str(uuid.uuid4()),
            "request": request_matcher,
            "response": response,
            "metadata": {
                "scenario": self.status_codes[status_code]["scenario"],
                "operation_id": operation_id,
                "api_name": api_name
            }
        }
    
    def process_api_spec(self, spec_info: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """Process a single API spec and return mappings grouped by method"""
        spec = self.load_spec_file(spec_info['file'])
        api_name = spec_info['api_name']
        
        # Store current spec for schema resolution
        self.current_spec = spec
        
        # Group mappings by HTTP method
        method_mappings = {}
        
        paths = spec.get('paths', {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                    continue
                    
                operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_').strip('_')}")
                operation_id = self.sanitize_filename(operation_id)
                
                method_upper = method.upper()
                if method_upper not in method_mappings:
                    method_mappings[method_upper] = []
                
                # Generate mappings for all status codes
                for status_code in self.status_codes.keys():
                    mapping_entry = self.create_mapping_entry(
                        operation_id, method_upper, path, operation, status_code, api_name
                    )
                    method_mappings[method_upper].append(mapping_entry)
        
        # Clear current spec reference
        self.current_spec = None
        
        return method_mappings
    
    def write_consolidated_mappings(self, api_name: str, method_mappings: Dict[str, List[Dict[str, Any]]]):
        """Write consolidated mapping files for each HTTP method"""
        api_mappings_dir = os.path.join(self.mappings_dir, api_name)
        os.makedirs(api_mappings_dir, exist_ok=True)
        
        for method, mappings in method_mappings.items():
            # Determine filename based on method
            if method == 'GET':
                filename = f"get_{api_name}_mappings.json"
            elif method == 'POST':
                filename = f"create_{api_name}_mappings.json"
            elif method == 'PUT':
                filename = f"update_{api_name}_mappings.json"
            elif method == 'PATCH':
                filename = f"patch_{api_name}_mappings.json"
            elif method == 'DELETE':
                filename = f"delete_{api_name}_mappings.json"
            else:
                filename = f"{method.lower()}_{api_name}_mappings.json"
            
            mapping_file = os.path.join(api_mappings_dir, filename)
            
            # Create consolidated mapping structure
            consolidated_mapping = {
                "mappings": mappings
            }
            
            with open(mapping_file, 'w') as f:
                json.dump(consolidated_mapping, f, indent=2)
            
            print(f"✓ Generated {len(mappings)} {method} mappings for {api_name}: {filename}")
    
    def generate_all_mappings(self):
        """Generate mappings for all discovered API specs"""
        print("🚀 Starting Multi-Spec WireMock Mapping Generation")
        print("=" * 60)
        
        # Discover all specs
        specs = self.discover_specs()
        
        if not specs:
            print("❌ No API specifications found in the spec directory")
            return
        
        # Ensure output directories exist
        os.makedirs(self.mappings_dir, exist_ok=True)
        os.makedirs(self.files_dir, exist_ok=True)
        
        total_mappings = 0
        
        # Process each spec
        for spec_info in specs:
            print(f"\n📋 Processing API: {spec_info['api_name']}")
            print("-" * 40)
            
            try:
                method_mappings = self.process_api_spec(spec_info)
                self.write_consolidated_mappings(spec_info['api_name'], method_mappings)
                
                spec_total = sum(len(mappings) for mappings in method_mappings.values())
                total_mappings += spec_total
                
                print(f"✅ Completed {spec_info['api_name']}: {spec_total} total mappings")
                
            except Exception as e:
                print(f"❌ Error processing {spec_info['api_name']}: {e}")
        
        print("\n" + "=" * 60)
        print(f"🎉 Generation Complete!")
        print(f"📊 Total mappings generated: {total_mappings}")
        print(f"📁 Mappings directory: {self.mappings_dir}")
        print(f"📁 Response files directory: {self.files_dir}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python multi_spec_wiremock_generator.py <spec_directory> <output_directory>")
        print("Example: python multi_spec_wiremock_generator.py ./spec ./wiremock")
        sys.exit(1)
    
    spec_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(spec_dir):
        print(f"❌ Spec directory not found: {spec_dir}")
        sys.exit(1)
    
    generator = MultiSpecWireMockGenerator(spec_dir, output_dir)
    generator.generate_all_mappings()


if __name__ == "__main__":
    main()
