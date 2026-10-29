"""Gera fontes relacionais e eventos sintéticos para a plataforma Customer 360."""

from __future__ import annotations

import argparse
import csv
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path


NAMES = ["Ana Lima", "Bruno Souza", "Carla Rocha", "Daniel Silva", "Eduarda Gomes", "Felipe Dias", "Gabriela Alves", "Henrique Martins"]
STATES = ["SP", "RJ", "MG", "PR", "BA", "PE"]
EVENTS = ["page_view", "product_view", "add_to_cart", "checkout_start", "purchase"]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def stable_id(namespace: str, value: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"customer360/{namespace}/{value}"))


def generate(output: Path, seed: int = 42, customer_count: int = 100, order_count: int = 400) -> dict:
    rng = random.Random(seed)
    origin = datetime(2025, 1, 1, tzinfo=timezone.utc)
    customers = []
    for number in range(1, customer_count + 1):
        name = rng.choice(NAMES); email = f"cliente{number:04d}@example.com"
        customers.append({
            "crm_customer_id": f"CRM{number:05d}", "full_name": name, "email": email,
            "phone": f"+55119{number:08d}", "state": rng.choice(STATES),
            "created_at": (origin - timedelta(days=rng.randint(1, 500))).isoformat(),
            "updated_at": (origin + timedelta(days=rng.randint(0, 300))).isoformat(),
            "marketing_consent": rng.choice(["true", "true", "false"]),
        })

    orders, items, payments, events, tickets = [], [], [], [], []
    for number in range(1, order_count + 1):
        customer = rng.choice(customers); occurred = origin + timedelta(days=rng.randint(0, 364), minutes=rng.randint(0, 1439))
        order_id = f"ORD{number:06d}"; amount = round(rng.uniform(30, 900), 2)
        orders.append({"order_id": order_id, "commerce_customer_ref": customer["email"] if number % 7 else customer["phone"], "ordered_at": occurred.isoformat(), "status": rng.choices(["completed", "cancelled", "refunded"], [0.91, 0.05, 0.04])[0], "total_amount": f"{amount:.2f}"})
        for line in range(1, rng.randint(2, 5)):
            items.append({"order_item_id": f"{order_id}-{line}", "order_id": order_id, "sku": f"SKU{rng.randint(1,60):04d}", "quantity": rng.randint(1, 3), "unit_price": f"{amount / 2:.2f}"})
        payments.append({"payment_id": f"PAY{number:06d}", "order_id": order_id, "payment_customer_ref": customer["email"].upper() if number % 11 == 0 else customer["email"], "authorized_at": (occurred + timedelta(minutes=rng.randint(0, 20))).isoformat(), "amount": f"{amount:.2f}", "status": "captured"})

        session_id = stable_id("session", str(number))
        for step, event_name in enumerate(EVENTS[:rng.randint(2, 6)]):
            event_time = occurred - timedelta(minutes=(5 - step) * rng.randint(1, 12))
            delay = rng.choice([1, 2, 3, 5, 60, 180])
            event = {"event_id": stable_id("event", f"{number}-{step}"), "schema_version": "1.0.0", "event_name": event_name, "event_time": event_time.isoformat(), "ingested_at": (event_time + timedelta(minutes=delay)).isoformat(), "anonymous_id": stable_id("anonymous", customer["crm_customer_id"]), "customer_ref": customer["email"] if step >= 2 else None, "session_id": session_id, "properties": {"page": f"/produto/{rng.randint(1,60)}", "device": rng.choice(["mobile", "desktop"])}}
            events.append(event)
            if number % 80 == 0 and step == 1: events.append(dict(event))

    for number in range(1, 81):
        customer = rng.choice(customers)
        tickets.append({"ticket_id": f"TKT{number:05d}", "support_customer_ref": customer["phone"] if number % 4 == 0 else customer["email"], "opened_at": (origin + timedelta(days=rng.randint(0,364))).isoformat(), "reason": rng.choice(["delivery", "payment", "product", "refund"]), "satisfaction_score": rng.choice([1,2,3,4,5,""])})

    # Falhas controladas para demonstrar contratos e quarentena.
    customers[4]["email"] = "invalid-email"
    orders[9]["total_amount"] = "-50.00"
    payments[14]["order_id"] = "ORD999999"
    tickets[7]["satisfaction_score"] = "9"

    write_csv(output / "crm_customers.csv", customers); write_csv(output / "orders.csv", orders)
    write_csv(output / "order_items.csv", items); write_csv(output / "payments.csv", payments)
    write_csv(output / "support_tickets.csv", tickets)
    with (output / "behavior_events.jsonl").open("w", encoding="utf-8") as stream:
        for event in sorted(events, key=lambda item: item["ingested_at"]): stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    manifest = {"seed": seed, "row_counts": {"crm_customers.csv": len(customers), "orders.csv": len(orders), "order_items.csv": len(items), "payments.csv": len(payments), "support_tickets.csv": len(tickets), "behavior_events.jsonl": len(events)}, "controlled_issues": ["invalid_email", "negative_order_amount", "orphan_payment", "invalid_satisfaction", "duplicate_event"]}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--output", type=Path, default=Path("data/sample")); parser.add_argument("--seed", type=int, default=42); parser.add_argument("--customers", type=int, default=100); parser.add_argument("--orders", type=int, default=400); args = parser.parse_args()
    print(json.dumps(generate(args.output, args.seed, args.customers, args.orders), indent=2, ensure_ascii=False))


if __name__ == "__main__": main()
