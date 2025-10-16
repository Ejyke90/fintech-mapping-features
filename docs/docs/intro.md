---
sidebar_position: 1
slug: /
---

# Welcome to Fintech Mapping Features

A **multi-module Spring Boot monorepo** providing microservices for fintech data transformation and ISO 20022 message processing.

## 🎯 Overview

This project contains two independent Spring Boot microservices designed for fintech operations:

### 1. XML Sanitizer (Port 8080)
Sanitizes XML payloads by removing invalid characters and ensuring XML compliance.

### 2. Intelligent Mapping Generator (Port 8081)
Generates intelligent mappings for fintech data transformations with ISO 20022 support and ActiveMQ Artemis integration.

## 🚀 Quick Start

### Prerequisites
- Java 21
- Gradle 8.x
- Git

### Clone the Repository
```bash
git clone https://github.com/Ejyke90/fintech-mapping-features.git
cd fintech-mapping-features
```

### Build All Modules
```bash
./gradlew build
```

### Run Services

#### XML Sanitizer (Terminal 1)
```bash
./gradlew :xml-sanitizer:bootRun
# Service available at http://localhost:8080
```

#### Intelligent Mapping Generator (Terminal 2)
```bash
./gradlew :intelligent-mapping-generator:bootRun
# Service available at http://localhost:8081
```

## 📚 API Documentation

Each microservice provides interactive API documentation via Swagger UI:

- **XML Sanitizer**: [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
- **Mapping Generator**: [http://localhost:8081/swagger-ui.html](http://localhost:8081/swagger-ui.html)
