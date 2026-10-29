import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AssetTests(unittest.TestCase):
    def test_event_contract_is_versioned_and_strict(self):
        contract = json.loads((ROOT / "contracts/behavior_event_v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["properties"]["schema_version"]["const"], "1.0.0")
        self.assertFalse(contract["additionalProperties"])

    def test_dbt_model_uses_safe_aggregations_and_qualified_sources(self):
        sql = (ROOT / "models/marts/customer_360.sql").read_text(encoding="utf-8")
        self.assertIn("COALESCE", sql.upper())
        self.assertIn("source('silver', 'orders')", sql)
        self.assertNotIn("SELECT *", sql.upper())

    def test_runbook_contains_verification_and_rollback(self):
        runbook = (ROOT / "docs/runbook.md").read_text(encoding="utf-8")
        self.assertIn("## Verificação", runbook)
        self.assertIn("## Rollback", runbook)
        self.assertIn("## Escalonamento", runbook)
