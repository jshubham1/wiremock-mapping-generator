#!/usr/bin/env python3
"""
Multi-Spec WireMock Mapping Generator
Converts multiple OpenAPI specifications to consolidated WireMock stub mappings organized by API and HTTP method
Includes Java code generation for Spring Boot and JUnit integration
"""

import json
import sys
import os
import re
import uuid
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import glob
from datetime import datetime

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


class JavaWireMockGenerator:
    """Generate Java WireMock configuration classes for Spring Boot and JUnit integration"""
    
    def __init__(self, package_name: str = "com.example.wiremock"):
        self.package_name = package_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_java_code_for_apis(self, specs: List[Dict[str, str]], output_dir: str):
        """Generate comprehensive Java code for all APIs"""
        java_base_dir = os.path.join(output_dir, 'java')
        
        # Create directory structure
        package_dirs = self.package_name.split('.')
        java_src_dir = os.path.join(java_base_dir, 'src', 'main', 'java', *package_dirs)
        java_test_dir = os.path.join(java_base_dir, 'src', 'test', 'java', *package_dirs)
        java_resources_dir = os.path.join(java_base_dir, 'src', 'test', 'resources')
        
        os.makedirs(java_src_dir, exist_ok=True)
        os.makedirs(java_test_dir, exist_ok=True)
        os.makedirs(java_resources_dir, exist_ok=True)
        
        print(f"\n🔧 Generating Java WireMock Code")
        print("-" * 40)
        
        # Generate main orchestrator class
        self.generate_multi_api_server(specs, java_src_dir)
        
        # Generate individual API configurations
        for spec_info in specs:
            self.generate_api_specific_classes(spec_info, java_src_dir, java_test_dir)
        
        # Generate Spring Boot configuration
        self.generate_spring_config(specs, java_src_dir)
        
        # Generate base test class
        self.generate_base_test_class(specs, java_test_dir)
        
        # Generate build files
        self.generate_build_files(java_base_dir)
        
        # Generate README
        self.generate_java_readme(specs, java_base_dir)
        
        print(f"✅ Java code generated in: {java_base_dir}")
    
    def generate_multi_api_server(self, specs: List[Dict[str, str]], output_dir: str):
        """Generate main multi-API server orchestrator"""
        api_names = [spec['api_name'] for spec in specs]
        api_list = ', '.join(api_names)
        
        class_content = f'''package {self.package_name};

import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import org.springframework.stereotype.Component;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Multi-API WireMock Server Manager
 * Auto-generated from OpenAPI specifications on {self.timestamp}
 * 
 * Manages WireMock servers for: {api_list}
 * 
 * Usage:
 * 1. Include in your Spring Boot test context
 * 2. Access individual servers via getServer(apiName)
 * 3. Get base URLs via getServerUrls()
 */
@Component
public class MultiApiWireMockServer {{
    
    private final Map<String, WireMockServer> servers = new HashMap<>();
    private static final int BASE_PORT = 8080;
    private static final AtomicInteger portCounter = new AtomicInteger(BASE_PORT);
    
    @PostConstruct
    public void startAllServers() {{
        System.out.println("🚀 Starting WireMock servers for all APIs...");
        
{self._generate_server_startup_code(specs)}
        
        System.out.println("✅ All WireMock servers started successfully");
        getServerUrls().forEach((api, url) -> 
            System.out.println("  - " + api + ": " + url));
    }}
    
    @PreDestroy
    public void stopAllServers() {{
        System.out.println("🛑 Stopping all WireMock servers...");
        servers.values().forEach(server -> {{
            if (server.isRunning()) {{
                server.stop();
            }}
        }});
        servers.clear();
    }}
    
    public WireMockServer getServer(String apiName) {{
        return servers.get(apiName);
    }}
    
    public Map<String, String> getServerUrls() {{
        Map<String, String> urls = new HashMap<>();
{self._generate_url_mapping_code(specs)}
        return urls;
    }}
    
    public boolean isRunning(String apiName) {{
        WireMockServer server = servers.get(apiName);
        return server != null && server.isRunning();
    }}
    
    public void resetAll() {{
        servers.values().forEach(WireMockServer::resetAll);
    }}
}}'''
        
        with open(os.path.join(output_dir, 'MultiApiWireMockServer.java'), 'w') as f:
            f.write(class_content)
        
        print(f"✓ Generated MultiApiWireMockServer.java")
    
    def _generate_server_startup_code(self, specs: List[Dict[str, str]]) -> str:
        """Generate server startup code for each API"""
        startup_code = ""
        for i, spec in enumerate(specs):
            api_name = spec['api_name']
            class_name = self._to_class_name(api_name)
            port_offset = i
            
            startup_code += f'''        // Start {class_name} WireMock Server
        try {{
            int {api_name}Port = BASE_PORT + {port_offset};
            WireMockServer {api_name}Server = new WireMockServer(
                WireMockConfiguration.options()
                    .port({api_name}Port)
                    .usingFilesUnderClasspath("wiremock/{api_name}")
                    .verbose(true)
            );
            {api_name}Server.start();
            servers.put("{api_name}", {api_name}Server);
            System.out.println("✓ {class_name} API server started on port " + {api_name}Port);
        }} catch (Exception e) {{
            System.err.println("❌ Failed to start {class_name} server: " + e.getMessage());
            throw new RuntimeException("Failed to start {class_name} WireMock server", e);
        }}
        
'''
        return startup_code
    
    def _generate_url_mapping_code(self, specs: List[Dict[str, str]]) -> str:
        """Generate URL mapping code"""
        url_code = ""
        for i, spec in enumerate(specs):
            api_name = spec['api_name']
            port_offset = i
            url_code += f'        urls.put("{api_name}", "http://localhost:" + (BASE_PORT + {port_offset}));\n'
        return url_code
    
    def generate_api_specific_classes(self, spec_info: Dict[str, str], src_dir: str, test_dir: str):
        """Generate API-specific configuration and test classes"""
        api_name = spec_info['api_name']
        class_name = self._to_class_name(api_name)
        
        # Generate configuration class
        config_content = f'''package {self.package_name}.config;

import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import static com.github.tomakehurst.wiremock.client.WireMock.*;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

/**
 * WireMock Configuration for {class_name} API
 * Auto-generated from OpenAPI specification: {spec_info['filename']}
 * Generated on: {self.timestamp}
 * 
 * Usage in tests:
 * @SpringBootTest
 * @Import({class_name}WireMockConfig.class)
 * class YourTest {{
 *     @Autowired
 *     private String {api_name}ApiBaseUrl;
 * }}
 */
@TestConfiguration
public class {class_name}WireMockConfig {{

    private WireMockServer wireMockServer;
    public static final int WIREMOCK_PORT = 8089;
    
    @PostConstruct
    public void setupWireMock() {{
        wireMockServer = new WireMockServer(
            WireMockConfiguration.options()
                .port(WIREMOCK_PORT)
                .usingFilesUnderClasspath("wiremock/{api_name}")
                .verbose(true)
        );
        wireMockServer.start();
        configureFor("localhost", WIREMOCK_PORT);
        setupDefaultStubs();
    }}
    
    @PreDestroy
    public void tearDown() {{
        if (wireMockServer != null && wireMockServer.isRunning()) {{
            wireMockServer.stop();
        }}
    }}
    
    @Bean
    @Primary
    public String {api_name}ApiBaseUrl() {{
        return "http://localhost:" + WIREMOCK_PORT;
    }}
    
    @Bean
    public WireMockServer {api_name}WireMockServer() {{
        return wireMockServer;
    }}
    
    private void setupDefaultStubs() {{
        // Health check endpoint
        stubFor(get(urlPathEqualTo("/health"))
            .willReturn(aResponse()
                .withStatus(200)
                .withHeader("Content-Type", "application/json")
                .withBody("{{\\"status\\": \\"UP\\", \\"service\\": \\"{api_name}\\"}}")));
                
        // Default 404 for unmapped endpoints
        stubFor(any(urlMatching(".*"))
            .atPriority(10)
            .willReturn(aResponse()
                .withStatus(404)
                .withHeader("Content-Type", "application/json")
                .withBody("{{\\"error\\": \\"Endpoint not found\\", \\"service\\": \\"{api_name}\\"}}")));
    }}
    
    public void resetStubs() {{
        if (wireMockServer != null) {{
            wireMockServer.resetAll();
            setupDefaultStubs();
        }}
    }}
}}'''
        
        # Create config directory
        config_dir = os.path.join(src_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, f'{class_name}WireMockConfig.java'), 'w') as f:
            f.write(config_content)
        
        # Generate test base class
        test_content = f'''package {self.package_name}.test;

import {self.package_name}.config.{class_name}WireMockConfig;
import com.github.tomakehurst.wiremock.WireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base test class for {class_name} API integration tests
 * Auto-generated from OpenAPI specification: {spec_info['filename']}
 * Generated on: {self.timestamp}
 * 
 * Extend this class in your integration tests:
 * 
 * class {class_name}IntegrationTest extends {class_name}WireMockTest {{
 *     @Test
 *     void shouldCallApi() {{
 *         // Your test here using {api_name}ApiBaseUrl
 *         String response = restTemplate.getForObject({api_name}ApiBaseUrl + "/endpoint", String.class);
 *         assertThat(response).isNotNull();
 *     }}
 * }}
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = {class_name}WireMockConfig.class)
public abstract class {class_name}WireMockTest {{

    @Autowired
    protected String {api_name}ApiBaseUrl;
    
    @Autowired
    protected WireMockServer {api_name}WireMockServer;
    
    @BeforeEach
    void setUp() {{
        // Reset to clean state before each test
        if ({api_name}WireMockServer.isRunning()) {{
            {api_name}WireMockServer.resetAll();
        }}
    }}
    
    @AfterEach
    void tearDown() {{
        // Clean up after each test
        if ({api_name}WireMockServer.isRunning()) {{
            {api_name}WireMockServer.resetAll();
        }}
    }}
    
    protected String getApiBaseUrl() {{
        return {api_name}ApiBaseUrl;
    }}
    
    protected WireMockServer getWireMockServer() {{
        return {api_name}WireMockServer;
    }}
}}'''
        
        # Create test directory
        test_package_dir = os.path.join(test_dir, 'test')
        os.makedirs(test_package_dir, exist_ok=True)
        
        with open(os.path.join(test_package_dir, f'{class_name}WireMockTest.java'), 'w') as f:
            f.write(test_content)
        
        print(f"✓ Generated {class_name} configuration and test classes")
    
    def generate_spring_config(self, specs: List[Dict[str, str]], output_dir: str):
        """Generate Spring Boot main configuration"""
        api_imports = []
        api_configs = []
        
        for spec in specs:
            class_name = self._to_class_name(spec['api_name'])
            api_imports.append(f"import {self.package_name}.config.{class_name}WireMockConfig;")
            api_configs.append(f"        {class_name}WireMockConfig.class,")
        
        imports_str = '\n'.join(api_imports)
        configs_str = '\n'.join(api_configs)
        
        config_content = f'''package {self.package_name}.config;

{imports_str}
import {self.package_name}.MultiApiWireMockServer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;

/**
 * Main WireMock Test Configuration
 * Auto-generated configuration for all APIs
 * Generated on: {self.timestamp}
 * 
 * Use this configuration to import all WireMock servers in your tests:
 * 
 * @SpringBootTest
 * @Import(WireMockTestConfig.class)
 * class IntegrationTest {{
 *     @Autowired
 *     private MultiApiWireMockServer multiApiServer;
 * }}
 */
@TestConfiguration
@Import({{
{configs_str}
}})
public class WireMockTestConfig {{
    
    @Bean
    @Primary
    public MultiApiWireMockServer multiApiWireMockServer() {{
        return new MultiApiWireMockServer();
    }}
}}'''
        
        config_dir = os.path.join(output_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, 'WireMockTestConfig.java'), 'w') as f:
            f.write(config_content)
        
        print(f"✓ Generated WireMockTestConfig.java")
    
    def generate_base_test_class(self, specs: List[Dict[str, str]], output_dir: str):
        """Generate base integration test class"""
        api_autowired = []
        api_getters = []
        
        for spec in specs:
            api_name = spec['api_name']
            api_autowired.append(f"    @Autowired\n    protected String {api_name}ApiBaseUrl;")
            api_getters.append(f'''    protected String get{self._to_class_name(api_name)}BaseUrl() {{
        return {api_name}ApiBaseUrl;
    }}''')
        
        autowired_str = '\n    \n'.join(api_autowired)
        getters_str = '\n    \n'.join(api_getters)
        
        test_content = f'''package {self.package_name}.test;

import {self.package_name}.config.WireMockTestConfig;
import {self.package_name}.MultiApiWireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base Integration Test Class
 * Auto-generated test base for all APIs
 * Generated on: {self.timestamp}
 * 
 * Extend this class for comprehensive integration tests:
 * 
 * class MyIntegrationTest extends BaseWireMockIntegrationTest {{
 *     @Test
 *     void shouldTestMultipleApis() {{
 *         // Test interactions between multiple APIs
 *         // All APIs are available via getXxxBaseUrl() methods
 *     }}
 * }}
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = WireMockTestConfig.class)
public abstract class BaseWireMockIntegrationTest {{

    @Autowired
    protected MultiApiWireMockServer multiApiServer;
    
{autowired_str}
    
    @BeforeEach
    void setUpAll() {{
        // Ensure all servers are running
        if (multiApiServer != null) {{
            // Reset all servers to clean state
            multiApiServer.resetAll();
        }}
    }}
    
    @AfterEach 
    void tearDownAll() {{
        // Clean up after each test
        if (multiApiServer != null) {{
            multiApiServer.resetAll();
        }}
    }}
    
    protected MultiApiWireMockServer getMultiApiServer() {{
        return multiApiServer;
    }}
    
{getters_str}
}}'''
        
        test_dir = os.path.join(output_dir, 'test')
        os.makedirs(test_dir, exist_ok=True)
        
        with open(os.path.join(test_dir, 'BaseWireMockIntegrationTest.java'), 'w') as f:
            f.write(test_content)
        
        print(f"✓ Generated BaseWireMockIntegrationTest.java")
    
    def generate_build_files(self, output_dir: str):
        """Generate Maven pom.xml and Gradle build.gradle"""
        
        # Maven pom.xml
        pom_content = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>wiremock-generated-stubs</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <name>WireMock Generated Stubs</name>
    <description>Auto-generated WireMock configurations from OpenAPI specifications</description>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <wiremock.version>3.3.1</wiremock.version>
        <spring-boot.version>2.7.15</spring-boot.version>
        <junit.version>5.10.0</junit.version>
    </properties>
    
    <dependencies>
        <!-- WireMock -->
        <dependency>
            <groupId>com.github.tomakehurst</groupId>
            <artifactId>wiremock-jre8</artifactId>
            <version>${wiremock.version}</version>
        </dependency>
        
        <!-- Spring Boot Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>${spring-boot.version}</version>
            <scope>test</scope>
        </dependency>
        
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        
        <!-- Spring Context for @Component -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.3.23</version>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
            
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>'''
        
        with open(os.path.join(output_dir, 'pom.xml'), 'w') as f:
            f.write(pom_content)
        
        # Gradle build.gradle
        gradle_content = '''plugins {
    id 'java'
    id 'org.springframework.boot' version '2.7.15'
    id 'io.spring.dependency-management' version '1.0.15.RELEASE'
}

