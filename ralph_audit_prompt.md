# Stateful Counterfactual Audit Loop For CLI Runs

## Summary

Use one reusable prompt for a repeated CLI loop where **each agent call completes exactly one SB state pass**, updates the evidence package and outward-facing docs for that state, rebuilds, tests, and stops.

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

## 0. Methodology Guardrails

Before changing any row, read the methodology in:

- `Docs/resources/README.md`

Do not treat this as a generic 1936 snapshot audit. The package uses two different model families and the agent must preserve that distinction.

### 0A. Non-land families are `1940-equivalent` models

For non-land numeric families such as:

- `Coal Mine`
- `Iron Mine`
- `Gold Fields`
- `Gold Mine`
- `Lead Mine`
- `Sulfur Mine`
- `Fishing`
- any other family that still uses comparator-derived output denominators

the governing method is:

1. gather target observations
2. choose a representative year using the frozen GDP-selection protocol
3. normalize the observation into the common `1940-equivalent` frame
4. compare against comparator denominators built on the same frame

Hard rules:

- Do **not** treat raw 1936 output as the primary target just because it is chronologically close to game start.
- A 1936 observation may be used as one candidate year, but it is not privileged over a better representative year once the package's GDP-selection and `1940-equivalent` logic are applied.
- When reviewing a non-land row, ask:
  - is the representative-year choice still defensible?
  - is the `1940-equivalent` normalized value still the right direct `X` basis?
  - is the comparator denominator family still appropriate?
- Do not silently replace the package's `1940-equivalent` method with a “closest to 1936” method.

### 0B. Land families are not `1940-equivalent` output models

For:

- `Arable Land`
- `Wood`
- `Rubber (undiscovered)`

the governing method is land capacity, not realized output.

Hard rules:

- `Arable Land` is based on potential effective commercial agricultural land.
- `Wood` is based on potential effective commercial forestry land.
- `Rubber (undiscovered)` is based on potential effective commercial plantation land.
- Representative year on these rows is audit metadata only; it is **not** a signal to convert the family back into a 1936 or 1940 output model.
- Do not introduce GDP-selected output normalization into arable, wood, or latent rubber.

### 0C. Counterfactual review standard

The counterfactual audit is not “what existed in 1936 and only 1936.”

Use this standard:

- direct local history matters
- bounded local counterfactual potential matters
- later-developed districts, belts, estates, mines, or forestry zones may still support a row if they reveal a local potential that plausibly existed before large-scale postwar buildout

But:

- later national dominance does not automatically justify earlier local caps
- later development must be converted into a bounded local counterfactual, not smuggled in as direct 1936 output

When a changed non-land row survives partly because of later evidence, the audit note must say clearly that the row is being carried by bounded counterfactual potential within the package's `1940-equivalent` non-land framework.

### 0D. Documented-working floor for quantity rows

For public numeric quantity rows only:

- if the numeric model resolves to `0`
- and there is documented in-state working, trial production, or commercial operation

then the row should be held at `1`, not `0`.

Hard rules:

- this applies only to quantity-cap public rows such as mines, fishing, whaling, and wood
- this does **not** apply to `Arable Land`, yes/no arable basket rows, or special-resource rows
- mere occurrence, geology, archaeological smelting, or unworked potential does not trigger the floor

### 0E. State scope before row localization

Before reviewing any row, bind the SB state to its **full split-state footprint**.

Only after that may you localize evidence to narrower belts, districts, estates, coalfields, river corridors, or plantation zones.

Hard rules:

- a localized belt must never redefine the state itself
- state-level notes must describe the full split-state footprint first
- row-localized evidence may narrow a specific row inside that footprint, but it does not shrink the state
- every state pass must actively check whether the corrected full-state footprint contains additional production systems, districts, estates, fisheries, forestry belts, or mine chains that were previously omitted by narrowed shorthand
- do not treat the listed trigger rows as the only scope-sensitive rows in a state; they are only the most failure-prone places to check first

Lock these mappings:

