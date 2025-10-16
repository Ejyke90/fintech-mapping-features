---
sidebar_position: 1
---

# XML Sanitizer Overview (Coming Soon)

The **XML Sanitizer** microservice is planned for future development.

## 🚧 Status: Planned

This module will provide robust XML processing capabilities, focusing on cleaning and validating XML payloads for fintech applications.

## Purpose

Future module that will remove invalid characters and ensure XML compliance before processing financial messages, particularly for ISO 20022 standards.

## Key Features

- ✅ Invalid character removal
- ✅ XML well-formedness validation
- ✅ REST API interface
- ✅ Spring Boot integration
- ✅ OpenAPI/Swagger documentation

## Service Details

| Property | Value |
|----------|-------|
| **Port** | 8080 |
| **Context Path** | `/` |
| **Package** | `com.fintech.sanitizer` |
| **OpenAPI Docs** | `/v3/api-docs` |
| **Swagger UI** | `/swagger-ui.html` |

## Quick Example

### Request
```bash
curl -X POST http://localhost:8080/sanitize-chars \
  -H "Content-Type: application/xml" \
  -d '<payment><amount>1000€</amount></payment>'
```

### Response
```xml
<payment><amount>1000</amount></payment>
```

## API Endpoints

The service exposes RESTful endpoints for XML sanitization. See the [API Reference](/docs/xml-sanitizer/api) for complete documentation.

## Configuration

Located in `xml-sanitizer/src/main/resources/application.properties`:

```properties
spring.application.name=xml-sanitizer
server.port=8080
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
```

## Running the Service

```bash
# From project root
./gradlew :xml-sanitizer:bootRun

# Or build and run JAR
./gradlew :xml-sanitizer:build
java -jar xml-sanitizer/build/libs/xml-sanitizer-0.0.1-SNAPSHOT.jar
```

## Next Steps

- [Getting Started](/docs/guides/getting-started)
- [System Architecture](/docs/architecture/overview)
- [Intelligent Mapping Generator](/docs/intelligent-mapping-generator/overview)
- [Back to Overview](/)
