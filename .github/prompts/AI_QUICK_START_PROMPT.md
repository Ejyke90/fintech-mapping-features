# Quick-Start AI Agent Prompt: SWIFT Character Sanitization

## 🚀 Prompt for AI Agent

Use this prompt with Claude Sonnet 4, GPT-4, or similar AI coding agents to implement SWIFT character sanitization in any language.

---

## Single Comprehensive Prompt

```
I need you to implement a SWIFT FIN X character set sanitization system for ISO 20022 payment messages (pain.001, pacs.008, etc.) in [SPECIFY YOUR LANGUAGE: Java/Python/C#/JavaScript/Go/etc.].

PROBLEM:
Payment messages containing names like "Björn" or "Åke" fail SWIFT validation because they contain diacritical marks (ö, å) that are not part of the SWIFT FIN X character set.

SWIFT ALLOWED CHARACTERS:
- Base (all fields): a-z A-Z 0-9 / - ? : ( ) . , ' + space
- Extended (Name/Address/Remittance only): ! # & % * = ^ _ ' { | } ~ " ; @ [ \ ] $ < >
- NOT allowed: ö å ä ü é è ñ ç and other diacritics, emojis, CJK characters

SOLUTION REQUIREMENTS:
Build a system that automatically transliterates non-compliant characters to SWIFT-compliant equivalents (e.g., Björn → Bjorn, François → Francois).

IMPLEMENTATION STEPS:

1. CHARACTER TRANSLITERATION MAP
   Create a HashMap/Dictionary mapping diacritical characters to ASCII:
   - Scandinavian: å→a, ä→a, ö→o, ø→o, æ→ae
   - German: ü→u, ö→o, ä→a, ß→ss
   - French: é→e, è→e, ê→e, ç→c, à→a
   - Spanish: ñ→n, á→a, é→e, í→i, ó→o, ú→u
   - Polish: ł→l, ą→a, ć→c, ę→e, ń→n, ś→s, ź→z, ż→z
   - Czech: č→c, ď→d, ř→r, š→s, ž→z
   Include both uppercase and lowercase (60+ total mappings)

2. VALIDATION FUNCTIONS
   Create functions to check if characters are SWIFT-compliant:
   - isBaseFinXCharacter(char) - for standard text fields
   - isExtendedFinXCharacter(char) - for Name/Address/Remittance fields
   - isValidForFieldType(char, fieldType) - field-type aware validation

3. CORE SANITIZATION LOGIC
   Implement: sanitizeText(input, allowExtendedCharset)
   Algorithm:
   - For each character in input:
     * If allowed → keep it
     * If in transliteration map → replace with mapped value
     * Try Unicode normalization (NFD)
     * Otherwise → replace with '.' (period)
   - Return SWIFT-compliant string

4. CONVENIENCE WRAPPERS
   Create easy-to-use functions:
   - sanitizeNameOrAddress(input)
   - sanitizeRemittanceInfo(input)
   - sanitizeStandardText(input)
   - isValidNameOrAddress(input)
   - isValidStandardText(input)

5. XML MESSAGE PARSER
   Parse ISO 20022 pain.001 messages and extract:
   - NAME fields: //InitgPty/Nm, //Dbtr/Nm, //Cdtr/Nm, etc.
   - ADDRESS fields: //PstlAdr/AdrLine, //PstlAdr/StrtNm, //PstlAdr/TwnNm
   - REMITTANCE fields: //RmtInf/Ustrd, //RmtInf/Strd/*
   Use DOM/lxml/xml parsing library with namespace support

6. MESSAGE PROCESSOR
   Create: processMessage(xmlString) that:
   - Parses XML
   - Extracts and sanitizes all Name, Address, Remittance fields
   - Updates XML nodes with sanitized values
   - Returns: {sanitizedXml, changeLog, wasModified}
   - Logs all changes for audit trail

7. VALIDATION & REPORTING
   Implement:
   - validateMessage(xmlString) - check compliance without modifying
   - generateSanitizationReport(changeLog) - human-readable report
   - analyzeCharacterIssues(text) - detailed character analysis

8. INTEGRATION PATTERNS
   Provide 3 ready-to-use patterns:
   - Pre-Processing: Sanitize on message receipt
   - Validation Pipeline: Check first, sanitize if needed
   - Just-in-Time: Sanitize before SWIFT transmission

9. COMPREHENSIVE TESTS
   Test suite covering:
   - All European diacritics (Scandinavian, German, French, Spanish, Polish, Czech)
   - Unicode normalization
   - Edge cases (null, empty, emojis, CJK)
   - Real names: "Björn Andersson", "François Müller", "José García", "Søren Østergård"
   - XML structure preservation
   - Test coverage goal: >90%

10. LOGGING & MONITORING
    Implement structured logging:
    - INFO: Message processed successfully
    - WARNING: Field sanitized (show original → sanitized)
    - ERROR: Parse/sanitization failures
    Include metrics tracking and audit trail

DELIVERABLES:
1. Core sanitization library with all functions
2. Message processor for pain.001 messages
3. Comprehensive test suite (>50 test cases)
4. Integration examples (3 patterns)
5. Documentation (README, API reference, usage guide)

VALIDATION:
Test with this example - should sanitize all diacritics:
```xml
<Dbtr><Nm>Björn Andersson</Nm></Dbtr>
<Cdtr><Nm>François Müller</Nm></Cdtr>
<RmtInf><Ustrd>Payment für Björn</Ustrd></RmtInf>
```

Expected output:
```xml
<Dbtr><Nm>Bjorn Andersson</Nm></Dbtr>
<Cdtr><Nm>Francois Muller</Nm></Cdtr>
<RmtInf><Ustrd>Payment fur Bjorn</Ustrd></RmtInf>
```

Please implement this system step by step, starting with the character transliteration map (Step 1) and building up to the complete solution. Show code for each component and explain key design decisions.
```