- `Cape Colony` = Western Cape core plus the small modern Northern Cape coastal strip inside `STATE_CAPE_COLONY`
- `Northern Cape` = the remainder of `STATE_NORTHERN_CAPE`, including inland South African Namaqualand / Karoo / Orange-Vaal country and the dry western side of the old North West split
- `West Transvaal` = Gauteng plus the interior plateau / mining-linked side of the old North West split
- `Zululand` = full modern KwaZulu-Natal / full `STATE_ZULULAND`
- `Drakensberg` = full Lesotho / full `STATE_DRAKENSBERG`
- `Botswana` = full `STATE_BOTSWANA`, including the north-west wet corridor and the vanilla-default Caprivi inclusion
- `Lourenço Marques` = Maputo Province, Maputo City, Inhambane Province, Gaza Province, Sofala south of the Pungwe inclusive, and Manica south of the Pungwe inclusive
- `Zambezi` = full Zimbabwe / full `STATE_ZAMBEZI`
- `Hereroland` = full northern Namibia / full `STATE_HEREROLAND`
- `Namaqualand` = full southern Namibia / full `STATE_NAMAQUALAND`

When a row note later uses labels like `Eastern Highlands`, `Maputo-Gaza lowland`, `Otavi-Grootfontein pocket`, `KwaZulu-Natal littoral`, or `Orange-Vaal corridor`, treat that as row localization only.

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
    - `full_state_footprint`
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
8. Zululand
9. Drakensberg
10. Botswana
11. Lourenço Marques
12. Zambezi
13. Hereroland
14. Namaqualand

Default behavior of one agent call:
1. read `state_pass_tracker.csv`
2. select the next unfinished or explicitly rerun-required state
3. audit every public row for that state in canonical workbook order
4. append any evidence/adjustment/counterevidence updates with citations
5. update `state_resource_counterfactual_audit.csv`
6. rebuild outputs and workbook
7. run tests
8. mark the state pass complete and stop

Exception:
- if a family contradiction appears, log it in `family_rewrite_log.csv`, rewrite the family model immediately, rerun all already-completed affected states, then exit only after the tracker and workbook are coherent again

The agent must not continue into the next untouched state in the same normal run.

### 2A. Final response contract for each CLI call

Do not use the word `complete` to mean “one state pass finished”.

Use `complete` only if the entire 14-state loop is finished and `state_pass_tracker.csv` shows no remaining `not started`, `in review`, or `rerun required` rows.

At the end of every call, the final response must include these plain-text status lines:

- `CURRENT_STATE=<state just processed, or NONE>`
- `STATE_PASS_COMPLETE=yes|no`
- `LOOP_COMPLETE=yes|no`
- `NEXT_STATE=<next state name, or NONE>`
- `FAMILY_REWRITE=yes|no`

Rules:
- If one state pass finished successfully and more states remain:
  - `STATE_PASS_COMPLETE=yes`
  - `LOOP_COMPLETE=no`
  - `NEXT_STATE=<next state from tracker>`
- If all 14 states are accepted:
  - `STATE_PASS_COMPLETE=yes`
  - `LOOP_COMPLETE=yes`
  - `NEXT_STATE=NONE`
- If the run stops before accepting the current state:
  - `STATE_PASS_COMPLETE=no`
  - `LOOP_COMPLETE=no`
  - `NEXT_STATE=<same state or rerun-required state>`
- Never output a bare “complete” or “done” without the status lines above.
- The final response should also include one short paragraph summarizing:
  - what changed
  - that live sync did not happen during the state pass
  - whether tests passed

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
- for every changed non-land numeric row, document whether the representative-year choice and `1940-equivalent` normalization were kept, revised, or explicitly rejected by a family rewrite

Counterfactual rules:
- neighboring, provincial, or national claims must be written explicitly into `regional_claim_note`
- they do not silently become local support
- strong national or provincial potential can only support a row if bounded into the actual SB footprint and recorded as counterfactual rather than disguised as direct local history

### 3A. Research protocol for each contested or changed row

The agent must do real research work during each state pass. Do not treat this as a pure spreadsheet-editing task.

Expected local tools:
- `python3`
- `rg`
- `curl`
- `jq`
- `pdftotext`
- `mutool`
- Codex CLI built-in web search
- local SearXNG endpoint at `http://127.0.0.1:8888/search` as fallback

If one of those tools is missing:
- continue with the strongest available fallback
- note the missing tool in the final response
- do not skip citation work silently

Research order for every row that is changed, reopened, or explicitly checked as a trigger row:

