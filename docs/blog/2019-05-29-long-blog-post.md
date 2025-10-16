---
slug: iso20022-microservices
title: Building ISO 20022-Compliant Microservices with Spring Boot
authors: [ejike]
tags: [iso20022, fintech, spring-boot, microservices, payments]
---

Deep dive into how we built ISO 20022-compliant microservices for financial message processing using Spring Boot 3.2.1 and Java 21.

<!-- truncate -->

## Understanding ISO 20022

ISO 20022 is the international standard for electronic data interchange between financial institutions. It provides a common platform for developing messages using XML and JSON.

### Key Message Types We Support

**PAIN Messages (Payments Initiation)**
- `pain.001.001.09` - Customer Credit Transfer Initiation
- `pain.002.001.10` - Payment Status Report

**PACS Messages (Payments Clearing and Settlement)**
- `pacs.008.001.08` - Financial Institution Credit Transfer
- `pacs.002.001.10` - Payment Status Report
- `pacs.004.001.09` - Payment Return

## Architecture Overview

Our monorepo contains two specialized microservices:

### 1. XML Sanitizer (Port 8080)
Ensures XML compliance before processing financial messages. Critical for handling ISO 20022 XML payloads that may contain invalid characters.

### 2. Intelligent Mapping Generator (Port 8081)
Transforms between different ISO 20022 message formats. For example, mapping `pain.001.001.09` (customer-initiated payment) to `pacs.008.001.08` (interbank credit transfer).

## Technical Implementation

### JAXB for XML Processing
```java
@XmlRootElement(name = "Document")
@XmlAccessorType(XmlAccessType.FIELD)
public class Pain00100109 {
    @XmlElement(name = "CstmrCdtTrfInitn")
    private CustomerCreditTransferInitiation creditTransfer;
}
```

### ActiveMQ Artemis Integration
We use embedded ActiveMQ Artemis for asynchronous message processing:

```properties
spring.artemis.mode=embedded
spring.artemis.embedded.enabled=true
spring.artemis.embedded.persistent=false
```

## Benefits of Our Approach

✅ **Compliance** - Full ISO 20022 standard adherence  
✅ **Scalability** - Stateless microservices can scale horizontally  
✅ **Modularity** - Independent deployment of sanitizer and mapper  
✅ **Performance** - Java 21 with virtual threads support  
✅ **Developer Experience** - Comprehensive API documentation

## What's Next?

We're planning to add support for:
- ISO 20022 CAMT messages (Cash Management)
- Real-time validation against XSD schemas
- Message routing based on BIC codes
- Enhanced error handling and retry logic

Stay tuned for more updates!

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elementum dignissim ultricies. Fusce rhoncus ipsum tempor eros aliquam consequat. Lorem ipsum dolor sit amet
