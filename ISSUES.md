# Known Issues and Limitations

This document lists known issues and limitations in RenderDocs SDKs and integrations.

## General

### Document Generation

1. **Maximum document size**: Generated PDFs are limited to 50MB
2. **Template complexity**: Templates with more than 1000 components may timeout
3. **Concurrent requests**: Rate limits apply (see your plan limits)

### File Formats

1. **Excel limitations**:
   - Maximum 1,048,576 rows per sheet (Excel limit)
   - Charts require explicit data ranges
   - Some complex formulas may not be supported

2. **PDF limitations**:
   - Custom fonts require WOFF2 format
   - Some CSS properties have limited support

## Node.js SDK

### v1.0.x

1. **TypeScript strict mode**: Some type definitions may require explicit casting
   - Workaround: Use type assertions where needed

2. **Large file downloads**: Memory usage may spike for documents > 10MB
   - Workaround: Use streaming endpoints (coming in v1.1.0)

## Python SDK

### v1.0.x

1. **Async client cleanup**: Ensure proper cleanup with context managers
   ```python
   async with AsyncRenderDocs(api_key="...") as client:
       # Use client here
   ```

2. **Type hints**: Some nested types may not have full type coverage
   - Workaround: Use `TypedDict` for complex variable structures

## Java SDK

### v1.0.x

1. **Java 8 compatibility**: Lambda expressions work but some Optional patterns require explicit handling

2. **Jackson serialization**: Custom objects require proper annotations for serialization

## Reporting Issues

If you encounter a bug not listed here:

1. Check the [GitHub Issues](https://github.com/renderdocs/developer-resources/issues) for existing reports
2. If not found, create a new issue with:
   - SDK version
   - Language/runtime version
   - Minimal reproduction code
   - Expected vs actual behavior
   - Error messages/stack traces

## Security Issues

For security vulnerabilities, please email security@renderdocs.com directly rather than creating a public issue.
