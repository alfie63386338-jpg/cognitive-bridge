"""Focused stdlib regression tests for the deterministic engineering scripts."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT / "scripts"
READ_ONLY_SCRIPTS = (
    "validate_yaml.py",
    "check_cb_ids.py",
    "validate_statuses.py",
    "check_wikilinks.py",
    "detect_duplicates.py",
    "detect_file_conflicts.py",
    "detect_orphans.py",
)


def run_script(name: str, *args: object, no_site: bool = False):
    command = [sys.executable, "-B"]
    if no_site:
        command.append("-S")
    command.extend([str(SCRIPTS / name), *(str(arg) for arg in args)])
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        check=False,
    )


def write_note(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def idea_note(cb_id: str = "cb-idea-test0001", body: str = "# Test\n") -> str:
    return (
        "---\n"
        f"cb_id: {cb_id}\n"
        "type: idea\n"
        "status: stable\n"
        "---\n\n"
        f"{body}"
    )


class EngineeringScriptTests(unittest.TestCase):
    def test_missing_roots_fail_without_creating_them(self):
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing vault"
            for script in READ_ONLY_SCRIPTS:
                with self.subTest(script=script):
                    result = run_script(script, missing, "--json")
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("does not exist", result.stderr)
                    self.assertFalse(missing.exists())
            result = run_script("build_qa_report.py", missing)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(missing.exists())

    def test_source_registry_preserves_source_and_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "Source with spaces 中文"
            write_note(source / "材料 → alpha.md", "fictional source\n")

            inside = source / "Source Registry.md"
            result = run_script("build_source_registry.py", source, inside)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside", result.stderr)
            self.assertFalse(inside.exists())

            output = root / "Registry → output.md"
            output.write_text("human sentinel", encoding="utf-8")
            result = run_script("build_source_registry.py", source, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "human sentinel")

            result = run_script("build_source_registry.py", source, output, "--force")
            self.assertEqual(result.returncode, 0, result.stderr)
            registry = output.read_text(encoding="utf-8")
            self.assertIn("材料 → alpha.md", registry)
            self.assertIn("Hashes support duplicate-ingestion detection", registry)

    def test_qa_report_requires_explicit_overwrite_and_handles_unicode(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "Vault with spaces 中文"
            write_note(root / "03_Ideas" / "想法 → alpha.md", idea_note())
            output = Path(temporary) / "QA → report.md"
            output.write_text("human sentinel", encoding="utf-8")

            result = run_script("build_qa_report.py", root, "--output", output)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "human sentinel")

            result = run_script(
                "build_qa_report.py", root, "--output", output, "--force"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("**Technical status:** PASS", report)
            self.assertIn("想法 → alpha.md", report)

    def test_portable_filename_collisions_are_detected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(root / "a" / "Alpha.md", "one")
            write_note(root / "b" / "alpha.MD", "two")
            write_note(root / "c" / "Café.md", "three")
            write_note(root / "d" / "Cafe\N{COMBINING ACUTE ACCENT}.md", "four")

            result = run_script("detect_file_conflicts.py", root, "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(len(payload["conflicts"]), 2)

            result = run_script("detect_duplicates.py", root, "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            filename_findings = [
                finding
                for finding in payload["findings"]
                if finding["kind"] == "duplicate_filename_stem"
            ]
            self.assertEqual(len(filename_findings), 2)

    def test_orphans_respect_qualified_links_and_ignore_self_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(root / "FolderA" / "Same.md", idea_note("cb-idea-alpha001"))
            write_note(
                root / "FolderB" / "Same.md",
                idea_note("cb-idea-beta0001", "# Other\n[[Same]]\n"),
            )
            write_note(root / "Index.md", "[[FolderA/Same]]\n")

            result = run_script("detect_orphans.py", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["orphans"], ["FolderB/Same.md"])

    def test_cb_id_scan_is_frontmatter_scoped_and_folder_aware(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(root / "00_System" / "Plain.md", "type: idea\ncb_id: body-only\n")
            write_note(root / "03_Ideas" / "Missing.md", "---\ntype: idea\n---\n")

            result = run_script("check_cb_ids.py", root, "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(
                payload["issues"],
                [{"file": "03_Ideas/Missing.md", "issue": "missing cb_id"}],
            )

    def test_status_validation_is_type_scoped(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(
                root / "05_Questions" / "Open.md",
                "---\ncb_id: cb-question-open001\ntype: question\nstatus: open\n---\n",
            )
            write_note(
                root / "05_Questions" / "Wrong.md",
                "---\ncb_id: cb-question-wrong01\ntype: question\nstatus: stable\n---\n",
            )
            write_note(
                root / "03_Ideas" / "Stable.md",
                idea_note("cb-idea-status001"),
            )

            result = run_script("validate_statuses.py", root, "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(len(payload["issues"]), 1)
            self.assertEqual(payload["issues"][0]["file"], "05_Questions/Wrong.md")
            self.assertIn("invalid status for type question: stable", payload["issues"][0]["issue"])

    def test_basic_yaml_validation_rejects_reserved_and_duplicate_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(
                root / "bad.md",
                "---\ntype: idea\ntype: seed\norigin: ?\nbroken: value: extra\n---\n",
            )
            bom = root / "bom.md"
            bom.write_text("---\ntype: idea\n---\n", encoding="utf-8-sig")

            result = run_script("validate_yaml.py", root, "--json", no_site=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            payload = json.loads(result.stdout)
            issues = "\n".join(item["issue"] for item in payload["issues"])
            self.assertIn("duplicate top-level key: type", issues)
            self.assertIn("reserved YAML indicator must be quoted: ?", issues)
            self.assertIn("unquoted scalar contains a mapping indicator", issues)
            self.assertNotIn("bom.md", "\n".join(item["file"] for item in payload["issues"]))

    def test_wikilinks_ignore_fenced_code_and_html_comments(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_note(root / "Target.md", "# Target\n")
            write_note(
                root / "CodeOnly.md",
                idea_note("cb-idea-codeonly1", "# Code only target\n"),
            )
            write_note(
                root / "Index.md",
                "[[Target]]\n\n```text\n[[Missing in code]]\n[[CodeOnly]]\n```\n\n"
                "<!-- [[Missing in comment]] -->\n",
            )

            result = run_script("check_wikilinks.py", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["missing"], [])

            result = run_script("detect_orphans.py", root, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["orphans"], ["CodeOnly.md"])

    def test_invalid_utf8_is_reported_as_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bad = root / "broken.md"
            bad.write_bytes(b"\xff\xfe\x00")
            for script in (
                "validate_yaml.py",
                "check_cb_ids.py",
                "check_wikilinks.py",
                "detect_duplicates.py",
                "detect_orphans.py",
            ):
                with self.subTest(script=script):
                    result = run_script(script, root, "--json")
                    self.assertNotEqual(result.returncode, 0)
                    payload = json.loads(result.stdout)
                    self.assertFalse(payload["ok"])
                    self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
