from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
INTERNAL_DIR = SCRIPT_DIR / "_internal"


def load_module(module_name: str, filename: str):
    path = INTERNAL_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def cmd_build() -> None:
    builder = load_module("resources_builder", "build_resources_workbook.py")
    result = builder.build_public_workbook()
    print(f"Wrote {builder.OUTPUT}")
    print(f"Wrote derived tables to {builder.DERIVED_DIR}")
    print(f"Wrote audit summary to {builder.AUDIT_DIR}")
    print("Live state file sync is frozen during the audit pass; build does not rewrite 04_subsaharan_africa.txt.")
    print(f"Tracked {len(result['resource_adjustment_rows'])} state-resource result rows")


def cmd_sync_live() -> None:
    builder = load_module("resources_builder", "build_resources_workbook.py")
    tracker_rows = builder.load_state_pass_tracker_rows()
    incomplete_states = [
        row["state"]
        for row in tracker_rows
        if row["pass_status"] != builder.TRACKER_ACCEPTED
    ]
    if incomplete_states:
        print("Refusing live sync because the state audit loop is still in progress.")
        print("Remaining states: " + ", ".join(incomplete_states))
        raise SystemExit(1)
    pre_sync_live = builder.parse_live_state_resources()
    result = builder.build_public_workbook()
    mismatch_count = 0
    for state, resources in result["final_caps"].items():
        for resource, audited_cap in resources.items():
            if pre_sync_live[state].get(resource, 0) != audited_cap:
                mismatch_count += 1
    builder.sync_live_state_file(result["final_caps"], result["arable_resource_expectation_rows"])
    synced_result = builder.build_public_workbook()
    print(f"Synced {builder.STATE_FILE}")
    print(f"Applied {mismatch_count} live cap updates from the audited result")
    print(f"Rebuilt {builder.OUTPUT}")
    print(f"Rebuilt derived tables to {builder.DERIVED_DIR}")
    print(f"Rebuilt audit summary to {builder.AUDIT_DIR}")
    print(f"Tracked {len(synced_result['resource_adjustment_rows'])} state-resource result rows")


def cmd_test() -> None:
    tester = load_module("resources_tester", "test_resources_pipeline.py")
    report = tester.run_tests()
    print(report)


def report_has_failures(report: str) -> bool:
    return "- Fails: 0" not in report


