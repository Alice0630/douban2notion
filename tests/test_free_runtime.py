from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "douban2notion"
BLOCKED_HOSTS = (
    "wereadassets.malinkang.com",
    "i.malinkang.com",
    "notionhub.app",
    "heatmap.malinkang.com",
    "notion-icon.malinkang.com",
)


class FreeRuntimeTest(unittest.TestCase):
    def test_source_does_not_call_notionhub_services(self):
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SOURCE.rglob("*.py")
        )
        for host in BLOCKED_HOSTS:
            self.assertNotIn(host, source)

    def test_free_scope_is_movie_and_book(self):
        source = (SOURCE / "update_heatmap.py").read_text(encoding="utf-8")
        self.assertIn('{"movie", "book"}', source)

    def test_sync_workflows_do_not_run_heatmaps(self):
        workflows = ROOT / ".github" / "workflows"
        for workflow in workflows.glob("*.yml"):
            source = workflow.read_text(encoding="utf-8")
            self.assertNotIn("github_heatmap", source)
            self.assertNotIn('heatmap "', source)


if __name__ == "__main__":
    unittest.main()
