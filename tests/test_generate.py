import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.customer360.generate import generate


class GenerateTests(unittest.TestCase):
    def temporary(self): return tempfile.TemporaryDirectory(dir=Path.cwd())

    def test_generation_is_deterministic(self):
        with self.temporary() as first, self.temporary() as second:
            generate(Path(first), seed=7, customer_count=30, order_count=60); generate(Path(second), seed=7, customer_count=30, order_count=60)
            one = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(first).iterdir()}
            two = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(second).iterdir()}
            self.assertEqual(one, two)

    def test_manifest_matches_files(self):
        with self.temporary() as folder:
            target = Path(folder); manifest = generate(target, customer_count=30, order_count=60)
            self.assertEqual(json.loads((target / "manifest.json").read_text(encoding="utf-8")), manifest)

    def test_event_ids_include_controlled_duplicate(self):
        with self.temporary() as folder:
            target = Path(folder); generate(target, customer_count=30, order_count=80)
            events = [json.loads(line) for line in (target / "behavior_events.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertLess(len({event["event_id"] for event in events}), len(events))
