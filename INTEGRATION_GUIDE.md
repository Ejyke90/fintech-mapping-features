# Integration Guide

This guide explains how the three microservices integrate to provide end-to-end financial data transformation capabilities.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway (Port 3000)                  │
│                    Orchestration & Routing Layer                │
└──────────┬────────────────┬────────────────┬────────────────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────────┐
    │   CSV    │     │   XML    │    │   Mapping    │
    │  Parser  │     │Sanitizer │    │  Generator   │
    │          │     │          │    │              │
    │Port 8000 │     │Port 8080 │    │  Port 8081   │
    │ Python   │     │   Java   │    │    Java      │
    └──────────┘     └──────────┘    └──────────────┘
```

## Integration Patterns

### 1. CSV to XML Transformation

**Use Case**: Convert payment instructions from CSV to ISO 20022 XML format

**Workflow**:
```
1. Client uploads CSV file to API Gateway
2. Gateway sends CSV to CSV Parser for parsing
3. CSV Parser returns structured JSON data
4. Gateway transforms JSON to XML format
5. Gateway sends XML to XML Sanitizer
6. Sanitizer returns cleaned XML
7. Gateway returns final XML to client
```

**Example Request**:
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-xml \
  -F "file=@payment_instructions.csv"
```

**Example Response**:
```json
{
  "success": true,
  "requestId": "abc-123-def",
  "message": "CSV successfully transformed to XML",
  "data": {
    "originalRowCount": 150,
    "originalColumns": ["debtor_name", "creditor_name", "amount", "currency"],
    "xml": "<?xml version=\"1.0\"?>...</xml>"
  }
}
```

---

### 2. CSV to Intelligent Mapping

**Use Case**: Analyze CSV data structure and generate field mappings for transformation

**Workflow**:
```
1. Client uploads CSV file to API Gateway
2. Gateway sends CSV to CSV Parser for schema extraction
3. CSV Parser analyzes structure and returns schema
4. Gateway sends schema to Mapping Generator
5. Mapping Generator uses AI to create field mappings
6. Gateway returns mappings to client
```

**Example Request**:
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-mapping \
  -F "file=@payment_data.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

**Example Response**:
```json
{
  "success": true,
  "requestId": "xyz-789-ghi",
  "message": "Field mappings generated successfully",
  "data": {
    "sourceSchema": {
      "columns": [
        {
          "name": "debtor_name",
          "dtype": "object",
          "nullable": false
        }
      ],
      "row_count": 150
    },
    "targetFormat": "ISO20022_pain.001.001.09",
    "mappings": [
      {
        "source_field": "debtor_name",
        "target_field": "Dbtr.Nm",
        "confidence": 0.95,
        "transformation": "direct"
      }
    ]
  }
}
```

---

### 3. Full Transformation Pipeline

**Use Case**: Complete end-to-end transformation from CSV to ISO 20022 XML

**Workflow**:
```
1. Client uploads CSV file
2. Parse CSV and extract data
3. Extract schema for mapping
4. Generate intelligent field mappings
5. Apply mappings and transform to XML
6. Sanitize XML output
7. Return complete transformation result
```

**Example Request**:
```bash
curl -X POST http://localhost:3000/api/v1/transform-pipeline \
  -F "file=@payments.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

**Example Response**:
```json
{
  "success": true,
  "requestId": "pipeline-456",
  "message": "Full transformation pipeline completed successfully",
  "processingTime": "1250ms",
  "data": {
    "source": {
      "rowCount": 150,
      "columnCount": 8,
      "columns": ["debtor_name", "creditor_name", "amount", ...]
    },
    "mappings": [...],
    "xml": "<?xml version=\"1.0\"?>...</xml>"
  }
}
```

---

## Direct Service Integration

### CSV Parser Integration

**Endpoint**: `http://localhost:8000/api/csv/prepare-for-xml`

```python
import requests

# Prepare CSV for XML transformation
with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/prepare-for-xml',
        files={'file': f}
    )
    
data = response.json()
print(f"Ready for XML: {data['xml_ready']}")
print(f"Columns: {data['columns']}")
```

**Endpoint**: `http://localhost:8000/api/csv/prepare-for-mapping`

```python
# Prepare CSV for mapping generation
with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/prepare-for-mapping',
        files={'file': f},
        params={'target_format': 'ISO20022_pain.001.001.09'}
    )
    
data = response.json()
print(f"Schema: {data['source_schema']}")
print(f"Sample data: {data['sample_data'][:3]}")
```

---

