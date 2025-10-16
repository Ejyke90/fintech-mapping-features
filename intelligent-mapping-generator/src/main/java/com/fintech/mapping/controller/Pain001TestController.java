package com.fintech.mapping.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.web.bind.annotation.*;

/**
 * REST Controller for testing pain.001 validation
 * Provides endpoints to submit messages to the queue
 */
@RestController
@RequestMapping("/api/pain001")
@Slf4j
public class Pain001TestController {
    
    @Autowired
    private JmsTemplate jmsTemplate;
    
    @Value("${app.validation.queue-name}")
    private String validationQueueName;
    
    /**
     * Submit pain.001 XML message to validation queue
     * 
     * Example:
     * curl -X POST http://localhost:8081/api/pain001/submit \
     *   -H "Content-Type: application/xml" \
     *   -d @sample_iso_pain.001.001.09.xml
     */
    @PostMapping(value = "/submit", 
                 consumes = MediaType.APPLICATION_XML_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<SubmitResponse> submitPain001(@RequestBody String xmlMessage) {
        log.info("Received pain.001 submission request (size: {} bytes)", xmlMessage.length());
        
        try {
            // Send message to validation queue
            jmsTemplate.convertAndSend(validationQueueName, xmlMessage);
            
            log.info("✓ Message submitted to queue: {}", validationQueueName);
            
            return ResponseEntity.ok(new SubmitResponse(
                true,
                "Message submitted successfully to validation queue",
                validationQueueName,
                xmlMessage.length()
            ));
            
        } catch (Exception e) {
            log.error("Failed to submit message: {}", e.getMessage(), e);
            
            return ResponseEntity.internalServerError().body(new SubmitResponse(
                false,
                "Failed to submit message: " + e.getMessage(),
                null,
                0
            ));
        }
    }
    
    /**
     * Submit multiple messages for testing
     */
    @PostMapping(value = "/submit-batch",
                 consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<BatchSubmitResponse> submitBatch(@RequestBody BatchSubmitRequest request) {
        log.info("Received batch submission request ({} messages)", request.messages().size());
        
        int successCount = 0;
        int failureCount = 0;
        
        for (String xmlMessage : request.messages()) {
            try {
                jmsTemplate.convertAndSend(validationQueueName, xmlMessage);
                successCount++;
            } catch (Exception e) {
                log.error("Failed to submit message in batch: {}", e.getMessage());
                failureCount++;
            }
        }
        
        log.info("Batch submission complete: {} success, {} failures", successCount, failureCount);
        
        return ResponseEntity.ok(new BatchSubmitResponse(
            successCount,
            failureCount,
            request.messages().size()
        ));
    }
    
    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    public ResponseEntity<HealthResponse> health() {
        return ResponseEntity.ok(new HealthResponse(
            "UP",
            "pain.001 validation service is running",
            validationQueueName
        ));
    }
    
    // Response DTOs
    record SubmitResponse(
        boolean success,
        String message,
        String queueName,
        int messageSizeBytes
    ) {}
    
    record BatchSubmitRequest(
        java.util.List<String> messages
    ) {}
    
    record BatchSubmitResponse(
        int successCount,
        int failureCount,
        int totalCount
    ) {}
    
    record HealthResponse(
        String status,
        String message,
        String queueName
    ) {}
}
