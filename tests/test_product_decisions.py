"""Regression tests for approved Step 12 and Step 15.6 product decisions."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts._script_utils import frontmatter_scalar, split_frontmatter
from scripts.validate_statuses import ALLOWED_STATUSES


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
EXAMPLE = ROOT / "examples" / "example-output-vault" / "Cognitive-Bridge"
AI_CONCEPT_MATRIX = json.loads(
    (ROOT / "tests" / "product-fixtures" / "ai-originated-proposed-concepts.json").read_text(
        encoding="utf-8"
    )
)
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
    def ai_concept_scenario(self, name: str) -> dict[str, object]:
        return AI_CONCEPT_MATRIX["scenarios"][name]

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

    def test_ai_originated_reusable_concept_defaults_to_proposed_unconfirmed(self) -> None:
        expected = {
            "type": "concept",
            "status": "proposed",
            "origin": "A0",
            "adoption": "unconfirmed",
        }
        self.assertEqual(AI_CONCEPT_MATRIX["canonical_default"], expected)
        scenario = self.ai_concept_scenario("ai_named_no_uptake")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "status": "proposed",
                "origin": "A0",
                "adoption": "unconfirmed",
                "evidence_level": "E3",
            },
        )

    def test_passive_agreement_does_not_establish_considering(self) -> None:
        scenario = self.ai_concept_scenario("passive_agreement")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "status": "proposed",
                "origin": "A0",
                "adoption": "unconfirmed",
                "evidence_level": "E3",
                "considering_allowed": False,
            },
        )

    def test_active_participation_can_establish_considering(self) -> None:
        scenario = self.ai_concept_scenario("active_user_exploration")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "origin": "A→U",
                "adoption": "considering",
                "evidence_level": "E3",
                "ai_first_history_preserved": True,
                "maximum_automatic_adoption": "considering",
            },
        )

    def test_later_reuse_preserves_ai_origin_history(self) -> None:
        scenario = self.ai_concept_scenario("later_active_reuse")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "origin": "A→U",
                "adoption": "integrated",
                "evidence_level": "E3",
                "historical_introducer": "AI",
                "minimum_supported_adoption": "considering",
                "higher_adoption_allowed_under_existing_model": True,
                "preserve_cb_id": True,
            },
        )

    def test_e3_ai_origin_evidence_does_not_imply_adoption(self) -> None:
        scenario = self.ai_concept_scenario("direct_ai_origin")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "status": "proposed",
                "origin": "A0",
                "adoption": "unconfirmed",
                "evidence_level": "E3",
                "evidence_supports": "historical occurrence and AI-origin attribution",
            },
        )
        self.assertNotIn("user adoption", scenario["evidence_supports"])

    def test_reconstructed_ai_origin_is_not_e3(self) -> None:
        scenario = self.ai_concept_scenario("source_ai_reconstruction")
        self.assertEqual(
            scenario,
            {
                "create_concept": True,
                "type": "concept",
                "status": "proposed",
                "origin": "A0",
                "adoption": "unconfirmed",
                "evidence_level": "E1",
                "direct_record": False,
            },
        )
        self.assertNotEqual(scenario["evidence_level"], "E3")

    def test_decorative_ai_labels_do_not_become_concepts(self) -> None:
        scenario = self.ai_concept_scenario("decorative_label")
        self.assertEqual(scenario, {"create_concept": False})

    def test_prior_generated_concept_is_not_new_adoption_evidence(self) -> None:
        scenario = self.ai_concept_scenario("feedback_contamination")
        self.assertEqual(
            scenario,
            {
                "create_concept": False,
                "type": "concept",
                "status": "proposed",
                "run_1_origin": "A0",
                "run_1_adoption": "unconfirmed",
                "run_1_evidence_level": "E3",
                "new_user_uptake_evidence": False,
                "run_2_origin": "A0",
                "run_2_adoption": "unconfirmed",
                "run_2_evidence_level": "E3",
                "preserve_cb_id": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
