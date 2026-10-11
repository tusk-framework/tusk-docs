from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class GoldenPathDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_getting_started_uses_the_public_composer_skeleton(self) -> None:
        for relative_path in (
            "docs/index.md",
            "docs/getting-started/quickstart.md",
        ):
            with self.subTest(page=relative_path):
                page = self.read(relative_path)
                self.assertIn("composer create-project tusk-framework/app", page)
                for command in ("tusk doctor", "tusk start"):
                    self.assertIn(command, page)
                self.assertNotIn("tusk build", page)

    def test_architecture_assigns_http_and_workers_to_roadrunner(self) -> None:
        for relative_path in (
            "docs/guides/engine-integration.md",
            "docs/architecture/engine.md",
            "docs/architecture/overview.md",
            "docs/architecture/runtime.md",
            "docs/architecture/web.md",
            "docs/api/kernel.md",
        ):
            with self.subTest(page=relative_path):
                page = self.read(relative_path).lower()
                self.assertIn("roadrunner", page)
                self.assertIn("owns", page)
                self.assertIn("http", page)
                self.assertIn("worker", page)
                self.assertNotIn("ndjson", page)
                self.assertNotIn("engine owns http", page)
                self.assertNotIn("engine owns the php worker pool", page)

    def test_active_pages_do_not_claim_legacy_native_engine_or_scaffolding(self) -> None:
        active_pages = (
            "docs/index.md",
            "docs/getting-started/installation.md",
            "docs/getting-started/quickstart.md",
            "docs/getting-started/first-app.md",
            "docs/guides/cli-usage.md",
            "docs/guides/deployment.md",
            "docs/guides/engine-integration.md",
            "docs/architecture/engine.md",
            "docs/architecture/overview.md",
            "docs/architecture/runtime.md",
        )
        for relative_path in active_pages:
            with self.subTest(page=relative_path):
                page = self.read(relative_path).lower()
                self.assertNotIn("ndjson", page)
                self.assertNotIn("tusk init <name>", page)
                self.assertNotIn("native engine", page)
                self.assertNotIn("tusk build", page)
                self.assertNotIn("native http", page)

    def test_reference_pages_do_not_advertise_removed_runtime_apis(self) -> None:
        for relative_path in ("docs/architecture/web.md", "docs/api/kernel.md"):
            with self.subTest(page=relative_path):
                page = self.read(relative_path)
                for obsolete_api in (
                    "Tusk\\Web\\Server\\HttpServer",
                    "loadEnv(",
                    "onBoot(",
                    "addWorker(",
                    "NDJSON",
                ):
                    self.assertNotIn(obsolete_api, page)


if __name__ == "__main__":
    unittest.main()