---

## Alternative: Incremental Prompts

If you prefer step-by-step guidance, use these individual prompts:

### Prompt 1: Character Map
```
Create a character transliteration map in [YOUR_LANGUAGE] that maps European diacritical characters to ASCII equivalents. Include:
- Scandinavian: å→a, ä→a, ö→o, ø→o, æ→ae (both cases)
- German: ü→u, ö→o, ä→a, ß→ss (both cases)
- French: é→e, è→e, ê→e, ë→e, ç→c, à→a, etc. (both cases)
- Spanish: ñ→n, á→a, é→e, í→i, ó→o, ú→u (both cases)
- Polish: ł→l, ą→a, ć→c, ę→e, ń→n, ś→s, ź→z, ż→z (both cases)
- Czech: č→c, ď→d, ě→e, ň→n, ř→r, š→s, ť→t, ž→z (both cases)

Use a HashMap/Dictionary for O(1) lookup. Make it easily extensible.
```

### Prompt 2: Validation Functions
```
Implement SWIFT character validation functions in [YOUR_LANGUAGE]:

1. isBaseFinXCharacter(char) - Returns boolean
   Allowed: a-z A-Z 0-9 / - ? : ( ) . , ' + space

2. isExtendedFinXCharacter(char) - Returns boolean
   Allowed: Base chars PLUS ! # & % * = ^ _ ' { | } ~ " ; @ [ \ ] $ < >

3. isValidForFieldType(char, fieldType) - Returns boolean
   Use extended for NAME/ADDRESS/REMITTANCE, base for STANDARD
```

### Prompt 3: Core Sanitization
```
Implement sanitizeText(input, allowExtendedCharset) in [YOUR_LANGUAGE]:

Algorithm:
- For each character in input:
    1. If allowed (use validation functions) → keep it
    2. If in transliteration map → use mapped value
    3. Try Unicode normalization (NFD form)
    4. Otherwise → replace with '.'
- Return SWIFT-compliant string

Test with: "Björn" → "Bjorn", "Café!" → "Cafe!", "Hello 😊" → "Hello ."
```

### Prompt 4: XML Processing
```
Implement an ISO 20022 pain.001 message processor in [YOUR_LANGUAGE] that:

1. Parses XML (handle namespaces)
2. Extracts NAME fields (//InitgPty/Nm, //Dbtr/Nm, //Cdtr/Nm, etc.)
3. Extracts ADDRESS fields (//PstlAdr/AdrLine, //PstlAdr/StrtNm, etc.)
4. Extracts REMITTANCE fields (//RmtInf/Ustrd, etc.)
5. Sanitizes each field using the sanitization functions
6. Updates XML nodes
7. Returns sanitized XML + change log

Preserve XML structure and namespaces.
```

### Prompt 5: Testing
```
Create comprehensive tests in [YOUR_LANGUAGE] for the SWIFT sanitization system:

Test these real-world names:
- Björn Andersson → Bjorn Andersson (Swedish)
- Åke Björkström → Ake Bjorkstrom (Swedish)
- François Müller → Francois Muller (French/German)
- José María García → Jose Maria Garcia (Spanish)
- Søren Østergård → Soren Ostergard (Danish)
- Władysław Łódź → Wladyslaw Lodz (Polish)
- Vladimír Dvořák → Vladimir Dvorak (Czech)

Include edge cases: null, empty, emojis, CJK characters, already-compliant text.
Test XML structure preservation and idempotency.
Aim for >90% code coverage.
```

