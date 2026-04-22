# Spes Bona Southern Africa Resource Rework

## Introduction

This document is the full public protocol for the Southern Africa resource rework used by *Spes Bona - A Southern Africa Flavour Pack*.

It is meant to stand on its own. A third party reading only this file, the maintained raw tables, and the generated workbook should be able to answer:

1. what problem the rework is solving
2. what each resource family is intended to measure
3. how target rows and comparator rows are built
4. how caps are calculated
5. how evidence quality is handled
6. what is still formula-driven versus explicit policy

The readable output surface is [RESOURCES.xlsx](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/RESOURCES.xlsx). The machine-readable outputs are in [data/derived](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/README.md).

## Why

The rework exists because vanilla resource values stop behaving coherently once Southern Africa is split into smaller SB state scopes.

The main problems are:

1. Vanilla caps are often assigned to a much larger undivided state than the SB target scope.
2. Vanilla frequently reflects realized development rather than plausible regional potential.
3. Different resource families need different models.
   Land-capacity families do not behave like mining or fishery output families.
4. Split-state allocation matters.
   A macro-Transvaal or macro-Cape number can look reasonable at the vanilla scale while becoming internally inconsistent once it is divided into west/east/north or coast/interior subregions.

The goal of the package is therefore not to preserve vanilla totals mechanically. The goal is to produce a coherent SB-state resource map with clear evidence rules and clear formulas.

## Methodology

### Scope

The package covers these 13 SB states:

- Cape Colony
- Northern Cape
- Eastern Cape
- West Transvaal
- Eastern Transvaal
- Northern Transvaal
- Transorangia
- Drakensberg
- Botswana
- Lourenço Marques
- Zambezi
- Hereroland
- Namaqualand

The public workbook also aggregates these regional tags:

- `CAP` = Cape states
- `TRN` = Transvaal states
- `SAF` = South African states
- `SWA` = Namibian states

### Common Cap Formula

Every cap still resolves through the same public arithmetic:

```text
final = X + Y - Z
cap = round(final / denominator)
```

Where:

- `X` is the direct target-side quantity
- `Y` is a named upward addition for a bounded omitted block
- `Z` is a downward plausibility haircut

The meanings of `X`, `Y`, and `Z` differ by family:

- for land-capacity families, `X` is effective hectares
- for non-land families, `X` is normalized representative output
- for explicit exceptions, `X` may be blank and the row is governed directly by documented policy

### Resource-Family Split

The package separates families by what they are actually trying to represent.

#### Non-land families

These remain output-based:

- `Coal Mine`
- `Iron Mine`
- `Gold Fields`
- `Gold Mine`
- `Lead Mine`
- `Sulfur Mine`
- `Fishing`
- and other non-land numeric families where a comparator pool exists

These rows use:

- target observations
- unit standardization
- growth-family normalization to a `1950-equivalent` value
- GDP-based representative-year selection
- comparator-derived denominators

#### Land-capacity families

These no longer use realized output as the main basis:

- `Arable Land`
- `Wood`

These rows use:

- weighted effective land classes
- direct target-side effective hectares
- comparator-side effective hectares per vanilla cap
- no GDP-selected output transform as the main cap driver

#### Arable-resource yes/no rows

Arable resource rows such as `Wheat Farm`, `Sugar Plantation`, or `Vineyard` are no longer cap drivers.

They are now:

- a gameplay-availability layer
- audited against a researched crop basket
- reported separately from the cap arithmetic

### Maintained Input Surfaces

The main maintained raw files are:

- [historical_anchors.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/historical_anchors.csv)
- [modern_maxima.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/modern_maxima.csv)
- [adjustment_inputs.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/adjustment_inputs.csv)
- [counterevidence_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/counterevidence_cases.csv)
- [non_arable_benchmark_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/non_arable_benchmark_cases.csv)
- [arable_land_class_weights.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_land_class_weights.csv)
- [arable_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_target_capacity_rows.csv)
- [arable_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_comparator_capacity_rows.csv)
- [arable_baskets.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_baskets.csv)
- [agri_rankings.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/agri_rankings.csv)
- [wood_land_class_weights.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_land_class_weights.csv)
- [wood_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_target_capacity_rows.csv)
- [wood_comparator_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_cases.csv)
- [wood_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_capacity_rows.csv)

### Evidence And Provenance Rules

Formula-driving target rows carry explicit validation metadata.

The key fields are:

- `evidence_scope`
  - `state_localized`
  - `regional_proxy`
  - `national_fallback`
- `target_match_status`
  - `direct`
  - `partial_overlap`
  - `indirect`
- `slot_support_status`
  - `distinct_slot_supported`
  - `broad_potential_only`
