"""Pipeline local Bronze → Silver → Gold, executável sem serviços externos."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def canonical_ref(value: str) -> str:
    value = value.strip().lower()
    return re.sub(r"\D", "", value) if value.startswith("+") else value


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream: return list(csv.DictReader(stream))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for row in rows: stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def load_jsonl(path: Path) -> list[dict]: return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def execute(source: Path, storage: Path) -> dict:
    run_id = hashlib.sha256((source / "manifest.json").read_bytes()).hexdigest()[:16]
    bronze, silver, gold = storage / "bronze", storage / "silver", storage / "gold"
    quarantine = []
    names = ["crm_customers", "orders", "order_items", "payments", "support_tickets"]
    source_rows = {name: read_csv(source / f"{name}.csv") for name in names}
    events = load_jsonl(source / "behavior_events.jsonl")
    for name, rows in source_rows.items():
        write_jsonl(bronze / f"{name}.jsonl", [{"run_id": run_id, "source": name, "payload": row} for row in rows])
    write_jsonl(bronze / "behavior_events.jsonl", [{"run_id": run_id, "source": "behavior_events", "payload": row} for row in events])

    customers = []
    for row in source_rows["crm_customers"]:
        if not EMAIL.match(row["email"]): quarantine.append({"source": "crm_customers", "key": row["crm_customer_id"], "rule": "valid_email"}); continue
        clean = dict(row); clean["email"] = canonical_ref(row["email"]); clean["phone"] = canonical_ref(row["phone"]); customers.append(clean)
    customer_refs = {row["email"]: row["crm_customer_id"] for row in customers} | {row["phone"]: row["crm_customer_id"] for row in customers}
    orders = []
    for row in source_rows["orders"]:
        if float(row["total_amount"]) < 0: quarantine.append({"source": "orders", "key": row["order_id"], "rule": "amount_non_negative"}); continue
        clean = dict(row); clean["crm_customer_id"] = customer_refs.get(canonical_ref(row["commerce_customer_ref"])); orders.append(clean)
    order_ids = {row["order_id"] for row in orders}
    payments = []
    for row in source_rows["payments"]:
        if row["order_id"] not in order_ids: quarantine.append({"source": "payments", "key": row["payment_id"], "rule": "order_fk"}); continue
        clean = dict(row); clean["crm_customer_id"] = customer_refs.get(canonical_ref(row["payment_customer_ref"])); payments.append(clean)
    tickets = []
    for row in source_rows["support_tickets"]:
        score = row["satisfaction_score"]
        if score and not 1 <= int(score) <= 5: quarantine.append({"source": "support_tickets", "key": row["ticket_id"], "rule": "satisfaction_range"}); continue
        clean = dict(row); clean["crm_customer_id"] = customer_refs.get(canonical_ref(row["support_customer_ref"])); tickets.append(clean)
    unique_events = {}
    for event in events: unique_events[event["event_id"]] = event
    duplicate_count = len(events) - len(unique_events)
    if duplicate_count: quarantine.append({"source": "behavior_events", "key": "multiple", "rule": "event_id_unique", "count": duplicate_count})

    silver_sets = {"customers": customers, "orders": orders, "payments": payments, "support_tickets": tickets, "behavior_events": list(unique_events.values())}
    for name, rows in silver_sets.items(): write_jsonl(silver / f"{name}.jsonl", rows)
    write_jsonl(silver / "quarantine.jsonl", quarantine)

    order_metrics, event_metrics, ticket_metrics = defaultdict(lambda: {"orders": 0, "revenue": 0.0}), defaultdict(int), defaultdict(int)
    for row in orders:
        if row["crm_customer_id"] and row["status"] == "completed": order_metrics[row["crm_customer_id"]]["orders"] += 1; order_metrics[row["crm_customer_id"]]["revenue"] += float(row["total_amount"])
    anonymous_to_customer = {event["anonymous_id"]: customer_refs.get(canonical_ref(event["customer_ref"])) for event in unique_events.values() if event.get("customer_ref")}
    for event in unique_events.values():
        customer_id = customer_refs.get(canonical_ref(event.get("customer_ref") or "")) or anonymous_to_customer.get(event["anonymous_id"])
        if customer_id: event_metrics[customer_id] += 1
    for ticket in tickets:
        if ticket["crm_customer_id"]: ticket_metrics[ticket["crm_customer_id"]] += 1
    customer360 = []
    for customer in customers:
        key = customer["crm_customer_id"]; metrics = order_metrics[key]
        customer360.append({"customer_id": key, "email_masked": customer["email"][:2] + "***@" + customer["email"].split("@")[1], "state": customer["state"], "order_count": metrics["orders"], "lifetime_value": round(metrics["revenue"], 2), "behavior_event_count": event_metrics[key], "support_ticket_count": ticket_metrics[key], "marketing_consent": customer["marketing_consent"]})
    write_jsonl(gold / "customer_360.jsonl", customer360)
    report = {"run_id": run_id, "bronze_rows": sum(len(rows) for rows in source_rows.values()) + len(events), "silver_rows": sum(len(rows) for rows in silver_sets.values()), "gold_customers": len(customer360), "quarantine_rows": len(quarantine), "duplicate_events": duplicate_count}
    (storage / "run_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--source", type=Path, default=Path("data/sample")); parser.add_argument("--storage", type=Path, default=Path("storage")); args = parser.parse_args(); print(json.dumps(execute(args.source, args.storage), indent=2))


if __name__ == "__main__": main()