1. Search the maintained local package first.
   - inspect the current raw evidence tables
   - inspect existing adjustment and counterevidence rows
   - inspect the existing counterfactual audit and state tracker
   - inspect the public workbook/state sheet for the current result
2. If local evidence is insufficient, use Codex CLI built-in web search as the primary external search path.
   - prefer the built-in CLI web search tool first
   - use it to discover candidate sources, localized districts, belts, mines, estates, and chronology references
3. If built-in web search is unavailable, weak, or does not surface the needed source type, fall back to shell-accessible search/fetch tools.
   - prefer the local SearXNG endpoint first:
     - `curl 'http://127.0.0.1:8888/search?q=<query>&format=json'`
   - use SearXNG to discover candidate URLs before fetching individual sources
   - use `curl` for HTML or downloadable reports
   - use `pdftotext` or `mutool draw -F txt` for PDFs
   - prefer sources that localize to the actual SB state footprint, district, belt, minefield, irrigation corridor, forestry belt, or fishery zone
4. Prefer source types in this order:
   - direct local historical or geological/agricultural evidence
   - district or belt-level evidence clearly overlapping the SB footprint
   - provincial/regional evidence with explicit overlap
   - national evidence only as bounded context, never as silent local support
5. Capture citation data immediately when a source is used.
   - title
   - URL
   - locator/page/section
   - short note on whether it is local, regional, or national in scope
6. If only broad regional or national support exists:
   - do not let it become direct local history
   - record it in `regional_claim_note`
   - either use bounded counterfactual treatment or reject it
7. If evidence remains insufficient after search:
   - keep the row unchanged or convert it to a defended exception/zero
   - explain the evidence gap explicitly
   - do not fabricate a formula-driving `X`

Minimum research expectation per state pass:
- every changed row must have refreshed citations
- every trigger row must be explicitly rechecked even if it ends unchanged
- at least one local-package search pass and one external search pass must be completed for any changed contested row
- if built-in Codex CLI web search is unavailable in the session, note that explicitly in the final response and fall back to SearXNG or direct-source fetching
- if the SearXNG endpoint is unreachable, note that explicitly in the final response and fall back to direct-source fetching
- if a touched row or touched README/workbook note still carries old normalization-anchor wording or another stale methodology phrase, update it in the same run instead of carrying stale method text forward

PDF handling rules:
- prefer `pdftotext <file> -` for quick extraction
- if that fails, use `mutool draw -F txt -o - <file>`
- when a PDF is downloaded temporarily for review, do not treat it as maintained project data unless you intentionally add it to the repo later
- cite page numbers or section locators, not just the PDF title

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

### 5. Hard focus areas for the rerun

Treat these as explicit trigger rows in the loop. A state pass is not accepted until any trigger rows in that state have been explicitly rechecked and the audit note says what happened.

These trigger rows are extra-sensitive checks, not a substitute for full-state review. For every state pass, you must still account for the whole corrected state footprint and confirm that no other in-footprint production system has been skipped just because it is not named below.

Immediate trigger rows:

- `West Transvaal / Iron Mine`
  - test Pretoria Iron Mines and the Magaliesberg-Marico belt before accepting zero
- `Zululand / Coal Mine`
  - treat Dundee, Newcastle, Utrecht, and Vryheid as in-footprint Natal evidence for the restored split state rather than as Drakensberg counterevidence
- `Zululand / Iron Mine`
  - recheck Sweetwaters, Alverstone, and the wider Natal-era ironworks chain as Zululand-side evidence before accepting zero
- `Zululand / Wood`
  - treat KwaZulu-Natal plantation/woodland belts as Zululand evidence and do not force Drakensberg’s Lesotho zero onto the restored coastal split
- `Zululand / Sugar Plantation`
  - keep the humid littoral sugar belt distinct from Drakensberg’s mountain-grain basket
- `Zululand / Fishing`
  - recheck the coast-facing fishery row as a real Zululand lane rather than a landlocked Drakensberg comparison
- `Drakensberg / Iron Mine`
  - test Dundee, Vryheid, Sweetwaters, Alverstone, and adjacent Natal-era / KwaZulu-Natal iron potential before accepting iron-emptiness
  - do not accept zero until you have explicitly compared the KZN ironworks/mining evidence against the current West Transvaal Pretoria standard
  - if the evidence looks more like a small bounded Pretoria-style row than a clean hard zero, say that explicitly in the audit note even if the final decision remains zero
