from collections import Counter
from pathlib import Path
import re
import unittest
from typing import Optional

from tools import validate


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def block_from_source(source: str, name: str, context: str = "source") -> str:
    match = re.search(
        rf"^\s*{re.escape(name)}\s*(?:\?=|=)\s*\{{",
        source,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"missing {name} in {context}")
    return validate.extract_braced(source, match.start())


def block(path: str, name: str) -> str:
    return block_from_source(text(path), name, path)


def nested_blocks(source: str, name: str) -> list[str]:
    return [
        validate.extract_braced(source, match.start())
        for match in re.finditer(
            rf"^\s*{re.escape(name)}\s*=\s*\{{", source, re.MULTILINE
        )
    ]


def shortest_block_containing(source: str, name: str, token: str) -> str:
    matches = [candidate for candidate in nested_blocks(source, name) if token in candidate]
    if not matches:
        raise AssertionError(f"missing {name} block containing {token}")
    return min(matches, key=len)


def simple_assignments(source: str) -> Counter[tuple[str, str]]:
    return Counter(
        re.findall(
            r"(?m)^\s*([A-Za-z0-9_.:-]+)\s*=\s*([A-Za-z0-9_.:-]+)\s*$",
            source,
        )
    )


def candidate_requirements(event: str, play: str, tag: str) -> Counter[tuple[str, str]]:
    branch_name = "if" if tag == "ABY" else "else_if"
    branch = shortest_block_containing(
        event,
        branch_name,
        f"target_country = c:{tag}",
    )
    limit = block_from_source(branch, "limit", f"{play}/{tag} selector")
    country = block_from_source(limit, f"c:{tag}", f"{play}/{tag} selector limit")
    return simple_assignments(country)


def selected_target(
    requirements: dict[str, Counter[tuple[str, str]]],
    facts: dict[str, set[tuple[str, str]]],
) -> Optional[str]:
    def qualifies(tag: str) -> bool:
        available = Counter(facts[tag])
        return all(
            available[requirement] >= count
            for requirement, count in requirements[tag].items()
        )

    if qualifies("ABY"):
        return "ABY"
    if qualifies("CAP"):
        return "CAP"
    return None


