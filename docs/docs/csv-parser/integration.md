---
sidebar_position: 4
---

# Integration Guide

Learn how to integrate the CSV Parser with other microservices in the Fintech Mapping Features ecosystem.

## Integration Architecture

```
CSV Parser (Port 8000)
        ↓
    ┌───┴───┐
    ↓       ↓
XML         Mapping
Sanitizer   Generator
Port 8080   Port 8081
```

## Direct Integration Patterns

### 1. CSV Parser → XML Sanitizer

Transform CSV data into ISO 20022 XML format.

**Workflow:**
```
1. Upload CSV to CSV Parser
2. Parse and extract data
3. Transform JSON to XML
4. Send XML to XML Sanitizer
5. Receive cleaned XML
```

**Example:**
```python
import requests
import xml.etree.ElementTree as ET

def csv_to_sanitized_xml(csv_file_path):
    # Step 1: Parse CSV
    with open(csv_file_path, 'rb') as f:
        parse_response = requests.post(
            'http://localhost:8000/api/csv/prepare-for-xml',
            files={'file': f}
        )
    
    csv_data = parse_response.json()
    
    if not csv_data['xml_ready']:
        raise Exception("CSV not ready for XML transformation")
    
    # Step 2: Transform to XML (simple example)
    root = ET.Element('Document')
    for row in csv_data['data']:
        record = ET.SubElement(root, 'Record')
        for key, value in row.items():
            field = ET.SubElement(record, key)
            field.text = str(value)
    
    xml_string = ET.tostring(root, encoding='unicode')
    
    # Step 3: Sanitize XML
    sanitize_response = requests.post(
        'http://localhost:8080/sanitize-chars',
        data=xml_string,
        headers={'Content-Type': 'application/xml'}
    )
    
    return sanitize_response.text

# Usage
cleaned_xml = csv_to_sanitized_xml('payment_data.csv')
print(cleaned_xml)
```

---

### 2. CSV Parser → Mapping Generator

Generate intelligent field mappings from CSV schema.

**Workflow:**
```
1. Upload CSV to CSV Parser
2. Extract schema and sample data
3. Send to Mapping Generator
4. Receive field mappings
```

**Example:**
```python
import requests

def generate_mappings_from_csv(csv_file_path, target_format='ISO20022_pain.001.001.09'):
    # Step 1: Prepare CSV for mapping
    with open(csv_file_path, 'rb') as f:
        prepare_response = requests.post(
            'http://localhost:8000/api/csv/prepare-for-mapping',
            files={'file': f},
            params={'target_format': target_format}
        )
    
    csv_schema = prepare_response.json()
    
    if not csv_schema['mapping_ready']:
        raise Exception("CSV not ready for mapping")
    
    # Step 2: Generate mappings
    mapping_request = {
        'sourceSchema': csv_schema['source_schema'],
        'targetFormat': target_format,
        'sampleData': csv_schema['sample_data']
    }
    
    mapping_response = requests.post(
        'http://localhost:8081/generate-mapping',
        json=mapping_request
    )
    
    mappings = mapping_response.json()
    
    # Display mappings
    print(f"Generated {len(mappings)} mappings:")
    for mapping in mappings:
        print(f"  {mapping['source_field']} → {mapping['target_field']}")
        print(f"    Confidence: {mapping['confidence']}")
    
    return mappings

# Usage
mappings = generate_mappings_from_csv('source_data.csv')
```

---

## Via API Gateway (Recommended)

The API Gateway provides orchestrated workflows that combine multiple services.

### Full Transformation Pipeline

```python
import requests

def full_transformation_pipeline(csv_file_path):
    """
    Complete end-to-end transformation:
    CSV → Parse → Map → Transform → Sanitize
    """
    with open(csv_file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:3000/api/v1/transform-pipeline',
            files={'file': f},
            data={'targetSchema': 'ISO20022_pain.001.001.09'}
        )
    
    result = response.json()
    
    if result['success']:
        print(f"✓ Pipeline completed in {result['processingTime']}")
        print(f"  Source: {result['data']['source']['rowCount']} rows")
        print(f"  Mappings: {len(result['data']['mappings'])}")
        print(f"  XML length: {len(result['data']['xml'])} chars")
        
        return result['data']
    else:
        print(f"✗ Pipeline failed: {result['error']['message']}")
        return None

# Usage
result = full_transformation_pipeline('payments.csv')
```

### CSV to XML Only

```python
import requests

def csv_to_xml_via_gateway(csv_file_path):
    """Use API Gateway for CSV to XML transformation"""
    with open(csv_file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:3000/api/v1/csv-to-xml',
            files={'file': f}
        )
    
    result = response.json()
    
    if result['success']:
        return result['data']['xml']
    else:
        raise Exception(result['error']['message'])

# Usage
xml_output = csv_to_xml_via_gateway('data.csv')
with open('output.xml', 'w') as f:
    f.write(xml_output)
```

### CSV to Mapping Only

