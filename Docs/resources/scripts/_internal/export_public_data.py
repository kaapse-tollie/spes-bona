from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent
PUBLIC_ROOT = SCRIPTS_DIR.parent
MOD_ROOT = PUBLIC_ROOT.parents[2]
REPO = MOD_ROOT / "Spes Bona - A Southern Africa Flavour Pack"
INTERNAL_BUILDER = MOD_ROOT / "References/.codex-build/build_public_resources_workbook.py"
RAW_DIR = PUBLIC_ROOT / "data/raw"
DERIVED_DIR = PUBLIC_ROOT / "data/derived"
AUDIT_DIR = PUBLIC_ROOT / "audit"
OVERRIDES_CSV = AUDIT_DIR / "overrides.csv"


def load_internal_builder():
    spec = importlib.util.spec_from_file_location("internal_resource_builder", INTERNAL_BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def first_two_sources(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str]] = set()
    selected: list[dict[str, Any]] = []
    for row in sorted(
        rows,
        key=lambda item: (
            -(float(item["normalized_1950_numeric"]) if item.get("normalized_1950_numeric") is not None else 0.0),
            abs(int(item["year"]) - 1936),
        ),
    ):
        key = (str(row.get("source_title", "")), str(row.get("source_url", "")), str(row.get("locator", "")))
        if key in seen or not key[0]:
            continue
        seen.add(key)
        selected.append(row)
        if len(selected) == 2:
            break
    return selected


def override_problem_type(resource: str, reason: str) -> str:
    lower = reason.lower()
    if "undercount" in lower or "undershoot" in lower:
        return "undercounting"
    if "overstate" in lower or "overstates" in lower:
        return "overstatement"
    if "chronolog" in lower or "late" in lower:
        return "chronology"
    if resource == "Arable Land":
        return "weak target evidence"
    if "proxy" in lower:
        return "bad proxy fit"
    return "manual audit"


def build_override_rows(builder, target_rows, agri_avg_values, mining_avg_values, final_cap_values) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for info in builder.STATE_INFO:
        state = info["official_name"]
        for _category, resource in builder.NUMERIC_RESOURCES:
            override = builder.AUDITED_OVERRIDES.get((state, resource))
            if not override:
                continue
            if resource == "Arable Land":
                target_max = builder.python_target_max(target_rows, state, resource)
                average = agri_avg_values[state]["avg_units_per_cap"] if agri_avg_values[state]["status"] == "formula-driven" else None
                source_candidates = [
                    row for row in target_rows
                    if row["official_state"] == state and row["resource"] in builder.LAND_ECONOMY_RESOURCES
                ]
            else:
                group = builder.resource_group(resource)
                average = mining_avg_values.get(group, {}).get("avg_units_per_cap") if mining_avg_values.get(group, {}).get("status") == "formula-driven" else None
                if resource in {"Gold Fields (discovered)", "Oil (discovered)", "Rubber (discovered)"}:
                    maxima = [
                        row["normalized_1950_numeric"]
                        for row in target_rows
                        if row["official_state"] == state and row["resource_group"] == group and int(row["year"]) <= 1836
                    ]
                    target_max = max(maxima) if maxima else None
                else:
                    target_max = builder.python_target_max(target_rows, state, resource)
                source_candidates = [
                    row for row in target_rows
                    if row["official_state"] == state and row["resource_group"] == group
                ]
            raw_cap = (target_max / average) if (target_max is not None and average not in (None, 0)) else None
            sources = first_two_sources(source_candidates)
            rows.append(
                {
                    "override_key": f"{state}::{resource}",
                    "state": state,
                    "resource": resource,
                    "raw_calculated_cap": "" if raw_cap is None else round(raw_cap, 6),
                    "final_audited_cap": int(final_cap_values[state][resource]),
                    "override_reason": override["reason"],
                    "problem_type": override_problem_type(resource, override["reason"]),
                    "citation_1_title": sources[0]["source_title"] if len(sources) >= 1 else "",
                    "citation_1_url": sources[0]["source_url"] if len(sources) >= 1 else "",
                    "citation_1_locator": sources[0]["locator"] if len(sources) >= 1 else "",
                    "citation_2_title": sources[1]["source_title"] if len(sources) >= 2 else "",
                    "citation_2_url": sources[1]["source_url"] if len(sources) >= 2 else "",
                    "citation_2_locator": sources[1]["locator"] if len(sources) >= 2 else "",
                }
            )
    return rows


