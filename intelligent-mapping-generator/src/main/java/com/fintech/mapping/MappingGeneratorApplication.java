package com.fintech.mapping;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jms.annotation.EnableJms;

/**
 * Main application class for Intelligent Mapping Generator
 * 
 * Features:
 * - Consumes pain.001 messages from ActiveMQ queue
 * - Dynamically detects CBPR+ vs ISO 20022 schema
 * - Validates XML against detected schema
 * - Publishes validation results
 */
@SpringBootApplication
@EnableJms
public class MappingGeneratorApplication {

    public static void main(String[] args) {
        SpringApplication.run(MappingGeneratorApplication.class, args);
    }
}
