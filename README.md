# Fintech Mapping Features - Mono-repo

This is a mono-repo project containing two independent Spring Boot microservices for fintech operations.

## Project Structure

```
fintech-mapping-features/
├── build.gradle                    # Parent build configuration
├── settings.gradle                 # Multi-module configuration
├── gradlew                         # Gradle wrapper script
├── Dockerfile                      # Docker configuration
├── xml-sanitizer/                  # XML Sanitizer microservice
│   ├── build.gradle
│   └── src/
│       ├── main/
│       │   ├── java/com/fintech/sanitizer/
│       │   │   ├── XmlSanitizerApplication.java
│       │   │   └── controller/
│       │   │       └── XmlSanitizerController.java
│       │   └── resources/
│       │       └── application.properties (port: 8080)
│       └── test/java/
└── intelligent-mapping-generator/  # Intelligent Mapping Generator microservice
    ├── build.gradle
    └── src/
        ├── main/
        │   ├── java/com/fintech/mapping/
        │   │   ├── MappingGeneratorApplication.java
        │   │   └── controller/
        │   │       └── MappingGeneratorController.java
        │   └── resources/
        │       └── application.properties (port: 8081)
        └── test/java/
```

## Modules

### 1. XML Sanitizer
- **Port**: 8080
- **Purpose**: Sanitizes XML payloads by removing invalid characters
- **Endpoint**: `POST /sanitize-chars`
- **Package**: `com.fintech.sanitizer`

### 2. Intelligent Mapping Generator
- **Port**: 8081
- **Purpose**: Generates intelligent mappings for fintech data transformations
- **Endpoint**: `POST /generate-mapping`
- **Package**: `com.fintech.mapping`

## Building the Project

### Build all modules
```bash
./gradlew build
```

### Build specific module
```bash
./gradlew :xml-sanitizer:build
./gradlew :intelligent-mapping-generator:build
```

### Clean all modules
```bash
./gradlew clean
```

## Running the Services

### Run XML Sanitizer (Port 8080)
```bash
./gradlew :xml-sanitizer:bootRun
```

### Run Intelligent Mapping Generator (Port 8081)
```bash
./gradlew :intelligent-mapping-generator:bootRun
```

### Run both services simultaneously (in separate terminals)
```bash
# Terminal 1
./gradlew :xml-sanitizer:bootRun

# Terminal 2
./gradlew :intelligent-mapping-generator:bootRun
```

## Testing

### Run all tests
```bash
./gradlew test
```

### Run tests for specific module
```bash
./gradlew :xml-sanitizer:test
./gradlew :intelligent-mapping-generator:test
```

## Creating JAR Files

### Create JAR for all modules
```bash
./gradlew bootJar
```

The JAR files will be created in:
- `xml-sanitizer/build/libs/xml-sanitizer-0.0.1-SNAPSHOT.jar`
- `intelligent-mapping-generator/build/libs/intelligent-mapping-generator-0.0.1-SNAPSHOT.jar`

### Run JAR files
```bash
java -jar xml-sanitizer/build/libs/xml-sanitizer-0.0.1-SNAPSHOT.jar
java -jar intelligent-mapping-generator/build/libs/intelligent-mapping-generator-0.0.1-SNAPSHOT.jar
```

## Development

### Technology Stack
- Java 21
- Spring Boot 3.2.1
- Gradle 8.x
- Spring Web

### Adding Dependencies
Add common dependencies in the root `build.gradle` under the `subprojects` block, or add module-specific dependencies in the respective module's `build.gradle` file.

## API Examples

### XML Sanitizer
```bash
curl -X POST http://localhost:8080/sanitize-chars \
  -H "Content-Type: application/xml" \
  -d '<Sample>XML Data</Sample>'
```

### Intelligent Mapping Generator
```bash
curl -X POST http://localhost:8081/generate-mapping \
  -H "Content-Type: application/json" \
  -d '{"source": "field1", "target": "field2"}'
```

## License
[Add your license here]
