# AI Agent Implementation Guide: SWIFT Character Sanitization System

## Overview

This document provides a step-by-step guide for an AI agent (Claude Sonnet 4 or similar) to implement a complete SWIFT FIN X character set sanitization system for ISO 20022 payment messages in **any technology stack**.

**Purpose:** Enable AI agents to build this solution from scratch in Java, Python, C#, JavaScript, Go, or any other language.

**Complexity:** Intermediate to Advanced  
**Estimated Implementation Time:** 12-19 hours (depending on language and expertise)  
**Target Audience:** AI coding agents, senior developers

---

## 🎯 Problem Definition

**Context:** ISO 20022 payment messages (pain.001, pacs.008, pacs.009, etc.) must comply with SWIFT FIN X character set restrictions. Messages containing non-compliant characters (diacritics like ö, å, ü, é, etc.) will be rejected by the SWIFT network.

**Goal:** Implement a production-ready sanitization system that:
1. Detects non-compliant characters in payment messages
2. Transliterates them to SWIFT-compliant equivalents (Björn → Bjorn)
3. Logs all changes for audit compliance
4. Integrates seamlessly into existing payment processing pipelines

---

## 📋 SWIFT Character Set Rules (Reference)

### Allowed Characters

**Base FIN X (All Text Fields):**
- Letters: `a-z A-Z`
- Numbers: `0-9`
- Punctuation: `/ - ? : ( ) . , ' +`
- Space

**Extended Characters (Name/Address/Remittance Fields Only):**
- `! # & % * = ^ _ ' { | } ~ " ; @ [ \ ] $ < >`

### Not Allowed
- Diacritical marks: `ö å ä ü é è ñ ç ê ë î ï ô û à â ì ò ù ÿ` (and uppercase)
- Extended Unicode (emojis, CJK, Arabic, Cyrillic, etc.)
- Currency symbols (except in specific contexts): `€ £ ¥ ¢`

### Replacement Rule
- Unknown/invalid characters should be replaced with `.` (period/full stop) per SWIFT guidelines

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Character Transliteration Engine               │
│ - Maps diacritics to ASCII equivalents                  │
│ - Handles Unicode normalization                         │
│ - Field-type aware validation                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Message Parser & Processor                     │
│ - Parses ISO 20022 XML messages                         │
│ - Identifies fields requiring sanitization              │
│ - Applies sanitization rules                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Integration Layer                              │
│ - Provides API for payment processing pipeline          │
│ - Handles logging and audit trails                      │
│ - Supports multiple integration patterns                │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Implementation Steps

---

## STEP 1: Create Character Transliteration Map

**Objective:** Build a comprehensive mapping of diacritical characters to their ASCII equivalents.

### Prompt for AI Agent:

```
Create a character transliteration map/dictionary that handles the following European diacritical characters. The map should be implemented in [YOUR_LANGUAGE] and be easily extensible.

Required mappings (minimum):

SCANDINAVIAN:
- å → a, Å → A
- ä → a, Ä → A
- ö → o, Ö → O
- æ → ae, Æ → AE
- ø → o, Ø → O

GERMAN:
- ü → u, Ü → U
- ö → o, Ö → O
- ä → a, Ä → A
- ß → ss

FRENCH:
- é → e, É → E
- è → e, È → E
- ê → e, Ê → E
- ë → e, Ë → E
- à → a, À → A
- â → a, Â → A
- ù → u, Ù → U
- û → u, Û → U
- ï → i, Ï → I
- î → i, Î → I
- ç → c, Ç → C

SPANISH:
- ñ → n, Ñ → N
- á → a, Á → A
- é → e, É → E
- í → i, Í → I
- ó → o, Ó → O
- ú → u, Ú → U

POLISH:
- ł → l, Ł → L
- ą → a, Ą → A
- ć → c, Ć → C
- ę → e, Ę → E
- ń → n, Ń → N
- ś → s, Ś → S
- ź → z, Ź → Z
- ż → z, Ż → Z

CZECH/SLOVAK:
- č → c, Č → C
- ď → d, Ď → D
- ě → e, Ě → E
- ň → n, Ň → N
- ř → r, Ř → R
- š → s, Š → S
- ť → t, Ť → T
- ů → u, Ů → U
- ý → y, Ý → Y
- ž → z, Ž → Z

Implementation requirements:
1. Use a data structure that allows O(1) lookup (hash map/dictionary)
2. Make it easily extensible for additional character mappings
3. Include inline comments explaining the language group
4. Consider case sensitivity (both upper and lowercase)

Return the complete transliteration map implementation.
```

