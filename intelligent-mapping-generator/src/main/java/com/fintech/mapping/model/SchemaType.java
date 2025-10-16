package com.fintech.mapping.model;

/**
 * Represents the type of ISO 20022 pain.001 schema
 */
public enum SchemaType {
    /**
     * SWIFT's Cross-Border Payments and Reporting Plus (CBPR+) implementation
     * - Requires Business Application Header (AppHdr)
     * - Strict FIN-X character set
     * - Single transaction per message
     * - UETR mandatory
     * - BIC mandatory for agents
     */
    CBPR_PLUS,
    
    /**
     * Standard ISO 20022 pain.001.001.09 implementation
     * - No AppHdr required
     * - Flexible character set
     * - Multiple transactions supported
     * - UETR optional
     * - BIC optional for agents
     */
    ISO_STANDARD,
    
    /**
     * Could not determine schema type
     */
    UNKNOWN;
    
    @Override
    public String toString() {
        return switch(this) {
            case CBPR_PLUS -> "CBPR+ (SWIFT Cross-Border)";
            case ISO_STANDARD -> "ISO 20022 Standard";
            case UNKNOWN -> "Unknown Schema Type";
        };
    }
}
