from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from scripts.validate_yaml import validate_file


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
EXAMPLE_VAULT = ROOT / "examples" / "example-output-vault" / "Cognitive-Bridge"
IF_BLOCK = re.compile(r"{{#if ([a-z_]+)}}\n?(.*?){{/if}}\n?", re.DOTALL)


def render(template: str, values: dict[str, str]) -> str:
    rendered = IF_BLOCK.sub(
        lambda match: match.group(2) if values.get(match.group(1)) else "",
        template,
    )
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


class TemplateTests(unittest.TestCase):
    def test_unknown_origin_renders_as_valid_yaml(self) -> None:
        common = {
            "cb_id": "cb-idea-template01",
            "status": "stable",
            "origin": "?",
            "created": "2026-08-29",
            "updated": "2026-08-29",
            "title": "Unknown origin remains explicit",
        }
        rendered = render((TEMPLATES / "idea.md").read_text(encoding="utf-8"), common)

        self.assertIn('origin: "?"', rendered)
        self.assertNotIn("{{", rendered)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "idea.md"
            path.write_text(rendered, encoding="utf-8")
            self.assertEqual(validate_file(path), [])

    def test_main_moc_separates_confirmed_and_proposed_connections(self) -> None:
        template = (TEMPLATES / "moc.md").read_text(encoding="utf-8")

        for heading in (
            "## Start Here",
            "## Important / Recent Evolution",
            "## Confirmed Connections",
            "## Proposed Connections",
            "## Review Needed",
            "## Source Coverage",
        ):
            self.assertIn(heading, template)

    def test_example_system_created_concept_remains_proposed(self) -> None:
        concept = (
            EXAMPLE_VAULT / "04_Concepts" / "Independent capability.md"
        ).read_text(encoding="utf-8")
        moc = (EXAMPLE_VAULT / "01_MOC" / "MOC - Cognitive Bridge.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("status: proposed", concept)
        self.assertIn("term_status: project-defined", concept)
        self.assertIn("## Proposed Concepts", moc)
        self.assertNotIn("## Key Concepts", moc)


if __name__ == "__main__":
    unittest.main()
