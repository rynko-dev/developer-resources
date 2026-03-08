# Submit and Monitor Flow Runs (Python)

This example shows how to submit a run to a Rynko Flow gate, wait for validation to complete, and handle the result using the Python SDK.

## Prerequisites

- Python 3.8+
- Rynko API key ([get one here](https://rynko.dev/dashboard/api-keys))
- A published Flow gate in your Rynko workspace

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
python src/submit_run.py
```

## Code Examples

### Submit a Run

Runs are validated asynchronously. The `submit_run()` method queues the run and returns immediately. Use `wait_for_run()` to poll until validation completes.

```python
from rynko import Rynko

client = Rynko(api_key="your-api-key")

# Submit a run to a gate
run = client.flow.submit_run(
    "gate_abc123",
    input={
        "customerName": "Acme Corporation",
        "email": "orders@acme.com",
        "amount": 2500.00,
        "items": [
            {"sku": "WIDGET-001", "quantity": 10, "unitPrice": 250.00},
        ],
    },
    metadata={"source": "api-example"},
)

print(f"Run ID: {run['id']}")

# Wait for validation to complete
result = client.flow.wait_for_run(run["id"])

if result["status"] == "approved":
    print("Approved!", result.get("output"))
elif result["status"] == "rejected":
    print("Rejected:", result.get("errors"))
```

### Async Client

```python
from rynko import AsyncRynko

async def submit_flow_run():
    async with AsyncRynko(api_key="your-api-key") as client:
        run = await client.flow.submit_run(
            "gate_abc123",
            input={"customerName": "Acme Corp", "amount": 500},
        )
        result = await client.flow.wait_for_run(run["id"])
        return result
```

### Error Handling

```python
from rynko import Rynko, RynkoError

try:
    run = client.flow.submit_run("gate_abc123", input={"name": "Test"})
    result = client.flow.wait_for_run(run["id"])
except RynkoError as e:
    print(f"API Error: {e.message}")
    print(f"Error Code: {e.code}")
    print(f"Status: {e.status}")
except TimeoutError:
    print("Run did not complete within the timeout period")
```

## Related Resources

- [Flow Documentation](https://docs.rynko.dev/api-reference/flow)
- [SDK Documentation](https://docs.rynko.dev/sdk/python)
