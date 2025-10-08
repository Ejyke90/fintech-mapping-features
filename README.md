# fintech-ai-features

XML Sanitization Service - A REST API for sanitizing XML characters in financial documents.

## Requirements

- Java 21
- Gradle 8.5+

## Build and Run

Build the project:
```bash
./gradlew build
```

Run the application:
```bash
./gradlew bootRun
```

The application will start on port 8080.

## API Endpoint

### POST /sanitize-chars

Accepts XML payload (e.g., pain.001 format) and returns a sanitized response.

**Request:**
- Method: POST
- URL: `http://localhost:8080/sanitize-chars`
- Content-Type: `application/xml`
- Accept: `application/xml`
- Body: XML document (e.g., pain.001 format)

**Response:**
```xml
<Success>Yes</Success>
```

**Example:**
```bash
curl -X POST http://localhost:8080/sanitize-chars \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
    <CstmrCdtTrfInitn>
        <GrpHdr>
            <MsgId>MSG-001</MsgId>
        </GrpHdr>
    </CstmrCdtTrfInitn>
</Document>'
```