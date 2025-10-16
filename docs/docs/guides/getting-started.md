---
sidebar_position: 1
---

# Getting Started

This guide will help you set up and run the Fintech Mapping Features monorepo locally.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Java JDK | 21+ | Runtime environment |
| Gradle | 8.x | Build automation |
| Git | Latest | Source control |

### Optional Tools

| Tool | Purpose |
|------|---------|
| Docker | Containerization |
| IntelliJ IDEA | IDE (recommended) |
| Postman | API testing |

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Ejyke90/fintech-mapping-features.git
cd fintech-mapping-features
```

### 2. Verify Java Installation

```bash
java -version
# Should output: openjdk version "21" or higher
```

### 3. Build the Project

Build all modules:

```bash
./gradlew clean build
```

Build specific module:

```bash
./gradlew :xml-sanitizer:build
./gradlew :intelligent-mapping-generator:build
```

### 4. Run Tests

```bash
# Run all tests
./gradlew test

# Run tests for specific module
./gradlew :xml-sanitizer:test
./gradlew :intelligent-mapping-generator:test
```

## Running the Services

### Option 1: Using Gradle (Recommended for Development)

Open two terminal windows:

#### Terminal 1: XML Sanitizer
```bash
./gradlew :xml-sanitizer:bootRun
```

Wait for the output:
```
Started XmlSanitizerApplication in X.XXX seconds
```

#### Terminal 2: Intelligent Mapping Generator
```bash
./gradlew :intelligent-mapping-generator:bootRun
```

Wait for the output:
```
Started MappingGeneratorApplication in X.XXX seconds
```

### Option 2: Using JAR Files

Build the JARs:
```bash
./gradlew build
```

Run the services:
```bash
# Terminal 1
java -jar xml-sanitizer/build/libs/xml-sanitizer-0.0.1-SNAPSHOT.jar

# Terminal 2
java -jar intelligent-mapping-generator/build/libs/intelligent-mapping-generator-0.0.1-SNAPSHOT.jar
```

### Option 3: Using Docker

```bash
# Build Docker images
docker build -t xml-sanitizer:latest -f Dockerfile .
docker build -t mapping-generator:latest -f Dockerfile .

# Run containers
docker run -p 8080:8080 xml-sanitizer:latest
docker run -p 8081:8081 mapping-generator:latest
```

## Verification

### Check Service Health

#### XML Sanitizer (Port 8080)
```bash
curl http://localhost:8080/actuator/health
```

Expected response:
```json
{"status":"UP"}
```

#### Mapping Generator (Port 8081)
```bash
curl http://localhost:8081/actuator/health
```

Expected response:
```json
{"status":"UP"}
```

### Access Swagger UI

Open in your browser:

- **XML Sanitizer**: [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
- **Mapping Generator**: [http://localhost:8081/swagger-ui.html](http://localhost:8081/swagger-ui.html)

## Testing the APIs

### XML Sanitizer Example

```bash
curl -X POST http://localhost:8080/sanitize-chars \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><payment><amount>€1000</amount></payment>'
```

### Mapping Generator Example

```bash
curl -X POST http://localhost:8081/generate-mapping \
  -H "Content-Type: application/json" \
  -d '{
    "sourceFormat": "pain.001.001.09",
    "targetFormat": "pacs.008.001.08",
    "mappingType": "PAYMENT_INITIATION"
  }'
```

## Troubleshooting

### Port Already in Use

If you see "Port 8080 is already in use":

```bash
# macOS/Linux: Find process using port
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use different port
SERVER_PORT=8082 ./gradlew :xml-sanitizer:bootRun
```

### Build Failures

```bash
# Clean and rebuild
./gradlew clean build --refresh-dependencies

# Build with debug info
./gradlew build --stacktrace
```

### Java Version Mismatch

Ensure Java 21 is active:

```bash
# macOS (using SDKMAN)
sdk list java
sdk use java 21-tem

# Or set JAVA_HOME
export JAVA_HOME=/path/to/java21
```

## IDE Setup

### IntelliJ IDEA

1. Open IntelliJ IDEA
2. **File → Open** → Select `fintech-mapping-features` folder
3. Wait for Gradle import to complete
4. **Run → Edit Configurations**
5. Add new **Spring Boot** configurations:
   - **XML Sanitizer**: Main class `com.fintech.sanitizer.XmlSanitizerApplication`
   - **Mapping Generator**: Main class `com.fintech.mapping.MappingGeneratorApplication`

### VS Code

1. Install extensions:
   - Extension Pack for Java
   - Spring Boot Extension Pack
2. Open folder in VS Code
3. Use **Run and Debug** panel to start services

## Next Steps

Now that your environment is set up:

- 📘 [Explore the Architecture](/docs/architecture/overview)
- 🔌 [Read the API Documentation](/docs/xml-sanitizer/overview)
- 🚀 [Learn about Deployment](/docs/deployment/local-development)
- 📝 [Contributing Guidelines](/docs/guides/contributing)

## Need Help?

- Check the [Troubleshooting Guide](/docs/guides/troubleshooting)
- Open an issue on [GitHub](https://github.com/Ejyke90/fintech-mapping-features/issues)