**Expected Output:** A data structure (HashMap, Dictionary, Object, etc.) containing all character mappings.

**Validation:** Test with: "Björn", "Åke", "François", "Müller", "José" - all should transliterate correctly.

---

## STEP 2: Implement Character Validation Functions

**Objective:** Create functions to determine if a character is SWIFT-compliant.

### Prompt for AI Agent:

```
Implement character validation functions in [YOUR_LANGUAGE] with the following specifications:

1. Function: isBaseFinXCharacter(char)
   - Returns: boolean
   - Purpose: Check if character is in base SWIFT character set
   - Allowed: a-z, A-Z, 0-9, /, -, ?, :, (, ), ., ,, ', +, space

2. Function: isExtendedFinXCharacter(char)
   - Returns: boolean
   - Purpose: Check if character is in extended SWIFT character set
   - Allowed: All base characters PLUS !, #, &, %, *, =, ^, _, ', {, |, }, ~, ", ;, @, [, \, ], $, <, >

3. Function: isValidForFieldType(char, fieldType)
   - Returns: boolean
   - Purpose: Check if character is valid for specific field type
   - Parameters:
     * char: character to validate
     * fieldType: enum or string ("NAME", "ADDRESS", "REMITTANCE", "STANDARD")
   - Logic:
     * NAME/ADDRESS/REMITTANCE → use isExtendedFinXCharacter
     * STANDARD → use isBaseFinXCharacter

Implementation requirements:
1. Use efficient character comparison (avoid regex if possible for single chars)
2. Handle null/empty input gracefully
3. Include comprehensive inline comments
4. Make functions pure (no side effects)

Return the complete validation function implementations.
```

**Expected Output:** 3 validation functions with clear, efficient logic.

**Validation:**
- `isBaseFinXCharacter('A')` → true
- `isBaseFinXCharacter('!')` → false
- `isExtendedFinXCharacter('!')` → true
- `isExtendedFinXCharacter('ö')` → false

---

## STEP 3: Implement Core Sanitization Logic

**Objective:** Create the main sanitization function that processes individual strings.

### Prompt for AI Agent:

```
Implement a comprehensive string sanitization function in [YOUR_LANGUAGE] with the following specifications:

Function: sanitizeText(input, allowExtendedCharset)
- Parameters:
  * input: string to sanitize
  * allowExtendedCharset: boolean (true for Name/Address/Remittance, false for standard text)
- Returns: sanitized string (SWIFT-compliant)

Algorithm:
1. If input is null or empty, return as-is
2. Initialize result container (StringBuilder/Array/String builder)
3. For each character in input:
   a. Check if character is allowed using validation functions from STEP 2
   b. If allowed → append to result
   c. If not allowed → check transliteration map from STEP 1
   d. If in transliteration map → append transliterated value
   e. If not in map → try Unicode normalization (NFD form)
   f. If normalized character is allowed → append it
   g. Otherwise → append '.' (period) as fallback
4. Return result

Additional requirements:
1. Handle both NFC and NFD Unicode normalization forms
2. Be efficient with string building (avoid concatenation in loops)
3. Preserve spaces and valid punctuation
4. Include error handling for edge cases
5. Add logging points for debugging (comments showing where logs should go)

Return the complete sanitization function implementation.
```

**Expected Output:** Core sanitization function with robust character handling.

**Validation:**
- `sanitizeText("Björn", true)` → "Bjorn"
- `sanitizeText("Café!", true)` → "Cafe!"
- `sanitizeText("Hello 😊", true)` → "Hello ."
- `sanitizeText("Test!", false)` → "Test." (! not allowed in standard text)

---

## STEP 4: Create Convenience Functions for Different Field Types

**Objective:** Provide easy-to-use functions for common sanitization scenarios.

### Prompt for AI Agent:

