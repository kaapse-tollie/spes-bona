# Stateful Counterfactual Audit Loop For CLI Runs

## Summary

Use one reusable prompt for a repeated CLI loop where **each agent call completes exactly one SB state pass**, updates the evidence package and outward-facing docs for that state, rebuilds, tests, syncs live, and stops.

Locked decisions:
- Unit of work per call: **one state**
- Standard: every public row gets both a **historical** label and a **counterfactual** label
- Documentation/citations: **must be updated during every state pass**
- Source safety: **append-only evidence policy**
  - do not delete source rows
  - do not overwrite away sourced data
  - do not remove citations during the loop
- Family/model rewrites are allowed, but they are the only case where a call may expand beyond one nominal state pass because affected already-completed states must be rerun before exit

This loop audits the exact public workbook surface for each state:
- `Arable Land`
- 15 arable-resource yes/no rows
- the remaining numeric/special resource rows now shown on each state sheet

## Key Changes

### 1. Make the loop stateful and append-only

Add three control/audit outputs that the CLI agent updates every run:

- `state_resource_counterfactual_audit.csv`
  - one row per public `state × resource`
  - required fields:
    - `state`
    - `resource`
    - `row_category`
    - `historical_label`
    - `counterfactual_label`
    - `driving_basis`
    - `current_value`
    - `proposed_value`
    - `decision`
    - `issue_type`
    - `chronology_note`
    - `regional_claim_note`
    - `primary_district_or_belt`
    - `citation_1_*`
    - `citation_2_*`
    - `state_pass_index`
    - `family_rewrite_triggered`
    - `notes`
- `state_pass_tracker.csv`
  - one row per SB state
  - required fields:
    - `state`
    - `pass_order`
    - `pass_status`
    - `completed_rows`
    - `changed_rows`
    - `family_rewrites_triggered`
    - `live_synced`
    - `last_completed_pass_index`
    - `summary_note`
- `family_rewrite_log.csv`
  - one row per family contradiction
  - required fields:
    - `resource_family`
    - `trigger_state`
    - `trigger_resource`
    - `old_rule_summary`
    - `new_rule_summary`
    - `why_rewrite_was_needed`
    - `affected_states`
    - `rerun_completed`

Add lifecycle metadata to all maintained evidence tables that can drive or constrain public rows:
- `historical_anchors.csv`
- `modern_maxima.csv`
- `arable_target_capacity_rows.csv`
- `wood_target_capacity_rows.csv`
- `adjustment_inputs.csv`
- `counterevidence_cases.csv`

Required lifecycle columns:
- `row_id`
- `row_status`
  - `active`
  - `superseded`
  - `rejected_reference`
- `supersedes_row_id`
- `state_pass_index`
- `changed_on`
- `change_reason`

Rules:
- no existing evidence row is deleted during the loop
- no sourced row loses its citations during the loop
- a changed row is handled by **appending** a new row and superseding the old one
- builder logic must resolve the current active row per logical key and ignore superseded rows for formula purposes
- if a source is no longer driving, preserve it as `superseded` or `rejected_reference`; do not remove it

Do not delete legacy/supporting source material during this loop. If a file becomes obsolete, mark it supporting-only and defer deletion until after the loop finishes.

### 2. Fix the run contract for each CLI call

State order is fixed:

1. Cape Colony
2. Northern Cape
3. Eastern Cape
4. West Transvaal
5. Eastern Transvaal
6. Northern Transvaal
7. Transorangia
8. Drakensberg
9. Botswana
10. Lourenço Marques
11. Zambezi
12. Hereroland
13. Namaqualand

Default behavior of one agent call:
1. read `state_pass_tracker.csv`
2. select the next unfinished or explicitly rerun-required state
3. audit every public row for that state in canonical workbook order
4. append any evidence/adjustment/counterevidence updates with citations
5. update `state_resource_counterfactual_audit.csv`
6. rebuild outputs and workbook
7. run tests
8. sync live
9. rerun tests
10. mark the state pass complete and stop

Exception:
- if a family contradiction appears, log it in `family_rewrite_log.csv`, rewrite the family model immediately, rerun all already-completed affected states, then exit only after the tracker and workbook are coherent again

The agent must not continue into the next untouched state in the same normal run.

### 3. Define the row review model and citation duties

Every public row must receive:

