---
sidebar_position: 2
---

# API Reference

Complete API reference for the CSV Parser microservice.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET /health

Check if the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Parse CSV

#### POST /api/csv/parse

Parse a CSV file and return its contents as JSON.

**Parameters:**
- `file` (required): CSV file to parse
- `auto_detect` (optional, default: true): Auto-detect encoding and delimiter
- `encoding` (optional): Character encoding (e.g., 'utf-8', 'iso-8859-1')
- `delimiter` (optional): CSV delimiter (e.g., ',', ';', '\t')
- `chunk_size` (optional): Process file in chunks for large files

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/csv/parse?auto_detect=true" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data.csv"
```

**Response:**
```json
{
  "status": "success",
  "message": "CSV file parsed successfully",
  "row_count": 100,
  "column_count": 5,
  "columns": ["name", "age", "email", "salary", "department"],
  "data": [
    {
      "name": "John Doe",
      "age": 30,
      "email": "john@example.com",
      "salary": 50000,
      "department": "Engineering"
    }
  ]
}
```

---

### Validate CSV

#### POST /api/csv/validate

Validate CSV structure without returning the full dataset.

**Parameters:**
- `file` (required): CSV file to validate
- `auto_detect` (optional, default: true): Auto-detect encoding and delimiter

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/csv/validate" \
  -F "file=@data.csv"
```

**Response:**
```json
{
  "is_valid": true,
  "row_count": 100,
  "column_count": 5,
  "columns": ["name", "age", "email", "salary", "department"],
  "missing_values": {
    "age": 2,
    "email": 1
  },
  "data_types": {
    "name": "object",
    "age": "float64",
    "email": "object",
    "salary": "int64",
    "department": "object"
  },
  "errors": []
}
```

---

### Get Schema

#### POST /api/csv/schema

Extract schema information from CSV file.

**Parameters:**
- `file` (required): CSV file to analyze
- `auto_detect` (optional, default: true): Auto-detect encoding and delimiter

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/csv/schema" \
  -F "file=@data.csv"
```

**Response:**
```json
{
  "row_count": 100,
  "estimated_size_mb": 0.05,
  "columns": [
    {
      "name": "name",
      "dtype": "object",
      "nullable": false,
      "unique_count": 98,
      "sample_values": ["John Doe", "Jane Smith", "Bob Johnson"]
    },
    {
      "name": "age",
      "dtype": "int64",
      "nullable": true,
      "unique_count": 45,
      "sample_values": [30, 25, 35],
      "stats": {
        "min": 22,
        "max": 65,
        "mean": 38.5
      }
    }
  ]
}
```

---

### Transform CSV

#### POST /api/csv/transform

Transform and clean CSV data.

**Parameters:**
- `file` (required): CSV file to transform
- `auto_detect` (optional, default: true): Auto-detect encoding and delimiter
- `remove_empty_rows` (optional, default: false): Remove empty rows
- `remove_duplicates` (optional, default: false): Remove duplicate rows
- `trim_whitespace` (optional, default: true): Trim whitespace from strings
- `lowercase_columns` (optional, default: false): Convert column names to lowercase

**Request Example:**
```bash
curl -X POST "http://localhost:8000/api/csv/transform?remove_duplicates=true&trim_whitespace=true" \
  -F "file=@data.csv"
```

**Response:**
```json
{
  "status": "success",
  "message": "CSV transformed successfully",
  "original_row_count": 100,
  "cleaned_row_count": 95,
  "data": [
    {
      "name": "John Doe",
      "age": 30,
      "email": "john@example.com"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid file type. Only CSV, TXT, and TSV files are allowed."
}
```

### 413 Payload Too Large
```json
{
  "detail": "File too large. Maximum size is 10MB"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Python Client Example

```python
import requests

# Parse CSV
with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f},
        params={'auto_detect': True}
    )
    
if response.status_code == 200:
    result = response.json()
    print(f"Parsed {result['row_count']} rows")
    print(f"Columns: {result['columns']}")
else:
    print(f"Error: {response.json()['detail']}")
```

---

## JavaScript/TypeScript Client Example

```typescript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/csv/parse?auto_detect=true', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Parsed ${result.row_count} rows`);
```
