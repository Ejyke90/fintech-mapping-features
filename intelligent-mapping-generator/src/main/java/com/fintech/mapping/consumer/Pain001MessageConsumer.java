package com.fintech.mapping.consumer;

import com.fintech.mapping.model.ValidationResult;
import com.fintech.mapping.service.ValidationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jms.annotation.JmsListener;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Component;

/**
 * JMS Consumer that listens for pain.001 messages and validates them
 */
@Component
@Slf4j
public class Pain001MessageConsumer {
    
    @Autowired
    private ValidationService validationService;
    
    @Autowired
    private JmsTemplate jmsTemplate;
    
    @Value("${app.validation.result-queue-name}")
    private String resultQueueName;
    
    @Value("${app.validation.dlq-name}")
    private String dlqName;
    
    /**
     * Listen for pain.001 messages from the validation queue
     */
    @JmsListener(destination = "${app.validation.queue-name}")
    public void consumePain001Message(String xmlMessage) {
        log.info("=" .repeat(80));
        log.info("📨 Received pain.001 message for validation");
        log.info("=" .repeat(80));
        
        try {
            // Validate the message
            ValidationResult result = validationService.validate(xmlMessage);
            
            // Log the result summary
            log.info("\n" + result.getSummary());
            
            // Publish result to result queue
            publishValidationResult(result);
            
            // If invalid, also send to DLQ with the original message
            if (!result.isValid()) {
                publishToDeadLetterQueue(xmlMessage, result);
            }
            
        } catch (Exception e) {
            log.error("❌ Fatal error processing message: {}", e.getMessage(), e);
            publishToDeadLetterQueue(xmlMessage, null);
        }
        
        log.info("=" .repeat(80));
    }
    
    /**
     * Publish validation result to result queue
     */
    private void publishValidationResult(ValidationResult result) {
        try {
            String resultMessage = formatResultAsJson(result);
            jmsTemplate.convertAndSend(resultQueueName, resultMessage);
            log.debug("✓ Published validation result to: {}", resultQueueName);
        } catch (Exception e) {
            log.error("Failed to publish validation result: {}", e.getMessage());
        }
    }
    
    /**
     * Send invalid messages to Dead Letter Queue
     */
    private void publishToDeadLetterQueue(String xmlMessage, ValidationResult result) {
        try {
            String dlqMessage = String.format(
                "--- INVALID MESSAGE ---\n%s\n\n--- VALIDATION RESULT ---\n%s",
                xmlMessage,
                result != null ? result.getSummary() : "Processing failed"
            );
            jmsTemplate.convertAndSend(dlqName, dlqMessage);
            log.warn("⚠️  Message sent to DLQ: {}", dlqName);
        } catch (Exception e) {
            log.error("Failed to send message to DLQ: {}", e.getMessage());
        }
    }
    
    /**
     * Format validation result as JSON-like string
     * (In production, use proper JSON serialization)
     */
    private String formatResultAsJson(ValidationResult result) {
        return String.format("""
            {
              "valid": %s,
              "detectedSchema": "%s",
              "validatedAgainst": "%s",
              "messageId": "%s",
              "errorCount": %d,
              "processingTimeMs": %d,
              "validatedAt": "%s"
            }
            """,
            result.isValid(),
            result.getDetectedSchemaType(),
            result.getValidatedAgainstSchema(),
            result.getMessageId(),
            result.getErrors() != null ? result.getErrors().size() : 0,
            result.getProcessingTimeMs(),
            result.getValidatedAt()
        );
    }
}
