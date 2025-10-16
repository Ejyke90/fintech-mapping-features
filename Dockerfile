# Build stage
FROM gradle:8.5-jdk21-alpine AS build
WORKDIR /app

# Copy Gradle configuration files
COPY build.gradle settings.gradle gradlew gradle.properties ./
COPY gradle gradle

# Copy all module sources
COPY intelligent-mapping-generator intelligent-mapping-generator
COPY xml-sanitizer xml-sanitizer
COPY schemas schemas

# Build the intelligent-mapping-generator module
RUN ./gradlew :intelligent-mapping-generator:build -x test --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Copy the built JAR from the intelligent-mapping-generator module
COPY --from=build /app/intelligent-mapping-generator/build/libs/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]