- `localization_discount`
- `validation_note`

The rules are:

- `state_localized` rows may drive `X` directly.
- `regional_proxy` and `national_fallback` may drive `X` only if they support a distinct slot and are explicitly discounted.
- `broad_potential_only` rows never drive `X`.
- `indirect` rows do not silently become direct support.
- target-side discounted values are what actually feed the cap arithmetic.

This is the main safeguard against over-reading broad national claims into local SB-state caps.

Example:

- a Mozambique-wide timber-potential claim may appear in notes
- it may justify reopening research
- it does **not** automatically create `Lourenço Marques / Wood`

### Append-Only Evidence Policy

Maintained evidence tables are append-only.

They carry lifecycle fields such as:

- `row_id`
- `row_status`
- `supersedes_row_id`
- `state_pass_index`
- `changed_on`
- `change_reason`

This means:

- sourced rows are not deleted during review
- superseded rows remain visible
- rejected references remain visible as rejected references
- current formula-driving rows are selected from the active set

The intent is to preserve provenance inside the package itself rather than relying on git history alone.

### Non-Land Family Protocol

#### 1. Target observations

Non-land target evidence comes from:

- [historical_anchors.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/historical_anchors.csv)
- [modern_maxima.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/modern_maxima.csv)

Each row is:

1. standardized into a canonical unit
2. assigned to a growth family
3. normalized to a `1950-equivalent` value

The standardization logic handles unit families such as:

- tons of output
- ore metal content
- catches
- fishery/whaling output
- agricultural proxies that still survive in non-land legacy rows

#### 2. What `1950-equivalent` means

`1950-equivalent` is the normalization frame used for non-land output families.

The logic is:

- choose a growth family for the resource
- use the frozen growth index for that family
- convert the row’s observed output year to a value comparable on a 1950 basis

This does **not** mean the package is trying to set 1950 caps directly.
It means non-land target and comparator rows are put into one common normalization frame before denominator arithmetic.

This is why the package still refers to:

- `normalized_1950_output`
- `wheat_equivalent_1950_output`
- `historical_1950_equivalent_output`

even though the land-capacity families no longer use that logic.

#### 3. Representative-year selection

For non-land families, GDP is still used, but only as a year selector.

The selection logic is:

1. collect candidate years from the target or comparator row package
2. map the entity to a frozen GDP geography if possible
3. compare candidate GDP per capita values to the `GBR 1950` reference anchor
4. select the candidate year whose GDP per capita is closest to the reference anchor

Important constraints:

- GDP is not used to rescale output directly
- if no usable GDP mapping or series exists, the representative year stays manual
- the selection note is recorded in the output

This is the part of the protocol the current README had become too thin on. The non-land model is still fundamentally a `representative-year + 1950-equivalent output` model.

#### 4. Comparator pools

Non-land comparator families use [non_arable_benchmark_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/non_arable_benchmark_cases.csv).

For each comparator row:

1. historical and optional peak observations are standardized
2. each is normalized to a 1950-equivalent output
3. GDP selects the representative comparator year
4. the selected 1950-equivalent maximum is divided by the vanilla cap

The denominator is then:

```text
A_family = mean_i( selected_1950_equivalent_maximum_i / vanilla_cap_i )
```

The benchmark registry is built around 20 comparator rows per formula-driven family where possible.

Current denominator methods in [resource_denominators.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/resource_denominators.csv) are:

- `simple_mean_of_20_comparator_pool` for the main non-land benchmarked families
- `denominator_unavailable` where a real comparator family does not yet exist

#### 5. Exceptions

Some non-land families remain explicit exceptions rather than fake formulas.

Currently this mainly affects:

- `Whaling`
- `Oil`
- `Rubber`

Those rows remain conservative because the package does not yet contain a frozen localized target/comparator chain strong enough to justify formula-driven `X`.

### Arable Land Protocol

#### 1. Why arable changed

The earlier output-based arable model was discarded because it overstated development and understated potential.

`Arable Land` now measures:

```text
potential effective commercial agricultural hectares
```

It is therefore a land-capacity model, not a realized crop-output model.

#### 2. Land classes and weights

The current land classes are:

- `irrigated_perennial = 1.25`
- `reliable_rainfed_crop = 1.00`
- `mixed_farming = 0.70`
- `commercial_pasture = 0.35`
- `marginal_grazing = 0.10`
- `desert_or_unusable = 0.00`

These weights are stored in [arable_land_class_weights.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_land_class_weights.csv).

The protocol is deliberately weighted rather than raw-hectare based:

- fertile but underdeveloped land still counts
- dry or desert-heavy states do not inflate simply because they are large

