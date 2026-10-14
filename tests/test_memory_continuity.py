import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("NIMO_ROOT", tempfile.mkdtemp(prefix="nimo-memory-test-"))
import NIMO_TERMINAL_MASTER_4_0 as nimo


class MemoryContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="nimo-memory-case-", dir=nimo.PROJECT_ROOT)
        self.db = nimo.DBManager(str(Path(self.temp_dir.name) / "memory.sqlite3"))
        self.db.init_db()
        self.memory = nimo.MemoryManager(self.db, nimo.OllamaClient("http://127.0.0.1:11434"))
        self.session = "session-current"
        self.db.create_session(self.session)

    def tearDown(self):
        for connection in (getattr(self.db.local, "conn", None),):
            if connection is not None:
                connection.close()
        self.temp_dir.cleanup()

    def add(self, session, role, content, **options):
        self.memory.add(session, role, content, **options)
        return int(self.db.connection().execute(
            "SELECT id FROM messages WHERE session_id=? ORDER BY id DESC LIMIT 1", (session,)
        ).fetchone()[0])

    def test_chat_duplicates_are_preserved_as_distinct_turns(self):
        first = self.add(self.session, "user", "repeat this")
        second = self.add(self.session, "user", "repeat this")
        self.assertNotEqual(first, second)
        self.assertEqual(len(self.memory.recent(self.session)), 2)

    def test_recent_context_excludes_sensitive_excluded_and_expired_records(self):
        self.add(self.session, "user", "keep this")
        sensitive = self.add(self.session, "user", "sensitive detail")
        excluded = self.add(self.session, "user", "excluded detail")
        expired = self.add(self.session, "user", "expired detail")
        self.memory.set_metadata(sensitive, sensitivity="sensitive")
        self.memory.set_excluded(excluded)
        self.memory.set_metadata(expired, retention_until="2000-01-01T00:00:00+00:00")
        self.assertEqual([row["content"] for row in self.memory.recent(self.session)], ["keep this"])

    def test_invalid_retention_date_is_rejected(self):
        message_id = self.add(self.session, "user", "retention stays active")
        with self.assertRaisesRegex(ValueError, "ISO 8601"):
            self.memory.set_metadata(message_id, retention_until="not-a-date")
        self.assertEqual(len(self.memory.recent(self.session)), 1)

    def test_checkpoints_are_relevant_after_a_new_session(self):
        contents = [
            "Remember the violet comet detail.", "I will remember it.",
            "It appeared in the eastern sky.", "That is the second detail.",
            "The observation was in winter.", "I will keep that context.",
        ]
        for index, content in enumerate(contents):
            self.add(self.session, "user" if index % 2 == 0 else "assistant", content)
        self.memory.summarize_if_needed(self.session)
        new_session = "session-after-restart"
        self.db.create_session(new_session)
        summaries = self.memory.summaries(new_session, "violet comet")
        self.assertEqual(len(summaries), 1)
        self.assertIn("violet comet", summaries[0].lower())
        self.assertTrue(any("violet" in item.lower() for item in self.memory.relevant("violet", new_session)))

    def test_excluding_a_checkpoint_source_removes_summary_and_restores_other_sources(self):
        ids = []
        for index in range(nimo.SUMMARY_TRIGGER):
            ids.append(self.add(self.session, "user" if index % 2 == 0 else "assistant", f"checkpoint detail {index}"))
        self.memory.summarize_if_needed(self.session)
        self.assertEqual(self.db.connection().execute("SELECT COUNT(*) FROM summaries").fetchone()[0], 1)
        self.memory.set_excluded(ids[0])
        self.assertEqual(self.db.connection().execute("SELECT COUNT(*) FROM summaries").fetchone()[0], 0)
        self.assertEqual(self.db.connection().execute("SELECT COUNT(*) FROM summary_sources").fetchone()[0], 0)
        rows = self.db.connection().execute(
            "SELECT id,memory_excluded FROM messages WHERE session_id=? ORDER BY id", (self.session,)
        ).fetchall()
        self.assertEqual([row["memory_excluded"] for row in rows], [1, 0, 0, 0, 0, 0])

    def test_checkpoint_is_not_retrieved_after_a_source_expires(self):
        for index in range(nimo.SUMMARY_TRIGGER):
            self.add(self.session, "user" if index % 2 == 0 else "assistant", f"expiry check {index}")
        self.memory.summarize_if_needed(self.session)
        source_id = self.db.connection().execute(
            "SELECT id FROM messages WHERE session_id=? ORDER BY id LIMIT 1", (self.session,)
        ).fetchone()[0]
        self.db.connection().execute(
            "UPDATE messages SET memory_retention_until='2000-01-01T00:00:00+00:00' WHERE id=?", (source_id,)
        )
        self.db.connection().commit()
        self.assertEqual(self.memory.summaries(self.session), [])

    def test_marking_a_source_sensitive_invalidates_checkpoint_and_embedding(self):
        ids = []
        for index in range(nimo.SUMMARY_TRIGGER):
            content = "secretneedle-xyz" if index == 0 else f"private checkpoint {index}"
            ids.append(self.add(self.session, "user" if index % 2 == 0 else "assistant", content))
        self.memory.summarize_if_needed(self.session)
        conn = self.db.connection()
        conn.execute(
            "INSERT INTO embeddings(message_id,vector,model_name,created_at) VALUES (?,?,?,?)",
            (ids[0], "[1.0]", "test", nimo.now_iso()),
        )
        conn.commit()
        self.memory.set_metadata(ids[0], sensitivity="sensitive")
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0], 0)
        self.assertEqual(conn.execute("SELECT COUNT(*) FROM embeddings WHERE message_id=?", (ids[0],)).fetchone()[0], 0)
        self.assertFalse(any("secretneedle-xyz" in item for item in self.memory.relevant("secretneedle-xyz", "another-session")))

    def test_compaction_keeps_sessions_separate_and_serves_its_checkpoint(self):
        other = "session-other"
        self.db.create_session(other)
        for session, prefix in ((self.session, "first session"), (other, "other session")):
            for index in range(2):
                self.add(session, "user" if index == 0 else "assistant", f"{prefix} detail {index}")
        self.db.connection().execute(
            "UPDATE messages SET created_at='2000-01-01T00:00:00+00:00'"
        )
        self.db.connection().commit()
        result = self.memory.compact(min_age_days=0, max_messages=10)
        self.assertEqual(result["summaries"], 1)
        sources = self.db.connection().execute(
            "SELECT m.session_id FROM summary_sources ss JOIN messages m ON m.id=ss.message_id"
        ).fetchall()
        self.assertEqual({row["session_id"] for row in sources}, {self.session})
        self.assertEqual(len(self.memory.summaries(self.session)), 1)
        self.assertEqual(self.memory.summaries(other), [])

    def test_trim_messages_never_exceeds_budget(self):
        messages = [
            {"role": "user", "content": "short"},
            {"role": "assistant", "content": "x" * 100},
        ]
        trimmed = nimo.trim_messages(messages, 20)
        self.assertEqual(sum(len(row["content"]) for row in trimmed), 20)
        self.assertTrue(trimmed[-1]["content"].endswith("x"))


if __name__ == "__main__":
    unittest.main()