class VictoriaThree114RegressionFixTests(unittest.TestCase):
    def test_ora_zul_small_arms_duplicate_matcher_is_exact(self):
        effect = block(
            "common/scripted_effects/sb_firearms_effects.txt",
            "sb_create_ora_zul_firearms_treaty",
        )
        outer_if = block_from_source(effect, "if", "ORA-ZUL treaty effect")
        limit = block_from_source(outer_if, "limit", "ORA-ZUL treaty gate")
        ora = block_from_source(limit, "c:ORA", "ORA-ZUL treaty gate")
        zul = block_from_source(limit, "c:ZUL", "ORA-ZUL treaty gate")

        self.assertEqual(1, ora.count("is_country_alive = yes"))
        self.assertEqual(1, zul.count("is_country_alive = yes"))
        self.assertEqual(
            Counter({"ORA": 1, "ZUL": 1}),
            Counter(re.findall(r"(?m)^\s*c:([A-Z]{3})\s*\?=", limit)),
        )
        required_alive = {"ORA", "ZUL"}
        for alive, expected in (
            ({"ORA", "ZUL"}, True),
            ({"ORA"}, False),
            ({"ZUL"}, False),
            (set(), False),
        ):
            with self.subTest(alive=alive):
                self.assertEqual(expected, required_alive <= alive)

        treaty = block_from_source(ora, "any_scope_treaty", "ORA duplicate matcher")
        article = block_from_source(treaty, "any_scope_article", "ORA duplicate matcher")
        self.assertEqual(
            Counter(
                {
                    ("has_type", "goods_transfer"): 1,
                    ("source_country", "c:ORA"): 1,
                    ("target_country", "c:ZUL"): 1,
                    ("input_goods", "g:small_arms"): 1,
                }
            ),
            simple_assignments(article),
        )
        self.assertEqual(
            Counter({("binds", "c:ZUL"): 1}),
            simple_assignments(treaty) - simple_assignments(article),
        )

        required = set(simple_assignments(article))
        exact = {
            ("has_type", "goods_transfer"),
            ("source_country", "c:ORA"),
            ("target_country", "c:ZUL"),
            ("input_goods", "g:small_arms"),
        }
        cases = {
            "exact small-arms transfer": (exact, True),
            "different goods": (
                exact - {("input_goods", "g:small_arms")}
                | {("input_goods", "g:artillery")},
                False,
            ),
            "different article type": (
                exact - {("has_type", "goods_transfer")}
                | {("has_type", "ship_transfer")},
                False,
            ),
            "reversed direction": (
                exact
                - {("source_country", "c:ORA"), ("target_country", "c:ZUL")}
                | {("source_country", "c:ZUL"), ("target_country", "c:ORA")},
                False,
            ),
        }
        for label, (article_facts, expected) in cases.items():
            with self.subTest(label=label):
                self.assertEqual(expected, required <= article_facts)

        create = block_from_source(outer_if, "create_treaty", "ORA-ZUL treaty creation")
        created_article = block_from_source(
            create, "articles_to_create", "ORA-ZUL treaty creation"
        )
        self.assertIn("first_country = c:ORA", create)
        self.assertIn("second_country = c:ZUL", create)
        self.assertIn("article = goods_transfer", created_article)
        self.assertIn("source_country = c:ORA", created_article)
        self.assertIn("target_country = c:ZUL", created_article)
        inputs = block_from_source(created_article, "inputs", "ORA-ZUL treaty inputs")
        self.assertEqual(
            Counter({("goods", "g:small_arms"): 1, ("quantity", "10"): 1}),
            Counter(
                re.findall(
                    r"\b(goods|quantity)\s*=\s*([A-Za-z0-9_.:-]+)", inputs
                )
            ),
        )

    def test_frontier_target_selection_uses_the_exact_outer_candidate_predicate(self):
        path = "events/sb_frontier_ai_wars_events.txt"
        event_contracts = {
            "sb_frontier_ai_wars.100": (
                "dp_sb_xhosa_war_7",
                Counter(
                    {
                        ("sb_xhosa_frontier_war_target_is_launchable", "yes"): 1,
                        ("has_variable", "sb_xhosa_frontier_war_7_scheduled_var"): 1,
                        ("has_technology_researched", "colonization"): 1,
                    }
                ),
            ),
            "sb_frontier_ai_wars.110": (
                "dp_sb_xhosa_war_8",
                Counter(
                    {
                        ("sb_xhosa_frontier_war_target_is_launchable", "yes"): 1,
                        ("has_variable", "sb_xhosa_frontier_war_8_scheduled_var"): 1,
                        ("has_variable", "sb_xhosa_frontier_war_7_resolved_var"): 1,
                        ("has_technology_researched", "colonization"): 1,
                    }
                ),
            ),
            "sb_frontier_ai_wars.120": (
                "dp_sb_xhosa_war_9",
                Counter(
                    {
                        ("sb_xhosa_frontier_war_target_is_launchable", "yes"): 1,
                        ("has_variable", "sb_xhosa_frontier_war_9_scheduled_var"): 1,
                        ("has_variable", "sb_xhosa_frontier_war_8_resolved_var"): 1,
                        ("has_technology_researched", "colonization"): 1,
                    }
                ),
            ),
        }

        for event_id, (play, expected) in event_contracts.items():
            with self.subTest(event=event_id):
                event = block(path, event_id)
                immediate = block_from_source(event, "immediate", event_id)
                outer = nested_blocks(immediate, "if")[0]
                outer_limit = block_from_source(outer, "limit", f"{event_id} outer gate")
                outer_or = block_from_source(outer_limit, "OR", f"{event_id} outer gate")

                selector_requirements = {}
                for tag in ("ABY", "CAP"):
                    outer_country = block_from_source(
                        outer_or, f"c:{tag}", f"{event_id} outer candidate"
                    )
                    outer_requirements = simple_assignments(outer_country)
                    actual = candidate_requirements(event, play, tag)
                    self.assertEqual(expected, outer_requirements, f"{event_id}/{tag} outer")
                    self.assertEqual(expected, actual, f"{event_id}/{tag} selector")
                    selector_requirements[tag] = actual

                full = {tag: set(values) for tag, values in selector_requirements.items()}
                none = {"ABY": set(), "CAP": set()}
                matrix = {
                    "CAP only": ({"ABY": set(), "CAP": full["CAP"]}, "CAP"),
                    "ABY only": ({"ABY": full["ABY"], "CAP": set()}, "ABY"),
                    "both": (full, "ABY"),
                    "neither": (none, None),
                }
                for label, (facts, selected) in matrix.items():
                    with self.subTest(event=event_id, case=label):
                        self.assertEqual(
                            selected,
                            selected_target(selector_requirements, facts),
                        )

                for requirement in expected:
                    if requirement[0] not in {"has_variable", "has_technology_researched"}:
                        continue
                    sequence_matrix = {
                        "ABY missing": (
                            {
                                "ABY": full["ABY"] - {requirement},
                                "CAP": full["CAP"],
                            },
                            "CAP",
                        ),
                        "CAP missing": (
                            {
                                "ABY": full["ABY"],
                                "CAP": full["CAP"] - {requirement},
                            },
                            "ABY",
                        ),
                        "both missing": (
                            {
                                "ABY": full["ABY"] - {requirement},
                                "CAP": full["CAP"] - {requirement},
                            },
                            None,
                        ),
                    }
                    for label, (facts, selected) in sequence_matrix.items():
                        with self.subTest(
                            event=event_id,
                            missing=requirement,
                            case=label,
                        ):
                            self.assertEqual(
                                selected,
                                selected_target(selector_requirements, facts),
                            )


if __name__ == "__main__":
    unittest.main()
