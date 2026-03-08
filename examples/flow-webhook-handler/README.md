# Flow Webhook Handler

This example demonstrates how to receive and process Rynko Flow webhook events using an Express server with signature verification.

## What It Does

1. Starts an Express server with a webhook endpoint
2. Verifies webhook signatures to ensure events are from Rynko
3. Handles Flow-specific webhook events:
   - `flow.run.completed` -- Run finished validation
   - `flow.run.approved` -- Run was approved
   - `flow.run.rejected` -- Run was rejected
   - `flow.run.review_required` -- Run needs human review
   - `flow.delivery.failed` -- Delivery failed (with retry example)

## Prerequisites

- Node.js 18+
- Rynko API key and webhook secret
- A publicly accessible URL (use ngrok for local development)

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file:
   ```bash
   RYNKO_API_KEY=your-api-key
   WEBHOOK_SECRET=your-webhook-secret
   PORT=3000
   ```

3. Start the server:
   ```bash
   npm start
   ```

   For development with auto-reload:
   ```bash
   npm run dev
   ```

4. For local development, use ngrok:
   ```bash
   ngrok http 3000
   ```

5. Register your webhook URL in Rynko:
   - Go to Dashboard > Settings > Webhooks
   - Add your ngrok URL: `https://your-subdomain.ngrok.io/webhooks/flow`
   - Select Flow events to subscribe to

## Flow Webhook Events

| Event | Description |
|-------|-------------|
| `flow.run.completed` | Run finished validation successfully |
| `flow.run.approved` | Run was approved (automatically or by reviewer) |
| `flow.run.rejected` | Run was rejected (automatically or by reviewer) |
| `flow.run.review_required` | Run needs human review before proceeding |
| `flow.delivery.failed` | Webhook delivery to your endpoint failed |

## Event Payload

```json
{
  "id": "evt_abc123",
  "type": "flow.run.approved",
  "createdAt": "2026-03-07T10:30:00.000Z",
  "data": {
    "runId": "run_xyz789",
    "gateId": "gate_abc123",
    "gateName": "Order Validation",
    "status": "approved",
    "input": {
      "customerName": "Acme Corp",
      "amount": 500
    },
    "output": {
      "validatedAt": "2026-03-07T10:30:00.000Z"
    },
    "metadata": {
      "source": "checkout"
    }
  }
}
```

## Related Resources

- [Flow Documentation](https://docs.rynko.dev/api-reference/flow)
- [Webhook Documentation](https://docs.rynko.dev/webhooks)
- [Security Best Practices](https://docs.rynko.dev/webhooks/security)