def main() -> None:
    builder = load_internal_builder()
    historical_rows, modern_rows = builder.load_raw_data()
    growth_anchor_series = builder.load_growth_anchor_series()
    agri_rankings = builder.parse_agricultural_rankings()
    vanilla_priors = builder.load_vanilla_priors()
    vanilla_text = builder.load_state_text(builder.VANILLA_STATE_DIR)
    growth_rows, growth_index_lookup = builder.build_growth_rows(growth_anchor_series)
    target_rows = builder.enrich_raw_rows(historical_rows + modern_rows, include_target=True, growth_index_lookup=growth_index_lookup)
    comparator_rows = builder.enrich_raw_rows(historical_rows + modern_rows, include_target=False, growth_index_lookup=growth_index_lookup)
    agri_avg_values = builder.python_agri_averages(agri_rankings, comparator_rows, vanilla_text)
    mining_avg_values = builder.python_mining_averages(vanilla_text, growth_index_lookup)
    live_values = builder.parse_live_state_resources()
    final_cap_values = builder.python_final_caps(live_values, target_rows, agri_avg_values, mining_avg_values)

    historical_fields = ["sheet", "geography", "resource", "year", "normalized_quantity", "normalized_unit", "source_title", "source_url", "citation_locator", "note"]
    modern_fields = ["sheet", "geography", "resource", "year", "normalized_quantity", "normalized_unit", "source_title", "source_url", "citation_locator", "note"]
    write_csv(RAW_DIR / "historical_anchors.csv", historical_rows, historical_fields)
    write_csv(RAW_DIR / "modern_maxima.csv", modern_rows, modern_fields)

    growth_anchor_rows: list[dict[str, Any]] = []
    for family, rows in growth_anchor_series.items():
        for row in rows:
            growth_anchor_rows.append(
                {
                    "family": family,
                    "year": row["year"],
                    "quantity": row["quantity"],
                    "unit": row["unit"],
                    "source_title": row["source_title"],
                    "source_url": row["source_url"],
                    "locator": row["locator"],
                }
            )
    write_csv(
        RAW_DIR / "growth_anchor_series.csv",
        growth_anchor_rows,
        ["family", "year", "quantity", "unit", "source_title", "source_url", "locator"],
    )

    rankings_rows = []
    for row in agri_rankings:
        rankings_rows.append(
            {
                "sheet_key": row["sheet_key"],
                "official_state": row["official_state"],
                "rank": row["rank"],
                "band": row["band"],
                "weight": row["weight"],
                "comparator": row["comparator"],
                "country": row["country"],
                "why": row["why"],
                "matched_raw_geography": row["matched_raw_geography"],
                "proxy_state_id": row["proxy_state_id"],
                "vanilla_proxy_arable_land": (
                    builder.parse_state_values_from_text(vanilla_text, row["proxy_state_id"]).get("Arable Land", "")
                    if row["proxy_state_id"]
                    else ""
                ),
            }
        )
    write_csv(
        RAW_DIR / "agri_rankings.csv",
        rankings_rows,
        ["sheet_key", "official_state", "rank", "band", "weight", "comparator", "country", "why", "matched_raw_geography", "proxy_state_id", "vanilla_proxy_arable_land"],
    )

    vanilla_rows = []
    for state, values in vanilla_priors.items():
        for resource, value in values.items():
            vanilla_rows.append({"state": state, "resource": resource, "value": value})
    write_csv(RAW_DIR / "vanilla_priors.csv", vanilla_rows, ["state", "resource", "value"])

    state_meta_rows = list(builder.STATE_INFO)
    write_csv(
        RAW_DIR / "state_metadata.csv",
        state_meta_rows,
        ["sheet_key", "state_id", "official_name", "vanilla_proxy_id", "vanilla_proxy_name"],
    )

    counterevidence_rows = []
    for row in builder.COUNTEREVIDENCE_CASES:
        counterevidence_rows.append(
            {
                "state": row["state"],
                "resource": row["resource"],
                "question": row["question"],
                "source_a_title": row["source_a_title"],
                "source_a_url": row["source_a_url"],
                "source_a_locator": row["source_a_locator"],
                "source_b_title": row["source_b_title"],
                "source_b_url": row["source_b_url"],
                "source_b_locator": row["source_b_locator"],
                "result": row["result"],
                "decision": row["decision"],
            }
        )
    write_csv(
        RAW_DIR / "counterevidence_cases.csv",
        counterevidence_rows,
        ["state", "resource", "question", "source_a_title", "source_a_url", "source_a_locator", "source_b_title", "source_b_url", "source_b_locator", "result", "decision"],
    )

    override_rows = build_override_rows(builder, target_rows, agri_avg_values, mining_avg_values, final_cap_values)
    write_csv(
        OVERRIDES_CSV,
        override_rows,
        ["override_key", "state", "resource", "raw_calculated_cap", "final_audited_cap", "override_reason", "problem_type", "citation_1_title", "citation_1_url", "citation_1_locator", "citation_2_title", "citation_2_url", "citation_2_locator"],
    )

    print(f"Wrote raw data snapshots to {RAW_DIR}")
    print(f"Wrote override ledger to {OVERRIDES_CSV}")


if __name__ == "__main__":
    main()
