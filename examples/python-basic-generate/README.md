# Basic Document Generation (Python)

This example shows how to generate PDF and Excel documents using the Renderbase Python SDK.

## Prerequisites

- Python 3.8+
- Renderbase API key ([get one here](https://renderbase.dev/dashboard/api-keys))
- A template created in Renderbase

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
   RENDERBASE_API_KEY=your-api-key-here
   ```

## Usage

```bash
python src/generate.py
```

## Code Examples

### Synchronous Client

```python
from renderbase import Renderbase

client = Renderbase(api_key="your-api-key")

result = client.documents.generate(
    template_id="tmpl_invoice",
    format="pdf",
    variables={
        "invoiceNumber": "INV-001",
        "customerName": "Acme Corp",
        "total": 1500,
    },
)

print(f"Download URL: {result['downloadUrl']}")
```

### Async Client

```python
from renderbase import AsyncRenderbase

async def generate_document():
    async with AsyncRenderbase(api_key="your-api-key") as client:
        result = await client.documents.generate(
            template_id="tmpl_invoice",
            format="pdf",
            variables={
                "invoiceNumber": "INV-001",
                "customerName": "Acme Corp",
            },
        )
        return result
```

### Error Handling

```python
from renderbase import Renderbase, RenderbaseError

try:
    result = client.documents.generate(...)
except RenderbaseError as e:
    print(f"API Error: {e.message}")
    print(f"Error Code: {e.code}")
    print(f"Status: {e.status}")
```

## Related Resources

- [API Reference](https://docs.renderbase.dev/api-reference)
- [SDK Documentation](https://docs.renderbase.dev/sdk/python)
