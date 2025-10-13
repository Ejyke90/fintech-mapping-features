# Mono-Repo Gradle Project Analysis Prompt Template

## Context Setup
I have a Gradle-based mono-repository project with 12 components that I need you to analyze comprehensively. This analysis will be conducted in phases to ensure thorough coverage.

**Project Structure:**
- Repository Type: Gradle Multi-Module/Mono-repo
- Total Components: 12
- Component Names: [LIST YOUR 12 COMPONENTS HERE]

---

## Phase 1: Component-by-Component Deep Dive

### Instructions for AI:
I need you to review this mono-repo systematically, **one component at a time**. For each component, you must analyze:

#### 1. Source Code Analysis
- Review all Java/Kotlin files in `src/main/java` or `src/main/kotlin`
- Identify main classes, interfaces, and their responsibilities
- Document key business logic and algorithms
- Note design patterns used
- Identify dependencies on other components

#### 2. Resource Files Analysis
- Review `src/main/resources` including:
    - Configuration files (application.yml, application.properties, etc.)
    - Database scripts (migrations, schemas)
    - Template files
    - Static resources
    - Any other relevant resource files

#### 3. Test Files Analysis
- Review all test files in `src/test/java` or `src/test/kotlin`
- Document test coverage patterns
- Identify integration vs unit tests
- Note testing frameworks and utilities used
- Understand test data setup and mocking strategies

#### 4. Build Configuration
- Review `build.gradle` or `build.gradle.kts`
- Document dependencies (internal and external)
- Note plugins and build configurations
- Identify exposed APIs/interfaces

#### 5. Component Summary
After reviewing each component, provide:
- **Purpose**: What does this component do?
- **Key Classes/Services**: Main building blocks
- **Dependencies**: What it depends on (internal components & external libraries)
- **Dependents**: What depends on it
- **Data Models**: Key entities and DTOs
- **APIs/Interfaces**: Exposed endpoints or interfaces
- **Configuration**: Key configuration parameters
- **Technology Stack**: Frameworks, libraries, databases used

### Review Order:
Please review components in this order:
1. [Component 1 Name]
2. [Component 2 Name]
3. [Component 3 Name]
4. [Component 4 Name]
5. [Component 5 Name]
6. [Component 6 Name]
7. [Component 7 Name]
8. [Component 8 Name]
9. [Component 9 Name]
10. [Component 10 Name]
11. [Component 11 Name]
12. [Component 12 Name]

**Important**:
- Complete the full analysis of one component before moving to the next
- Do not skip any directories (main, resources, test)
- Take note of inter-component relationships as you discover them

---

## Phase 2: Technical Design & Documentation Generation

After completing Phase 1 for ALL 12 components, proceed to create comprehensive technical documentation.

### Task 1: Individual Component Technical Design

For each of the 12 components, create:

#### A. Component Architecture Diagram (Mermaid)
```mermaid
// Include:
// - Internal class structure
// - Key interfaces and implementations
// - Data flow within the component
// - External dependencies
```

#### B. Technical Documentation
Include the following sections:

**1. Component Overview**
- Name and purpose
- Business domain/capability
- Position in the overall architecture

**2. Architecture & Design**
- Architectural patterns used (e.g., layered, hexagonal, CQRS)
- Key design decisions
- Technology choices and rationale

**3. Component Structure**
```
src/
├── main/
│   ├── java/kotlin/
│   └── resources/
└── test/
```

**4. Core Components**
- Controllers/Endpoints
- Services/Business Logic
- Repositories/Data Access
- Models/Entities
- DTOs and Mappers
- Utilities

**5. Data Management**
- Database schema (if applicable)
- Data models
- Migration strategy
- Caching strategy (if any)

**6. API Specification**
- REST endpoints (if applicable)
- Request/Response formats
- Authentication/Authorization
- Error handling

**7. Dependencies**
- Internal component dependencies (with version/artifact IDs)
- External library dependencies
- Infrastructure dependencies

**8. Configuration**
- Configuration parameters
- Environment-specific settings
- Feature flags (if any)

**9. Testing Strategy**
- Unit test approach
- Integration test approach
- Test coverage areas
- Testing tools used

**10. Deployment Considerations**
- Build artifacts
- Runtime requirements
- Environment variables
- Scaling considerations

---

### Task 2: End-to-End System Architecture & Payment Flow

After documenting all individual components, create:

#### A. Complete System Architecture Diagram (Mermaid)
Create a comprehensive diagram showing:
- All 12 components and their relationships
- External systems/services
- Data stores
- Message queues/event buses (if present)
- API Gateway/Load Balancers (if present)
- Component boundaries and communication protocols

```mermaid
graph TB
    // Show all components and their interactions
    // Use subgraphs for logical groupings
    // Include external dependencies
```

#### B. Payment Flow E2E Analysis

**Trace the complete payment flow** through the system:

1. **Payment Initiation Flow**
    - Entry point (API Gateway, UI, etc.)
    - Components involved in order
    - Data transformations at each step
    - Validation points

2. **Payment Processing Flow**
    - Payment method handling
    - Authentication/Authorization checkpoints
    - Transaction management
    - External payment gateway integration (if any)
    - State transitions

3. **Payment Completion Flow**
    - Success scenarios
    - Failure scenarios
    - Callback/webhook handling
    - Notification mechanisms
    - Reconciliation processes

Create a **sequence diagram** showing the payment flow:

```mermaid
sequenceDiagram
    // Show actors and components
    // Show message flows
    // Show decision points
    // Show error handling
```

#### C. System Integration Map

Document how components integrate:
- **Synchronous Communication**: REST APIs, gRPC, etc.
- **Asynchronous Communication**: Message queues, events, etc.
- **Data Sharing**: Shared databases, caches, etc.
- **Service Dependencies**: Hard vs soft dependencies

#### D. Cross-Cutting Concerns Analysis
- Authentication & Authorization strategy
- Logging and monitoring approach
- Error handling and recovery
- Transaction management
- Security considerations
- Performance optimization strategies

---

## Output Format Requirements

### For Phase 1:
Provide a detailed summary for each component as you complete it.

### For Phase 2:
Deliver the following artifacts:

1. **Individual Component Documentation** (12 documents)
    - One comprehensive technical document per component
    - Include architecture diagrams in Mermaid format

2. **System-Level Documentation**
    - Overall system architecture diagram
    - Payment flow sequence diagrams
    - Integration map
    - Cross-cutting concerns summary

3. **Executive Summary**
    - Technology stack overview
    - Architectural patterns identified
    - Key design decisions
    - Technical debt observations (if any)
    - Recommended improvements (if any)

---

## Important Notes for AI

- **Accuracy**: Base ALL documentation ONLY on what you observe in the actual code, configuration, and test files. Do not make assumptions.
- **Completeness**: Do not skip any component or any section of a component (main/resources/test).
- **Traceability**: When documenting payment flows or integrations, reference specific classes and methods.
- **Clarity**: Use clear, professional technical language suitable for developers and architects.
- **Mermaid Diagrams**: Ensure all Mermaid code is syntactically correct and renders properly.
- **Consistency**: Use consistent terminology and naming conventions throughout the documentation.

---

## Ready to Begin?

Please confirm you understand these instructions, and I will provide you with access to the repository files. Begin with Component 1 and proceed systematically through all 12 components before moving to Phase 2.