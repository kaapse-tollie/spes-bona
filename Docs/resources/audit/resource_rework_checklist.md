# Resource Rework Checklist

This is the current backlog after the validation tranche, localization tranche, gameplay-compensation design tranche, non-arable exception cleanup tranche, docs cleanup tranche, and live sync tranche.

The resource package is now structurally working, live-synced, and third-party readable. The remaining work is mostly gameplay-layer implementation, non-arable follow-up where rows are still exception-dominated, and final presentation polish.

## 1. Target-Data Validation

- [x] Add a formula-driving target-data validation layer.
- [x] Add `evidence_scope`, `target_match_status`, `slot_support_status`, `localization_discount`, and `validation_note` to formula-driving target raw files.
- [x] Generate [target_data_validation.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/target_data_validation.csv).
- [x] Block `broad_potential_only` evidence from driving `X`.
- [x] Apply localization discounts before target inputs contribute to `X`.
- [x] Add tests for bounded fallback, localization discount rules, and placeholder-language rejection.

### Remaining target-data work

- [x] Tighten state-scope localization for the proxy-heavy states previously flagged in [state_review_status.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_review_status.csv):
  - `Northern Cape`
  - `Northern Transvaal`
  - `Lourenço Marques`
  - `Zambezi`
  - `Hereroland`
- [ ] Revisit any future row that still relies on `national_fallback` or a strong `regional_proxy` discount and decide whether it can be localized further or should stay explicitly bounded.

### Mozambique wood note

- [x] Treat the Mozambique `26.9 million hectares suitable for timber production` claim as a re-audit trigger only.
- [x] Prevent that claim from directly creating a `Lourenço Marques / Wood` cap.
- [ ] If `Lourenço Marques / Wood` is reopened later, replace national-scale timber-potential claims with state-footprint commercial-forestry evidence.

## 2. Resource-Family Model Logic

### Non-arable families

- [x] Keep non-arable families on GDP-selected representative output.
- [x] Keep GDP as a year selector only, not an output normalizer.
- [x] Stop weak target provenance from silently looking like direct `X`.

### Wood

- [x] Rebuild `Wood` as potential effective commercial forestry land.
- [x] Remove wood from the GDP-selection path.
- [x] Use a plantation-first model with capped restoration allowance.
- [x] Re-audit the previously unresolved wood zeroes.

### Arable Land

- [x] Rebuild `Arable Land` as potential effective commercial agricultural land.
- [x] Remove arable GDP gating/interpolation/penalty logic.
- [x] Keep baskets as gameplay/crop-suitability audit, not cap arithmetic.

### Remaining family-logic work

- [x] Add the authoritative non-land comparator registry [non_arable_benchmark_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/non_arable_benchmark_cases.csv).
- [x] Migrate the live mining-family comparator content into the non-land registry.
- [x] Give `Gold Mine` a real denominator path by inheriting the gold comparator family.
- [x] Retire unsupported latent-rubber carry-over rows in `Lourenço Marques` and `Zambezi`.
- [x] Convert blank non-arable `denominator unavailable` placeholders for `Whaling`, `Oil`, and `Rubber` into explicit audited exceptions where the package still lacks frozen target evidence.
- [ ] Revisit non-land families with large explicit-exception footprints in [priority_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/priority_rows.csv).
- [ ] Decide whether `Whaling`, `Oil`, and `Rubber` should stay on the current explicit-exception policy or get a future evidence/comparator rebuild.
- [ ] Recheck whether any remaining hard zero is still “defended zero” rather than “accepted only because no localized target evidence is frozen.”

## 3. Regional Advantages Outside Raw Caps

- [x] Create a per-state regional-advantages audit table: [state_regional_advantages.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_regional_advantages.csv).
- [x] Create a per-state package review table: [state_review_status.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_review_status.csv).
- [x] Separate “should stay in caps” from “belongs in modifier/flavour/discoverability.”

### Remaining regional-advantage work

- [x] Finish the gameplay-layer compensation design for the states currently marked `needs_gameplay_compensation`:
  - `West Transvaal`
  - `Drakensberg`
  - `Botswana`
- [x] Decide whether each of those should use:
  - `state_modifier`
  - `journal_flavour`
  - `discoverability_unlock`
  - or a small targeted script system outside raw caps
- [ ] Implement the chosen gameplay-layer compensation for:
  - `West Transvaal`
  - `Drakensberg`
  - `Botswana`

## 4. Docs And Package Presentation

