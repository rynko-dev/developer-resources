# Rynko Developer Resources

Official developer resources for [Rynko](https://rynko.dev) - the document generation platform for creating professional PDFs and Excel files from templates.

## What is Rynko?

Rynko is a document generation platform that lets you:

- **Design once, generate everywhere**: Create templates that generate both PDF and Excel documents
- **Generate PDFs**: Professional documents with tables, charts, QR codes, and more
- **Generate Excel files**: Spreadsheets with formulas, charts, and multiple sheets
- **API-first**: RESTful API with SDKs for Node.js, Python, and Java
- **Template variables**: Dynamic content with loops, conditionals, and calculations
- **Webhook events**: Track document generation status in real-time

## Resources

### SDKs

Official client libraries for integrating Rynko into your applications:

| Language | Package | Repository | Registry |
|----------|---------|------------|----------|
| Node.js | `@rynko/sdk` | [rynko-dev/sdk-node](https://github.com/rynko-dev/sdk-node) | [![npm](https://img.shields.io/npm/v/@rynko/sdk)](https://www.npmjs.com/package/@rynko/sdk) |
| Python | `rynko` | [rynko-dev/sdk-python](https://github.com/rynko-dev/sdk-python) | [![PyPI](https://img.shields.io/pypi/v/rynko)](https://pypi.org/project/rynko/) |
| Java | `dev.rynko:sdk` | [rynko-dev/sdk-java](https://github.com/rynko-dev/sdk-java) | [![Maven](https://img.shields.io/maven-central/v/dev.rynko/sdk)](https://search.maven.org/artifact/dev.rynko/sdk) |

### Examples

Ready-to-use code examples and starter projects:

| Example | Description |
|---------|-------------|
| [Basic Generate (Node.js)](./examples/node-basic-generate) | Generate your first PDF with Rynko |
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

Sign up at [rynko.dev](https://rynko.dev) and create an API key from your dashboard.

### 2. Install the SDK

```bash
# Node.js
npm install @rynko/sdk

# Python
pip install rynko

# Java (Maven)
<dependency>
  <groupId>dev.rynko</groupId>
  <artifactId>sdk</artifactId>
  <version>1.0.0</version>
</dependency>
```

### 3. Generate your first document

```javascript
// Node.js
import { Rynko } from '@rynko/sdk';

const client = new Rynko({
  apiKey: process.env.RYNKO_API_KEY,
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
from rynko import Rynko

client = Rynko(api_key="your-api-key")

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
import dev.rynko.Rynko;
import dev.rynko.models.*;

Rynko client = new Rynko("your-api-key");

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

- **API Reference**: [docs.rynko.dev/api-reference](https://docs.rynko.dev/api-reference)
- **Developer Guide**: [docs.rynko.dev/developer-guide](https://docs.rynko.dev/developer-guide)
- **Template Schema**: [docs.rynko.dev/developer-guide/template-schema](https://docs.rynko.dev/developer-guide/template-schema)

## Support

- **Issues & Bug Reports**: [GitHub Issues](./ISSUES.md)
- **Feature Requests**: [GitHub Discussions](https://github.com/rynko-dev/developer-resources/discussions)
- **Email Support**: support@rynko.dev

## Roadmap

See our [public roadmap](./ROADMAP.md) for upcoming features and improvements.

## License

The code in this repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

Templates and documentation are licensed under CC BY 4.0.
