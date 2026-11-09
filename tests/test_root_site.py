"""Verify branch-based Pages mirrors without overwriting research data."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_root_site import sync


class RootPublication(unittest.TestCase):
    def test_root_and_legacy_pages_share_the_same_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "site"
            source.mkdir()
            (source / "index.html").write_text("<h1>Infrathon</h1>")
            (source / "tasks.html").write_text("<h1>Tasks</h1>")
            (source / "assets").mkdir()
            (source / "assets/logo.svg").write_text("<svg/>")
            (root / "data").mkdir()
            research_data = root / "data/tasks.json"
            research_data.write_text("research data")
            sync(root)
            self.assertEqual((root / "index.html").read_text(), "<h1>Infrathon</h1>")
            self.assertEqual((root / "assets/logo.svg").read_bytes(),
                             (source / "assets/logo.svg").read_bytes())
            self.assertTrue((source / "tasks.html").is_file())
            self.assertEqual(research_data.read_text(), "research data")
            self.assertEqual(sync(root, check=True), [])

    def test_detect_changes_and_remove_only_previously_managed_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "site"
            source.mkdir()
            (source / "index.html").write_text("first homepage")
            old_page = source / "obsolete.html"
            old_page.write_text("old page")
            untouched = root / "README.md"
            untouched.write_text("keep me")
            sync(root)
            (source / "index.html").write_text("new homepage")
            old_page.unlink()
            self.assertTrue(sync(root, check=True))
            self.assertEqual((root / "index.html").read_text(), "first homepage")
            sync(root)
            self.assertEqual((root / "index.html").read_text(), "new homepage")
            self.assertFalse((root / "obsolete.html").exists())
            self.assertEqual(untouched.read_text(), "keep me")
            self.assertEqual(sync(root, check=True), [])


if __name__ == "__main__":
    unittest.main()
