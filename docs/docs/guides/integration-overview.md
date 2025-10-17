---
sidebar_position: 1
---

# Integration Guide

Complete guide for integrating the Fintech Mapping Features microservices.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway (Port 3000)                  │
│                    Orchestration & Routing Layer                │
└──────────┬────────────────┬────────────────┬────────────────────┘
           │                │                │
           ▼                ▼                ▼
    ┌──────────┐     ┌──────────┐    ┌──────────────┐
    │   CSV    │     │   XML    │    │   Mapping    │
    │  Parser  │     │Sanitizer │    │  Generator   │
    │          │     │          │    │              │
    │Port 8000 │     │Port 8080 │    │  Port 8081   │
    │ Python   │     │   Java   │    │    Java      │
    └──────────┘     └──────────┘    └──────────────┘
```

## Quick Start with Docker Compose

The easiest way to run all services together:

```bash
# Start all services
docker-compose up -d

# Check health
curl http://localhost:3000/health

# Stop all services
docker-compose down
```

## Integration Patterns

### 1. CSV to XML Transformation

**Workflow**: CSV → Parse → Transform → Sanitize → XML

**Example**:
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-xml \
  -F "file=@payment_data.csv"
```

### 2. CSV to Mapping Generation

**Workflow**: CSV → Schema Extraction → AI Mapping → Mappings

**Example**:
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-mapping \
  -F "file=@payment_data.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

### 3. Full Transformation Pipeline

**Workflow**: CSV → Parse → Map → Transform → Sanitize → Complete

**Example**:
```bash
curl -X POST http://localhost:3000/api/v1/transform-pipeline \
  -F "file=@payments.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

## Service URLs

When running with Docker Compose:

- **API Gateway**: http://localhost:3000
- **CSV Parser**: http://localhost:8000
- **XML Sanitizer**: http://localhost:8080
- **Mapping Generator**: http://localhost:8081

## For More Details

See the full [INTEGRATION_GUIDE.md](https://github.com/Ejyke90/fintech-mapping-features/blob/intelligentMappingPoC/INTEGRATION_GUIDE.md) in the repository root for:

- Detailed workflow diagrams
- Advanced integration patterns
- Error handling strategies
- Security best practices
- Performance optimization
- Monitoring and observability
