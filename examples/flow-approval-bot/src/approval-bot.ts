import 'dotenv/config';
import { Rynko } from '@rynko/sdk';

interface ApprovalDecision {
  action: 'approve' | 'reject' | 'skip';
  note?: string;
  reason?: string;
}

/**
 * Evaluate a run's input data and decide whether to approve, reject, or skip.
 *
 * Customize this function with your own business rules.
 */
function evaluateApproval(input: Record<string, unknown>): ApprovalDecision {
  const customerName = input.customerName as string | undefined;
  const customerEmail = input.customerEmail as string | undefined;
  const amount = input.amount as number | undefined;
  const items = input.items as unknown[] | undefined;

  // Rule 1: Reject if required fields are missing
  if (!customerName || !customerEmail) {
    return {
      action: 'reject',
      reason: `Missing required fields: ${[
        !customerName && 'customerName',
        !customerEmail && 'customerEmail',
      ]
        .filter(Boolean)
        .join(', ')}`,
    };
  }

  // Rule 2: Reject if no items
  if (!items || items.length === 0) {
    return {
      action: 'reject',
      reason: 'Order has no items',
    };
  }

  // Rule 3: Auto-approve small orders (under $1,000)
  if (typeof amount === 'number' && amount < 1000) {
    return {
      action: 'approve',
      note: `Auto-approved: amount $${amount.toFixed(2)} is under $1,000 threshold`,
    };
  }

  // Rule 4: Skip large orders for manual review
  return {
    action: 'skip',
    note: `Amount $${amount?.toFixed(2) ?? 'unknown'} requires manual review`,
  };
}

async function main() {
  // Initialize the client
  const client = new Rynko({
    apiKey: process.env.RYNKO_API_KEY!,
  });

  // ── Fetch pending approvals ───────────────────────────────────
  console.log('Fetching pending approvals...\n');
  const { data: approvals, meta } = await client.flow.listApprovals({
    status: 'pending',
  });

  if (approvals.length === 0) {
    console.log('No pending approvals found.');
    return;
  }

  console.log(`Found ${meta.total} pending approval(s). Processing...\n`);

  // ── Process each approval ─────────────────────────────────────
  let approved = 0;
  let rejected = 0;
  let skipped = 0;

  for (const approval of approvals) {
    console.log(`--- Approval ${approval.id} ---`);
    console.log(`  Run ID: ${approval.runId}`);
    console.log(`  Gate ID: ${approval.gateId}`);

    // Fetch the associated run to inspect its input data
    const run = await client.flow.getRun(approval.runId);
    console.log(`  Run status: ${run.status}`);

    // Apply business rules
    const decision = evaluateApproval(run.input);

    switch (decision.action) {
      case 'approve':
        console.log(`  Decision: APPROVE`);
        console.log(`  Note: ${decision.note}`);
        await client.flow.approve(approval.id, {
          note: decision.note,
        });
        approved++;
        break;

      case 'reject':
        console.log(`  Decision: REJECT`);
        console.log(`  Reason: ${decision.reason}`);
        await client.flow.reject(approval.id, {
          reason: decision.reason,
        });
        rejected++;
        break;

      case 'skip':
        console.log(`  Decision: SKIP (manual review needed)`);
        console.log(`  Note: ${decision.note}`);
        skipped++;
        break;
    }

    console.log('');
  }

  // ── Print summary ─────────────────────────────────────────────
  console.log('=== Summary ===');
  console.log(`  Approved: ${approved}`);
  console.log(`  Rejected: ${rejected}`);
  console.log(`  Skipped:  ${skipped}`);
  console.log(`  Total:    ${approvals.length}`);
}

main().catch(console.error);
