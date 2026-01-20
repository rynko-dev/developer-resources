# Renderbase Developer Resources

Official developer resources for [Renderbase](https://renderbase.dev) - the document generation platform for creating professional PDFs and Excel files from templates.

## What is Renderbase?

Renderbase is a document generation platform that lets you:

- **Design once, generate everywhere**: Create templates that generate both PDF and Excel documents
- **Generate PDFs**: Professional documents with tables, charts, QR codes, and more
- **Generate Excel files**: Spreadsheets with formulas, charts, and multiple sheets
- **API-first**: RESTful API with SDKs for Node.js, Python, and Java
- **Template variables**: Dynamic content with loops, conditionals, and calculations
- **Webhook events**: Track document generation status in real-time

## Resources

### SDKs

Official client libraries for integrating Renderbase into your applications:

| Language | Package | Repository | Registry |
|----------|---------|------------|----------|
| Node.js | `@renderbase/sdk` | [renderbase/sdk-node](https://github.com/renderbase/sdk-node) | [![npm](https://img.shields.io/npm/v/@renderbase/sdk)](https://www.npmjs.com/package/@renderbase/sdk) |
| Python | `renderbase` | [renderbase/sdk-python](https://github.com/renderbase/sdk-python) | [![PyPI](https://img.shields.io/pypi/v/renderbase)](https://pypi.org/project/renderbase/) |
| Java | `renderbase-sdk` | [renderbase/sdk-java](https://github.com/renderbase/sdk-java) | [![Maven](https://img.shields.io/maven-central/v/com.renderbase/sdk)](https://search.maven.org/artifact/com.renderbase/sdk) |

### Examples

Ready-to-use code examples and starter projects:

| Example | Description |
|---------|-------------|
| [Basic Generate (Node.js)](./examples/node-basic-generate) | Generate your first PDF with Renderbase |
| [Basic Generate (Python)](./examples/python-basic-generate) | Generate PDFs using Python |
| [Batch Documents](./examples/batch-documents) | Generate multiple documents from data |
| [Webhook Handler](./examples/webhook-handler) | Handle document generation events |

### Templates

Sample PDF and Excel templates in JSON format:

| Template | Type | Description |
|----------|------|-------------|
| [Invoice](./templates/invoice.json) | PDF | Professional invoice template |
| [Report](./templates/report.json) | PDF | Business report with charts |
| [Data Export](./templates/data-export.json) | Excel | Spreadsheet export template |

### Legal & Compliance

- [Data Processing Agreement (DPA)](./legal/DPA.md)
- [Terms of Service](./legal/TERMS.md)

## Quick Start

### 1. Get your API Key

Sign up at [renderbase.dev](https://renderbase.dev) and create an API key from your dashboard.

### 2. Install the SDK

```bash
# Node.js
npm install @renderbase/sdk

# Python
pip install renderbase

# Java (Maven)
<dependency>
  <groupId>com.renderbase</groupId>
  <artifactId>sdk</artifactId>
  <version>1.0.0</version>
</dependency>
```

### 3. Generate your first document

```javascript
// Node.js
import { Renderbase } from '@renderbase/sdk';

const client = new Renderbase({
  apiKey: process.env.RENDERBASE_API_KEY,
});

const result = await client.documents.generate({
  templateId: 'tmpl_invoice',
  format: 'pdf',
  variables: {
    invoiceNumber: 'INV-001',
    customerName: 'Acme Corp',
    items: [
      { description: 'Consulting', quantity: 10, rate: 150, amount: 1500 },
    ],
    total: 1500,
  },
});

console.log('Document URL:', result.downloadUrl);
```

```python
# Python
from renderbase import Renderbase

client = Renderbase(api_key="your-api-key")

result = client.documents.generate(
    template_id="tmpl_invoice",
    format="pdf",
    variables={
        "invoiceNumber": "INV-001",
        "customerName": "Acme Corp",
        "items": [
            {"description": "Consulting", "quantity": 10, "rate": 150, "amount": 1500},
        ],
        "total": 1500,
    },
)

print(f"Document URL: {result['downloadUrl']}")
```

```java
// Java
import com.renderbase.Renderbase;
import com.renderbase.models.*;

Renderbase client = new Renderbase("your-api-key");

Map<String, Object> variables = new HashMap<>();
variables.put("invoiceNumber", "INV-001");
variables.put("customerName", "Acme Corp");
variables.put("total", 1500);

GenerateResult result = client.documents().generate(
    GenerateRequest.builder()
        .templateId("tmpl_invoice")
        .format("pdf")
        .variables(variables)
        .build()
);

System.out.println("Document URL: " + result.getDownloadUrl());
```

## Documentation

- **API Reference**: [docs.renderbase.dev/api-reference](https://docs.renderbase.dev/api-reference)
- **Developer Guide**: [docs.renderbase.dev/developer-guide](https://docs.renderbase.dev/developer-guide)
- **Template Schema**: [docs.renderbase.dev/developer-guide/template-schema](https://docs.renderbase.dev/developer-guide/template-schema)

## Support

- **Issues & Bug Reports**: [GitHub Issues](./ISSUES.md)
- **Feature Requests**: [GitHub Discussions](https://github.com/renderbase/developer-resources/discussions)
- **Email Support**: support@renderbase.dev

## Roadmap

See our [public roadmap](./ROADMAP.md) for upcoming features and improvements.

## License

The code in this repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

Templates and documentation are licensed under CC BY 4.0.
