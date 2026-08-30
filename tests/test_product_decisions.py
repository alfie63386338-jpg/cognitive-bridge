"""Regression tests for the six approved Step 12 product decisions."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

from scripts._script_utils import frontmatter_scalar, split_frontmatter
from scripts.validate_statuses import ALLOWED_STATUSES


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
EXAMPLE = ROOT / "examples" / "example-output-vault" / "Cognitive-Bridge"
EVENT_RE = re.compile(
    r"(?ms)^## (?P<heading>cb-decision-[a-z0-9]+)\s*\n+"
    r"```yaml\s*\n(?P<body>.*?)^```\s*$"
)


def decision_events(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    events = []
    for match in EVENT_RE.finditer(text):
        fields = {}
        for line in match.group("body").splitlines():
            key, separator, value = line.partition(":")
            if separator:
                fields[key.strip()] = value.strip()
        fields["heading"] = match.group("heading")
        events.append(fields)
    return events


class ProductDecisionTests(unittest.TestCase):
    def test_priority_has_one_canonical_definition(self) -> None:
        canonical = (REFERENCES / "cognitive-integrity-rules.md").read_text(
            encoding="utf-8"
        )
        expected = (
            "1. User privacy & explicit scope",
            "2. Historical accuracy",
            "3. Ownership accuracy",
            "4. User meaning",
            "5. Epistemic accuracy",
            "6. Existing-data preservation",
            "7. Structural usefulness",
            "8. Completeness",
            "9. Graph aesthetics",
        )
        positions = [canonical.index(item) for item in expected]
        self.assertEqual(positions, sorted(positions))

        for path in (ROOT / "SKILL.md", REFERENCES / "universal-protocol.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("1. User privacy & explicit scope", text)
            self.assertIn("cognitive-integrity-rules.md", text)

    def test_status_values_are_type_scoped(self) -> None:
        self.assertEqual(
            ALLOWED_STATUSES,
            {
                "idea": {
                    "developing",
                    "reasoned",
                    "stable",
                    "core",
                    "dormant",
                    "superseded",
                    "rejected",
                },
                "concept": {"proposed", "developing", "stable", "deprecated"},
                "question": {"open", "refined", "dormant", "closed"},
                "seed": {"seed", "promoted", "dormant"},
                "discussion": {"developing", "reasoned", "revisited", "closed"},
                "moc": {"active", "dormant", "archived"},
            },
        )

    def test_ai_candidate_question_stays_in_review(self) -> None:
        template = (ROOT / "templates" / "candidate-question.md").read_text(
            encoding="utf-8"
        )
        case = (ROOT / "tests" / "cases" / "case-08-cross-domain-link.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("proposal_origin: inferred", template)
        self.assertIn("proposal_status: proposed", template)
        self.assertIn("Move this into `05_Questions/` only if", template)
        self.assertIn("do not place an AI-derived Candidate Question", case)

    def test_reconstructed_example_question_uses_unknown_origin(self) -> None:
        question = (
            EXAMPLE
            / "05_Questions"
            / "When does assistance strengthen rather than replace judgment.md"
        ).read_text(encoding="utf-8")
        frontmatter, _ = split_frontmatter(question)
        self.assertEqual(frontmatter_scalar(frontmatter, "origin"), "?")
        self.assertEqual(frontmatter_scalar(frontmatter, "evidence_level"), "E1")

    def test_example_does_not_invent_cross_conversation_discussion(self) -> None:
        removed = (
            EXAMPLE
            / "02_Discussions"
            / "What kind of help builds independence.md"
        )
        moc = (EXAMPLE / "01_MOC" / "MOC - Cognitive Bridge.md").read_text(
            encoding="utf-8"
        )
        self.assertFalse(removed.exists())
        self.assertNotIn("## Major Discussion", moc)

    def test_user_decisions_are_append_only_and_superseding(self) -> None:
        path = ROOT / "tests" / "product-fixtures" / "user-decisions-supersession.md"
        events = decision_events(path)
        self.assertEqual(len(events), 2)
        required = {
            "decision_id",
            "target_id",
            "decision",
            "decided_at",
            "supersedes",
            "heading",
        }
        for event in events:
            self.assertEqual(set(event), required)
            self.assertEqual(event["decision_id"], event["heading"])
        self.assertEqual(events[0]["supersedes"], "null")
        self.assertEqual(events[1]["supersedes"], events[0]["decision_id"])
        self.assertIn(events[0]["decision"], {"accepted", "rejected", "revised", "unresolved"})
        self.assertIn(events[1]["decision"], {"accepted", "rejected", "revised", "unresolved"})


if __name__ == "__main__":
    unittest.main()