```
Create convenient wrapper functions around the core sanitization logic from STEP 3 for different field types in [YOUR_LANGUAGE]:

1. Function: sanitizeNameOrAddress(input)
   - Purpose: Sanitize Name and Address fields
   - Implementation: Call sanitizeText(input, true)
   - Returns: SWIFT-compliant name/address string

2. Function: sanitizeRemittanceInfo(input)
   - Purpose: Sanitize Remittance Information fields
   - Implementation: Call sanitizeText(input, true)
   - Returns: SWIFT-compliant remittance string

3. Function: sanitizeStandardText(input)
   - Purpose: Sanitize standard text fields
   - Implementation: Call sanitizeText(input, false)
   - Returns: SWIFT-compliant standard text string

4. Function: isValidNameOrAddress(input)
   - Purpose: Validate if string is already SWIFT-compliant for Name/Address
   - Returns: boolean (true if valid, false otherwise)
   - Implementation: Check all characters against extended character set

5. Function: isValidStandardText(input)
   - Purpose: Validate if string is already SWIFT-compliant for standard text
   - Returns: boolean (true if valid, false otherwise)
   - Implementation: Check all characters against base character set

Implementation requirements:
1. Add comprehensive doc comments/JSDoc/docstrings
2. Include usage examples in comments
3. Handle null/empty inputs gracefully
4. Make functions stateless (thread-safe if applicable)

Return the complete wrapper function implementations with documentation.
```

**Expected Output:** 5 well-documented convenience functions.

**Validation:**
- `sanitizeNameOrAddress("Björn & Co")` → "Bjorn & Co"
- `isValidNameOrAddress("John Smith")` → true
- `isValidNameOrAddress("Björn")` → false

---

## STEP 5: Implement XML Message Parser

**Objective:** Create functionality to parse ISO 20022 XML messages and extract fields.

### Prompt for AI Agent:

```
Implement an XML message parser for ISO 20022 pain.001 messages in [YOUR_LANGUAGE] with the following specifications:

Class/Module: MessageParser or Pain001Parser

Required functionality:

1. Function: parseXml(xmlString)
   - Purpose: Parse XML string into a document/DOM structure
   - Parameters: xmlString (the ISO 20022 XML message)
   - Returns: Parsed XML document object
   - Requirements:
     * Handle namespaces (xmlns)
     * Preserve document structure
     * Handle malformed XML gracefully (error handling)

2. Function: extractFieldsByType(xmlDocument, fieldType)
   - Purpose: Extract all fields of a specific type from the message
   - Parameters:
     * xmlDocument: parsed XML document
     * fieldType: "NAME", "ADDRESS", or "REMITTANCE"
   - Returns: List/Array of objects containing:
     * xpath: XPath to the field
     * value: current field value
     * nodeReference: reference to XML node (for updating)

Field identification rules for pain.001:

NAME FIELDS (tag name ends with 'Nm'):
- //InitgPty/Nm (Initiating Party Name)
- //Dbtr/Nm (Debtor Name)
- //UltmtDbtr/Nm (Ultimate Debtor Name)
- //Cdtr/Nm (Creditor Name)
- //UltmtCdtr/Nm (Ultimate Creditor Name)
- //DbtrAgt/FinInstnId/Nm (Debtor Agent Name)
- //CdtrAgt/FinInstnId/Nm (Creditor Agent Name)

ADDRESS FIELDS:
- //PstlAdr/AdrLine (Address Lines)
- //PstlAdr/StrtNm (Street Name)
- //PstlAdr/TwnNm (Town Name)
- //PstlAdr/Ctry (Country - but usually codes, rarely needs sanitization)

REMITTANCE FIELDS:
- //RmtInf/Ustrd (Unstructured Remittance)
- //RmtInf/Strd/CdtrRefInf/Ref (Creditor Reference)
- //RmtInf/Strd/AddtlRmtInf (Additional Remittance Info)

Implementation requirements:
1. Use native XML parsing library (DOM, lxml, JAXP, etc.)
2. Handle namespace-aware parsing
3. Return results in a consistent data structure
4. Include error handling for missing fields
5. Make it extensible for other message types (pacs.008, pacs.009)

Return the complete XML parser implementation.
```

**Expected Output:** XML parser that can extract relevant fields from ISO 20022 messages.

