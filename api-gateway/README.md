# API Gateway & Orchestrator

API Gateway and orchestration service for coordinating between CSV Parser, XML Sanitizer, and Intelligent Mapping Generator microservices.

## Features

- **Service Orchestration**: Coordinate workflows across multiple microservices
- **CSV to XML Pipeline**: Parse CSV files and transform to ISO 20022 XML
- **Mapping Generation**: Analyze CSV schemas and generate field mappings
- **Full Transformation Pipeline**: End-to-end data transformation workflows
- **Request Tracking**: Correlation IDs for distributed tracing
- **Error Handling**: Centralized error handling and logging

## Architecture

```
Client Request
     ↓
API Gateway (Port 3000)
     ↓
  ┌──┴──┬─────────┬──────────┐
  ↓     ↓         ↓          ↓
CSV   XML    Mapping    Response
Parser Sanitizer Generator
```

## Installation

```bash
# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# Build TypeScript
npm run build
```

## Running

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm run build
npm start
```

## API Endpoints

### Health Check
```bash
GET /health
```

### CSV to XML Transformation
```bash
POST /api/v1/csv-to-xml
Content-Type: multipart/form-data

file: <csv-file>
```

**Response:**
```json
{
  "success": true,
  "requestId": "uuid",
  "message": "CSV successfully transformed to XML",
  "data": {
    "originalRowCount": 100,
    "originalColumns": ["name", "amount", "date"],
    "xml": "<Document>...</Document>"
  }
}
```

### CSV to Mapping Generation
```bash
POST /api/v1/csv-to-mapping
Content-Type: multipart/form-data

file: <csv-file>
targetSchema: ISO20022_pain.001.001.09
```

**Response:**
```json
{
  "success": true,
  "requestId": "uuid",
  "message": "Field mappings generated successfully",
  "data": {
    "sourceSchema": {...},
    "targetFormat": "ISO20022_pain.001.001.09",
    "mappings": [...]
  }
}
```

### Full Transformation Pipeline
```bash
POST /api/v1/transform-pipeline
Content-Type: multipart/form-data

file: <csv-file>
targetSchema: ISO20022_pain.001.001.09
```

**Response:**
```json
{
  "success": true,
  "requestId": "uuid",
  "message": "Full transformation pipeline completed successfully",
  "processingTime": "1250ms",
  "data": {
    "source": {
      "rowCount": 100,
      "columnCount": 5,
      "columns": [...]
    },
    "mappings": [...],
    "xml": "<Document>...</Document>"
  }
}
```

## Usage Examples

### Using cURL

```bash
# CSV to XML
curl -X POST http://localhost:3000/api/v1/csv-to-xml \
  -F "file=@payments.csv"

# CSV to Mapping
curl -X POST http://localhost:3000/api/v1/csv-to-mapping \
  -F "file=@payments.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"

# Full Pipeline
curl -X POST http://localhost:3000/api/v1/transform-pipeline \
  -F "file=@payments.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

### Using JavaScript/TypeScript

```typescript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('targetSchema', 'ISO20022_pain.001.001.09');

const response = await fetch('http://localhost:3000/api/v1/transform-pipeline', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

### Using Python

```python
import requests

with open('payments.csv', 'rb') as f:
    files = {'file': f}
    data = {'targetSchema': 'ISO20022_pain.001.001.09'}
    
    response = requests.post(
        'http://localhost:3000/api/v1/transform-pipeline',
        files=files,
        data=data
    )
    
    print(response.json())
```

## Configuration

Edit `.env` file:

```env
PORT=3000
CSV_PARSER_URL=http://localhost:8000
XML_SANITIZER_URL=http://localhost:8080
MAPPING_GENERATOR_URL=http://localhost:8081
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "statusCode": 400,
    "requestId": "uuid"
  }
}
```

## Logging

Structured JSON logging with Winston:

```json
{
  "level": "info",
  "message": "CSV to XML transformation completed",
  "requestId": "abc-123",
  "timestamp": "2025-10-16T10:30:00.000Z"
}
```

## Development

```bash
# Run with auto-reload
npm run watch

# Run tests
npm test

# Lint code
npm run lint
```

## Docker

```bash
# Build image
docker build -t api-gateway:latest .

# Run container
docker run -p 3000:3000 \
  -e CSV_PARSER_URL=http://csv-parser:8000 \
  -e XML_SANITIZER_URL=http://xml-sanitizer:8080 \
  -e MAPPING_GENERATOR_URL=http://mapping-generator:8081 \
  api-gateway:latest
```

## Integration with Services

The gateway orchestrates three core services:

1. **CSV Parser** (Python/FastAPI - Port 8000)
   - Parse and validate CSV files
   - Extract schemas
   - Data transformation

2. **XML Sanitizer** (Java/Spring Boot - Port 8080)
   - Clean XML payloads
   - Remove invalid characters

3. **Intelligent Mapping Generator** (Java/Spring Boot - Port 8081)
   - Generate field mappings
   - AI-powered mapping suggestions
