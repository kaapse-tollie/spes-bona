# Audit Outputs

This folder contains generated review surfaces.

## Review Surface

- `target_data_validation.csv`
  - provenance and bounded-fallback check for every formula-driving target input
- `row_audit.csv`
  - row-level reasoning trail
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
- `resource_rework_checklist.md`
  - remaining backlog
- `test_report.md`
  - latest pipeline checks

These are review surfaces, not formula-driving inputs.

Rebuild them with:

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' build
```
