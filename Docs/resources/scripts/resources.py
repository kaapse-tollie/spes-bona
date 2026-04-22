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
    pre_sync_live = builder.parse_live_state_resources()
    result = builder.build_public_workbook()
    mismatch_count = 0
    for state, resources in result["final_caps"].items():
        for resource, audited_cap in resources.items():
            if pre_sync_live[state].get(resource, 0) != audited_cap:
                mismatch_count += 1
    builder.sync_live_state_file(result["final_caps"])
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
