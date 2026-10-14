import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("NIMO_ROOT", tempfile.mkdtemp(prefix="nimo-safety-test-"))
import NIMO_TERMINAL_MASTER_4_0 as nimo
import NIMO_WINDOWS_INSTALL as windows_install


class ReleaseSafetyTests(unittest.TestCase):
    def test_default_runtime_root_uses_windows_user_data_location(self):
        with patch.dict(nimo.os.environ, {"NIMO_ROOT": "", "LOCALAPPDATA": "C:/Users/Example/AppData/Local", "XDG_DATA_HOME": ""}):
            self.assertEqual(nimo._default_runtime_root(), Path("C:/Users/Example/AppData/Local/NIMO"))

    def test_secret_store_and_default_data_are_outside_source_checkout(self):
        self.assertNotEqual(nimo.SECRET_STORE_PATH.parent.resolve(), nimo.PROJECT_ROOT.resolve())
        self.assertNotEqual(Path(nimo.DB_PATH).resolve().parent, nimo.PROJECT_ROOT.resolve())

    def test_personal_learning_and_vault_backups_use_runtime_root(self):
        source = Path(nimo.__file__).read_text(encoding="utf-8")
        self.assertIn('RUNTIME_ROOT / "vault_fact_backups"', source)
        self.assertIn('RUNTIME_ROOT / "backups" / "learning"', source)
        self.assertNotIn('Path(PROJECT_ROOT) / "vault_fact_backups"', source)

    def test_public_url_validator_rejects_private_destinations_and_credentials(self):
        self.assertFalse(nimo.validate_public_http_url("http://127.0.0.1/admin")[0])
        self.assertFalse(nimo.validate_public_http_url("http://user:pass@example.com/")[0])
        self.assertFalse(nimo.validate_public_http_url("http://example.com:8080/")[0])

    def test_public_url_validator_rejects_a_hostname_with_private_dns_answer(self):
        dns_rows = [
            (nimo.socket.AF_INET, nimo.socket.SOCK_STREAM, 6, "", ("93.184.216.34", 80)),
            (nimo.socket.AF_INET, nimo.socket.SOCK_STREAM, 6, "", ("192.168.1.10", 80)),
        ]
        with patch.object(nimo.socket, "getaddrinfo", return_value=dns_rows):
            valid, reason, _ = nimo.validate_public_http_url("https://mixed.example/path")
        self.assertFalse(valid)
        self.assertEqual(reason, "private_or_nonpublic_address_blocked")

    def test_page_fetch_rejects_localhost_before_network_request(self):
        searcher = nimo.SearchProvider(timeout=3)
        with patch.object(nimo.requests, "get") as request:
            with self.assertRaisesRegex(ValueError, "local_host_blocked"):
                searcher.extract("http://localhost/private")
        request.assert_not_called()

    def test_page_redirect_to_local_address_is_blocked(self):
        class FakeResponse:
            is_redirect = True
            is_permanent_redirect = False
            headers = {"location": "http://127.0.0.1/admin"}

            def close(self):
                self.closed = True

        response = FakeResponse()
        dns_rows = [(nimo.socket.AF_INET, nimo.socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        with patch.object(nimo.socket, "getaddrinfo", return_value=dns_rows), patch.object(nimo.requests, "get", return_value=response) as request:
            with self.assertRaisesRegex(ValueError, "redirect blocked"):
                nimo.SearchProvider(timeout=3).extract("https://public.example/path")
        request.assert_called_once()
        self.assertTrue(response.closed)

    def test_page_response_size_is_bounded_and_response_is_closed(self):
        class FakeResponse:
            is_redirect = False
            is_permanent_redirect = False
            headers = {"content-type": "text/html", "content-length": str(nimo.SearchProvider.MAX_PAGE_BYTES + 1)}
            encoding = "utf-8"

            def raise_for_status(self):
                return None

            def close(self):
                self.closed = True

        response = FakeResponse()
        dns_rows = [(nimo.socket.AF_INET, nimo.socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))]
        with patch.object(nimo.socket, "getaddrinfo", return_value=dns_rows), patch.object(nimo.requests, "get", return_value=response):
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                nimo.SearchProvider(timeout=3).extract("https://public.example/path")
        self.assertTrue(response.closed)

    def test_snapshot_verification_and_overwrite_prevention(self):
        with tempfile.TemporaryDirectory(prefix="nimo-backup-test-", dir=nimo.PROJECT_ROOT) as temp_dir:
            root = Path(temp_dir)
            source = root / "memory.db"
            connection = sqlite3.connect(source)
            connection.execute("CREATE TABLE sample (value TEXT)")
            connection.execute("INSERT INTO sample VALUES ('local test data')")
            connection.commit()
            connection.close()
            manager = nimo.DBManager(str(source))
            target = root / "snapshot.db"
            manifest = manager.backup_snapshot(str(target))
            verified = nimo.DBManager.verify_snapshot(str(target))
            self.assertEqual(verified["integrity"], "ok")
            self.assertEqual(verified["manifest_sha256"], manifest["sha256"])
            with self.assertRaises(FileExistsError):
                manager.backup_snapshot(str(target))
            manager.close()

    def test_book_reader_opens_local_default_viewer_without_local_server(self):
        class FakeJobs:
            def action(self, *args, **kwargs):
                return 1

        class FakeTools:
            jobs = FakeJobs()

            def safe_path(self, raw, must_exist=False):
                return Path(raw)

        with tempfile.TemporaryDirectory(prefix="nimo-reader-test-", dir=nimo.PROJECT_ROOT) as temp_dir:
            pdf_path = Path(temp_dir) / "book.pdf"
            pdf_path.write_bytes(b"%PDF-test")
            with patch.object(nimo.webbrowser, "open", return_value=True) as open_file:
                result = nimo.BookReaderManager(FakeTools()).launch(str(pdf_path))
        open_file.assert_called_once_with(pdf_path.as_uri())
        self.assertTrue(result.startswith("file:"))
        self.assertFalse((pdf_path.parent / ".nimo_book_reader.html").exists())

    def test_install_and_launch_scripts_use_one_virtual_environment(self):
        root = nimo.PROJECT_ROOT
        for filename in ("START_NIMO_FINAL.cmd", "nimo.cmd", "NIMO_DOCTOR.cmd"):
            text = (root / filename).read_text(encoding="utf-8")
            self.assertIn("set \"NIMO_VENV=%NIMO_RUNTIME%\\venv\"", text)
            self.assertIn("%NIMO_VENV%\\Scripts\\python.exe", text)
            self.assertNotIn("C:\\Python314", text)
            self.assertNotIn("C:\\Nimo\\nimo_env", text)

    def test_windows_command_installer_preserves_and_deduplicates_user_path(self):
        original = r"C:\Tools;%LOCALAPPDATA%\NIMO\bin;C:\Other"
        merged, changed = windows_install.merge_user_path(original, r"%LOCALAPPDATA%\NIMO\bin")
        self.assertFalse(changed)
        self.assertEqual(merged, original)
        added, changed = windows_install.merge_user_path(r"C:\Tools", r"%LOCALAPPDATA%\NIMO\bin")
        self.assertTrue(changed)
        self.assertEqual(added, r"C:\Tools;%LOCALAPPDATA%\NIMO\bin")

    def test_windows_launcher_targets_user_runtime_and_forwards_arguments(self):
        launcher = windows_install.launcher_text()
        self.assertIn('set "NIMO_RUNTIME=%LOCALAPPDATA%\\NIMO"', launcher)
        self.assertIn('set "NIMO_APP=%NIMO_RUNTIME%\\app\\NIMO_TERMINAL_MASTER_4_0.py"', launcher)
        self.assertIn('set "NIMO_PYTHON=%NIMO_RUNTIME%\\venv\\Scripts\\python.exe"', launcher)
        self.assertIn('"%NIMO_PYTHON%" -B "%NIMO_APP%" %*', launcher)

    def test_ollama_server_helper_describes_two_terminal_flow(self):
        text = (nimo.PROJECT_ROOT / "NIMO_OLLAMA_SERVER.cmd").read_text(encoding="utf-8")
        self.assertIn("ollama serve", text)
        self.assertIn("Do not start a second server", text)
        self.assertIn("another Command Prompt and type: nimo", text)

    def test_model_manager_discovers_arbitrary_ollama_model_ids(self):
        manager = nimo.ModelManager()
        installed = {"community/model-x:latest", "qwen-test:small"}
        details = {
            "community/model-x:latest": {"size": 4_000_000_000, "capabilities": ["completion"]},
            "qwen-test:small": {"size": 1_000_000_000, "capabilities": ["chat"]},
        }
        manager.sync_discovered(installed, details)
        model_key = manager.key_for_model("community/model-x:latest", installed)
        self.assertTrue(model_key.startswith("ollama_"))
        manager.set_manual(model_key)
        self.assertEqual(manager.active_key(installed), model_key)
        self.assertEqual(manager.raw(model_key), "community/model-x:latest")
        self.assertEqual(manager.friendly(model_key), "community/model-x:latest")

    def test_selected_model_is_saved_as_an_exact_runtime_model_id(self):
        manager = nimo.ModelManager()
        installed = {"community/model-x:latest"}
        manager.sync_discovered(installed, {"community/model-x:latest": {"size": 1_000_000_000}})
        model_key = manager.key_for_model("community/model-x:latest", installed)
        manager.set_manual(model_key)

        class FakeConfig:
            data = {}

            def save(self):
                self.saved = True

        app = nimo.NIMOApplication.__new__(nimo.NIMOApplication)
        app.models = manager
        app.config = FakeConfig()
        app._persist_model_selection()
        self.assertEqual(app.config.data["model"], {"mode": "manual", "model_id": "community/model-x:latest"})
        self.assertTrue(app.config.saved)


if __name__ == "__main__":
    unittest.main()
