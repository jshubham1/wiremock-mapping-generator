#!/bin/bash

# Script to generate WireMock mappings from multiple OpenAPI specifications
set -e

echo "=== Multi-Spec WireMock Mapping Generator ==="

# Configuration
SPEC_DIR="/spec"
MAPPINGS_DIR="/output/mappings"
FILES_DIR="/output/__files"

# Create output directories if they don't exist
mkdir -p "$MAPPINGS_DIR"
mkdir -p "$FILES_DIR"

# Check if spec directory exists
if [ ! -d "$SPEC_DIR" ]; then
    echo "Error: Spec directory not found at $SPEC_DIR"
    exit 1
fi

echo "Processing OpenAPI specs from: $SPEC_DIR"

# Parse the OpenAPI spec and generate mappings using Multi-Spec Python script
echo "Using Multi-Spec WireMock Generator..."
python3 /scripts/multi_spec_wiremock_generator.py /spec /output

echo "=== Mapping generation completed ==="
echo "Mappings saved to: $MAPPINGS_DIR"
echo "Response files saved to: $FILES_DIR"

# List generated files
echo "Generated mapping files:"
ls -la "$MAPPINGS_DIR"

echo "Generated response files:"
ls -la "$FILES_DIR"