def cmd_state_pass() -> None:
    builder = load_module("resources_builder", "build_resources_workbook.py")
    tester = load_module("resources_tester", "test_resources_pipeline.py")

    tracker_rows = builder.load_state_pass_tracker_rows()
    state = builder.select_next_state_for_pass(tracker_rows)
    if state is None:
        print("No unfinished or rerun-required state passes remain.")
        print("CURRENT_STATE=NONE")
        print("STATE_PASS_COMPLETE=yes")
        print("LOOP_COMPLETE=yes")
        print("NEXT_STATE=NONE")
        print("FAMILY_REWRITE=no")
        return

    pass_index = builder.next_state_pass_index(tracker_rows)
    for row in tracker_rows:
        if row["state"] != state:
            continue
        row["pass_status"] = builder.TRACKER_IN_REVIEW
        row["live_synced"] = "no"
        row["summary_note"] = f"{state} pass {pass_index} is in review."
    builder.write_state_pass_tracker_rows(tracker_rows)

    result = builder.build_public_workbook()
    report = tester.run_tests()
    if report_has_failures(report):
        print(f"Selected {state} for pass {pass_index}, but the in-review build/test cycle failed.")
        print(f"CURRENT_STATE={state}")
        print("STATE_PASS_COMPLETE=no")
        print("LOOP_COMPLETE=no")
        print(f"NEXT_STATE={state}")
        print("FAMILY_REWRITE=no")
        print(report)
        raise SystemExit(1)

    state_audit_rows = [
        row
        for row in result["counterfactual_audit_rows"]
        if row["state"] == state
    ]
    changed_rows = sum(1 for row in state_audit_rows if row["decision"] != "keep")
    family_rewrite_rows = [
        row
        for row in result["family_rewrite_rows"]
        if row.get("trigger_state") == state or state in str(row.get("affected_states", "")).split(";")
    ]

    for row in tracker_rows:
        if row["state"] != state:
            continue
        row["pass_status"] = builder.TRACKER_ACCEPTED
        row["completed_rows"] = len(state_audit_rows)
        row["changed_rows"] = changed_rows
        row["family_rewrites_triggered"] = len(family_rewrite_rows)
        row["live_synced"] = "no"
        row["last_completed_pass_index"] = pass_index
        row["summary_note"] = (
            f"Accepted on pass {pass_index}; {changed_rows} of {len(state_audit_rows)} public rows differ from the vanilla baseline. "
            "Live sync remains frozen during the audit loop."
        )
    builder.write_state_pass_tracker_rows(tracker_rows)

    accepted_result = builder.build_public_workbook()
    accepted_report = tester.run_tests()
    if report_has_failures(accepted_report):
        for row in tracker_rows:
            if row["state"] != state:
                continue
            row["pass_status"] = builder.TRACKER_IN_REVIEW
            row["completed_rows"] = 0
            row["changed_rows"] = 0
            row["family_rewrites_triggered"] = 0
            row["live_synced"] = "no"
            row["last_completed_pass_index"] = ""
            row["summary_note"] = (
                f"{state} pass {pass_index} remains in review because the post-accept rebuild/test cycle failed."
            )
        builder.write_state_pass_tracker_rows(tracker_rows)
        builder.build_public_workbook()
        tester.run_tests()
        print(f"{state} passed the in-review build/test run but failed after the acceptance rebuild on pass {pass_index}.")
        print(f"CURRENT_STATE={state}")
        print("STATE_PASS_COMPLETE=no")
        print("LOOP_COMPLETE=no")
        print(f"NEXT_STATE={state}")
        print(f"FAMILY_REWRITE={'yes' if family_rewrite_rows else 'no'}")
        print(accepted_report)
        raise SystemExit(1)

    refreshed_tracker_rows = builder.load_state_pass_tracker_rows()
    next_state = builder.select_next_state_for_pass(refreshed_tracker_rows)
    loop_complete = next_state is None

    print(f"Finished {state} state pass {pass_index}.")
    print("Live state file sync remains frozen during the audit loop.")
    print(f"Tracked {len(accepted_result['counterfactual_audit_rows'])} public state-resource audit rows")
    print(f"CURRENT_STATE={state}")
    print("STATE_PASS_COMPLETE=yes")
    print(f"LOOP_COMPLETE={'yes' if loop_complete else 'no'}")
    print(f"NEXT_STATE={next_state if next_state is not None else 'NONE'}")
    print(f"FAMILY_REWRITE={'yes' if family_rewrite_rows else 'no'}")
    print(accepted_report)


def cmd_refresh_public_data() -> None:
    exporter = load_module("resources_exporter", "export_public_data.py")
    exporter.main()


def cmd_refresh_comparators() -> None:
    puller = load_module("resources_comparators", "pull_official_comparator_data.py")
    puller.main()


def cmd_refresh_growth() -> None:
    growth = load_module("resources_growth", "pull_growth_series.py")
    growth.main()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Public resource audit pipeline entrypoint for Spes Bona."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build", help="Rebuild Docs/resources/RESOURCES.xlsx and the derived tables.")
    subparsers.add_parser(
        "state-pass",
        help="Run exactly one state audit pass: rebuild, test, update the tracker, rebuild, retest, and stop without live sync.",
    )
    subparsers.add_parser("sync-live", help="Sync audited caps into the live SB state file, then rebuild outputs.")
    subparsers.add_parser("test", help="Run the public audit tests and rewrite the test report.")
    subparsers.add_parser(
        "refresh-public-data",
        help="Freeze raw public snapshots from the maintainer-side research pipeline.",
    )
    subparsers.add_parser(
        "refresh-comparators",
        help="Refresh comparator-series inputs only.",
    )
    subparsers.add_parser(
        "refresh-growth",
        help="Refresh growth-series inputs only.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "build":
        cmd_build()
    elif args.command == "state-pass":
        cmd_state_pass()
    elif args.command == "sync-live":
        cmd_sync_live()
    elif args.command == "test":
        cmd_test()
    elif args.command == "refresh-public-data":
        cmd_refresh_public_data()
    elif args.command == "refresh-comparators":
        cmd_refresh_comparators()
    elif args.command == "refresh-growth":
        cmd_refresh_growth()


if __name__ == "__main__":
    main()