- `historical_label`
  - `direct_historical_support`
  - `indirect_historical_support`
  - `no_material_historical_support`
- `counterfactual_label`
  - `strong_local_counterfactual`
  - `bounded_counterfactual`
  - `rejected_counterfactual`
  - `not_needed`
- `driving_basis`
  - `historical`
  - `counterfactual`
  - `exception`
  - `unchanged_baseline`

Allowed row decisions:
- `keep`
- `raise`
- `lower`
- `flip_yes_no`
- `convert_to_exception`
- `remove_exception`
- `trigger_family_rewrite`

Citation/update rules for every changed row:
- update the driving raw row in the relevant maintained source table
- update the matching audit row in `state_resource_counterfactual_audit.csv`
- preserve old citations on superseded rows
- do not ship a changed row with only prose and no citations
- for defended zeroes and exceptions, the limiting rationale must also be documented in `adjustment_inputs.csv` or `counterevidence_cases.csv`

Counterfactual rules:
- neighboring, provincial, or national claims must be written explicitly into `regional_claim_note`
- they do not silently become local support
- strong national or provincial potential can only support a row if bounded into the actual SB footprint and recorded as counterfactual rather than disguised as direct local history

### 4. Require outward-facing documentation updates on every state pass

Every accepted state pass must update outward-facing presentation, not just internal audit files.

Per-state documentation duties:
- update the state sheet in `Docs/resources/RESOURCES.xlsx`
  - keep the public presentation layout
  - add/update a visible `Basis` column:
    - `Historical`
    - `Counterfactual`
    - `Exception`
    - `Unchanged`
- update the `Overview` sheet progress block so it shows:
  - `not started`
  - `in review`
  - `accepted`
- refresh all derived outputs touched by the state pass
- update citation-bearing raw rows and the counterfactual audit table in the same run

README policy during the loop:
- do **not** rewrite the top-level README on every state pass
- update the README only when a family method, evidence rule, or public interpretation materially changes
- if a family rewrite happens, the same run must also update the README sections that describe methodology or remaining limits

This keeps public documentation current without turning README edits into per-state noise.

### 5. Hard focus areas for the early passes

Treat these as explicit trigger rows in the loop:

- `West Transvaal / Iron Mine`
  - test Pretoria Iron Mines and the Magaliesberg-Marico belt before accepting zero
- `Drakensberg / Iron Mine`
  - test Dundee, Vryheid, Sweetwaters, Alverstone, and adjacent Natal-era iron potential before accepting iron-emptiness
- `Northern Transvaal / Iron Mine`
  - test Phalaborwa/Lowveld and Tshimbupfe-Venda style iron potential against the current split
- `Northern Cape / Iron Mine`
  - do not let later nationally dominant Northern Cape iron development substitute for earlier stronger belts elsewhere
- `Lourenço Marques / Wood`
  - national Mozambique timber claims remain non-driving unless state-footprint commercial forestry evidence appears

## Test Plan

After every accepted state pass:

1. `build`
2. `test`
3. review:
   - `state_resource_counterfactual_audit.csv`
   - `state_pass_tracker.csv`
   - `family_rewrite_log.csv`
   - `state_resource_deltas.csv`
   - `Docs/resources/RESOURCES.xlsx`
4. `sync-live`
5. rerun `test`

Add automated checks for:
- lifecycle columns exist on all maintained evidence tables listed above
- no logical key has more than one `active` evidence row
- superseded rows remain present after a change
- every audited public row has both labels and one `driving_basis`
- no changed row lacks citations
- workbook `Overview` progress matches `state_pass_tracker.csv`
- state sheets expose the public `Basis` column
- no family rewrite is marked complete unless all affected completed states were rerun

Manual acceptance for each state pass:
- every public row in that state is classified
- documentation and citations for changed rows are updated in the same run
- no placeholder language remains
- no sourced data was deleted or overwritten away
- live file and docs remain aligned after sync

## Assumptions And Defaults

- “Documentation updated during each loop” means: workbook, derived outputs, audit tables, and row-level citations are updated every state pass; README is updated only when methodology or interpretation changes.
- “Do not destroy data” means append-only evidence handling inside maintained source tables, not merely relying on git history.
- One state per call is the normal contract; family rewrites are the only allowed reason to exceed that boundary.
- The workbook remains outward-facing; detailed reasoning stays in the audit CSVs, not in visible narrative blocks on state sheets.
