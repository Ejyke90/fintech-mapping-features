---
sidebar_position: 3
---

# Examples

Practical examples for using the CSV Parser microservice.

## Basic Usage

### Parse a Simple CSV File

**Sample CSV:**
```csv
name,age,email,department
John Doe,30,john@example.com,Engineering
Jane Smith,25,jane@example.com,Marketing
Bob Johnson,35,bob@example.com,Sales
```

**Python Example:**
```python
import requests

# Parse the CSV file
with open('employees.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f}
    )

result = response.json()
print(f"Status: {result['status']}")
print(f"Rows: {result['row_count']}")
print(f"Columns: {result['columns']}")

# Access data
for row in result['data']:
    print(f"{row['name']} - {row['department']}")
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/csv/parse \
  -F "file=@employees.csv" \
  | jq '.'
```

---

## Validation

### Validate CSV Structure

```python
import requests

with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/validate',
        files={'file': f}
    )

validation = response.json()

if validation['is_valid']:
    print("✓ CSV is valid")
    print(f"Rows: {validation['row_count']}")
    print(f"Columns: {validation['column_count']}")
else:
    print("✗ CSV has errors:")
    for error in validation['errors']:
        print(f"  - {error}")

# Check for missing values
if validation['missing_values']:
    print("\nMissing values found:")
    for col, count in validation['missing_values'].items():
        print(f"  {col}: {count} missing")
```

---

## Schema Extraction

### Get CSV Schema Information

```python
import requests

with open('financial_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/schema',
        files={'file': f}
    )

schema = response.json()

print(f"File size: {schema['estimated_size_mb']:.2f} MB")
print(f"Total rows: {schema['row_count']}")
print("\nColumns:")

for col in schema['columns']:
    print(f"\n  {col['name']}:")
    print(f"    Type: {col['dtype']}")
    print(f"    Nullable: {col['nullable']}")
    print(f"    Unique values: {col['unique_count']}")
    print(f"    Sample: {col['sample_values']}")
    
    if 'stats' in col:
        print(f"    Min: {col['stats']['min']}")
        print(f"    Max: {col['stats']['max']}")
        print(f"    Mean: {col['stats']['mean']}")
```

---

## Data Transformation

### Clean and Transform CSV Data

```python
import requests

# Transform with cleaning options
with open('messy_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/transform',
        files={'file': f},
        params={
            'remove_empty_rows': True,
            'remove_duplicates': True,
            'trim_whitespace': True,
            'lowercase_columns': True
        }
    )

result = response.json()
print(f"Original rows: {result['original_row_count']}")
print(f"Cleaned rows: {result['cleaned_row_count']}")
print(f"Removed: {result['original_row_count'] - result['cleaned_row_count']} rows")

# Save cleaned data
import json
with open('cleaned_data.json', 'w') as f:
    json.dump(result['data'], f, indent=2)
```

---

## Advanced Usage

### Process Large Files with Chunking

```python
import requests

# For files larger than 10MB, use chunking
with open('large_dataset.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f},
        params={'chunk_size': 5000}  # Process 5000 rows at a time
    )

result = response.json()
print(f"Processed {result['row_count']} rows")
```

### Handle Different Encodings and Delimiters

```python
import requests

# CSV with semicolon delimiter and ISO-8859-1 encoding
with open('european_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f},
        params={
            'auto_detect': True,  # Let the parser detect encoding and delimiter
        }
    )

# Or specify manually
with open('european_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f},
        params={
            'auto_detect': False,
            'encoding': 'iso-8859-1',
            'delimiter': ';'
        }
    )
```

---

## Integration Examples

### Prepare CSV for XML Transformation

```python
import requests

# Prepare CSV data for XML transformation
with open('payment_instructions.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/prepare-for-xml',
        files={'file': f}
    )

result = response.json()

if result['xml_ready']:
    print("✓ Data ready for XML transformation")
    print(f"Schema: {result['schema']}")
    
    # Use the data with XML Sanitizer
    xml_data = result['data']
    # ... transform to XML and send to XML Sanitizer
```

### Prepare CSV for Mapping Generation

```python
import requests

# Prepare CSV schema for intelligent mapping
with open('source_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/prepare-for-mapping',
        files={'file': f},
        params={'target_format': 'ISO20022_pain.001.001.09'}
    )

result = response.json()

if result['mapping_ready']:
    print("✓ Schema ready for mapping generation")
    print(f"Source schema: {result['source_schema']}")
    print(f"Sample data: {result['sample_data'][:3]}")
    
    # Send to Mapping Generator
    # mapping_response = requests.post(
    #     'http://localhost:8081/generate-mapping',
    #     json=result
    # )
```

---

## Error Handling

### Robust Error Handling

```python
import requests
from requests.exceptions import RequestException

def parse_csv_safely(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                'http://localhost:8000/api/csv/parse',
                files={'file': f},
                timeout=30
            )
        
        response.raise_for_status()
        result = response.json()
        
        if result['status'] == 'success':
            return result['data']
        else:
            print(f"Error: {result.get('message')}")
            return None
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
    except RequestException as e:
        print(f"Request failed: {e}")
        return None
    
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        return None

# Usage
data = parse_csv_safely('mydata.csv')
if data:
    print(f"Successfully parsed {len(data)} rows")
```

---

## Batch Processing

### Process Multiple CSV Files

```python
import requests
import os
from pathlib import Path

def process_csv_directory(directory_path):
    results = []
    
    for csv_file in Path(directory_path).glob('*.csv'):
        print(f"Processing {csv_file.name}...")
        
        try:
            with open(csv_file, 'rb') as f:
                response = requests.post(
                    'http://localhost:8000/api/csv/parse',
                    files={'file': f}
                )
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    'filename': csv_file.name,
                    'row_count': result['row_count'],
                    'column_count': result['column_count'],
                    'status': 'success'
                })
            else:
                results.append({
                    'filename': csv_file.name,
                    'status': 'error',
                    'error': response.text
                })
        
        except Exception as e:
            results.append({
                'filename': csv_file.name,
                'status': 'error',
                'error': str(e)
            })
    
    return results

# Process all CSVs in a directory
results = process_csv_directory('./data/')

# Print summary
print("\nProcessing Summary:")
print(f"Total files: {len(results)}")
print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")
```

---

## JavaScript/TypeScript Examples

### Using Fetch API

```typescript
async function parseCSV(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://localhost:8000/api/csv/parse', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log(`Parsed ${result.row_count} rows`);
    return result.data;
    
  } catch (error) {
    console.error('Error parsing CSV:', error);
    throw error;
  }
}

// Usage in React
function CSVUploader() {
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const data = await parseCSV(file);
      console.log('CSV data:', data);
    } catch (error) {
      alert('Failed to parse CSV');
    }
  };

  return <input type="file" accept=".csv" onChange={handleFileUpload} />;
}
```

---

## Next Steps

- Review the [API Reference](./api-reference.md) for complete endpoint documentation
- Check the [Integration Guide](../guides/integration-overview.md) for service orchestration patterns
- Explore the API Gateway documentation (see repository root)