### XML Sanitizer Integration

**Endpoint**: `http://localhost:8080/sanitize-chars`

```python
import requests

xml_content = """<?xml version="1.0"?>
<Document>
    <Payment>
        <Amount>1000.00</Amount>
    </Payment>
</Document>"""

response = requests.post(
    'http://localhost:8080/sanitize-chars',
    data=xml_content,
    headers={'Content-Type': 'application/xml'}
)

print(response.text)
```

---

### Mapping Generator Integration

**Endpoint**: `http://localhost:8081/generate-mapping`

```python
import requests

mapping_request = {
    "sourceSchema": {
        "columns": [
            {"name": "debtor_name", "dtype": "object"},
            {"name": "amount", "dtype": "float64"}
        ],
        "row_count": 100
    },
    "targetFormat": "ISO20022_pain.001.001.09"
}

response = requests.post(
    'http://localhost:8081/generate-mapping',
    json=mapping_request
)

mappings = response.json()
print(f"Generated {len(mappings)} mappings")
```

---

## Running with Docker Compose

### Start All Services

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api-gateway
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Service URLs

Once running, services are available at:

- **API Gateway**: http://localhost:3000
- **CSV Parser**: http://localhost:8000
- **XML Sanitizer**: http://localhost:8080
- **Mapping Generator**: http://localhost:8081

### Health Checks

```bash
# Check all services
curl http://localhost:3000/health
curl http://localhost:8000/health
curl http://localhost:8080/actuator/health
curl http://localhost:8081/actuator/health
```

---

## Error Handling

### Consistent Error Format

All services return errors in a consistent format:

```json
{
  "success": false,
  "error": {
    "message": "Detailed error description",
    "statusCode": 400,
    "requestId": "abc-123"
  }
}
```

### Common Error Codes

- **400 Bad Request**: Invalid input data
- **413 Payload Too Large**: File size exceeds limit
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Service error
- **503 Service Unavailable**: Downstream service unavailable

---

## Best Practices

### Request Correlation

Use request IDs for tracking across services:

```bash
curl -X POST http://localhost:3000/api/v1/transform-pipeline \
  -H "X-Request-ID: my-custom-id-123" \
  -F "file=@data.csv"
```

### Timeout Configuration

Set appropriate timeouts for long-running operations:

```python
import requests

response = requests.post(
    'http://localhost:3000/api/v1/transform-pipeline',
    files={'file': open('large_file.csv', 'rb')},
    timeout=60  # 60 seconds
)
```

### Retry Logic

Implement exponential backoff for resilience:

```python
import time
import requests

def call_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)
```

---

## Monitoring & Observability

### Distributed Tracing

Request IDs are propagated across all services for end-to-end tracing.

### Logging

All services use structured logging:

```json
{
  "timestamp": "2025-10-16T10:30:00.000Z",
  "level": "info",
  "service": "api-gateway",
  "requestId": "abc-123",
  "message": "Pipeline completed",
  "duration": "1250ms"
}
```

### Metrics

Monitor key metrics:
- Request latency
- Success/error rates
- File sizes processed
- Transformation throughput

---

## Security Considerations

### File Upload Validation

- Maximum file size: 10MB (configurable)
- Allowed extensions: .csv, .txt, .tsv
- Content-type validation
- Virus scanning (recommended for production)

### CORS Configuration

Configure CORS origins in production:

```env
CORS_ORIGINS=https://your-domain.com,https://app.your-domain.com
```

### API Authentication

Add authentication middleware for production:

```typescript
// Example: JWT authentication
app.use('/api/v1', authenticateJWT, orchestrationRouter);
```

---

## Performance Optimization

### Streaming Large Files

For files > 10MB, use streaming:

```python
# CSV Parser with chunking
parser.parse_file(content, chunk_size=10000)
```

### Caching

Cache schema analysis results:

```typescript
const schemaCache = new Map();

if (schemaCache.has(fileHash)) {
  return schemaCache.get(fileHash);
}
```

### Parallel Processing

Process multiple files concurrently:

```python
import asyncio

async def process_files(files):
    tasks = [transform_file(f) for f in files]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Next Steps

1. **Add Message Queue**: Implement Kafka/RabbitMQ for async processing
2. **Add Database**: Store transformation history and mappings
3. **Add Metrics**: Implement Prometheus metrics
4. **Add Tracing**: Add Jaeger/Zipkin for distributed tracing
5. **Add Authentication**: Implement OAuth2/JWT authentication
6. **Add Rate Limiting**: Protect services from abuse
