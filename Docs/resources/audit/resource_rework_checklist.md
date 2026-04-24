# Resource Follow-up Backlog

This is a handoff note, not a formula input. The resource cap package itself is on the accepted v3 baseline.

## Closed In This Baseline

- The audited state set is the full 14-state SB scope.
- `Zululand` and `Drakensberg` are both present and audited as separate public states.
- Full-state footprint rules are explicit in the builder, workbook, README, and audit prompt.
- `Arable Land`, `Wood`, and `Rubber (undiscovered)` use hectare-capacity models.
- Non-land quantity rows use the `GBR 1940` selector and `1940-equivalent` frame.
- The documented-working floor exists for eligible quantity rows only.
- The live state file has been synced from the accepted caps.
- The current test gate is [test_report.md](./test_report.md): `81 passes / 0 fails`.

## Remaining Work

- Implement non-cap gameplay compensation recorded in [gameplay_compensation_spec.md](./gameplay_compensation_spec.md).
- Revisit rows listed in [priority_rows.csv](./priority_rows.csv) only when opening a new balance or evidence pass.
- Keep `Whaling`, `Oil`, and `Rubber (discovered)` as explicit-policy families unless a future evidence/comparator rebuild is approved.
- Treat future state/resource changes as append-only raw evidence updates followed by rebuild, test, sync-live, and test.

## Gameplay-Layer Candidates

- `West Transvaal`: future industrial/infrastructure state modifier.
- `Drakensberg`: Basotho frontier or mountain-pastoral journal flavour.
- `Botswana`: future ranching-quality state modifier or equivalent ownership logic.

## Reference Surfaces

- Public method: [../README.md](../README.md)
- Current accepted caps: [../data/derived/final_resource_caps.csv](../data/derived/final_resource_caps.csv)
- Current state review status: [state_review_status.csv](./state_review_status.csv)
- Current state delta report: [sb_state_delta_report.md](./sb_state_delta_report.md)
