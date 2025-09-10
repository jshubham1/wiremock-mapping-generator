#!/bin/bash

# Script to generate WireMock mappings from OpenAPI specification
set -e

echo "=== WireMock OpenAPI Mapping Generator ==="

# Configuration
SPEC_FILE="/spec/open-api-spec.yaml"
MAPPINGS_DIR="/output/mappings"
FILES_DIR="/output/__files"

# Create output directories if they don't exist
mkdir -p "$MAPPINGS_DIR"
mkdir -p "$FILES_DIR"

# Check if OpenAPI spec exists
if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: OpenAPI spec file not found at $SPEC_FILE"
    exit 1
fi

echo "Processing OpenAPI spec: $SPEC_FILE"

# Parse the OpenAPI spec and generate mappings using Enhanced Python script
echo "Using Enhanced OpenAPI to WireMock Generator..."
python3 /scripts/enhanced_openapi_to_wiremock.py "$SPEC_FILE" "$MAPPINGS_DIR" "$FILES_DIR"

echo "=== Mapping generation completed ==="
echo "Mappings saved to: $MAPPINGS_DIR"
echo "Response files saved to: $FILES_DIR"

# List generated files
echo "Generated mapping files:"
ls -la "$MAPPINGS_DIR"

echo "Generated response files:"
ls -la "$FILES_DIR"
