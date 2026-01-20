#!/usr/bin/env python3
"""Basic document generation example with Renderbase Python SDK."""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from renderbase import Renderbase

load_dotenv()


def main():
    # Initialize the client
    client = Renderbase(api_key=os.environ["RENDERBASE_API_KEY"])

    # Generate a PDF document
    result = client.documents.generate(
        template_id="invoice",  # Your template ID (UUID, shortId, or slug)
        format="pdf",
        variables={
            "invoiceNumber": "INV-2025-001",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "dueDate": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "company": {
                "name": "Your Company",
                "logoUrl": "https://example.com/logo.png",
                "address": {
                    "line1": "123 Business St",
                    "city": "San Francisco",
                    "state": "CA",
                    "postalCode": "94102",
                    "country": "USA",
                },
            },
            "customer": {
                "name": "Acme Corporation",
                "address": {
                    "line1": "456 Customer Ave",
                    "city": "Los Angeles",
                    "state": "CA",
                    "postalCode": "90001",
                },
            },
            "items": [
                {"description": "Professional Services", "quantity": 10, "rate": 150, "amount": 1500},
                {"description": "Software License", "quantity": 1, "rate": 500, "amount": 500},
            ],
            "subtotal": 2000,
            "taxRate": 8,
            "tax": 160,
            "total": 2160,
            "paymentTerms": "Net 30",
        },
    )

    print("Document generated successfully!")
    print(f"Download URL: {result['downloadUrl']}")
    print(f"Job ID: {result['jobId']}")


if __name__ == "__main__":
    main()
