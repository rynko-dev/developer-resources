# Submit and Monitor Flow Runs (Node.js)

This example shows how to submit a run to a Rynko Flow gate, wait for validation to complete, and handle the result.

## What It Does

1. Lists your published Flow gates
2. Submits a run with sample customer order data to the first gate
3. Waits for the run to reach a terminal state (approved, rejected, etc.)
4. Prints the outcome and lists any deliveries

## Prerequisites

- Node.js 18+
- Rynko API key ([get one here](https://rynko.dev/dashboard/api-keys))
- A published Flow gate in your Rynko workspace

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

```bash
npm start
```

## Code Examples

### Submit a Run

Runs are validated asynchronously. The `submitRun()` method queues the run and returns immediately. Use `waitForRun()` to poll until validation completes.

```typescript
import { Rynko } from '@rynko/sdk';

const client = new Rynko({
  apiKey: process.env.RYNKO_API_KEY,
});

// Submit a run to a gate
const run = await client.flow.submitRun('gate_abc123', {
  input: {
    customerName: 'Acme Corporation',
    email: 'orders@acme.com',
    amount: 2500.00,
    items: [
      { sku: 'WIDGET-001', quantity: 10, unitPrice: 250.00 },
    ],
  },
  metadata: { source: 'api-example' },
});

console.log('Run ID:', run.id);
console.log('Status:', run.status); // 'pending'

// Wait for validation to complete
const result = await client.flow.waitForRun(run.id);

if (result.status === 'approved') {
  console.log('Approved!', result.output);
} else if (result.status === 'rejected') {
  console.log('Rejected:', result.errors);
}
```

### Handle All Outcomes

```typescript
const result = await client.flow.waitForRun(run.id);

switch (result.status) {
  case 'approved':
    console.log('Run approved. Output:', result.output);
    break;
  case 'rejected':
    console.log('Run rejected. Errors:', result.errors);
    break;
  case 'review_required':
    console.log('Human review required.');
    break;
  case 'validation_failed':
    console.log('Input did not match the gate schema.');
    break;
  case 'delivery_failed':
    console.log('Validation passed but delivery failed.');
    break;
}
```

## Error Handling

```typescript
import { Rynko, RynkoError } from '@rynko/sdk';

try {
  const run = await client.flow.submitRun('gate_abc123', {
    input: { name: 'Test' },
  });
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

- [Flow Documentation](https://docs.rynko.dev/api-reference/flow)
- [API Reference](https://docs.rynko.dev/api-reference)
- [SDK Documentation](https://docs.rynko.dev/sdk/node)
