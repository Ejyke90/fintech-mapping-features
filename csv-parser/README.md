# CSV Parser Microservice

A Python-based microservice for parsing and processing CSV files for financial data transformation.

## Features

- Parse CSV files with various delimiters and encodings
- Validate CSV structure and data types
- Transform CSV data to JSON format
- Support for large file processing with streaming
- Data validation and cleansing
- REST API endpoints for file upload and processing

## Requirements

- Python 3.9+
- pandas
- FastAPI
- python-dotenv

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running the Service

```bash
python src/main.py
```

The service will start on `http://localhost:8000`

### API Endpoints

- `POST /api/csv/parse` - Upload and parse a CSV file
- `POST /api/csv/validate` - Validate CSV structure
- `POST /api/csv/schema` - Get detected schema from CSV
- `POST /api/csv/transform` - Transform CSV to JSON

### Example

```python
import requests

# Parse a CSV file
with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/csv/parse',
        files={'file': f}
    )
    
print(response.json())
```

## Configuration

Configure the service using environment variables or `.env` file:

```
CSV_MAX_FILE_SIZE=10485760  # 10MB
CSV_UPLOAD_DIR=./uploads
CSV_ALLOWED_EXTENSIONS=.csv,.txt
```

## Docker

```bash
# Build image
docker build -t csv-parser:latest .

# Run container
docker run -p 8000:8000 csv-parser:latest
```

## Integration with Other Modules

This CSV parser can be used in conjunction with:
- **XML Sanitizer**: Convert CSV to XML for ISO 20022 processing
- **Intelligent Mapping Generator**: Use CSV data as source for mapping generation

## Testing

```bash
pytest tests/
```
