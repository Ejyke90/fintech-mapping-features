#!/bin/bash

# Test script for pain.001 validation service
# Usage: ./test-validation.sh

BASE_URL="http://localhost:8081/api/pain001"
SCHEMA_DIR="../schemas/iso20022"

echo "======================================"
echo "pain.001 Validation Service - Test Script"
echo "======================================"
echo ""

# Test 1: Health Check
echo "1. Testing Health Endpoint..."
curl -s $BASE_URL/health | jq .
echo ""

# Test 2: Submit ISO Standard pain.001
echo "2. Submitting ISO Standard pain.001 message..."
curl -s -X POST $BASE_URL/submit \
  -H "Content-Type: application/xml" \
  -d @"$SCHEMA_DIR/sample_iso_pain.001.001.09.xml" | jq .
echo ""
echo "Check application logs for validation results!"
echo ""

# Wait a moment for processing
sleep 2

# Test 3: Submit CBPR+ pain.001
echo "3. Submitting CBPR+ pain.001 message..."
curl -s -X POST $BASE_URL/submit \
  -H "Content-Type: application/xml" \
  -d @"$SCHEMA_DIR/sample_cbpr_pain.001.001.09.xml" | jq .
echo ""
echo "Check application logs for validation results!"
echo ""

echo "======================================"
echo "Testing Complete!"
echo "======================================"