**Validation:** Parse a sample pain.001 XML and verify all Name, Address, and Remittance fields are extracted.

---

## STEP 6: Implement Message Processor

**Objective:** Create the main processor that sanitizes entire messages.

### Prompt for AI Agent:

```
Implement a message processor in [YOUR_LANGUAGE] that sanitizes complete ISO 20022 payment messages:

Class/Module: MessageProcessor or Pain001MessageProcessor

Required functionality:

1. Function: processMessage(xmlString)
   - Purpose: Sanitize all relevant fields in a pain.001 message
   - Parameters: xmlString (the original ISO 20022 XML message)
   - Returns: Object containing:
     * sanitizedXml: the sanitized XML string
     * changeLog: array of changes made (for audit)
     * wasModified: boolean indicating if any changes were made
   
Algorithm:
1. Parse XML using parser from STEP 5
2. Extract NAME fields
3. For each NAME field:
   a. Get current value
   b. Sanitize using sanitizeNameOrAddress() from STEP 4
   c. If changed:
      - Update XML node
      - Log change (field path, original value, new value)
4. Repeat for ADDRESS fields
5. Repeat for REMITTANCE fields
6. Convert XML document back to string
7. Return result object with sanitized XML and change log

2. Function: generateChangeLog(fieldType, fieldPath, originalValue, sanitizedValue)
   - Purpose: Create structured log entry for changes
   - Returns: Object with:
     * timestamp: current timestamp
     * fieldType: "NAME", "ADDRESS", or "REMITTANCE"
     * fieldPath: XPath or field identifier
     * originalValue: value before sanitization
     * sanitizedValue: value after sanitization

3. Function: xmlToString(xmlDocument)
   - Purpose: Convert XML document back to formatted string
   - Parameters: XML document object
   - Returns: formatted XML string
   - Requirements:
     * Preserve namespaces
     * Use proper indentation (4 spaces recommended)
     * UTF-8 encoding

Implementation requirements:
1. Preserve XML structure and attributes
2. Handle namespace declarations properly
3. Make it idempotent (running twice gives same result)
4. Include comprehensive error handling
5. Support batch processing (multiple messages)
6. Add logging hooks for production use

Return the complete message processor implementation.
```

**Expected Output:** Complete message processor that handles end-to-end sanitization.

**Validation:** Process a pain.001 message with "Björn", "Åke", etc., and verify:
- All names are sanitized
- XML structure is preserved
- Change log is accurate

---

## STEP 7: Implement Validation and Reporting

**Objective:** Create validation and reporting capabilities.

### Prompt for AI Agent:

```
Implement validation and reporting functions in [YOUR_LANGUAGE]:

1. Function: validateMessage(xmlString)
   - Purpose: Validate if message is SWIFT-compliant without modifying it
   - Returns: Object containing:
     * isValid: boolean (true if all fields are compliant)
     * violations: array of objects describing non-compliant fields:
       - fieldPath: XPath to the field
       - fieldType: "NAME", "ADDRESS", or "REMITTANCE"
       - currentValue: the non-compliant value
       - suggestedValue: what it should be sanitized to
       - invalidCharacters: list of specific invalid characters found

2. Function: generateSanitizationReport(changeLog)
   - Purpose: Create human-readable report of sanitization changes
   - Parameters: changeLog from message processor (STEP 6)
   - Returns: formatted string report with:
     * Summary: total number of fields sanitized
     * Breakdown by field type (NAME, ADDRESS, REMITTANCE)
     * Detailed list of each change
     * Timestamp of report generation

3. Function: analyzeCharacterIssues(text)
   - Purpose: Analyze a string and identify specific character issues
   - Returns: Object containing:
     * hasIssues: boolean
     * totalCharacters: count
     * invalidCharacters: array of objects:
       - character: the invalid character
       - position: position in string
       - suggestedReplacement: what it should become
       - characterName: descriptive name (e.g., "Latin Small Letter O with Diaeresis")

Report format example:
```
Sanitization Report
Generated: 2025-10-08 14:30:00 UTC

Summary:
- Total fields sanitized: 4
- NAME fields: 2
- ADDRESS fields: 1
- REMITTANCE fields: 1

