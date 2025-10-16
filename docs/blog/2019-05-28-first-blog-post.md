---
slug: springdoc-openapi-integration
title: Integrating SpringDoc OpenAPI with Docusaurus
authors: [ejike]
tags: [spring-boot, openapi, documentation, swagger]
---

Learn how we integrated SpringDoc OpenAPI with Docusaurus to create automated, interactive API documentation for our fintech microservices.

<!-- truncate -->

## The Challenge

Managing API documentation for multiple microservices can be challenging. We needed a solution that would:

- Automatically generate API docs from our Spring Boot services
- Provide interactive API testing via Swagger UI
- Integrate seamlessly with our documentation site
- Stay in sync with code changes

## The Solution

We implemented SpringDoc OpenAPI for both microservices:

```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
```

This automatically generates OpenAPI 3.0 specifications at `/v3/api-docs` and provides Swagger UI at `/swagger-ui.html`.

## Benefits

✅ **Automatic Updates** - Documentation stays in sync with code  
✅ **Interactive Testing** - Try APIs directly from the browser  
✅ **Developer Experience** - Easy to explore and understand APIs  
✅ **CI/CD Integration** - Deployed automatically with GitHub Actions

Check out our [API Documentation](/docs/xml-sanitizer/overview) to see it in action!
