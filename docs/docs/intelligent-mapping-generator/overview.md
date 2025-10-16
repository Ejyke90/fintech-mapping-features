---
sidebar_position: 1
---

# Intelligent Mapping Generator Overview

The **Intelligent Mapping Generator** microservice provides advanced data transformation capabilities for fintech applications with ISO 20022 message processing support.

## Purpose

Generate and manage intelligent mappings between different fintech data formats, with special focus on ISO 20022 payment message standards (PAIN, PACS).

## Key Features

- ✅ Intelligent mapping generation
- ✅ ISO 20022 standard support
- ✅ ActiveMQ Artemis messaging integration
- ✅ CBPR+ (Cross-Border Payments and Reporting Plus) support
- ✅ REST API interface
- ✅ OpenAPI/Swagger documentation

## Service Details

| Property | Value |
|----------|-------|
| **Port** | 8081 |
| **Context Path** | `/` |
| **Package** | `com.fintech.mapping` |
| **OpenAPI Docs** | `/v3/api-docs` |
| **Swagger UI** | `/swagger-ui.html` |
| **Message Broker** | ActiveMQ Artemis (Embedded) |

## Supported ISO 20022 Messages

- **pain.001.001.09** - Customer Credit Transfer Initiation
- **pain.002.001.10** - Payment Status Report
- **pacs.008.001.08** - Financial Institution Credit Transfer
- **pacs.002.001.10** - Payment Status Report
- **pacs.004.001.09** - Payment Return

## Quick Example

### Request
```bash
curl -X POST http://localhost:8081/generate-mapping \
  -H "Content-Type: application/json" \
  -d '{
    "sourceFormat": "pain.001.001.09",
    "targetFormat": "pacs.008.001.08",
    "mappingType": "PAYMENT_INITIATION"
  }'
```

### Response
```json
{
  "mappingId": "map-12345",
  "status": "GENERATED",
  "fields": [
    {
      "source": "CstmrCdtTrfInitn.GrpHdr.MsgId",
      "target": "FIToFICstmrCdtTrf.GrpHdr.MsgId",
      "transformation": "DIRECT"
    }
  ]
}
```

## Architecture Components

### Message Processing
- **Embedded Artemis Broker**: In-memory message queue
- **JMS Integration**: Asynchronous message handling
- **Transaction Management**: ACID compliance

### Data Transformation
- **JAXB**: XML marshalling/unmarshalling
- **XSD Validation**: Schema validation
- **Custom Transformers**: Business logic implementation

## Configuration

Located in `intelligent-mapping-generator/src/main/resources/application.properties`:

```properties
spring.application.name=intelligent-mapping-generator
server.port=8081

# SpringDoc OpenAPI
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html

# ActiveMQ Artemis
spring.artemis.mode=embedded
spring.artemis.embedded.enabled=true
spring.artemis.embedded.persistent=false
```

## Running the Service

```bash
# From project root
./gradlew :intelligent-mapping-generator:bootRun

# Or build and run JAR
./gradlew :intelligent-mapping-generator:build
java -jar intelligent-mapping-generator/build/libs/intelligent-mapping-generator-0.0.1-SNAPSHOT.jar
```

## Dependencies

```gradle
// ActiveMQ Artemis
implementation 'org.springframework.boot:spring-boot-starter-artemis'
implementation 'org.apache.activemq:artemis-jakarta-server:2.31.2'

// XML Processing
implementation 'javax.xml.bind:jaxb-api:2.3.1'
implementation 'com.sun.xml.bind:jaxb-impl:2.3.9'

// SpringDoc OpenAPI
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
```

## Next Steps

- [Getting Started](/guides/getting-started)
- [System Architecture](/architecture/overview)
- [XML Sanitizer](/xml-sanitizer/overview)
- [Back to Overview](/intro)
