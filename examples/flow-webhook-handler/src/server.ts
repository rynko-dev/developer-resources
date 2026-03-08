import 'dotenv/config';
import express from 'express';
import { Rynko, verifyWebhookSignature, WebhookSignatureError } from '@rynko/sdk';

const app = express();
const port = process.env.PORT || 3000;

// Initialize the Rynko client (used for retrying failed deliveries)
const client = new Rynko({
  apiKey: process.env.RYNKO_API_KEY!,
});

// Use raw body for webhook signature verification
app.use('/webhooks', express.raw({ type: 'application/json' }));
app.use(express.json());

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// Flow webhook endpoint
app.post('/webhooks/flow', async (req, res) => {
  const signature = req.headers['x-rynko-signature'] as string;
  const payload = req.body.toString(); // Convert Buffer to string

  // Verify the webhook signature
  try {
    const event = verifyWebhookSignature({
      payload,
      signature,
      secret: process.env.WEBHOOK_SECRET!,
    });

    console.log(`Received event: ${event.type}`);
    console.log(`Event ID: ${event.id}`);
    console.log(`Timestamp: ${event.timestamp}`);

    // Handle different Flow event types
    switch (event.type) {
      case 'flow.run.completed': {
        const data = event.data as {
          runId: string;
          gateId: string;
          gateName: string;
          status: string;
          input: Record<string, unknown>;
          output?: Record<string, unknown>;
          metadata?: Record<string, unknown>;
        };
        console.log(`Run completed: ${data.runId}`);
        console.log(`Gate: ${data.gateName} (${data.gateId})`);
        console.log(`Final status: ${data.status}`);
        if (data.output) {
          console.log('Output:', JSON.stringify(data.output, null, 2));
        }
        // Example: Update your database with the run result
        // await db.orders.update({ runId: data.runId }, { validationStatus: data.status });
        break;
      }

      case 'flow.run.approved': {
        const data = event.data as {
          runId: string;
          gateId: string;
          gateName: string;
          status: string;
          input: Record<string, unknown>;
          output?: Record<string, unknown>;
          metadata?: Record<string, unknown>;
        };
        console.log(`Run approved: ${data.runId}`);
        console.log(`Gate: ${data.gateName}`);
        if (data.metadata) {
          console.log('Metadata:', JSON.stringify(data.metadata, null, 2));
        }
        // Example: Trigger downstream processing
        // await processApprovedOrder(data.input, data.output);

        // Example: Send confirmation notification
        // await sendEmail(data.input.customerEmail, 'Order approved', { orderId: data.metadata?.orderId });
        break;
      }

      case 'flow.run.rejected': {
        const data = event.data as {
          runId: string;
          gateId: string;
          gateName: string;
          status: string;
          errors?: Array<{ field?: string; rule?: string; message: string }>;
          metadata?: Record<string, unknown>;
        };
        console.error(`Run rejected: ${data.runId}`);
        console.error(`Gate: ${data.gateName}`);
        if (data.errors && data.errors.length > 0) {
          console.error('Validation errors:');
          for (const error of data.errors) {
            console.error(`  - ${error.field ? `[${error.field}] ` : ''}${error.message}`);
          }
        }
        // Example: Alert your team about the rejection
        // await slack.send('#alerts', `Flow run rejected: ${data.runId} - ${data.errors?.[0]?.message}`);

        // Example: Update order status in your system
        // await db.orders.update({ runId: data.runId }, { status: 'validation_failed' });
        break;
      }

      case 'flow.run.review_required': {
        const data = event.data as {
          runId: string;
          gateId: string;
          gateName: string;
          metadata?: Record<string, unknown>;
        };
        console.log(`Review required for run: ${data.runId}`);
        console.log(`Gate: ${data.gateName}`);
        // Example: Notify reviewers
        // await slack.send('#reviews', `Flow run ${data.runId} needs review for gate "${data.gateName}"`);

        // Example: Create a task in your project management tool
        // await createReviewTask({ runId: data.runId, gate: data.gateName });
        break;
      }

      case 'flow.delivery.failed': {
        const data = event.data as {
          deliveryId: string;
          runId: string;
          error: string;
          attempts: number;
        };
        console.error(`Delivery failed: ${data.deliveryId}`);
        console.error(`Run: ${data.runId}`);
        console.error(`Error: ${data.error}`);
        console.error(`Attempts: ${data.attempts}`);

        // Example: Retry the failed delivery using the SDK
        if (data.attempts < 3) {
          console.log('Retrying delivery...');
          try {
            const retried = await client.flow.retryDelivery(data.deliveryId);
            console.log(`Retry status: ${retried.status}`);
          } catch (retryError) {
            console.error('Retry failed:', retryError);
          }
        } else {
          console.error('Max retry attempts reached. Manual intervention required.');
          // await slack.send('#alerts', `Flow delivery ${data.deliveryId} permanently failed after ${data.attempts} attempts`);
        }
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    // Always respond with 200 to acknowledge receipt
    res.status(200).json({ received: true });
  } catch (error) {
    if (error instanceof WebhookSignatureError) {
      console.error('Invalid webhook signature:', error.message);
      res.status(401).json({ error: 'Invalid signature' });
    } else {
      console.error('Webhook processing error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});

app.listen(port, () => {
  console.log(`Flow webhook server listening on port ${port}`);
  console.log(`Webhook endpoint: http://localhost:${port}/webhooks/flow`);
  console.log(`Health check:     http://localhost:${port}/health`);
});
