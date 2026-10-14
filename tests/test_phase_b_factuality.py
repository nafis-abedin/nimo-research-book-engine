import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("NIMO_ROOT", tempfile.mkdtemp(prefix="nimo-phase-b-test-"))
import NIMO_TERMINAL_MASTER_4_0 as nimo


class PhaseBFactualityTests(unittest.TestCase):
    def setUp(self):
        self.engine = nimo.ResearchEngine.__new__(nimo.ResearchEngine)

    def test_current_high_impact_requires_primary_and_independent_publisher(self):
        rows = [
            {"domain": "cabinet.gov.bd", "tier": 1, "title": "Official statement", "content": "The office holder is listed."},
            {"domain": "reuters.com", "tier": 2, "title": "Independent report", "content": "The same office holder is reported."},
        ]
        status, confidence, notes = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("VERIFIED", "HIGH"))
        self.assertTrue(notes)

    def test_current_claim_with_one_source_is_not_verified(self):
        rows = [{"domain": "reuters.com", "tier": 2, "title": "Report", "content": "A current claim."}]
        status, confidence, _ = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("SINGLE-SOURCE", "LOW"))

    def test_conflict_signal_is_contested(self):
        rows = [
            {"domain": "gov.bd", "tier": 1, "title": "Statement", "content": "The statement was corrected."},
            {"domain": "reuters.com", "tier": 2, "title": "Report", "content": "The claim is disputed."},
        ]
        status, confidence, notes = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("CONTESTED", "LOW"))
        self.assertIn("human review", notes[0])

    def test_non_current_multi_source_claim_is_corroborated(self):
        rows = [
            {"domain": "example-a.org", "tier": 3, "title": "A", "content": "Historical evidence."},
            {"domain": "example-b.org", "tier": 3, "title": "B", "content": "Historical evidence."},
        ]
        status, confidence, _ = self.engine._claim_status(rows)
        self.assertEqual((status, confidence), ("CORROBORATED", "MEDIUM"))


if __name__ == "__main__":
    unittest.main()
