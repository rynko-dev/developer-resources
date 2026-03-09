"""
CrewAI + Rynko Flow — Output Validation with Self-Correction
=============================================================

A CrewAI crew with two agents: one extracts order data, and another
validates it through a Rynko Flow gate. If validation fails, the
validator reads the structured errors and resubmits with fixes.

Usage:
  1. Create a Flow gate in the Rynko dashboard (see README.md)
  2. Copy .env.example to .env and fill in your keys
  3. pip install -r requirements.txt
  4. python src/main.py

Env vars:
  OPENAI_API_KEY    Required. OpenAI API key.
  RYNKO_API_KEY     Required. Rynko API key (workspace-scoped).
  FLOW_GATE_ID      Required. The ID of your published Flow gate.
"""

import os
import json
import httpx
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────

RYNKO_BASE_URL = os.environ.get("RYNKO_BASE_URL", "https://api.rynko.dev/api")
RYNKO_API_KEY = os.environ["RYNKO_API_KEY"]
GATE_ID = os.environ["FLOW_GATE_ID"]


# ── Flow Validation Tool ─────────────────────────────────────────────────────

@tool("validate_order")
def validate_order(order_json: str) -> str:
    """Validate an order payload against the Rynko Flow gate.
    Input must be a JSON string with fields: vendor (string),
    amount (number), currency (USD/EUR/GBP/INR), po_number (optional string).
    Returns validation result with status and any errors."""

    try:
        payload = json.loads(order_json)
    except json.JSONDecodeError as e:
        return json.dumps({"success": False, "error": f"Invalid JSON: {e}"})

    response = httpx.post(
        f"{RYNKO_BASE_URL}/flow/gates/{GATE_ID}/runs",
        json={"input": payload},
        headers={
            "Authorization": f"Bearer {RYNKO_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    result = response.json()

    if result.get("status") == "validation_failed":
        errors = result.get("errors", [])
        error_lines = [f"- {e.get('field')}: {e.get('message')}" for e in errors]
        return json.dumps({
            "success": False,
            "status": "validation_failed",
            "errors": error_lines,
            "message": "Fix these errors and call validate_order again with corrected JSON.",
        }, indent=2)

    return json.dumps({
        "success": True,
        "status": result.get("status"),
        "run_id": result.get("runId"),
        "validation_id": result.get("validation_id"),
        "message": "Order validated successfully.",
    }, indent=2)


# ── Flow Approval Polling Tool ────────────────────────────────────────────────

@tool("check_run_status")
def check_run_status(run_id: str) -> str:
    """Check the current status of a Flow run by its ID.
    Use this to poll runs that require human approval."""

    response = httpx.get(
        f"{RYNKO_BASE_URL}/flow/runs/{run_id}",
        headers={"Authorization": f"Bearer {RYNKO_API_KEY}"},
        timeout=30,
    )

    result = response.json()
    return json.dumps({
        "run_id": run_id,
        "status": result.get("status"),
        "validation_id": result.get("validation_id"),
    }, indent=2)


# ── Agents ────────────────────────────────────────────────────────────────────

order_processor = Agent(
    role="Order Processor",
    goal="Extract structured order data from customer requests accurately",
    backstory=(
        "You are an order processing specialist. You extract vendor name, "
        "amount, currency, and PO number from natural language requests. "
        "You output clean JSON with fields: vendor, amount, currency, po_number. "
        "Currency must be a 3-letter ISO code (USD, EUR, GBP, or INR). "
        "Amount must be a positive number. Vendor must not be empty."
    ),
    verbose=True,
    allow_delegation=False,
)

order_validator = Agent(
    role="Order Validator",
    goal="Validate extracted orders against business rules and fix any issues",
    backstory=(
        "You validate order data by submitting it to the validation gateway "
        "using the validate_order tool. The tool accepts a JSON string.\n\n"
        "If validation fails, you MUST:\n"
        "1. Read each error message carefully\n"
        "2. Fix every issue in the JSON\n"
        "3. Call validate_order again with the corrected JSON\n"
        "4. Repeat until validation passes or you've tried 3 times\n\n"
        "Always report the final validation status and run ID."
    ),
    tools=[validate_order, check_run_status],
    verbose=True,
    allow_delegation=False,
)


# ── Tasks ─────────────────────────────────────────────────────────────────────

def create_tasks(user_request: str):
    extract_task = Task(
        description=(
            f"Extract order data from this customer request:\n\n"
            f"{user_request}\n\n"
            f"Output a JSON object with fields: vendor (string), amount (number), "
            f"currency (3-letter code: USD, EUR, GBP, or INR), po_number (string, optional). "
            f"Output ONLY the JSON object, nothing else."
        ),
        expected_output="A JSON object with vendor, amount, currency, and optional po_number",
        agent=order_processor,
    )

    validate_task = Task(
        description=(
            "Take the order JSON from the previous task and validate it using the "
            "validate_order tool. Pass the JSON as a string to the tool.\n\n"
            "If validation fails:\n"
            "1. Read the error messages in the response\n"
            "2. Fix each issue in the JSON\n"
            "3. Call validate_order again with the corrected JSON string\n"
            "4. Repeat until it passes or you've tried 3 times\n\n"
            "Report the final run ID and validation status."
        ),
        expected_output="Validation result with run ID and status (validated or failed)",
        agent=order_validator,
        context=[extract_task],
    )

    return [extract_task, validate_task]


# ── Main ──────────────────────────────────────────────────────────────────────

def run_example(title: str, user_request: str):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")

    tasks = create_tasks(user_request)

    crew = Crew(
        agents=[order_processor, order_validator],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print(f"\n{'─' * 60}")
    print(f"  Result: {result}")
    print(f"{'─' * 60}\n")
    return result


def main():
    print("\n" + "=" * 60)
    print("  CrewAI + Rynko Flow — Validation Demo")
    print("=" * 60)

    # Example 1: Clean order — should pass on first try
    run_example(
        "Example 1: Clean order (should pass first try)",
        "Process an order from Globex Corp for $12,500 USD, PO number PO-2026-042",
    )

    # Example 2: Ambiguous/bad data — self-correction needed
    run_example(
        "Example 2: Bad data (needs self-correction)",
        "Submit an order: vendor is empty, amount is negative five hundred, currency is Yen",
    )


if __name__ == "__main__":
    main()
