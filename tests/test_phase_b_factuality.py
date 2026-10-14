import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

os.environ.setdefault("NIMO_ROOT", tempfile.mkdtemp(prefix="nimo-phase-b-test-"))
import NIMO_TERMINAL_MASTER_4_0 as nimo


class PhaseBFactualityTests(unittest.TestCase):
    def setUp(self):
        self.engine = nimo.ResearchEngine.__new__(nimo.ResearchEngine)

    def test_current_high_impact_requires_primary_and_independent_publisher(self):
        rows = [
            {"domain": "cabinet.gov.bd", "tier": 1, "title": "Official statement", "content": "The office holder is listed.", "status": "retrieved", "published_at": "2026-09-15", "updated_at": "2026-09-15", "recency_status": "current_window"},
            {"domain": "reuters.com", "tier": 2, "title": "Independent report", "content": "The same office holder is reported.", "status": "retrieved", "published_at": "2026-09-16", "recency_status": "current_window"},
        ]
        status, confidence, notes = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("VERIFIED", "HIGH"))
        self.assertTrue(notes)

    def test_current_claim_with_one_source_is_not_verified(self):
        rows = [{"domain": "reuters.com", "tier": 2, "title": "Report", "content": "A current claim.", "status": "retrieved", "published_at": "2026-09-16", "recency_status": "current_window"}]
        status, confidence, _ = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("SINGLE-SOURCE", "LOW"))

    def test_conflict_signal_is_contested(self):
        rows = [
            {"domain": "gov.bd", "tier": 1, "title": "Statement", "content": "The statement was corrected.", "status": "retrieved"},
            {"domain": "reuters.com", "tier": 2, "title": "Report", "content": "The claim is disputed.", "status": "retrieved"},
        ]
        status, confidence, notes = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("CONTESTED", "LOW"))
        self.assertIn("human review", notes[0])

    def test_non_current_multi_source_claim_is_corroborated(self):
        rows = [
            {"domain": "example-a.org", "tier": 3, "title": "A", "content": "Historical evidence.", "status": "retrieved"},
            {"domain": "example-b.org", "tier": 3, "title": "B", "content": "Historical evidence.", "status": "retrieved"},
        ]
        status, confidence, _ = self.engine._claim_status(rows)
        self.assertEqual((status, confidence), ("CORROBORATED", "MEDIUM"))

    def test_bengali_office_holder_query_triggers_live_research_and_date_gate(self):
        query = "বাংলাদেশের প্রধানমন্ত্রী কে"
        self.assertTrue(nimo.should_auto_web(query))
        self.assertTrue(nimo.is_current_office_holder_query(query))
        self.assertIn("as of", nimo.recency_constraint(query))
        tree = nimo.ResearchEngine.question_tree(query)
        self.assertEqual(len(tree), 2)
        self.assertTrue(all(leaf["time_sensitive"] for leaf in tree))

    def test_web_routing_preserves_conversation_and_stable_explanations(self):
        self.assertFalse(nimo.should_auto_web("Hi, how are you?"))
        self.assertFalse(nimo.should_auto_web("What is gravity?"))
        self.assertFalse(nimo.should_auto_web("কেমন আছ?"))
        self.assertTrue(nimo.should_auto_web("Gather sources about gravitational waves"))
        self.assertTrue(nimo.should_auto_web("বাংলাদেশের সর্বশেষ মূল্যস্ফীতির তথ্য খুঁজে দাও"))

    def test_research_auto_enables_online_but_offline_override_wins(self):
        app = nimo.NIMOApplication.__new__(nimo.NIMOApplication)
        app.network_policy = "auto"
        app.online_mode = False
        with patch.object(nimo.console, "print"):
            self.assertTrue(app._require_online("Research"))
        self.assertTrue(app.online_mode)

        app.network_policy = "offline"
        app.online_mode = False
        with patch.object(nimo.console, "print"):
            self.assertFalse(app._require_online("Research"))
        self.assertFalse(app.online_mode)

    def test_bengali_historical_office_holder_query_is_not_treated_as_current(self):
        query = "২০১০ সালে বাংলাদেশের প্রধানমন্ত্রী কে ছিলেন"
        self.assertFalse(nimo.is_current_office_holder_query(query))
        self.assertTrue(nimo.should_auto_web(query))

    def test_office_holder_query_has_official_and_independent_search_angles(self):
        queries = nimo.ResearchEngine.query_battery("বাংলাদেশের প্রধানমন্ত্রী কে", "বর্তমান পদধারী", quick=True)
        self.assertTrue(any("official government" in query for query in queries))
        self.assertTrue(any("independent reporting" in query for query in queries))
        self.assertTrue(any("বাংলাদেশ" in query for query in queries))

    def test_office_holder_query_planning_is_not_limited_to_one_country(self):
        queries = nimo.ResearchEngine.query_battery("Who is the current Prime Minister of India?", "verify current office holder", quick=True)
        self.assertTrue(any("official government" in query for query in queries))
        self.assertTrue(any("independent reporting" in query for query in queries))

    def test_public_domains_are_not_excluded_from_discovery(self):
        topic = "Who is Jane Doe?"
        row = {"url": "https://example-research-site.invalid/jane-doe", "title": "Jane Doe profile", "snippet": "Jane Doe", "content": "Jane Doe biography"}
        self.assertTrue(nimo.ResearchEngine._source_is_relevant(topic, row))

    def test_python_research_accepts_relevant_non_allowlisted_sources(self):
        topic = "Python 3.14 release changes"
        row = {"url": "https://independent-engineering.example/python-release-review", "title": "Python 3.14 release notes explained", "content": "This Python 3.14 article reviews release changes and behavior."}
        self.assertTrue(nimo.ResearchEngine._source_is_relevant(topic, row, require_content=True))
        unrelated = {"url": "https://independent-engineering.example/python-release-review", "title": "Python 3.13 release notes", "content": "This Python 3.13 article reviews release changes and behavior."}
        self.assertFalse(nimo.ResearchEngine._source_is_relevant(topic, unrelated, require_content=True))

    def test_current_sources_without_dates_cannot_be_verified(self):
        rows = [
            {"domain": "cabinet.gov.bd", "tier": 1, "content": "The office holder is listed.", "status": "retrieved"},
            {"domain": "reuters.com", "tier": 2, "content": "The same office holder is reported.", "status": "retrieved"},
        ]
        status, confidence, _ = self.engine._claim_status(rows, strict_current=True, high_impact=True)
        self.assertEqual((status, confidence), ("UNVERIFIED", "LOW"))

    def test_failed_extraction_snippet_is_never_claim_evidence(self):
        lead = {"source_ref": "S1", "title": "Search result", "snippet": "STALE CLAIM", "status": "extraction_failed"}
        safe = nimo.ResearchEngine._mark_lead_only(lead, "extraction_failed", "Timeout")
        self.assertEqual(safe["content"], "")
        self.assertEqual(safe["discovery_snippet"], "STALE CLAIM")
        self.assertFalse(nimo.ResearchEngine._is_extracted_source(safe))
        self.assertEqual(nimo.ResearchEngine._claim_status([safe])[0], "UNVERIFIED")
        self.assertNotIn("STALE CLAIM", nimo.ResearchEngine._quick_direct_answer("What happened?", [safe]))

    def test_content_without_explicit_retrieved_status_is_not_evidence(self):
        unmarked = {"source_ref": "S1", "title": "Page", "content": "A claim from an unmarked record."}
        self.assertFalse(nimo.ResearchEngine._is_extracted_source(unmarked))
        self.assertEqual(nimo.ResearchEngine._claim_status([unmarked])[0], "UNVERIFIED")

    def test_official_domain_classification_rejects_lookalike_hostnames(self):
        tier, _ = nimo.ResearchEngine.tier_for("cabinet.gov.bd.attacker.example", "contextual")
        self.assertGreater(tier, 1)
        self.assertEqual(nimo.ResearchEngine._authority("www.gov.in"), "government/official")
        self.assertEqual(nimo.ResearchEngine._authority("pmo.go.jp"), "government/official")
        self.assertNotEqual(nimo.ResearchEngine._authority("example.gov.in.attacker.com"), "government/official")

    def test_chat_web_context_uses_extracted_pages_and_not_search_snippets(self):
        class FakeSearchProvider:
            available = True

            def __init__(self, **kwargs):
                pass

            def search(self, query, limit=8):
                if "official government" in query:
                    return [{"title": "Official office directory", "url": "https://cabinet.gov.bd/pages/office-heads", "snippet": "STALE SNIPPET", "search_provider": "DuckDuckGo"}]
                return [{"title": "Independent report", "url": "https://apnews.com/article/current-government", "snippet": "STALE SNIPPET", "search_provider": "DuckDuckGo"}]

            def extract(self, url):
                return {"content": "DIRECT PAGE: named current office holder", "published_at": "2026-09-15", "updated_at": ""}

        with patch.object(nimo, "SearchProvider", FakeSearchProvider):
            rows = nimo.auto_web_context("বাংলাদেশের প্রধানমন্ত্রী কে", limit=5)
        self.assertEqual(len(rows), 2)
        self.assertTrue(all("DIRECT PAGE" in row for row in rows))
        self.assertTrue(all("STALE SNIPPET" not in row for row in rows))
        self.assertTrue(any("Tier: 1" in row for row in rows))
        self.assertTrue(any("Tier: 2" in row for row in rows))
        self.assertNotEqual(nimo.ResearchEngine._publisher_bucket("cabinet.gov.bd"), nimo.ResearchEngine._publisher_bucket("apnews.com"))

    def test_explicit_web_lookup_overrides_automatic_intent_gate(self):
        class FakeSearchProvider:
            available = True

            def __init__(self, **kwargs):
                pass

            def search(self, query, limit=8):
                return [{"title": "Gravity overview", "url": "https://example.org/gravity", "snippet": "snippet", "search_provider": "DuckDuckGo"}]

            def extract(self, url):
                return {"content": "A directly retrieved stable explanation of gravity."}

        with patch.object(nimo, "SearchProvider", FakeSearchProvider):
            self.assertEqual(nimo.auto_web_context("gravity"), [])
            rows = nimo.auto_web_context("gravity", force=True)
        self.assertEqual(len(rows), 1)
        self.assertIn("directly retrieved", rows[0])

    def test_page_extraction_failures_are_counted_and_reported(self):
        class FakeSearchProvider:
            available = True
            last_error = ""
            last_provider = "Test Search"

            def __init__(self, **kwargs):
                pass

            def search(self, query, limit=8):
                return [
                    {"title": "Readable", "url": "https://example.org/readable", "search_provider": "Test Search"},
                    {"title": "Unreadable", "url": "https://example.net/unreadable", "search_provider": "Test Search"},
                ]

            def extract(self, url):
                if "unreadable" in url:
                    raise ValueError("unsafe target details are not shown to the user")
                return {"content": "Retrieved page evidence."}

        with patch.object(nimo, "SearchProvider", FakeSearchProvider):
            rows = nimo.auto_web_context("gather information on gravity", limit=5)
        self.assertEqual(len(rows), 1)
        status = nimo.auto_web_context.last_status
        self.assertEqual(status["page_failure_count"], 1)
        self.assertIn("could not be safely retrieved", nimo.web_retrieval_notice(status))
        self.assertNotIn("unsafe target details", nimo.web_retrieval_notice(status))

    def test_bangladesh_state_news_is_not_counted_as_independent_from_government(self):
        self.assertEqual(nimo.ResearchEngine._publisher_bucket("bssnews.net"), "bangladesh-government")


if __name__ == "__main__":
    unittest.main()
