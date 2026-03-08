# Automated Approval Bot (Node.js)

This example demonstrates how to build an automated approval bot that polls for pending Flow approvals and applies business rules to auto-approve or auto-reject them.

## What It Does

1. Fetches all pending Flow approvals
2. For each approval, retrieves the associated run and its input data
3. Applies configurable business rules:
   - Auto-approves if the order amount is under $1,000
   - Auto-rejects if required fields (customer name, email) are missing
   - Skips approvals that need manual review (amount >= $1,000 with all fields present)
4. Prints a summary of actions taken

## Prerequisites

- Node.js 18+
- Rynko API key ([get one here](https://rynko.dev/dashboard/api-keys))
- A published Flow gate with approval rules configured

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

## Customizing Business Rules

Edit the `evaluateApproval()` function in `src/approval-bot.ts` to implement your own approval logic. The function receives the run's input data and returns an approval decision.

```typescript
function evaluateApproval(input: Record<string, unknown>): ApprovalDecision {
  // Add your own rules here
  const amount = input.amount as number;

  if (amount > 10000) {
    return { action: 'reject', reason: 'Amount exceeds auto-approval limit' };
  }

  return { action: 'approve', note: 'Within auto-approval threshold' };
}
```

## Related Resources

- [Flow Documentation](https://docs.rynko.dev/api-reference/flow)
- [API Reference](https://docs.rynko.dev/api-reference)
- [SDK Documentation](https://docs.rynko.dev/sdk/node)