```python
import requests

def csv_to_mapping_via_gateway(csv_file_path, target_schema):
    """Use API Gateway for CSV to mapping generation"""
    with open(csv_file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:3000/api/v1/csv-to-mapping',
            files={'file': f},
            data={'targetSchema': target_schema}
        )
    
    result = response.json()
    
    if result['success']:
        return result['data']['mappings']
    else:
        raise Exception(result['error']['message'])

# Usage
mappings = csv_to_mapping_via_gateway(
    'source.csv',
    'ISO20022_pain.001.001.09'
)
```

---

## Service-to-Service Communication

### Async Integration with Message Queue

For production environments, use message queues for async processing:

```python
import pika
import json

def publish_csv_for_processing(csv_file_path, queue_name='csv-processing'):
    """Publish CSV to message queue for async processing"""
    
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    # Declare queue
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Read and encode file
    with open(csv_file_path, 'rb') as f:
        file_content = f.read()
    
    # Publish message
    message = {
        'file_name': csv_file_path,
        'file_content': file_content.decode('latin-1'),  # or base64
        'target_format': 'ISO20022_pain.001.001.09'
    }
    
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )
    
    print(f"Published {csv_file_path} to queue")
    connection.close()

# Usage
publish_csv_for_processing('large_dataset.csv')
```

---

## Docker Integration

### Docker Compose Network

All services communicate via Docker network:

```yaml
version: '3.8'

services:
  csv-parser:
    image: csv-parser:latest
    networks:
      - fintech-network
  
  xml-sanitizer:
    image: xml-sanitizer:latest
    networks:
      - fintech-network
  
  mapping-generator:
    image: mapping-generator:latest
    networks:
      - fintech-network

networks:
  fintech-network:
    driver: bridge
```

**Access services from within containers:**
```python
# Instead of localhost, use service names
CSV_PARSER_URL = 'http://csv-parser:8000'
XML_SANITIZER_URL = 'http://xml-sanitizer:8080'
MAPPING_GENERATOR_URL = 'http://mapping-generator:8081'
```

---

## Error Handling & Retry Logic

### Resilient Integration

```python
import requests
import time
from typing import Optional

def call_service_with_retry(
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    **kwargs
) -> Optional[requests.Response]:
    """
    Call a service with exponential backoff retry
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            
            wait_time = backoff_factor ** attempt
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
            time.sleep(wait_time)
    
    return None

# Usage
with open('data.csv', 'rb') as f:
    response = call_service_with_retry(
        'http://localhost:8000/api/csv/parse',
        files={'file': f},
        max_retries=3
    )

if response:
    result = response.json()
    print(f"Success: {result['row_count']} rows")
else:
    print("Failed to process CSV")
```

---

## Monitoring & Observability

### Request Tracking

Track requests across services:

```python
import requests
import uuid

def tracked_request(csv_file_path):
    """Make a request with correlation ID for tracking"""
    
    # Generate correlation ID
    correlation_id = str(uuid.uuid4())
    
    headers = {
        'X-Request-ID': correlation_id,
        'X-User-ID': 'user-123'
    }
    
    print(f"Request ID: {correlation_id}")
    
    # Parse CSV
    with open(csv_file_path, 'rb') as f:
        parse_response = requests.post(
            'http://localhost:8000/api/csv/parse',
            files={'file': f},
            headers=headers
        )
    
    # Check response headers
    response_id = parse_response.headers.get('X-Request-ID')
    print(f"Response ID: {response_id}")
    
    return parse_response.json()

# Usage - trace this request through all services
result = tracked_request('data.csv')
```

---

## Security Considerations

### API Authentication

```python
import requests

def authenticated_request(csv_file_path, api_key):
    """Make authenticated request to CSV Parser"""
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'X-API-Key': api_key
    }
    
    with open(csv_file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/api/csv/parse',
            files={'file': f},
            headers=headers
        )
    
    response.raise_for_status()
    return response.json()

# Usage
API_KEY = 'your-api-key-here'
result = authenticated_request('secure_data.csv', API_KEY)
```

---

## Performance Optimization

### Parallel Processing

```python
import concurrent.futures
import requests

def process_csv_file(file_path):
    """Process a single CSV file"""
    with open(file_path, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/api/csv/parse',
            files={'file': f}
        )
    return file_path, response.json()

def process_multiple_csvs(file_paths, max_workers=5):
    """Process multiple CSV files in parallel"""
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(process_csv_file, fp): fp 
            for fp in file_paths
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                file_path, result = future.result()
                results[file_path] = result
                print(f"✓ Processed {file_path}")
            except Exception as e:
                print(f"✗ Failed {file_path}: {e}")
                results[file_path] = None
    
    return results

# Usage
files = ['file1.csv', 'file2.csv', 'file3.csv', 'file4.csv']
results = process_multiple_csvs(files)
```

---

## Next Steps

- Review the [Integration Overview](../guides/integration-overview.md) for complete integration patterns
- Check the API Gateway documentation in the repository
- See the docker-compose.yml configuration in the repository root
- See [Examples](./examples.md) for more code samples