#### 3. Target rows

Target arable capacity comes from [arable_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_target_capacity_rows.csv).

For each row:

```text
effective_area_ha = raw_area_ha * effective_weight * localization_discount
```

Then for each state:

```text
X_state = sum( effective_area_ha )
```

#### 4. Comparator construction

Arable uses local comparator sets, not one global comparator pool.

The comparator ranking file is [agri_rankings.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/agri_rankings.csv).

Each SB state has 20 ranked comparator analogues with weight bands:

- ranks `1-5` -> weight `10`
- ranks `6-10` -> weight `5`
- ranks `11-15` -> weight `2`
- ranks `16-20` -> weight `1`

Arable comparator rows live in [arable_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_comparator_capacity_rows.csv).

For each target state `s` and comparator `k`:

```text
U_s,k = comparator_effective_hectares / comparator_vanilla_arable_cap
```

Then the state-level denominator benchmark is:

```text
B_s = weighted_mean_k( U_s,k )
```

The shared SB arable denominator is then:

```text
A_arable = mean_s( B_s )
```

The current shared denominator method in [arable_shared_denominator.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/arable_shared_denominator.csv) is:

- `simple_mean_of_13_effective_land_state_means`

This is a deliberate simplification. The old arable GDP-gating/interpolation/penalty stack was removed because it was compensating for the wrong base metric.

#### 5. Crop baskets

The arable crop basket still exists, but its role changed.

[arable_baskets.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_baskets.csv) now defines:

- researched crop/resource plausibility
- gameplay audit
- mismatch reporting against live enabled resources

It does **not** drive the arable cap arithmetic.

That is why outputs such as [arable_resource_expectations.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/arable_resource_expectations.csv) and the basket mismatch fields still exist.

### Wood Protocol

#### 1. Why wood changed

The earlier wood model used observed managed forestry area and before that implicitly behaved like industrial logging output. That understated historically depleted but commercially workable forestry belts and over-exposed the package to the wrong comparator family.

`Wood` now measures:

```text
potential effective commercial forestry hectares
```

#### 2. Land classes and weights

The current wood classes are:

- `high_suitability_plantation = 1.00`
- `moderate_suitability_plantation = 0.65`
- `restorable_commercial_forest = 0.40`
- `marginal_forestry = 0.15`
- `noncommercial_wooded_land = 0.00`
- `arid_or_unusable = 0.00`

These weights are stored in [wood_land_class_weights.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_land_class_weights.csv).

#### 3. Plantation-first with capped restoration

Wood is a plantation-first model with a restoration allowance.

The restoration rule is hard-capped:

```text
restorable_commercial_forest_effective_ha
<= 0.5 * (high_suitability_plantation_effective_ha + moderate_suitability_plantation_effective_ha)
```

This cap applies on:

- the target side
- the comparator side

The purpose is to allow depleted forestry belts to count without letting broad “this used to be wooded” claims dominate the cap.

#### 4. Target rows

Target wood capacity comes from [wood_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_target_capacity_rows.csv).

For each row:

```text
effective_area_ha = raw_area_ha * effective_weight * localization_discount
```

For each state:

```text
X_state = sum( effective_area_ha )
```

Rows that are only `broad_potential_only` do not drive `X`.

#### 5. Dedicated comparator family

Wood uses its own comparator family.

The seed source is [wood_comparator_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_cases.csv), and the maintained formula-driving comparator table is [wood_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_capacity_rows.csv).

The denominator is:

```text
A_wood = mean_i( effective_commercial_forestry_hectares_i / benchmark_vanilla_wood_cap_i )
```

The current denominator method in [resource_denominators.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/resource_denominators.csv) is:

- `mean_of_effective_commercial_forestry_comparator_pool`

#### 6. What wood no longer is

The current wood family is **not**:

- total forest cover
- generic woodland
- direct roundwood output
- GDP-selected plantation-estate output

Roundwood and forestry-estate evidence may still inform notes, counterevidence, or `Y`, but they are not the cap basis.

### Adjustments, Exceptions, And Defended Zeroes

#### `Y`

`Y` survives where a named omitted block must be restored.

Typical valid uses:

- omitted irrigation belt
- omitted plateau block
- omitted plantation belt
- split-state undercount that is specifically identified

#### `Z`

`Z` is a rare plausibility haircut.

It is used where:

- a raw land or output estimate is too permissive for a plausible 1836-1936 ceiling

#### Explicit exceptions

Some rows remain explicit exceptions because a formula path would be weaker than an explicitly documented policy row.

These rows are visible in:

- [adjustment_inputs.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/adjustment_inputs.csv)
- [counterevidence_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/counterevidence_cases.csv)

