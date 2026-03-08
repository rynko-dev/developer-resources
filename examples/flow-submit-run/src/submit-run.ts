import 'dotenv/config';
import { Rynko } from '@rynko/sdk';

async function main() {
  // Initialize the client
  const client = new Rynko({
    apiKey: process.env.RYNKO_API_KEY!,
  });

  // ── Step 1: List published gates ──────────────────────────────
  console.log('Fetching published gates...');
  const { data: gates } = await client.flow.listGates({ status: 'published' });

  if (gates.length === 0) {
    console.error('No published gates found. Create and publish a gate in the Rynko dashboard first.');
    process.exit(1);
  }

  const gate = gates[0];
  console.log(`Using gate: ${gate.name} (${gate.id})`);

  // ── Step 2: Submit a run with sample order data ───────────────
  console.log('\nSubmitting run...');
  const run = await client.flow.submitRun(gate.id, {
    input: {
      orderNumber: 'ORD-2026-0042',
      customerName: 'Acme Corporation',
      customerEmail: 'purchasing@acme.com',
      shippingAddress: {
        line1: '456 Commerce Blvd',
        city: 'Austin',
        state: 'TX',
        postalCode: '73301',
        country: 'US',
      },
      amount: 2475.0,
      currency: 'USD',
      items: [
        { sku: 'WIDGET-A', name: 'Standard Widget', quantity: 5, unitPrice: 195.0 },
        { sku: 'WIDGET-B', name: 'Premium Widget', quantity: 3, unitPrice: 350.0 },
        { sku: 'SHIP-STD', name: 'Standard Shipping', quantity: 1, unitPrice: 25.0 },
      ],
      paymentMethod: 'invoice',
      notes: 'Please deliver before end of month.',
    },
    metadata: {
      source: 'sdk-example',
      environment: 'development',
    },
  });

  console.log(`Run submitted! ID: ${run.id}`);
  console.log(`Initial status: ${run.status}`);

  // ── Step 3: Wait for the run to complete ──────────────────────
  console.log('\nWaiting for validation...');
  const result = await client.flow.waitForRun(run.id, {
    pollInterval: 1000,
    timeout: 120000,
  });

  console.log(`\nRun completed with status: ${result.status}`);

  // ── Step 4: Handle all possible outcomes ──────────────────────
  switch (result.status) {
    case 'approved':
    case 'completed':
    case 'delivered':
      console.log('Run approved successfully!');
      if (result.output) {
        console.log('Output:', JSON.stringify(result.output, null, 2));
      }
      break;

    case 'rejected':
      console.log('Run was rejected.');
      if (result.errors && result.errors.length > 0) {
        console.log('Validation errors:');
        for (const error of result.errors) {
          console.log(`  - ${error.field ? `[${error.field}] ` : ''}${error.message}`);
        }
      }
      break;

    case 'review_required':
      console.log('Run requires human review.');
      console.log('A reviewer will approve or reject this run in the Rynko dashboard.');
      break;

    case 'validation_failed':
      console.log('Validation failed - input did not match the gate schema.');
      if (result.errors && result.errors.length > 0) {
        console.log('Schema errors:');
        for (const error of result.errors) {
          console.log(`  - ${error.field ? `[${error.field}] ` : ''}${error.message}`);
        }
      }
      break;

    case 'render_failed':
      console.log('Validation passed but rendering failed.');
      break;

    case 'delivery_failed':
      console.log('Validation passed but delivery failed.');
      break;

    default:
      console.log(`Unexpected status: ${result.status}`);
  }

  // ── Step 5: List deliveries for the run ───────────────────────
  console.log('\nFetching deliveries...');
  const { data: deliveries } = await client.flow.listDeliveries(result.id);

  if (deliveries.length === 0) {
    console.log('No deliveries for this run.');
  } else {
    console.log(`Found ${deliveries.length} delivery(ies):`);
    for (const delivery of deliveries) {
      console.log(`  - ${delivery.id}: ${delivery.status} (attempts: ${delivery.attempts})`);
      if (delivery.url) {
        console.log(`    URL: ${delivery.url}`);
      }
      if (delivery.error) {
        console.log(`    Error: ${delivery.error}`);
      }
    }
  }
}

main().catch(console.error);
