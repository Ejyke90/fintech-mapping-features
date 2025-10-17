---
sidebar_position: 1
---

# CSV Parser Overview

The CSV Parser is a Python-based microservice that provides robust parsing, validation, and transformation capabilities for CSV files in financial data processing workflows.

## Features

### 🔍 Auto-Detection
- Automatic encoding detection (UTF-8, ISO-8859-1, etc.)
- Delimiter detection (comma, semicolon, tab, pipe)
- Smart handling of various CSV formats

### ✅ Validation
- Structure validation
- Data type detection
- Missing value analysis
- Duplicate detection

### 🔄 Transformation
- CSV to JSON conversion
- Data cleansing and normalization
- Column name standardization
- Whitespace trimming

### 📊 Schema Extraction
- Column metadata extraction
- Data type inference
- Statistical analysis for numeric columns
- Sample value preview

## Architecture

The CSV Parser is built with:
- **FastAPI** - Modern, high-performance web framework
- **Pandas** - Powerful data manipulation library
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Lightning-fast ASGI server

```
csv-parser/
├── src/
│   ├── main.py          # FastAPI application
│   └── parser.py        # Core CSV parsing logic
├── tests/
│   └── test_parser.py   # Unit tests
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Quick Start

### Installation

```bash
cd csv-parser

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Service

```bash
# Start the server
python src/main.py
```

The service will be available at `http://localhost:8000`

### Using Docker

```bash
# Build the image
docker build -t csv-parser:latest .

# Run the container
docker run -p 8000:8000 csv-parser:latest
```

## API Documentation

Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Integration

The CSV Parser integrates seamlessly with other modules:

- **XML Sanitizer**: Convert CSV data to ISO 20022 XML format
- **Intelligent Mapping Generator**: Use CSV as source data for field mapping

## Configuration

Configure via environment variables or `.env` file:

```bash
CSV_MAX_FILE_SIZE=10485760  # 10MB
CSV_UPLOAD_DIR=./uploads
CSV_ALLOWED_EXTENSIONS=.csv,.txt,.tsv
API_HOST=0.0.0.0
API_PORT=8000
```

## Next Steps

- [API Reference](./api-reference.md) - Detailed API documentation
- [Examples](./examples.md) - Usage examples and code snippets
- [Integration Guide](./integration.md) - Connecting with other services