- `Drakensberg / Fishing`
  - recheck whether the documented-working floor should apply at all to a landlocked Lesotho fishery row
  - if the statewide commercial-slot standard is not met, say explicitly why the row returns to `0`
- `Botswana / Coal Mine`
  - recheck the Palapye-Morupule corridor against the chronology rule and the statewide-slot standard
  - say explicitly whether the current outcome is a defended late zero or whether a different bounded treatment is required
- `Botswana / Wood`
  - recheck the experimental plantation and woodlot record against the commercial-forestry threshold
  - do not keep a hard zero by inertia if the evidence clears the documented-working standard
- `Lourenço Marques / Wood`
  - national Mozambique timber claims remain non-driving unless state-footprint commercial forestry evidence appears
- `Transorangia / Iron Mine`
  - recheck Kroonstad/Vredefort-style ore occurrence, any localized working evidence, and the documented-working floor standard before keeping an explicit zero
- `Northern Cape / Tobacco Plantation`
  - do not keep a yes row on broad basket plausibility alone; require direct state-local support or remove it
- `Northern Transvaal / Coffee Plantation`
  - recheck for direct Limpopo-local coffee evidence rather than warm-climate plausibility alone

General review targets:

- `Tobacco review`
  - explicitly recheck `Northern Cape / Tobacco Plantation` and `Northern Transvaal / Tobacco Plantation`
  - require direct state-local support, not only broad basket logic or neighboring analogies

Family policy locks:

- `Oil`
  - no dedicated audit check is required for this rerun
  - keep oil disabled unless a state pass uncovers direct localized commercial evidence strong enough to break the current explicit-zero rule
- `Rubber`
  - treat rubber as discoverable-only through the hectare-based `Rubber (undiscovered)` model
  - do not spend rerun time defending or extending a separate discovered-rubber family
- `Whaling`
  - treat whaling as a relative coastal row rather than a family-wide rewrite target
  - only escalate to a family rewrite if a state pass shows the current relative treatment is internally inconsistent

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
4. do **not** sync live during the state loop
5. stop after updating the tracker and outputs for that one state

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

## Final release gate

Do **not** sync the live state file during ordinary state passes.

Only allow final live sync after all of the following are true:

- all 14 rows in `state_pass_tracker.csv` are `accepted`
- `resources.py test` passes cleanly on the full package
- the high-impact flagged rows and general reviews have been explicitly rechecked:
  - `West Transvaal / Iron Mine`
  - `Zululand / Coal Mine`
  - `Zululand / Iron Mine`
  - `Zululand / Wood`
  - `Zululand / Sugar Plantation`
  - `Zululand / Fishing`
  - `Drakensberg / Iron Mine`
  - `Drakensberg / Fishing`
  - `Botswana / Coal Mine`
  - `Botswana / Wood`
  - `Lourenço Marques / Wood`
  - `Transorangia / Iron Mine`
  - `Northern Cape / Tobacco Plantation`
  - `Northern Transvaal / Tobacco Plantation`
  - `Northern Transvaal / Coffee Plantation`
- the family policy locks are still coherent in the final outputs:
  - `Oil` remains disabled with no open audit contradiction
  - `Rubber` is still handled only through the hectare-based discoverable model
  - `Whaling` has no unresolved family contradiction after the rerun
- no touched active row or public doc still carries stale normalization-anchor wording or obsolete chronology-rule language
- the final workbook and derived outputs reflect the accepted v3 method

Only then:

1. run `sync-live`
2. rerun `test`
3. report whether docs and live state file are aligned

## Assumptions And Defaults

- “Documentation updated during each loop” means: workbook, derived outputs, audit tables, and row-level citations are updated every state pass; README is updated only when methodology or interpretation changes.
- “Do not destroy data” means append-only evidence handling inside maintained source tables, not merely relying on git history.
- One state per call is the normal contract; family rewrites are the only allowed reason to exceed that boundary.
- The workbook remains outward-facing; detailed reasoning stays in the audit CSVs, not in visible narrative blocks on state sheets.
- Live sync is a final release action, not part of the ordinary one-state loop.