---

## Customization Variables

Before using the prompt, customize these:

1. **[YOUR_LANGUAGE]** - Replace with: Java, Python, C#, JavaScript, TypeScript, Go, Ruby, etc.

2. **[YOUR_FRAMEWORK]** - If applicable: Spring Boot, Django, .NET Core, Express, etc.

3. **[YOUR_TEST_FRAMEWORK]** - JUnit, pytest, NUnit, Jest, Mocha, etc.

4. **[YOUR_XML_LIBRARY]** - JAXP, lxml, System.Xml, xml2js, encoding/xml, etc.

5. **[YOUR_BUILD_TOOL]** - Maven, Gradle, pip, npm, NuGet, Go modules, etc.

---

## Expected Outputs

After running the comprehensive prompt, you should receive:

### Phase 1: Core Components (~30 minutes)
- ✅ Character transliteration map (60+ mappings)
- ✅ Validation functions (3 functions)
- ✅ Core sanitization logic
- ✅ Convenience wrapper functions

### Phase 2: Message Processing (~45 minutes)
- ✅ XML parser for pain.001
- ✅ Message processor with change logging
- ✅ Field extraction logic
- ✅ XML serialization

### Phase 3: Integration & Testing (~60 minutes)
- ✅ 3 integration patterns
- ✅ Comprehensive test suite (>50 tests)
- ✅ Validation and reporting functions
- ✅ Real-world test data

### Phase 4: Production Features (~30 minutes)
- ✅ Structured logging
- ✅ Monitoring hooks
- ✅ Configuration system
- ✅ Documentation

**Total Time: ~2.5 hours** (may vary based on language and AI agent performance)

---

## Validation Checklist

After implementation, verify:

- [ ] "Björn" becomes "Bjorn"
- [ ] "Åke" becomes "Ake"
- [ ] "François" becomes "Francois"
- [ ] "Müller" becomes "Muller"
- [ ] Extended chars (!, &, #) are preserved in Name fields
- [ ] Extended chars are rejected in standard text fields
- [ ] XML structure is preserved after processing
- [ ] Change log captures all sanitization events
- [ ] Tests pass with >90% coverage
- [ ] Performance: <15ms per message

---

## Example Follow-Up Prompts

If the AI agent needs clarification:

**For character mapping:**
```
Add these additional character mappings to the transliteration map:
[list specific characters]
```

**For XML handling:**
```
The XML parser should also handle pacs.008 messages. Add support for:
- //GrpHdr/InstgAgt/FinInstnId/Nm
- //CdtTrfTxInf/Cdtr/Nm
  etc.
```

**For testing:**
```
Add test cases for these edge scenarios:
- Very long names (>100 characters)
- Names with multiple consecutive diacritics
- Null values in XML fields
```

**For performance:**
```
Optimize the sanitization logic for processing batches of 1000+ messages.
Add batch processing support with parallel execution.
```

---

## Success Metrics

Your implementation is successful when:

✅ All European diacritics are correctly transliterated  
✅ XML structure is preserved  
✅ Tests achieve >90% coverage  
✅ Performance meets <15ms per message  
✅ Logging provides complete audit trail  
✅ Integration patterns work in real systems  
✅ Documentation is clear and complete  

---

## Troubleshooting

**If AI agent produces incomplete code:**
- Use incremental prompts (Prompts 1-5) instead of comprehensive prompt
- Ask for specific components one at a time
- Request detailed comments and explanations

**If character mappings are missing:**
- Provide the full list from the comprehensive prompt
- Ask to "complete all 60+ character mappings"

**If XML handling is incorrect:**
- Specify your exact message type (pain.001.001.03, pacs.008.001.08, etc.)
- Provide sample XML structure
- Request namespace-aware parsing

**If tests are insufficient:**
- Provide the exact test data from the comprehensive prompt
- Request specific test categories (unit, integration, edge cases)
- Ask for higher coverage percentage

---

**Prompt Template Version:** 1.0  
**Last Updated:** October 8, 2025  
**Compatible With:** Claude Sonnet 4, GPT-4, GPT-4 Turbo, Claude 3 Opus  
**Tested Languages:** Java, Python, C#, JavaScript, TypeScript, Go  
**Status:** Production Ready ✅