- [x] Remove `.DS_Store` files from `Docs/resources`.
- [x] Remove dead public legacy files such as the old `Docs/RESOURCES.md` redirect and retired raw-support exports.
- [x] Move the generated workbook to [resources/RESOURCES.xlsx](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/RESOURCES.xlsx).
- [x] Add [data/raw/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/README.md).
- [x] Add [data/derived/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/README.md).
- [x] Rewrite [README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/README.md) as an explanatory paper-style document:
  - introduction
  - why
  - methodology
  - analysis
  - problems and what we did
  - how to modify / run
  - references
- [x] Rewrite the workbook surface to:
  - use an `Overview` sheet
  - show SB-wide totals and tag deltas
  - provide one readable sheet per SB state
- [x] Mark the remaining seed-only support file `wood_comparator_cases.csv` explicitly as retained seed material, not day-to-day audit input.

### Remaining docs work

- [ ] Minor copy-edit pass on README/workbook wording for brevity and consistency.

## 5. Historical/Plausibility Checks

- [x] Add basic plausibility and localization checks to the automated test surface.
- [x] Add sentinel checks for:
  - `Eastern Cape / Arable Land`
  - `Northern Cape / Arable Land`
  - `Cape Colony / Wood`
  - `Eastern Cape / Wood`
  - `Eastern Transvaal / Wood`
  - `Lourenço Marques / Wood`
  - `Zambezi / Wood`
- [x] Add a no-placeholder-language check for validation notes.

### Remaining plausibility work

- [ ] Run a second deep counterfactual audit for every `state × resource` row.
  - Goal: check whether each final cap still matches the strongest historical or near-historical counterfactual for that SB state scope, rather than only whether the current family model is internally consistent.
  - Focus first on rows where the current result risks suppressing historically plausible regional production belts or over-attributing later 20th-century dominance.
  - Explicit trigger examples for the next pass:
    - `West Transvaal / Iron Mine`: recheck Pretoria Iron Mines, the Magaliesberg-Marico belt, and nearby pre-mid-century ironworking/mining evidence before accepting a hard zero.
    - `Drakensberg / Iron Mine`: recheck Natal-side and upper-Tugela / Dundee / Vryheid / Sweetwaters style iron potential before treating the state as cleanly iron-empty.
    - `Northern Transvaal / Iron Mine`: recheck Phalaborwa / Lowveld and Tshimbupfe-Venda style iron potential against the current distribution.
    - `Northern Cape / Iron Mine`: keep the current cap if still defensible, but separate later nationally dominant mid-20th-century Northern Cape iron development from the stronger 19th- and early-20th-century belts elsewhere.
  - For this pass, treat “historically attested” and “strong local counterfactual” as different labels in the review notes rather than collapsing them into one judgment.
- [ ] After that counterfactual pass, update the affected notes and exceptions so they explain whether a row is:
  - historically evidenced
  - bounded counterfactual potential
  - or explicitly rejected despite a known neighboring/provincial claim
- [ ] Add a manual spot-review pass on the highest-impact non-land rows after any future comparator-family rewrite.
- [ ] Promote any future family-level contradiction into a model redesign, not another adjustment-only patch.

## 6. State-By-State Review

- [x] Add [sb_state_delta_report.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/sb_state_delta_report.md).
- [x] Add [state_resource_deltas.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/state_resource_deltas.csv).
- [x] Record per-state review status in [state_review_status.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_review_status.csv).

### Remaining state review work

- [x] Finish the tighter localization pass for the states that were previously marked `needs_another_audit_pass`.
- [ ] After any targeted re-audit, recheck:
  - total delta versus vanilla
  - resource mix plausibility
  - gameplay identity plausibility

## 7. Release State

- [x] Rebuild the package.
- [x] Re-test the package.
- [x] Sync the current accepted tranche into the live SB state file.
- [x] Re-test after live sync.

Current release state:

- Live file and docs are aligned.
- [test_report.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/test_report.md) is `52 passes / 0 fails`.

## Current Priority Order

- [ ] First: second deep counterfactual audit for each `state × resource` row, starting with iron-family distribution and other rows where historical belts may be landing in the wrong SB state.
- [ ] Second: gameplay-layer implementation for:
  - `West Transvaal`
  - `Drakensberg`
  - `Botswana`
- [ ] Third: non-arable family follow-up for rows still dominated by explicit exceptions:
  - `Whaling`
  - `Oil`
  - `Rubber`
- [ ] Fourth: decide whether the explicit-exception-heavy mining/fishing families need another formula pass or can be frozen as defended policy rows.
- [ ] Fifth: light documentation polish after the next substantive audit pass.
