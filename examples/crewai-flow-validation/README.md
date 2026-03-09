# CrewAI + Rynko Flow — Output Validation with Self-Correction

A CrewAI crew with two agents: one extracts order data from natural language, another validates it through a Rynko Flow gate and self-corrects on failure.

## How It Works

1. **Order Processor** agent extracts structured data from the user's request
2. **Order Validator** agent submits the data to a Flow gate using a custom tool
3. If validation fails, the validator reads the structured errors, fixes the JSON, and resubmits
4. This happens automatically — no retry logic coded, just clear error messages

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

## Run

```bash
python src/main.py
```

The script runs two examples:
1. A clean order ("$12,500 USD from Globex Corp") — passes first try
2. Bad data ("vendor empty, amount negative, currency Yen") — validator self-corrects

## Example Output

```
[Order Processor] Extracting order data...
> {"vendor": "Globex Corp", "amount": 12500, "currency": "USD", "po_number": "PO-2026-042"}

[Order Validator] Validating order...
> Using tool: validate_order
> {"success": true, "status": "validated", "run_id": "..."}

Result: Order validated successfully. Run ID: 550e8400-...
```

With bad data:

```
[Order Processor] Extracting...
> {"vendor": "", "amount": -500, "currency": "JPY"}

[Order Validator] Validating...
> Using tool: validate_order
> {"success": false, "errors": ["- vendor: required", "- amount: must be >= 0", "- currency: must be one of USD, EUR, GBP, INR"]}

[Order Validator] Fixing errors and resubmitting...
> Using tool: validate_order
> {"success": true, "status": "validated", "run_id": "..."}
```

## Multiple Crews, Same Gate

Different CrewAI crews can validate against the same gate:

```python
domestic_crew = Crew(agents=[domestic_processor, validator], ...)
intl_crew = Crew(agents=[intl_processor, validator], ...)
```

Change a business rule once in the Flow dashboard — every crew picks it up.

## Blog Post

Full walkthrough: [Validating CrewAI Agent Outputs with Rynko Flow](https://rynko.hashnode.dev/crewai-flow-validation)

## Related

- [Rynko Flow documentation](https://docs.rynko.dev/flow)
- [CrewAI documentation](https://docs.crewai.com/)
- [LangGraph + Flow example](../langgraph-flow-validation/)
- [Self-correction demo (terminal recording)](https://asciinema.org/a/824113)
