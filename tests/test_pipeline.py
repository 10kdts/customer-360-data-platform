import json
import tempfile
import unittest
from pathlib import Path

from src.customer360.generate import generate
from src.customer360.pipeline import execute, load_jsonl


class PipelineTests(unittest.TestCase):
    def test_pipeline_builds_layers_and_quarantines_controlled_issues(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as source, tempfile.TemporaryDirectory(dir=Path.cwd()) as storage:
            generate(Path(source), customer_count=30, order_count=80)
            report = execute(Path(source), Path(storage))
            self.assertGreater(report["bronze_rows"], report["silver_rows"])
            self.assertGreaterEqual(report["quarantine_rows"], 5)
            self.assertEqual(len(load_jsonl(Path(storage) / "gold/customer_360.jsonl")), 29)

    def test_reprocessing_is_deterministic(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as source, tempfile.TemporaryDirectory(dir=Path.cwd()) as one, tempfile.TemporaryDirectory(dir=Path.cwd()) as two:
            generate(Path(source), customer_count=30, order_count=80)
            self.assertEqual(execute(Path(source), Path(one)), execute(Path(source), Path(two)))
