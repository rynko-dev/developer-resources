# LangGraph + Rynko Flow — Output Validation with Self-Correction

A LangGraph agent that extracts order data from natural language, validates it through a Rynko Flow gate, and self-corrects when validation fails.

## How It Works

```
extract → validate → process
              ↓ (if failed)
          extract (retry with error context)
```

1. **Extract** — LLM extracts structured order data from the user's request
2. **Validate** — Submits the data to a Rynko Flow gate for schema + business rule validation
3. **Process** — Handles the validated order (or routes back for correction)

When validation fails, the structured errors are fed back to the extract node so the LLM can fix its output — no custom retry logic needed.

## Prerequisites

- Python 3.10+
- [Rynko account](https://app.rynko.dev/signup) (free tier works — 500 runs/month)
- OpenAI API key
- A published Flow gate (see below)

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```

## Create the Flow Gate

In the [Flow dashboard](https://app.rynko.dev/flow/gates), create a gate with:

| Field | Type | Constraints |
|-------|------|-------------|
| vendor | string | required, min 1 char |
| amount | number | required, >= 0 |
| currency | string | required, one of: USD, EUR, GBP, INR |
| po_number | string | optional |

Add a business rule: `amount >= 10` with message "Order amount must be at least $10."

Publish the gate and copy the gate ID to your `.env` file.

**Tip:** If you have a Pydantic model, run `YourModel.model_json_schema()` and paste the output into the gate's Import Schema dialog. See the [import tutorial](https://docs.rynko.dev/tutorials/import-pydantic-zod).

## Run

```bash
python src/main.py
```

The script runs two examples:
1. A clean order that passes validation on the first try
2. An ambiguous order ("500 Yen") where the LLM may extract an invalid currency — Flow catches it, and the self-correction loop fixes it

## Example Output

```
Example 1: Clean order (should pass first try)
  [extract] {"vendor": "Globex Corp", "amount": 12500, "currency": "USD", "po_number": "PO-2026-042"}
  [validate] status=validated
  [router] Validation passed, proceeding.
  [process] Order processed successfully.

Example 2: Ambiguous order (may need self-correction)
  [extract] {"vendor": "Acme Inc", "amount": 500, "currency": "JPY"}
  [validate] status=validation_failed
  [validate] errors:
  - currency: must be one of: USD, EUR, GBP, INR
  [router] Retrying (attempt 1/3)...
  [extract] {"vendor": "Acme Inc", "amount": 500, "currency": "USD"}
  [validate] status=validated
  [router] Validation passed, proceeding.
  [process] Order processed successfully.
```

## Blog Post

Full walkthrough: [Adding Output Validation to Your LangGraph Agent with Rynko Flow](https://rynko.hashnode.dev/langgraph-flow-validation)

## Related

- [Rynko Flow documentation](https://docs.rynko.dev/flow)
- [Flow API reference](https://docs.rynko.dev/api-reference/flow)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Self-correction demo (terminal recording)](https://asciinema.org/a/824113)