group = 'com.example'
version = '1.0.0'
sourceCompatibility = '11'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.github.tomakehurst:wiremock-jre8:3.3.1'
    implementation 'org.springframework:spring-context:5.3.23'
    
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

test {
    useJUnitPlatform()
}

jar {
    enabled = true
    archiveClassifier = ''
}'''
        
        with open(os.path.join(output_dir, 'build.gradle'), 'w') as f:
            f.write(gradle_content)
        
        print(f"✓ Generated pom.xml and build.gradle")
    
    def generate_java_readme(self, specs: List[Dict[str, str]], output_dir: str):
        """Generate comprehensive README for Java code"""
        api_list = '\n'.join([f"- {spec['api_name']}: {spec['filename']}" for spec in specs])
        
        readme_content = f'''# WireMock Java Integration

Auto-generated Java WireMock configurations from OpenAPI specifications.

**Generated on:** {self.timestamp}

## APIs Included
{api_list}

## Quick Start

### 1. Add Dependencies

**Maven:**
```xml
<dependency>
    <groupId>com.github.tomakehurst</groupId>
    <artifactId>wiremock-jre8</artifactId>
    <version>3.3.1</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

**Gradle:**
```gradle
testImplementation 'com.github.tomakehurst:wiremock-jre8:3.3.1'
testImplementation 'org.springframework.boot:spring-boot-starter-test'
```

### 2. Use in Tests

**Option 1: Single API**
```java
@SpringBootTest
@Import(ProductsWireMockConfig.class)
class ProductServiceTest {{
    @Autowired
    private String productsApiBaseUrl;
    
