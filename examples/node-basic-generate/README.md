# Basic Document Generation (Node.js)

This example shows how to generate PDF and Excel documents using the Rynko Node.js SDK.

## Prerequisites

- Node.js 18+
- Rynko API key ([get one here](https://rynko.dev/dashboard/api-keys))
- A template created in Rynko

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file with your API key:
   ```bash
   RYNKO_API_KEY=your-api-key-here
   ```

## Usage

### Generate a PDF

```bash
npm run generate:pdf
```

### Generate an Excel file

```bash
npm run generate:excel
```

## Code Examples

### Basic PDF Generation

```typescript
import { Rynko } from '@rynko/sdk';

const client = new Rynko({
  apiKey: process.env.RYNKO_API_KEY,
});

const result = await client.documents.generate({
  templateId: 'your-template-id',
  format: 'pdf',
  variables: {
    title: 'My Document',
    date: new Date().toISOString().split('T')[0],
  },
});

console.log('Download URL:', result.downloadUrl);
```

### PDF with Dynamic Data

```typescript
const invoice = await client.documents.generate({
  templateId: 'tmpl_invoice',
  format: 'pdf',
  variables: {
    invoiceNumber: 'INV-2025-001',
    customer: {
      name: 'Acme Corporation',
      address: {
        line1: '123 Business St',
        city: 'San Francisco',
        state: 'CA',
        postalCode: '94102',
      },
    },
    items: [
      { description: 'Consulting Services', quantity: 10, rate: 150, amount: 1500 },
      { description: 'Software License', quantity: 1, rate: 500, amount: 500 },
    ],
    subtotal: 2000,
    tax: 160,
    total: 2160,
  },
});
```

### Excel Generation

```typescript
const report = await client.documents.generate({
  templateId: 'tmpl_report',
  format: 'excel',
  variables: {
    reportTitle: 'Monthly Sales Report',
    month: 'December 2025',
    salesData: [
      { region: 'North', sales: 125000, target: 100000 },
      { region: 'South', sales: 98000, target: 90000 },
      { region: 'East', sales: 142000, target: 120000 },
      { region: 'West', sales: 88000, target: 95000 },
    ],
  },
});
```

## Template Variables

Variables in your template use the `{{variableName}}` syntax:

- **Simple variables**: `{{title}}`, `{{date}}`
- **Nested objects**: `{{customer.name}}`, `{{customer.address.city}}`
- **Array loops**: Use `{{#each items}}...{{/each}}` in templates

## Error Handling

```typescript
import { Rynko, RynkoError } from '@rynko/sdk';

try {
  const result = await client.documents.generate({...});
} catch (error) {
  if (error instanceof RynkoError) {
    console.error('API Error:', error.message);
    console.error('Error Code:', error.code);
    console.error('Status:', error.status);
  } else {
    throw error;
  }
}
```

## Related Resources

- [API Reference](https://docs.rynko.dev/api-reference)
- [Template Schema](https://docs.rynko.dev/developer-guide/template-schema)
- [SDK Documentation](https://docs.rynko.dev/sdk/node)
