#!/usr/bin/env python3
"""Submit and monitor a Flow run using the Rynko Python SDK."""

import os
import sys
from dotenv import load_dotenv
from rynko import Rynko

load_dotenv()


def main():
    # Initialize the client
    client = Rynko(api_key=os.environ["RYNKO_API_KEY"])

    # ── Step 1: List published gates ─────────────────────────────
    print("Fetching published gates...")
    result = client.flow.list_gates(status="published")
    gates = result["data"]

    if not gates:
        print("No published gates found. Create and publish a gate in the Rynko dashboard first.")
        sys.exit(1)

    gate = gates[0]
    print(f"Using gate: {gate['name']} ({gate['id']})")

    # ── Step 2: Submit a run with sample order data ──────────────
    print("\nSubmitting run...")
    run = client.flow.submit_run(
        gate["id"],
        input={
            "orderNumber": "ORD-2026-0042",
            "customerName": "Acme Corporation",
            "customerEmail": "purchasing@acme.com",
            "shippingAddress": {
                "line1": "456 Commerce Blvd",
                "city": "Austin",
                "state": "TX",
                "postalCode": "73301",
                "country": "US",
            },
            "amount": 2475.00,
            "currency": "USD",
            "items": [
                {"sku": "WIDGET-A", "name": "Standard Widget", "quantity": 5, "unitPrice": 195.00},
                {"sku": "WIDGET-B", "name": "Premium Widget", "quantity": 3, "unitPrice": 350.00},
                {"sku": "SHIP-STD", "name": "Standard Shipping", "quantity": 1, "unitPrice": 25.00},
            ],
            "paymentMethod": "invoice",
            "notes": "Please deliver before end of month.",
        },
        metadata={
            "source": "sdk-example",
            "environment": "development",
        },
    )

    print(f"Run submitted! ID: {run['id']}")
    print(f"Initial status: {run['status']}")

    # ── Step 3: Wait for the run to complete ─────────────────────
    print("\nWaiting for validation...")
    result = client.flow.wait_for_run(
        run["id"],
        poll_interval=1.0,
        timeout=120.0,
    )

    status = result["status"]
    print(f"\nRun completed with status: {status}")

    # ── Step 4: Handle all possible outcomes ─────────────────────
    if status in ("approved", "completed", "delivered"):
        print("Run approved successfully!")
        output = result.get("output")
        if output:
            import json
            print(f"Output: {json.dumps(output, indent=2)}")

    elif status == "rejected":
        print("Run was rejected.")
        errors = result.get("errors", [])
        if errors:
            print("Validation errors:")
            for error in errors:
                field = error.get("field", "")
                prefix = f"[{field}] " if field else ""
                print(f"  - {prefix}{error['message']}")

    elif status == "review_required":
        print("Run requires human review.")
        print("A reviewer will approve or reject this run in the Rynko dashboard.")

    elif status == "validation_failed":
        print("Validation failed - input did not match the gate schema.")
        errors = result.get("errors", [])
        if errors:
            print("Schema errors:")
            for error in errors:
                field = error.get("field", "")
                prefix = f"[{field}] " if field else ""
                print(f"  - {prefix}{error['message']}")

    elif status == "render_failed":
        print("Validation passed but rendering failed.")

    elif status == "delivery_failed":
        print("Validation passed but delivery failed.")

    else:
        print(f"Unexpected status: {status}")

    # ── Step 5: List deliveries for the run ──────────────────────
    print("\nFetching deliveries...")
    deliveries_result = client.flow.list_deliveries(result["id"])
    deliveries = deliveries_result["data"]

    if not deliveries:
        print("No deliveries for this run.")
    else:
        print(f"Found {len(deliveries)} delivery(ies):")
        for delivery in deliveries:
            print(f"  - {delivery['id']}: {delivery['status']} (attempts: {delivery['attempts']})")
            if delivery.get("url"):
                print(f"    URL: {delivery['url']}")
            if delivery.get("error"):
                print(f"    Error: {delivery['error']}")


if __name__ == "__main__":
    main()