    @Test
    void shouldCallProductsApi() {{
        // Your test here
    }}
}}
```

**Option 2: Multiple APIs**
```java
@SpringBootTest
@Import(WireMockTestConfig.class)
class IntegrationTest extends BaseWireMockIntegrationTest {{
    @Test
    void shouldTestMultipleApis() {{
        String productsUrl = getProductsBaseUrl();
        String usersUrl = getUsersBaseUrl();
        // Test API interactions
    }}
}}
```

**Option 3: Manual Configuration**
```java
class ManualTest {{
    private MultiApiWireMockServer server = new MultiApiWireMockServer();
    
    @BeforeEach
    void setUp() {{
        server.startAllServers();
    }}
    
    @AfterEach
    void tearDown() {{
        server.stopAllServers();
    }}
}}
```

## Generated Classes

### Core Classes
- `MultiApiWireMockServer` - Main orchestrator for all APIs
- `WireMockTestConfig` - Spring Boot configuration for all APIs
- `BaseWireMockIntegrationTest` - Base test class for integration tests

### Per-API Classes
Each API gets:
- `<ApiName>WireMockConfig` - Spring configuration for single API
- `<ApiName>WireMockTest` - Base test class for API-specific tests

## Configuration

### Default Ports
- Base port: 8080
- Each API gets: basePort + index (8080, 8081, 8082, etc.)

### WireMock Files
Place your generated WireMock files in:
```
src/test/resources/wiremock/
├── products/
│   ├── mappings/
│   └── __files/
├── users/
│   ├── mappings/
│   └── __files/
```

## Advanced Usage

### Custom Stubs
```java
@Test
void testWithCustomStub() {{
    WireMockServer server = getMultiApiServer().getServer("products");
    
    server.stubFor(get(urlEqualTo("/custom"))
        .willReturn(aResponse()
            .withStatus(200)
            .withBody("custom response")));
}}
```

### Dynamic Configuration
```java
@Test
void testWithDynamicConfig() {{
    Map<String, String> urls = getMultiApiServer().getServerUrls();
    urls.forEach((api, url) -> {{
        // Configure your HTTP clients
        configureClient(api, url);
    }});
}}
```

### Health Checks
```java
@Test
void allServersHealthy() {{
    getMultiApiServer().getServerUrls().forEach((api, url) -> {{
        boolean isRunning = getMultiApiServer().isRunning(api);
        assertThat(isRunning).isTrue();
    }});
}}
```

## Troubleshooting

### Common Issues

**Port conflicts:**
```java
// Check if ports are available
server.getServerUrls().forEach((api, url) -> 
    System.out.println(api + " running on: " + url));
