package com.fintech.sanitizer.controller;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class XmlSanitizerController {

    @PostMapping(value = "/sanitize-chars", 
                 consumes = MediaType.APPLICATION_XML_VALUE,
                 produces = MediaType.APPLICATION_XML_VALUE)
    public String sanitizeXml(@RequestBody String xmlPayload) {
        // For now, just return success response
        return "<Success>Yes</Success>";
    }
}
