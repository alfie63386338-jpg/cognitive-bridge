"""Regression tests for truthful build provenance and persistent privacy."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.build_execution_fingerprint import build_provenance
from scripts.build_qa_report import run as run_qa_helper


PROJECT = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT / "scripts"
MANIFEST = PROJECT / "references" / "build-provenance-manifest.json"
SOURCE_HASH = "sha256:" + "1" * 64
OTHER_HASH = "sha256:" + "2" * 64
WRITTEN_ENTRY_ARGS = (
    "--source-id",
    "cb-source-test",
    "--created-summary",
    "1 idea",
    "--updated-summary",
    "none",
    "--skipped-summary",
    "none",
    "--conflicts-summary",
    "none",
    "--review-items-summary",
    "1 candidate question",
)


def run_script(name: str, *args: object):
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPTS / name), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=environment,
        check=False,
    )


class BuildProvenanceTests(unittest.TestCase):
    def test_fingerprint_is_deterministic_and_truthfully_scoped(self):
        common = (
            "--execution-mode",
            "first_build",
            "--source-intake-mode",
            "pasted_text",
            "--source-hash",
            SOURCE_HASH,
        )
        first = run_script("build_execution_fingerprint.py", *common)
        second = run_script("build_execution_fingerprint.py", *common)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        one = json.loads(first.stdout)
        two = json.loads(second.stdout)
        self.assertEqual(one["execution_fingerprint"], two["execution_fingerprint"])
        self.assertEqual(one["cognitive_bridge_version"], "0.2.0-beta.1")
        self.assertEqual(one["protocol_version"], "1")
        self.assertEqual(one["schema_version"], "1.1")
        self.assertEqual(one["execution_mode"], "first_build")
        self.assertEqual(one["source_intake_mode"], "pasted_text")
        self.assertRegex(one["execution_fingerprint"], r"^sha256:[0-9a-f]{64}$")
        serialized = json.dumps(one).casefold()
        self.assertNotIn("runtime_skill_loaded", serialized)
        self.assertNotIn("skill_path", serialized)
        for unsupported in (
            "native loader confirmed",
            "runtime skill loaded",
            "codex verified installation",
            "plugin invocation confirmed",
        ):
            self.assertNotIn(unsupported, serialized)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            set(manifest["canonical_rule_files"]),
            {
                "SKILL.md",
                "references/cognitive-integrity-rules.md",
                "references/universal-protocol.md",
                "references/cognitive-knowledge-model.md",
                "references/ownership-evolution-model.md",
                "references/latent-connection-model.md",
                "references/obsidian-output-protocol.md",
                "references/terminology.md",
            },
        )

    def test_manifest_rejects_empty_or_duplicate_canonical_rules(self):
        base = {
            "cognitive_bridge_version": "0.2.0-beta.1",
            "protocol_version": "1",
            "schema_version": "1.1",
            "fingerprint_format": "cb-execution-fingerprint-v1",
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            references = root / "references"
            references.mkdir()
            (root / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
            manifest_path = references / "build-provenance-manifest.json"
            for canonical in ([], ["SKILL.md", "SKILL.md"]):
                with self.subTest(canonical=canonical):
                    manifest_path.write_text(
                        json.dumps({**base, "canonical_rule_files": canonical}),
                        encoding="utf-8",
                    )
                    with self.assertRaises(ValueError):
                        build_provenance(
                            manifest_path,
                            execution_mode="first_build",
                            source_intake_mode="pasted_text",
                            source_hashes=[SOURCE_HASH],
                        )

    def test_fingerprint_changes_for_declared_semantic_inputs_only(self):
        base = build_provenance(
            MANIFEST,
            execution_mode="first_build",
            source_intake_mode="pasted_text",
            source_hashes=[SOURCE_HASH, OTHER_HASH],
        )
        reordered = build_provenance(
            MANIFEST,
            execution_mode="first_build",
            source_intake_mode="pasted_text",
            source_hashes=[OTHER_HASH, SOURCE_HASH],
        )
        changed_mode = build_provenance(
            MANIFEST,
            execution_mode="update_build",
            source_intake_mode="pasted_text",
            source_hashes=[SOURCE_HASH, OTHER_HASH],
        )
        changed_source = build_provenance(
            MANIFEST,
            execution_mode="first_build",
            source_intake_mode="pasted_text",
            source_hashes=[SOURCE_HASH],
        )
        self.assertEqual(
            base["execution_fingerprint"], reordered["execution_fingerprint"]
        )
        self.assertNotEqual(
            base["execution_fingerprint"], changed_mode["execution_fingerprint"]
        )
        self.assertNotEqual(
            base["execution_fingerprint"], changed_source["execution_fingerprint"]
        )

    def test_rule_line_endings_normalize_but_rule_changes_do_not(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "references").mkdir()
            for relative in manifest["canonical_rule_files"]:
                source = PROJECT / relative
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            local_manifest = root / "references" / "build-provenance-manifest.json"
            local_manifest.write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
            )
            before = build_provenance(
                local_manifest,
                execution_mode="first_build",
                source_intake_mode="single_markdown",
                source_hashes=[SOURCE_HASH],
            )
            rule = root / "references" / "terminology.md"
            text = rule.read_text(encoding="utf-8")
            rule.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
            line_ending_only = build_provenance(
                local_manifest,
                execution_mode="first_build",
                source_intake_mode="single_markdown",
                source_hashes=[SOURCE_HASH],
            )
            self.assertEqual(before["ruleset_hash"], line_ending_only["ruleset_hash"])
            rule.write_text(text + "\nMaterial rule change.\n", encoding="utf-8")
            changed = build_provenance(
                local_manifest,
                execution_mode="first_build",
                source_intake_mode="single_markdown",
                source_hashes=[SOURCE_HASH],
            )
            self.assertNotEqual(before["ruleset_hash"], changed["ruleset_hash"])

    def test_build_log_contains_metadata_but_no_physical_path_or_attestation(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "Build Log.md"
            result = run_script(
                "build_execution_fingerprint.py",
                "--execution-mode",
                "first_build",
                "--source-intake-mode",
                "pasted_text",
                "--source-hash",
                SOURCE_HASH,
                "--build-id",
                "cb-build-test",
                "--processed-at",
                "2026-09-01T00:00:00+08:00",
                *WRITTEN_ENTRY_ARGS,
                "--output",
                output,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            for field in (
                "cognitive_bridge_version:",
                "protocol_version:",
                "schema_version:",
                "execution_mode:",
                "source_intake_mode:",
                "execution_fingerprint:",
            ):
                self.assertIn(field, text)
            self.assertIn("does not authenticate", text)
            self.assertNotIn(str(PROJECT), text)
            self.assertNotIn("runtime_skill_loaded", text)

    def test_v02_entry_appends_without_rewriting_a_legacy_build_log(self):
        with tempfile.TemporaryDirectory() as temporary:
            log = Path(temporary) / "Build Log.md"
            legacy = (
                b"# Build Log\r\n\r\n## legacy\r\n\r\n"
                b"- human entry\r\n"
                b"- source path: C:\\Users\\RealName\\Private\\source.md\r\n"
            )
            log.write_bytes(legacy)
            result = run_script(
                "build_execution_fingerprint.py",
                "--execution-mode",
                "update_build",
                "--source-intake-mode",
                "single_markdown",
                "--source-hash",
                SOURCE_HASH,
                "--build-id",
                "cb-build-v02",
                "--processed-at",
                "2026-09-01T00:00:00+08:00",
                *WRITTEN_ENTRY_ARGS,
                "--append-to",
                log,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = log.read_bytes()
            self.assertTrue(updated.startswith(legacy))
            self.assertIn(b"## cb-build-v02", updated)
            self.assertIn(b'execution_mode: "update_build"', updated)
            privacy = run_script(
                "check_persistent_metadata.py", Path(temporary), "--json"
            )
            self.assertEqual(privacy.returncode, 0, privacy.stdout)
            payload = json.loads(privacy.stdout)
            self.assertEqual(payload["issues"], [])
            self.assertEqual(
                payload["warnings"][0]["kind"], "legacy_absolute_path_warning"
            )
            self.assertNotIn("RealName", privacy.stdout)

    def test_written_metadata_rejects_heading_and_path_injection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bad_heading = run_script(
                "build_execution_fingerprint.py",
                "--execution-mode",
                "first_build",
                "--source-intake-mode",
                "pasted_text",
                "--source-hash",
                SOURCE_HASH,
                "--build-id",
                "cb-build-ok\nruntime_skill_loaded: true",
                "--processed-at",
                "2026-09-01T00:00:00+08:00",
                *WRITTEN_ENTRY_ARGS,
                "--output",
                root / "heading.md",
            )
            self.assertNotEqual(bad_heading.returncode, 0)
            self.assertFalse((root / "heading.md").exists())

            bad_outcomes = list(WRITTEN_ENTRY_ARGS)
            index = bad_outcomes.index("--created-summary") + 1
            bad_outcomes[index] = r"C:\Users\RealName\Private\node.md"
            bad_path = run_script(
                "build_execution_fingerprint.py",
                "--execution-mode",
                "first_build",
                "--source-intake-mode",
                "pasted_text",
                "--source-hash",
                SOURCE_HASH,
                "--build-id",
                "cb-build-safe",
                "--processed-at",
                "2026-09-01T00:00:00+08:00",
                *bad_outcomes,
                "--output",
                root / "path.md",
            )
            self.assertNotEqual(bad_path.returncode, 0)
            self.assertFalse((root / "path.md").exists())

            bad_outcomes[index] = "/private/var/alice/source.md"
            bad_posix = run_script(
                "build_execution_fingerprint.py",
                "--execution-mode",
                "first_build",
                "--source-intake-mode",
                "pasted_text",
                "--source-hash",
                SOURCE_HASH,
                "--build-id",
                "cb-build-safe",
                "--processed-at",
                "2026-09-01T00:00:00+08:00",
                *bad_outcomes,
                "--output",
                root / "posix-path.md",
            )
            self.assertNotEqual(bad_posix.returncode, 0)
            self.assertFalse((root / "posix-path.md").exists())

    def test_qa_helper_hashes_raw_failure_streams_instead_of_persisting_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake = root / "helper.py"
            private_path = r"C:\Users\RealName\Private\Gemini\source.md"
            fake.write_text(
                "import sys\n"
                f"sys.stderr.write({private_path!r})\n"
                "print('not-json')\n"
                "raise SystemExit(1)\n",
                encoding="utf-8",
            )
            result = run_qa_helper(fake, root)
            serialized = json.dumps(result)
            self.assertEqual(result["error_kind"], "helper_failed_without_json")
            self.assertIn("stderr_sha256", result)
            self.assertNotIn("RealName", serialized)
            self.assertNotIn(private_path, serialized)
            self.assertNotIn("raw_stdout", result)
            self.assertNotIn("stderr", result)

    def test_qa_helper_redacts_paths_inside_valid_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake = root / "helper.py"
            private_path = r"C:\Users\RealName\Private\Gemini\source.md"
            fake.write_text(
                "import json\n"
                f"print(json.dumps({{'ok': False, 'errors': [{{'issue': {private_path!r}}}]}}))\n"
                "raise SystemExit(1)\n",
                encoding="utf-8",
            )
            result = run_qa_helper(fake, root)
            serialized = json.dumps(result)
            self.assertNotIn("RealName", serialized)
            self.assertNotIn(private_path, serialized)
            self.assertIn("redacted physical path", serialized)
            self.assertFalse(result["execution_ok"])

    def test_qa_helper_cannot_claim_success_with_a_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake = root / "validate_yaml.py"
            fake.write_text(
                "print('{\"ok\": true}')\nraise SystemExit(1)\n",
                encoding="utf-8",
            )
            result = run_qa_helper(fake, root)
            self.assertTrue(result["helper_reported_ok"])
            self.assertFalse(result["execution_ok"])
            self.assertFalse(result["ok"])
            self.assertEqual(result["returncode"], 1)

    def test_duplicate_candidates_are_advisory_but_helper_errors_are_not(self):
        helper = SCRIPTS / "detect_duplicates.py"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "a").mkdir()
            (root / "b").mkdir()
            (root / "a" / "Same.md").write_text("# One\n", encoding="utf-8")
            (root / "b" / "same.md").write_text("# Two\n", encoding="utf-8")
            advisory = run_qa_helper(helper, root)
            self.assertFalse(advisory["ok"])
            self.assertTrue(advisory["execution_ok"])
            self.assertEqual(advisory["returncode"], 1)

            (root / "broken.md").write_bytes(b"\xff\xfe")
            failed = run_qa_helper(helper, root)
            self.assertFalse(failed["ok"])
            self.assertFalse(failed["execution_ok"])
            self.assertEqual(failed["returncode"], 1)

    def test_persistent_metadata_check_covers_paths_and_runtime_claims(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            moc = root / "01_MOC" / "MOC - Cognitive Bridge.md"
            moc.parent.mkdir(parents=True)
            moc.write_text(
                "# Safe MOC\n\nhttps://example.invalid/reference\n",
                encoding="utf-8",
            )
            safe = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(safe.returncode, 0, safe.stderr)

            moc.write_text(
                "# Safe generated markup\n\n"
                "Source Artifact: <code>source.md</code>\n",
                encoding="utf-8",
            )
            html_safe = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(html_safe.returncode, 0, html_safe.stderr)

            moc.write_text(
                "# Unsafe MOC\n\nC:\\Users\\RealName\\Private\\Gemini\\source.md\n",
                encoding="utf-8",
            )
            path_result = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(path_result.returncode, 1)
            payload = json.loads(path_result.stdout)
            self.assertEqual(payload["issues"][0]["kind"], "absolute_path_candidate")
            self.assertNotIn("RealName", json.dumps(payload))

            moc.write_text(
                "# Unsafe POSIX path\n\n/opt/private/alice/source.md\n",
                encoding="utf-8",
            )
            posix_result = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(posix_result.returncode, 1)

            moc.write_text(
                "# Unsafe file URI\n\nfile:///private/alice/source.md\n",
                encoding="utf-8",
            )
            file_uri_result = run_script(
                "check_persistent_metadata.py", root, "--json"
            )
            self.assertEqual(file_uri_result.returncode, 1)

            for label, physical_path in (
                ("forward UNC", "//server/share/private/source.md"),
                ("rooted Windows", r"\Users\RealName\Private\source.md"),
                ("Unicode POSIX", "/用户/私人/来源.md"),
            ):
                with self.subTest(path=label):
                    moc.write_text(
                        f"# Unsafe {label}\n\n{physical_path}\n", encoding="utf-8"
                    )
                    result = run_script(
                        "check_persistent_metadata.py", root, "--json"
                    )
                    self.assertEqual(result.returncode, 1, result.stdout)

            moc.write_text(
                "# Forged body marker\n\n"
                "potentially_sensitive_metadata: true\n"
                "C:\\Users\\RealName\\Private\\Gemini\\source.md\n",
                encoding="utf-8",
            )
            forged = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(forged.returncode, 1)

            moc.write_text(
                "---\npotentially_sensitive_metadata: true\n---\n"
                "# Explicitly retained debug path\n\n"
                "C:\\Users\\RealName\\Private\\Gemini\\source.md\n",
                encoding="utf-8",
            )
            explicit = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(explicit.returncode, 0, explicit.stderr)

            log = root / "00_System" / "Build Log.md"
            log.parent.mkdir(parents=True)
            log.write_text("# Unsupported\n\nnative loader confirmed\n", encoding="utf-8")
            claim_result = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(claim_result.returncode, 1)
            payload = json.loads(claim_result.stdout)
            self.assertEqual(payload["issues"][0]["kind"], "unsupported_runtime_claim")

            runtime_variants = (
                "Codex native Skill loader confirmed",
                'runtime_skill_loaded: "true"',
                "native_loader_confirmed: true",
                "plugin_invocation_confirmed: true",
            )
            for value in runtime_variants:
                with self.subTest(runtime_claim=value):
                    log.write_text(f"# Unsupported\n\n{value}\n", encoding="utf-8")
                    result = run_script(
                        "check_persistent_metadata.py", root, "--json"
                    )
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertTrue(json.loads(result.stdout)["issues"])

            log.write_text(
                "# Truthful boundary\n\n"
                "runtime_skill_loaded: false\n\n"
                "The fingerprint does not authenticate a native loader.\n",
                encoding="utf-8",
            )
            negative = run_script("check_persistent_metadata.py", root, "--json")
            self.assertEqual(negative.returncode, 0, negative.stdout)


if __name__ == "__main__":
    unittest.main()
