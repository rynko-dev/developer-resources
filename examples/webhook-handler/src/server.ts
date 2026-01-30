import 'dotenv/config';
import express from 'express';
import { verifyWebhookSignature, WebhookSignatureError } from '@rynko/sdk';

const app = express();
const port = process.env.PORT || 3000;

// Use raw body for webhook signature verification
app.use('/webhooks', express.raw({ type: 'application/json' }));
app.use(express.json());

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// Rynko webhook endpoint
app.post('/webhooks/rynko', async (req, res) => {
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

    // Handle different event types
    switch (event.type) {
      case 'document.generated':
        const generatedData = event.data as {
          jobId: string;
          downloadUrl: string;
          templateId: string;
          format: string;
          metadata?: Record<string, unknown>;
        };
        console.log(`Document ready: ${generatedData.downloadUrl}`);
        console.log(`Job ID: ${generatedData.jobId}`);
        // Download the document, send notification, update database, etc.
        await handleDocumentGenerated(generatedData);
        break;

      case 'document.failed':
        const failedData = event.data as {
          jobId: string;
          error: string;
          templateId: string;
        };
        console.error(`Document generation failed for job: ${failedData.jobId}`);
        console.error(`Error: ${failedData.error}`);
        // Handle the failure - retry, notify user, etc.
        await handleDocumentFailed(failedData);
        break;

      case 'document.downloaded':
        const downloadedData = event.data as { jobId: string };
        console.log(`Document downloaded: ${downloadedData.jobId}`);
        // Track download analytics
        break;

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

// Example handler for generated documents
async function handleDocumentGenerated(data: {
  jobId: string;
  downloadUrl: string;
  templateId: string;
  format: string;
  metadata?: Record<string, unknown>;
}) {
  console.log('Processing generated document...');
  console.log(`Job ID: ${data.jobId}`);
  console.log(`Template: ${data.templateId}`);
  console.log(`Format: ${data.format}`);

  if (data.metadata) {
    console.log('Metadata:', JSON.stringify(data.metadata, null, 2));
  }

  // Example: Download and store the document
  // const response = await fetch(data.downloadUrl);
  // const buffer = await response.arrayBuffer();
  // await fs.writeFile(`./documents/${data.jobId}.${data.format}`, Buffer.from(buffer));

  // Example: Update database
  // await db.documents.update({ jobId: data.jobId }, { status: 'completed', url: data.downloadUrl });

  // Example: Send notification
  // await sendEmail(user.email, 'Your document is ready', { downloadUrl: data.downloadUrl });
}

// Example handler for failed documents
async function handleDocumentFailed(data: { jobId: string; error: string; templateId: string }) {
  console.error('Document generation failed');
  console.error(`Job ID: ${data.jobId}`);
  console.error(`Error: ${data.error}`);

  // Example: Update database
  // await db.documents.update({ jobId: data.jobId }, { status: 'failed', error: data.error });

  // Example: Retry logic
  // if (shouldRetry(data.jobId)) {
  //   await rynko.documents.retry(data.jobId);
  // }

  // Example: Alert team
  // await slack.send('#alerts', `Document generation failed: ${data.error}`);
}

app.listen(port, () => {
  console.log(`Webhook server listening on port ${port}`);
  console.log(`Webhook endpoint: http://localhost:${port}/webhooks/rynko`);
});
