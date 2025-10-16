package com.fintech.mapping.service;

import com.fintech.mapping.model.SchemaType;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.ByteArrayInputStream;
import java.util.regex.Pattern;

/**
 * Service to detect whether a pain.001 message is CBPR+ or ISO Standard
 * 
 * Detection Strategy (Heuristic-based):
 * 1. Check for Business Application Header (AppHdr) - CBPR+ requires it
 * 2. Check if NbOfTxs is exactly "1" - CBPR+ restriction
 * 3. Check for UETR presence in specific location
 * 4. Analyze character patterns for FIN-X restrictions
 * 5. Check for single payment information block
 */
@Service
@Slf4j
public class SchemaDetectionService {
    
    // FIN-X character set pattern: [0-9a-zA-Z/\-\?:\(\)\.,'\+ ]
    private static final Pattern FINX_PATTERN = Pattern.compile("^[0-9a-zA-Z/\\-?:().,'\\ +]+$");
    
    /**
     * Detect schema type from XML string
     */
    public SchemaType detectSchemaType(String xmlContent) {
        try {
            Document doc = parseXml(xmlContent);
            return detectSchemaType(doc);
        } catch (Exception e) {
            log.warn("Failed to parse XML for schema detection: {}", e.getMessage());
            return SchemaType.UNKNOWN;
        }
    }
    
    /**
     * Detect schema type from parsed Document
     */
    public SchemaType detectSchemaType(Document doc) {
        int cbprScore = 0;
        int isoScore = 0;
        
        log.debug("Starting schema detection...");
        
        // 1. Check for AppHdr (Business Application Header) - Strong CBPR+ indicator
        if (hasAppHdr(doc)) {
            cbprScore += 50;
            log.debug("✓ AppHdr found (+50 CBPR+ score) - CBPR+ requires this");
        } else {
            isoScore += 10;
            log.debug("✗ No AppHdr (+10 ISO score) - ISO doesn't require this");
        }
        
        // 2. Check NbOfTxs (Number of Transactions)
        String nbOfTxs = getElementText(doc, "NbOfTxs");
        if ("1".equals(nbOfTxs)) {
            cbprScore += 20;
            log.debug("✓ NbOfTxs is '1' (+20 CBPR+ score) - CBPR+ requires exactly 1");
        } else if (nbOfTxs != null && !nbOfTxs.equals("1")) {
            isoScore += 40;
            log.debug("✓ NbOfTxs is '{}' (+40 ISO score) - CBPR+ only allows '1'", nbOfTxs);
        }
        
        // 3. Check for UETR (Unique End-to-End Transaction Reference)
        if (hasUETR(doc)) {
            cbprScore += 15;
            log.debug("✓ UETR found (+15 CBPR+ score) - Mandatory in CBPR+");
        } else {
            isoScore += 5;
            log.debug("✗ No UETR (+5 ISO score) - Optional in ISO");
        }
        
        // 4. Check for single PmtInf (Payment Information) block
        int pmtInfCount = countElements(doc, "PmtInf");
        if (pmtInfCount == 1) {
            cbprScore += 10;
            log.debug("✓ Single PmtInf block (+10 CBPR+ score) - CBPR+ allows only 1");
        } else if (pmtInfCount > 1) {
            isoScore += 30;
            log.debug("✓ Multiple PmtInf blocks: {} (+30 ISO score) - CBPR+ only allows 1", pmtInfCount);
        }
        
        // 5. Check MsgId for FIN-X character set compliance
        String msgId = getElementText(doc, "MsgId");
        if (msgId != null && FINX_PATTERN.matcher(msgId).matches()) {
            cbprScore += 10;
            log.debug("✓ MsgId follows FIN-X pattern (+10 CBPR+ score)");
        } else if (msgId != null) {
            isoScore += 10;
            log.debug("✓ MsgId contains non-FIN-X characters (+10 ISO score)");
        }
        
        // 6. Check for BIC in FwdgAgt (Forwarding Agent) - mandatory in CBPR+
        if (hasBICFI(doc, "FwdgAgt")) {
            cbprScore += 5;
            log.debug("✓ BIC in FwdgAgt (+5 CBPR+ score) - Mandatory in CBPR+");
        }
        
        log.info("Schema Detection Scores - CBPR+: {}, ISO: {}", cbprScore, isoScore);
        
        // Determine schema based on scores
        if (cbprScore > isoScore && cbprScore >= 50) {
            log.info("✓ Detected Schema: CBPR+ (High confidence)");
            return SchemaType.CBPR_PLUS;
        } else if (isoScore > cbprScore) {
            log.info("✓ Detected Schema: ISO Standard");
            return SchemaType.ISO_STANDARD;
        } else if (cbprScore >= 30) {
            log.info("✓ Detected Schema: CBPR+ (Moderate confidence)");
            return SchemaType.CBPR_PLUS;
        } else {
            log.info("? Detected Schema: ISO Standard (Default)");
            return SchemaType.ISO_STANDARD; // Default to ISO
        }
    }
    
    /**
     * Check if document has AppHdr (Business Application Header)
     */
    private boolean hasAppHdr(Document doc) {
        NodeList appHdrList = doc.getElementsByTagNameNS("*", "AppHdr");
        if (appHdrList.getLength() == 0) {
            appHdrList = doc.getElementsByTagName("AppHdr");
        }
        return appHdrList.getLength() > 0;
    }
    
    /**
     * Check if document has UETR element
     */
    private boolean hasUETR(Document doc) {
        NodeList uetrList = doc.getElementsByTagNameNS("*", "UETR");
        if (uetrList.getLength() == 0) {
            uetrList = doc.getElementsByTagName("UETR");
        }
        return uetrList.getLength() > 0;
    }
    
    /**
     * Check if specific parent element contains BICFI
     */
    private boolean hasBICFI(Document doc, String parentElementName) {
        NodeList parentList = doc.getElementsByTagNameNS("*", parentElementName);
        if (parentList.getLength() == 0) {
            parentList = doc.getElementsByTagName(parentElementName);
        }
        
        for (int i = 0; i < parentList.getLength(); i++) {
            Element parent = (Element) parentList.item(i);
            NodeList bicList = parent.getElementsByTagNameNS("*", "BICFI");
            if (bicList.getLength() == 0) {
                bicList = parent.getElementsByTagName("BICFI");
            }
            if (bicList.getLength() > 0) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Get text content of first matching element
     */
    private String getElementText(Document doc, String elementName) {
        NodeList nodeList = doc.getElementsByTagNameNS("*", elementName);
        if (nodeList.getLength() == 0) {
            nodeList = doc.getElementsByTagName(elementName);
        }
        
        if (nodeList.getLength() > 0) {
            return nodeList.item(0).getTextContent();
        }
        return null;
    }
    
    /**
     * Count occurrences of element
     */
    private int countElements(Document doc, String elementName) {
        NodeList nodeList = doc.getElementsByTagNameNS("*", elementName);
        if (nodeList.getLength() == 0) {
            nodeList = doc.getElementsByTagName(elementName);
        }
        return nodeList.getLength();
    }
    
    /**
     * Parse XML string to Document
     */
    private Document parseXml(String xmlContent) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(xmlContent.getBytes("UTF-8")));
    }
}