```

**Missing mapping files:**
```
Ensure mapping files are in src/test/resources/wiremock/<api_name>/mappings/
```

**Spring context issues:**
```java
// Make sure to import the configuration
@Import(WireMockTestConfig.class)
```

## Integration Examples

### RestTemplate
```java
@Test
void testWithRestTemplate() {{
    RestTemplate restTemplate = new RestTemplate();
    String url = getProductsBaseUrl() + "/products";
    
    ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
}}
```

### WebTestClient
```java
@Test
void testWithWebTestClient() {{
    WebTestClient client = WebTestClient.bindToServer()
        .baseUrl(getUsersBaseUrl())
        .build();
        
    client.get().uri("/users")
        .exchange()
        .expectStatus().isOk();
}}
```

---

**Generated by Multi-Spec WireMock Mapping Generator**
'''
        
        with open(os.path.join(output_dir, 'README.md'), 'w') as f:
            f.write(readme_content)
        
        print(f"✓ Generated Java README.md")
    
    def _to_class_name(self, api_name: str) -> str:
        """Convert API name to Java class name"""
        # Split by underscores and capitalize each part
        parts = api_name.split('_')
        return ''.join(part.capitalize() for part in parts)


def main():
    parser = argparse.ArgumentParser(
        description='Multi-Spec WireMock Mapping Generator with Java Code Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate only JSON mappings
  python multi_spec_wiremock_generator.py ./spec ./wiremock
  
  # Generate JSON mappings and Java code
  python multi_spec_wiremock_generator.py ./spec ./wiremock --java
  
  # Generate with custom Java package
  python multi_spec_wiremock_generator.py ./spec ./wiremock --java --package com.mycompany.wiremock
        '''
    )
    
    parser.add_argument('spec_dir', help='Directory containing OpenAPI specifications')
    parser.add_argument('output_dir', help='Output directory for generated files')
    parser.add_argument('--java', action='store_true', 
                       help='Generate Java WireMock configuration classes')
    parser.add_argument('--package', default='com.example.wiremock',
                       help='Java package name for generated classes (default: com.example.wiremock)')
    
    # Support legacy command line arguments
    if len(sys.argv) >= 3 and not sys.argv[1].startswith('-'):
        # Legacy mode: python script.py <spec_dir> <output_dir>
        args = parser.parse_args([sys.argv[1], sys.argv[2]] + sys.argv[3:])
    else:
        args = parser.parse_args()
    
    if not os.path.exists(args.spec_dir):
        print(f"❌ Spec directory not found: {args.spec_dir}")
        sys.exit(1)
    
    # Generate JSON mappings
    generator = MultiSpecWireMockGenerator(args.spec_dir, args.output_dir)
    generator.generate_all_mappings()
    
    # Generate Java code if requested
    if args.java:
        print(f"\n🔧 Generating Java WireMock integration code...")
        java_generator = JavaWireMockGenerator(args.package)
        specs = generator.discover_specs()
        java_generator.generate_java_code_for_apis(specs, args.output_dir)


if __name__ == "__main__":
    main()
