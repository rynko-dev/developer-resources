import 'dotenv/config';
import { Rynko } from '@rynko/sdk';

async function main() {
  // Initialize the client
  const client = new Rynko({
    apiKey: process.env.RYNKO_API_KEY!,
  });

  // Generate a PDF document
  const result = await client.documents.generate({
    templateId: 'invoice', // Your template ID (UUID, shortId, or slug)
    format: 'pdf',
    variables: {
      invoiceNumber: 'INV-2025-001',
      date: new Date().toISOString().split('T')[0],
      dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      company: {
        name: 'Your Company',
        logoUrl: 'https://example.com/logo.png',
        address: {
          line1: '123 Business St',
          city: 'San Francisco',
          state: 'CA',
          postalCode: '94102',
          country: 'USA',
        },
      },
      customer: {
        name: 'Acme Corporation',
        address: {
          line1: '456 Customer Ave',
          city: 'Los Angeles',
          state: 'CA',
          postalCode: '90001',
        },
      },
      items: [
        { description: 'Professional Services', quantity: 10, rate: 150, amount: 1500 },
        { description: 'Software License', quantity: 1, rate: 500, amount: 500 },
      ],
      subtotal: 2000,
      taxRate: 8,
      tax: 160,
      total: 2160,
      paymentTerms: 'Net 30',
    },
  });

  console.log('Document generated successfully!');
  console.log('Download URL:', result.downloadUrl);
  console.log('Job ID:', result.jobId);
}

main().catch(console.error);
