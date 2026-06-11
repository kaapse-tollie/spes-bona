# Audit Outputs

This folder contains generated review surfaces.

## Review Surface

- `target_data_validation.csv`
  - provenance and bounded-fallback check for every formula-driving target input
- `state_resource_counterfactual_audit.csv`
  - one row per public state-resource row with historical/counterfactual labels, basis, and pass index
- `state_pass_tracker.csv`
  - fixed-order progress tracker for the one-state-per-run audit loop
- `family_rewrite_log.csv`
  - family contradictions that force already-completed states to rerun
- `row_audit.csv`
  - legacy row-level reasoning trail retained as a supporting review surface during the loop
- `adjustments.csv`
  - public `X + Y - Z` ledger
- `priority_rows.csv`
  - rows that still deserve focused review
- `state_regional_advantages.csv`
  - state strengths that may belong outside raw caps
- `state_review_status.csv`
  - current acceptance status per SB state
- `sb_state_delta_report.md`
  - readable per-state delta report
- `test_report.md`
  - latest pipeline checks

These are review surfaces, not formula-driving inputs.

Rebuild them from the repo root with:

```bash
python3 Docs/resources/scripts/resources.py build
```