Details:
1. Field: Debtor Name (//Dbtr/Nm)
   Original:  Björn Andersson
   Sanitized: Bjorn Andersson
   Changes: ö → o

2. Field: Creditor Name (//Cdtr/Nm)
   Original:  François Müller
   Sanitized: Francois Muller
   Changes: ç → c, ü → u
   ...
```

Implementation requirements:
1. Clear, professional formatting
2. Include timestamps
3. Support multiple output formats (text, JSON, CSV)
4. Make reports suitable for audit compliance
5. Handle large change logs efficiently

Return the complete validation and reporting implementation.
```

**Expected Output:** Validation and reporting utilities.

**Validation:** Run validation on non-compliant message and verify all violations are detected.

---

## STEP 8: Create Integration Patterns

**Objective:** Provide multiple ways to integrate the sanitization system.

### Prompt for AI Agent:

```
Implement 3 integration patterns in [YOUR_LANGUAGE] for the sanitization system:

PATTERN 1: Pre-Processing Pipeline
- Purpose: Sanitize messages immediately upon receipt
- Use case: Ensure clean data throughout the system
- Implementation:
  * Create a wrapper function that accepts raw message
  * Sanitize using MessageProcessor
  * Return sanitized message for further processing
  * Log all sanitization events

PATTERN 2: Validation-then-Sanitize Pipeline
- Purpose: Check if sanitization is needed before applying
- Use case: Monitor data quality and selectively sanitize
- Implementation:
  * First validate the message
  * If violations found, sanitize
  * If clean, pass through unchanged
  * Log validation results and any sanitization

PATTERN 3: Just-in-Time Sanitization
- Purpose: Sanitize right before sending to SWIFT network
- Use case: Minimal changes to existing systems
- Implementation:
  * Accept processed message ready for transmission
  * Sanitize as final step
  * Send to SWIFT gateway
  * Log if changes were made at last moment

For each pattern, provide:
1. Complete function implementation
2. Usage example with sample code
3. Error handling strategy
4. Logging recommendations
5. Performance considerations

Also create:
4. A comparison matrix showing:
   - When to use each pattern
   - Pros and cons
   - Performance characteristics
   - Audit trail differences

Return all 3 pattern implementations with comprehensive documentation.
```

**Expected Output:** 3 ready-to-use integration patterns with guidance.

**Validation:** Verify each pattern works with sample messages and produces correct audit logs.

---

## STEP 9: Implement Comprehensive Testing

**Objective:** Create a thorough test suite.

### Prompt for AI Agent:

```
Create a comprehensive test suite in [YOUR_LANGUAGE] for the SWIFT character sanitization system:

Test Categories:

1. UNIT TESTS for Character Transliteration (from STEP 1):
   - Test all Scandinavian characters (å, ä, ö, ø, æ)
   - Test all German characters (ü, ö, ä, ß)
   - Test all French characters (é, è, ê, ë, ç, etc.)
   - Test all Spanish characters (ñ, á, é, í, ó, ú)
   - Test all Polish characters (ł, ą, ć, ę, ń, ś, ź, ż)
   - Test all Czech/Slovak characters (č, ď, ě, ň, ř, š, ť, ů, ž)
   - Test both uppercase and lowercase

2. UNIT TESTS for Validation Functions (from STEP 2):
   - Test base character set validation
   - Test extended character set validation
   - Test field-type specific validation
   - Test edge cases (null, empty, whitespace)

3. UNIT TESTS for Sanitization Logic (from STEP 3-4):
   - Test name sanitization with various international names
   - Test address sanitization
   - Test remittance info sanitization
   - Test Unicode normalization (NFD/NFC)
   - Test unknown characters (emojis, CJK) → should become '.'
   - Test already-compliant text (no changes)
   - Test mixed valid/invalid characters

4. INTEGRATION TESTS for Message Processing (from STEP 5-6):
   - Test complete pain.001 message sanitization
   - Test XML structure preservation
   - Test namespace handling
   - Test change log generation
   - Test idempotent behavior (process twice = same result)

5. EDGE CASE TESTS:
   - Null/empty inputs
   - Very long strings (performance)
   - Strings with all invalid characters
   - Malformed XML
   - Missing fields in XML
   - Duplicate field names

Test Data - Real-world names to test:
- Björn Andersson (Swedish)
- Åke Björkström (Swedish)
- François Müller (French/German)
- José María García (Spanish)
- Søren Østergård (Danish)
- Władysław Łódź (Polish)
- Vladimír Dvořák (Czech)
- Société Générale (French company)
- Zürich Versicherung (German company)

Expected test coverage: >90% of code

Return the complete test suite implementation with clear test names and assertions.
```

**Expected Output:** Comprehensive test suite with >50 test cases.

**Validation:** Run all tests and verify 100% pass rate.

---

## STEP 10: Create Production-Ready Logging and Monitoring

**Objective:** Implement robust logging and monitoring capabilities.

### Prompt for AI Agent:

```
Implement production-ready logging and monitoring in [YOUR_LANGUAGE]:

1. Logging Levels and Messages:

   INFO Level:
   - "Message received for sanitization: [messageId]"
   - "Message processed successfully: [messageId], modified=[true/false]"
   - "No sanitization needed - message is SWIFT-compliant"

   WARNING Level:
   - "Sanitized [fieldType] field: '[original]' → '[sanitized]'"
   - "High sanitization rate detected: [X]% of messages require sanitization"
   - "Unusual character detected: [char] at position [pos] in field [path]"

   ERROR Level:
   - "Failed to parse XML message: [messageId], error: [error]"
   - "Sanitization failed for field: [path], error: [error]"
   - "Invalid message structure: [details]"

2. Structured Logging Format:
   Create log entries as JSON objects with:
   {
     "timestamp": "ISO 8601 timestamp",
     "level": "INFO|WARNING|ERROR",
     "service": "swift-sanitizer",
     "messageId": "unique message identifier",
     "eventType": "SANITIZATION_APPLIED|VALIDATION_FAILED|etc",
     "details": {
       "fieldType": "NAME|ADDRESS|REMITTANCE",
       "fieldPath": "XPath to field",
       "originalValue": "value before",
       "sanitizedValue": "value after",
       "characterChanges": ["ö→o", "å→a"]
     }
   }

3. Metrics to Track:
   - Total messages processed (counter)
   - Messages sanitized vs. passed through (counter)
   - Sanitization processing time (histogram)
   - Fields sanitized by type (counter per NAME/ADDRESS/REMITTANCE)
   - Most common character replacements (counter)
   - Error rate (counter)

4. Monitoring Hooks:
   Create functions that can integrate with monitoring systems:
   - recordSanitizationEvent(messageId, changes)
   - recordProcessingTime(messageId, durationMs)
   - recordValidationFailure(messageId, violations)
   - recordError(messageId, error)

5. Audit Trail Requirements:
   Create persistent audit records with:
   - Message ID
   - Timestamp
   - Original values
   - Sanitized values
   - User/system that initiated processing
   - Processing duration
   - Result status

Implementation requirements:
1. Support multiple logging backends (console, file, remote)
2. Include log sampling for high-volume scenarios
3. Make logging configurable (levels, formats)
4. Ensure PII/sensitive data is handled appropriately
5. Include correlation IDs for distributed tracing

Return the complete logging and monitoring implementation.
```

**Expected Output:** Production-ready logging framework.

**Validation:** Verify logs are generated correctly for various scenarios and contain all required information.

---

## STEP 11: Create Configuration and Deployment Guide

**Objective:** Provide configuration options and deployment documentation.

### Prompt for AI Agent:

```
Create a configuration system and deployment guide for the SWIFT sanitization system in [YOUR_LANGUAGE]:

1. Configuration File/Object:
   Create a configuration structure with the following options:

   {
     "sanitization": {
       "enabled": true,
       "mode": "STRICT|PERMISSIVE",
       "failOnError": false,
       "preserveWhitespace": true,
       "customCharacterMappings": {
         // Allow users to add custom mappings
       }
     },
     "logging": {
       "level": "INFO|WARNING|ERROR",
       "format": "JSON|TEXT",
       "destination": "CONSOLE|FILE|REMOTE",
       "auditEnabled": true,
       "includeOriginalValues": true
     },
     "processing": {
       "batchSize": 100,
       "maxConcurrentMessages": 10,
       "timeoutMs": 5000
     },
     "validation": {
       "strictMode": true,
       "validateBeforeSanitize": true,
       "rejectInsteadOfSanitize": false
     },
     "messageTypes": {
       "supported": ["pain.001", "pacs.008", "pacs.009"],
       "defaultType": "pain.001"
     }
   }

2. Environment-Specific Configurations:
   - Development (verbose logging, strict validation)
   - Testing (moderate logging, validation enabled)
   - Production (optimized logging, audit enabled)

3. Deployment Checklist:
   Create a comprehensive checklist with:
   □ Verify all dependencies are installed
   □ Configure logging destination
   □ Set up audit trail storage
   □ Configure monitoring/alerting
   □ Test with sample messages
   □ Validate performance benchmarks
   □ Review security settings
   □ Enable error notifications
   □ Document rollback procedure
   □ Set up health checks

4. Integration Documentation:
   Provide step-by-step integration guide:
   - How to add to existing payment pipeline
   - API/function signatures
   - Error handling recommendations
   - Performance tuning tips
   - Scaling considerations

5. Troubleshooting Guide:
   Common issues and solutions:
   - "Characters still invalid after sanitization" → Check Unicode normalization
   - "XML structure corrupted" → Verify namespace handling
   - "Performance degradation" → Enable batch processing
   - "Audit logs too large" → Implement log rotation

Return the complete configuration system and deployment documentation.
```

**Expected Output:** Configuration framework and deployment guide.

**Validation:** Verify configuration changes take effect correctly.

---

## STEP 12: Create Final Documentation Package

**Objective:** Compile comprehensive user and developer documentation.

### Prompt for AI Agent:

```
Create a complete documentation package for the SWIFT character sanitization system:

Required Documents:

1. README.md - Quick Start Guide
   - Project overview
   - Quick start (5-minute setup)
   - Basic usage examples
   - Link to detailed docs

2. ARCHITECTURE.md - Technical Architecture
   - System components diagram
   - Data flow diagrams
   - Integration points
   - Technology stack
   - Design decisions and rationale

3. API_REFERENCE.md - Complete API Documentation
   - All public functions/methods
   - Parameters and return types
   - Usage examples
   - Error codes and handling
   - Version compatibility

4. USER_GUIDE.md - End User Guide
   - How to use the system
   - Integration patterns explained
   - Configuration options
   - Best practices
   - FAQ section

5. DEVELOPER_GUIDE.md - Developer Documentation
   - How to extend the system
   - Adding new character mappings
   - Supporting new message types
   - Contributing guidelines
   - Code style guide

6. TROUBLESHOOTING.md - Troubleshooting Guide
   - Common errors and solutions
   - Debug mode instructions
   - Performance optimization
   - Log analysis guide

7. COMPLIANCE.md - SWIFT Compliance Guide
   - SWIFT character set rules reference
   - Compliance verification steps
   - Audit trail requirements
   - Regulatory considerations

8. CHANGELOG.md - Version History
   - Version tracking
   - Breaking changes
   - New features
   - Bug fixes

Documentation Requirements:
- Clear, concise writing
- Code examples in multiple scenarios
- Visual diagrams where helpful
- Cross-references between documents
- Searchable/indexed content
- Version information

Return the complete documentation package with all 8 documents.
```

**Expected Output:** Complete documentation set ready for publication.

**Validation:** Review documentation for clarity, completeness, and accuracy.

---

## 📊 Success Criteria

The implementation is considered complete when:

✅ **Functional Requirements:**
- [ ] All European diacritical characters (60+) are correctly transliterated
- [ ] Extended character set is properly handled in Name/Address/Remittance fields
- [ ] Base character set is enforced in standard text fields
- [ ] XML structure and namespaces are preserved
- [ ] Unknown characters are replaced with '.' (period)

✅ **Quality Requirements:**
- [ ] Test coverage >90%
- [ ] All tests pass successfully
- [ ] Performance: <15ms per typical pain.001 message
- [ ] Memory efficient (no memory leaks)
- [ ] Thread-safe (if applicable to language)

✅ **Integration Requirements:**
- [ ] At least 3 integration patterns implemented
- [ ] Clear API for external systems
- [ ] Backward compatible with existing systems
- [ ] Graceful error handling

✅ **Operational Requirements:**
- [ ] Comprehensive logging implemented
- [ ] Audit trail capability
- [ ] Configurable behavior
- [ ] Health check endpoint (if applicable)
- [ ] Monitoring hooks available

✅ **Documentation Requirements:**
- [ ] All 8 documentation files complete
- [ ] Code comments thorough
- [ ] Usage examples provided
- [ ] Troubleshooting guide available

---

## 🎯 Technology Adaptation Guide

This guide is language-agnostic. Adapt implementations to your technology stack:

### Java
- Use `HashMap` for transliteration map
- Use `Pattern` and `Matcher` for validation
- Use `DocumentBuilder` for XML parsing
- Use `StringBuilder` for string construction
- Use JUnit for testing

### Python
- Use `dict` for transliteration map
- Use `unicodedata` for normalization
- Use `xml.etree.ElementTree` or `lxml` for XML
- Use `pytest` or `unittest` for testing

### JavaScript/TypeScript
- Use `Object` or `Map` for transliteration
- Use template literals for strings
- Use `DOMParser` or `xml2js` for XML
- Use Jest or Mocha for testing

### C#
- Use `Dictionary<char, string>` for transliteration
- Use `XDocument` or `XmlDocument` for XML
- Use `StringBuilder` for string construction
- Use NUnit or xUnit for testing

### Go
- Use `map[rune]string` for transliteration
- Use `encoding/xml` for XML parsing
- Use `strings.Builder` for string construction
- Use built-in testing framework

---

## 📝 Example Usage (Language-Agnostic Pseudocode)

```
// STEP 1-4: Character sanitization
sanitizer = new SwiftCharacterSanitizer()
result = sanitizer.sanitizeNameOrAddress("Björn Andersson")
print(result)  // Output: "Bjorn Andersson"

// STEP 5-6: Message processing
processor = new MessageProcessor()
painMessage = readFile("pain001_message.xml")
result = processor.processMessage(painMessage)

print(result.wasModified)     // true
print(result.sanitizedXml)    // Clean XML
print(result.changeLog)       // Array of changes

// STEP 7: Validation
validator = new MessageValidator()
violations = validator.validateMessage(painMessage)

if (violations.length > 0) {
    print("Found violations:")
    for (violation in violations) {
        print(violation.fieldPath + ": " + violation.currentValue + 
              " → " + violation.suggestedValue)
    }
}

// STEP 8: Integration pattern
// Pattern 1: Pre-processing
function processIncomingPayment(xmlMessage) {
    // Sanitize immediately
    result = processor.processMessage(xmlMessage)
    
    // Log changes
    if (result.wasModified) {
        logger.warn("Message sanitized", result.changeLog)
    }
    
    // Continue processing with clean message
    validateSchema(result.sanitizedXml)
    enrichMessage(result.sanitizedXml)
    persistToDatabase(result.sanitizedXml)
}
```

---

## 🔄 Iterative Implementation Approach

Implement in phases:

**Phase 1 (Steps 1-4):** Core Sanitization
- Minimum viable product
- Can be used standalone
- ~2-4 hours development

**Phase 2 (Steps 5-6):** Message Processing
- Full XML handling
- Production-ready for single message type
- ~4-6 hours development

**Phase 3 (Steps 7-9):** Testing & Validation
- Enterprise-grade quality
- Comprehensive test coverage
- ~3-5 hours development

**Phase 4 (Steps 10-12):** Production Hardening
- Logging, monitoring, documentation
- Ready for production deployment
- ~3-4 hours development

**Total Estimated Time:** 12-19 hours for complete implementation

---

## 📞 Support and Extension

After completing this implementation:

1. **Extend to other message types:**
    - Adapt STEP 5 to handle pacs.008, pacs.009, pacs.002
    - Add message-type specific field mappings

2. **Add custom character mappings:**
    - Extend transliteration map in STEP 1
    - Add test cases in STEP 9

3. **Integrate with existing systems:**
    - Use patterns from STEP 8
    - Follow deployment guide from STEP 11

4. **Monitor and optimize:**
    - Use metrics from STEP 10
    - Tune configuration from STEP 11

---

**Document Version:** 1.0  
**Last Updated:** October 8, 2025  
**Compatible AI Agents:** Claude Sonnet 4, GPT-4, and similar  
**Status:** Production Ready ✅
