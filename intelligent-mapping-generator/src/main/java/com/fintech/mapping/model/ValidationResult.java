package com.fintech.mapping.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the result of a pain.001 validation
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ValidationResult {
    
    /**
     * Whether the validation was successful
     */
    private boolean valid;
    
    /**
     * Detected schema type (CBPR+ or ISO Standard)
     */
    private SchemaType detectedSchemaType;
    
    /**
     * Schema type used for validation
     */
    private SchemaType validatedAgainstSchema;
    
    /**
     * Message ID from the pain.001 message (if extractable)
     */
    private String messageId;
    
    /**
     * List of validation errors (if any)
     */
    @Builder.Default
    private List<ValidationError> errors = new ArrayList<>();
    
    /**
     * Timestamp of validation
     */
    @Builder.Default
    private LocalDateTime validatedAt = LocalDateTime.now();
    
    /**
     * Processing time in milliseconds
     */
    private long processingTimeMs;
    
    /**
     * Additional information or warnings
     */
    private String additionalInfo;
    
    /**
     * Convenience method to add an error
     */
    public void addError(ValidationError error) {
        if (this.errors == null) {
            this.errors = new ArrayList<>();
        }
        this.errors.add(error);
        this.valid = false;
    }
    
    /**
     * Get a summary of the validation result
     */
    public String getSummary() {
        StringBuilder sb = new StringBuilder();
        sb.append("Validation Result: ").append(valid ? "VALID ✓" : "INVALID ✗").append("\n");
        sb.append("Detected Schema: ").append(detectedSchemaType).append("\n");
        sb.append("Validated Against: ").append(validatedAgainstSchema).append("\n");
        
        if (messageId != null) {
            sb.append("Message ID: ").append(messageId).append("\n");
        }
        
        if (!valid && errors != null && !errors.isEmpty()) {
            sb.append("\nErrors (").append(errors.size()).append("):\n");
            errors.forEach(error -> sb.append("  - ").append(error).append("\n"));
        }
        
        sb.append("\nProcessing Time: ").append(processingTimeMs).append(" ms");
        
        if (additionalInfo != null) {
            sb.append("\nInfo: ").append(additionalInfo);
        }
        
        return sb.toString();
    }
}
