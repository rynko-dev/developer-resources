# Webhook Handler Example

This example demonstrates how to receive and process Renderbase webhook events for document generation status updates.

## Prerequisites

- Node.js 18+
- Renderbase API key and webhook secret
- A publicly accessible URL (use ngrok for local development)

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file:
   ```bash
   RENDERBASE_API_KEY=your-api-key
   WEBHOOK_SECRET=your-webhook-secret
   PORT=3000
   ```

3. Start the server:
   ```bash
   npm start
   ```

4. For local development, use ngrok:
   ```bash
   ngrok http 3000
   ```

5. Register your webhook URL in Renderbase:
   - Go to Dashboard > Settings > Webhooks
   - Add your ngrok URL: `https://your-subdomain.ngrok.io/webhooks/renderbase`

## Webhook Events

Renderbase sends the following webhook events:

| Event | Description |
|-------|-------------|
| `document.generated` | Document generated successfully |
| `document.failed` | Document generation failed |
| `document.downloaded` | Document was downloaded |

## Event Payload

```json
{
  "id": "evt_abc123",
  "type": "document.generated",
  "createdAt": "2025-01-15T10:30:00.000Z",
  "data": {
    "jobId": "job_xyz789",
    "templateId": "tmpl_invoice",
    "format": "pdf",
    "downloadUrl": "https://api.renderbase.dev/api/v1/documents/jobs/job_xyz789/download",
    "expiresAt": "2025-01-22T10:30:00.000Z",
    "metadata": {
      "invoiceNumber": "INV-001"
    }
  }
}
```

## Signature Verification

Always verify webhook signatures to ensure events are from Renderbase:

```typescript
import { verifyWebhookSignature } from '@renderbase/sdk';

const event = verifyWebhookSignature({
  payload: requestBody,
  signature: headers['x-renderbase-signature'],
  secret: process.env.WEBHOOK_SECRET,
});
```

## Related Resources

- [Webhook Documentation](https://docs.renderbase.dev/webhooks)
- [Security Best Practices](https://docs.renderbase.dev/webhooks/security)