#### Defended zeroes

A defended zero is not “nothing was researched.”

It means:

- the package reviewed the row
- evidence did not justify a distinct commercial slot
- a broad neighboring or national claim was not allowed to substitute for local support

This distinction matters especially for:

- wood in dry or wooded-but-noncommercial states
- non-land rows where geology exists but a commercial 1836-1936 slot is not defensible

### Stateful Counterfactual Audit Loop

The package is now under a state-by-state second-pass counterfactual audit.

The loop outputs are:

- [state_resource_counterfactual_audit.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_resource_counterfactual_audit.csv)
- [state_pass_tracker.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/state_pass_tracker.csv)
- [family_rewrite_log.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/family_rewrite_log.csv)

That loop is meant to answer a stricter question than the first family rebuilds:

- not only “is this family internally coherent?”
- but also “does this specific state/resource row still match the strongest historical or bounded counterfactual case?”

## Analysis

### Public workbook

The workbook is outward-facing rather than pipeline-facing.

- `Overview` shows:
  - SB-wide vanilla totals versus SB totals
  - major regional tag totals
  - current loop progress
- each state sheet shows:
  - vanilla baseline
  - proposed SB update
  - public-facing `Basis` label

The visible basis labels are:

- `Historical`
- `Counterfactual`
- `Exception`
- `Unchanged`

### Main machine-readable outputs

The core generated outputs are:

- [final_resource_caps.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/final_resource_caps.csv)
- [state_delta_summary.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/state_delta_summary.csv)
- [state_resource_deltas.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/state_resource_deltas.csv)
- [target_observations.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/target_observations.csv)
- [resource_denominators.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/resource_denominators.csv)
- [row_audit.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/row_audit.csv)

## Problems And What We Did

### Vanilla area inheritance

Several SB states inherit caps from much larger vanilla spaces.

The rework addresses this by rebuilding state-level caps rather than subdividing vanilla by intuition.

### Vanilla development bias

`Arable Land` and `Wood` were the clearest cases where realized output distorted capacity.

The rework replaced those with land-capacity models so that:

- fertile but underdeveloped regions do not read as barren
- dry or scrub-heavy states do not inflate from raw area alone

### Comparator-family mismatch

Earlier iterations treated some families with the wrong analogues.

The current package now distinguishes:

- global non-land benchmark pools
- local arable comparator sets
- dedicated wood comparator family

instead of forcing all families through one logic.

### Provenance drift

The package previously risked losing method clarity as the model changed.

The current protocol addresses that by:

- explicit validation metadata
- append-only evidence tables
- row-level citations
- audit tables for state-by-state review

### Remaining limits

The main remaining limitations are:

- `Whaling`, `Oil`, and `Rubber` are still explicit-exception-heavy
- the second deep counterfactual audit is still in progress
- some gameplay identity problems are intentionally held outside caps and will be implemented later as gameplay compensation

## How To Modify / Run

### Maintain the package

Edit the relevant maintained raw table in [data/raw](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/README.md).

Do not delete sourced rows from append-only evidence tables. Supersede them.

### Rebuild only

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' build
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

### Sync current accepted state to live

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' sync-live
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

### Run one counterfactual state pass

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' state-pass
```

`state-pass` performs the normal sequence:

1. select the next state from the tracker
2. apply the next accepted row updates
3. rebuild
4. test
5. sync live
6. test again

### Expected validation behavior

The package should remain clean under:

- no placeholder validation notes
- no deleted sourced evidence rows
- no duplicate active logical keys in append-only tables
- workbook and live file alignment

## References

### Row-level references

References for specific rows live with the rows they support:

- [historical_anchors.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/historical_anchors.csv)
- [modern_maxima.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/modern_maxima.csv)
- [arable_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_target_capacity_rows.csv)
- [wood_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_target_capacity_rows.csv)
- [adjustment_inputs.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/adjustment_inputs.csv)
- [counterevidence_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/counterevidence_cases.csv)

### Methodology sources inside the package

The current protocol is implemented and auditable through:

- [build_resources_workbook.py](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/scripts/_internal/build_resources_workbook.py)
- [agri_rankings.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/agri_rankings.csv)
- [non_arable_benchmark_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/non_arable_benchmark_cases.csv)
- [wood_comparator_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_cases.csv)

### Earlier public reasoning retained in the repo

Earlier reference notes that still help explain the package’s evolution are:

- [resource_proposal.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/References/resource_proposal.md)
- [resource_upperbound_audit.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/References/resource_upperbound_audit.md)

For the full file map:

- [data/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/README.md)
- [data/raw/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/README.md)
- [data/derived/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/README.md)
- [audit/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/README.md)
