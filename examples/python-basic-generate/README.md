# Basic Document Generation (Python)

This example shows how to generate PDF and Excel documents using the Rynko Python SDK.

## Prerequisites

- Python 3.8+
- Rynko API key ([get one here](https://rynko.dev/dashboard/api-keys))
- A template created in Rynko

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API key:
   ```bash
   RYNKO_API_KEY=your-api-key-here
   ```

## Usage

```bash
python src/generate.py
```

## Code Examples

Document generation in Rynko is **asynchronous**. The `generate()` method queues the job and returns immediately with a job ID. Use `wait_for_completion()` to poll until the document is ready.

### Synchronous Client

```python
from rynko import Rynko

client = Rynko(api_key="your-api-key")

# Queue the document generation
job = client.documents.generate(
    template_id="tmpl_invoice",
    format="pdf",
    variables={
        "invoiceNumber": "INV-001",
        "customerName": "Acme Corp",
        "total": 1500,
    },
)

print(f"Job ID: {job['jobId']}")
print(f"Status: {job['status']}")  # 'queued'

# Wait for completion to get the download URL
completed = client.documents.wait_for_completion(job["jobId"])
print(f"Download URL: {completed['downloadUrl']}")
```

### Async Client

```python
from rynko import AsyncRynko

async def generate_document():
    async with AsyncRynko(api_key="your-api-key") as client:
        # Queue the document generation
        job = await client.documents.generate(
            template_id="tmpl_invoice",
            format="pdf",
            variables={
                "invoiceNumber": "INV-001",
                "customerName": "Acme Corp",
            },
        )

        # Wait for completion
        completed = await client.documents.wait_for_completion(job["jobId"])
        return completed
```

### Error Handling

```python
from rynko import Rynko, RynkoError

try:
    job = client.documents.generate(...)
    completed = client.documents.wait_for_completion(job["jobId"])
except RynkoError as e:
    print(f"API Error: {e.message}")
    print(f"Error Code: {e.code}")
    print(f"Status: {e.status}")
```

## Related Resources

- [API Reference](https://docs.rynko.dev/api-reference)
- [SDK Documentation](https://docs.rynko.dev/sdk/python)
