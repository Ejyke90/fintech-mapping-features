# Fintech Mapping Features - Mono-repo

This is a mono-repo project containing three independent microservices for fintech data transformation and processing operations.

## Project Structure

```
fintech-mapping-features/
├── build.gradle                    # Parent build configuration
├── settings.gradle                 # Multi-module configuration
├── gradlew                         # Gradle wrapper script
├── Dockerfile                      # Docker configuration
├── xml-sanitizer/                  # XML Sanitizer microservice (Java/Spring Boot)
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
├── intelligent-mapping-generator/  # Intelligent Mapping Generator microservice (Java/Spring Boot)
│   ├── build.gradle
│   └── src/
│       ├── main/
│       │   ├── java/com/fintech/mapping/
│       │   │   ├── MappingGeneratorApplication.java
│       │   │   └── controller/
│       │   │       └── MappingGeneratorController.java
│       │   └── resources/
│       │       └── application.properties (port: 8081)
│       └── test/java/
└── csv-parser/                     # CSV Parser microservice (Python/FastAPI)
    ├── src/
    │   ├── main.py                 # FastAPI application
    │   └── parser.py               # Core CSV parsing logic
    ├── tests/
    │   └── test_parser.py          # Unit tests
    ├── Dockerfile                  # Container configuration
    ├── requirements.txt            # Python dependencies
    └── README.md                   # Module documentation
```

## Modules

### 1. API Gateway & Orchestrator (Node.js/TypeScript)
- **Port**: 3000
- **Purpose**: Orchestrate workflows across all microservices
- **Endpoints**:
  - `POST /api/v1/csv-to-xml` - CSV to XML transformation
  - `POST /api/v1/csv-to-mapping` - Generate field mappings
  - `POST /api/v1/transform-pipeline` - Full end-to-end pipeline
- **Technology**: Node.js 20, TypeScript, Express

### 2. CSV Parser (Python/FastAPI)
- **Port**: 8000
- **Purpose**: Parse, validate, and transform CSV files
- **Endpoints**: 
  - `POST /api/csv/parse` - Parse CSV files
  - `POST /api/csv/validate` - Validate CSV structure
  - `POST /api/csv/schema` - Extract schema information
  - `POST /api/csv/transform` - Clean and transform data
  - `POST /api/csv/prepare-for-xml` - Prepare for XML conversion
  - `POST /api/csv/prepare-for-mapping` - Prepare for mapping generation
- **Technology**: Python 3.9+, FastAPI, Pandas

### 3. XML Sanitizer (Java/Spring Boot)
- **Port**: 8080
- **Purpose**: Sanitizes XML payloads by removing invalid characters
- **Endpoint**: `POST /sanitize-chars`
- **Package**: `com.fintech.sanitizer`
- **Technology**: Java 21, Spring Boot 3.2.1

### 4. Intelligent Mapping Generator (Java/Spring Boot)
- **Port**: 8081
- **Purpose**: Generates intelligent mappings for fintech data transformations
- **Endpoint**: `POST /generate-mapping`
- **Package**: `com.fintech.mapping`
- **Technology**: Java 21, Spring Boot 3.2.1

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

### Option 1: Docker Compose (Recommended)

Run all services with a single command:

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- API Gateway: http://localhost:3000
- CSV Parser: http://localhost:8000
- XML Sanitizer: http://localhost:8080
- Mapping Generator: http://localhost:8081

### Option 2: Run Individually

#### Run API Gateway (Port 3000)
```bash
cd api-gateway
npm install
npm run dev
```

#### Run CSV Parser (Port 8000)
```bash
cd csv-parser
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

#### Run XML Sanitizer (Port 8080)
```bash
./gradlew :xml-sanitizer:bootRun
```

#### Run Intelligent Mapping Generator (Port 8081)
```bash
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

### Integrated Workflows (via API Gateway)

#### Full Transformation Pipeline
```bash
curl -X POST http://localhost:3000/api/v1/transform-pipeline \
  -F "file=@payment_data.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

#### CSV to XML Transformation
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-xml \
  -F "file=@payment_data.csv"
```

#### CSV to Mapping Generation
```bash
curl -X POST http://localhost:3000/api/v1/csv-to-mapping \
  -F "file=@payment_data.csv" \
  -F "targetSchema=ISO20022_pain.001.001.09"
```

### Direct Service Access

#### CSV Parser
```bash
# Parse a CSV file
curl -X POST http://localhost:8000/api/csv/parse \
  -F "file=@data.csv"

# Validate CSV structure
curl -X POST http://localhost:8000/api/csv/validate \
  -F "file=@data.csv"

# Get CSV schema
curl -X POST http://localhost:8000/api/csv/schema \
  -F "file=@data.csv"
```

#### XML Sanitizer
```bash
curl -X POST http://localhost:8080/sanitize-chars \
  -H "Content-Type: application/xml" \
  -d '<Sample>XML Data</Sample>'
```

#### Intelligent Mapping Generator
```bash
curl -X POST http://localhost:8081/generate-mapping \
  -H "Content-Type: application/json" \
  -d '{"source": "field1", "target": "field2"}'
```

## Documentation

Full documentation is available at: [GitHub Pages Documentation](https://ejyke90.github.io/fintech-mapping-features/)

### Quick Links
- [Integration Guide](INTEGRATION_GUIDE.md) - **⭐ Start Here for Integration Patterns**
- [API Gateway Guide](api-gateway/README.md)
- [CSV Parser Guide](docs/docs/csv-parser/overview.md)
- [XML Sanitizer Guide](docs/docs/xml-sanitizer/overview.md)
- [Intelligent Mapping Generator Guide](docs/docs/intelligent-mapping-generator/overview.md)

## License
[Add your license here]
