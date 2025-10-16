package com.fintech.mapping.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents an individual validation error
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ValidationError {
    private String message;
    private int lineNumber;
    private int columnNumber;
    private String errorType;
    private String xpath;
    
    @Override
    public String toString() {
        return String.format("[Line %d, Col %d] %s: %s", 
            lineNumber, columnNumber, errorType, message);
    }
}
