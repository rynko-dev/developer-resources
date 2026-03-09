"""
LangGraph + Rynko Flow — Output Validation with Self-Correction
================================================================

A LangGraph agent that extracts order data from natural language,
validates it through a Rynko Flow gate, and self-corrects on failure.

Graph:
  extract → validate → process
                ↓ (if failed)
            extract (retry with error context)

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
from typing import TypedDict, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────

RYNKO_BASE_URL = os.environ.get("RYNKO_BASE_URL", "https://api.rynko.dev/api")
RYNKO_API_KEY = os.environ["RYNKO_API_KEY"]
GATE_ID = os.environ["FLOW_GATE_ID"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ── Flow API Client ───────────────────────────────────────────────────────────

def validate_with_flow(gate_id: str, payload: dict) -> dict:
    """Submit a payload to a Flow gate and return the validation result."""
    response = httpx.post(
        f"{RYNKO_BASE_URL}/flow/gates/{gate_id}/runs",
        json={"input": payload},
        headers={
            "Authorization": f"Bearer {RYNKO_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    return response.json()


# ── Graph State ───────────────────────────────────────────────────────────────

class OrderState(TypedDict):
    user_request: str
    extracted_data: Optional[dict]
    validation_result: Optional[dict]
    validation_errors: Optional[str]
    retry_count: int
    final_result: Optional[str]


# ── Nodes ─────────────────────────────────────────────────────────────────────

def extract_order(state: OrderState) -> dict:
    """LLM extracts structured order data from the user request.
    If previous validation errors exist, they're included so the LLM can correct."""

    error_context = ""
    if state.get("validation_errors"):
        error_context = (
            f"\n\nYour previous extraction had validation errors:\n"
            f"{state['validation_errors']}\n"
            f"Fix these issues in your new extraction."
        )

    response = llm.invoke(
        f"Extract order data from this request as JSON with fields: "
        f"vendor (string), amount (number), currency (string, one of USD/EUR/GBP/INR), "
        f"po_number (string, optional).\n\n"
        f"Request: {state['user_request']}"
        f"{error_context}\n\n"
        f"Respond with ONLY valid JSON, no markdown fences."
    )

    try:
        extracted = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from markdown fences
        content = response.content
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            try:
                extracted = json.loads(content.strip())
            except json.JSONDecodeError:
                extracted = {"vendor": "", "amount": 0, "currency": ""}
        else:
            extracted = {"vendor": "", "amount": 0, "currency": ""}

    print(f"  [extract] {json.dumps(extracted)}")
    return {"extracted_data": extracted}


def validate_order(state: OrderState) -> dict:
    """Submit extracted data to the Flow gate for validation."""

    result = validate_with_flow(GATE_ID, state["extracted_data"])
    status = result.get("status", "unknown")
    print(f"  [validate] status={status}")

    if status == "validation_failed":
        errors = result.get("errors", [])
        error_text = "\n".join(
            f"- {e.get('field', 'unknown')}: {e.get('message', 'invalid')}"
            for e in errors
        )
        print(f"  [validate] errors:\n{error_text}")
        return {
            "validation_result": result,
            "validation_errors": error_text,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    return {
        "validation_result": result,
        "validation_errors": None,
    }


def process_order(state: OrderState) -> dict:
    """Handle the validated order. In production this would write to your DB,
    trigger fulfillment, etc."""

    validation_id = state["validation_result"].get("validation_id", "N/A")
    data = state["extracted_data"]
    result_text = (
        f"Order processed successfully.\n"
        f"  Vendor: {data.get('vendor')}\n"
        f"  Amount: {data.get('amount')} {data.get('currency')}\n"
        f"  PO: {data.get('po_number', 'N/A')}\n"
        f"  Validation ID: {validation_id}"
    )
    print(f"  [process] {result_text}")
    return {"final_result": result_text}


# ── Conditional Routing ───────────────────────────────────────────────────────

def should_retry(state: OrderState) -> str:
    """Route based on validation result: retry, proceed, or give up."""
    if state.get("validation_errors") and state.get("retry_count", 0) < 3:
        print(f"  [router] Retrying (attempt {state['retry_count']}/3)...")
        return "retry"
    elif state.get("validation_errors"):
        print(f"  [router] Max retries reached, giving up.")
        return "give_up"
    print(f"  [router] Validation passed, proceeding.")
    return "proceed"


# ── Build Graph ───────────────────────────────────────────────────────────────

def build_graph():
    graph = StateGraph(OrderState)

    graph.add_node("extract", extract_order)
    graph.add_node("validate", validate_order)
    graph.add_node("process", process_order)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "validate")

    graph.add_conditional_edges(
        "validate",
        should_retry,
        {
            "retry": "extract",
            "proceed": "process",
            "give_up": END,
        },
    )
    graph.add_edge("process", END)

    return graph.compile()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    app = build_graph()

    # Print graph structure
    print("Graph structure:")
    try:
        app.get_graph().print_ascii()
    except Exception:
        print("  extract → validate → process (with retry loop)")
    print()

    # Example 1: Clean input — should pass on first try
    print("=" * 60)
    print("Example 1: Clean order (should pass first try)")
    print("=" * 60)
    result = app.invoke({
        "user_request": "Process an order from Globex Corp for twelve thousand five hundred dollars USD, PO number PO-2026-042",
        "retry_count": 0,
    })
    print(f"\nFinal: {result.get('final_result', 'FAILED')}")

    print()

    # Example 2: Ambiguous input — LLM might extract wrong currency,
    # Flow catches it, and the self-correction loop fixes it
    print("=" * 60)
    print("Example 2: Ambiguous order (may need self-correction)")
    print("=" * 60)
    result = app.invoke({
        "user_request": "We got an order from Acme Inc for 500 Yen, PO number PO-JP-001",
        "retry_count": 0,
    })
    print(f"\nFinal: {result.get('final_result', 'FAILED — validation errors not resolved')}")

    if result.get("validation_errors"):
        print(f"Unresolved errors:\n{result['validation_errors']}")


if __name__ == "__main__":
    main()
