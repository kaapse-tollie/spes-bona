# Spes Bona Southern Africa Resource Rework

## Introduction

This document sets out the Southern Africa resource rework used by *Spes Bona - A Southern Africa Flavour Pack*.

We intend it to stand on its own. A third party reading only this file, the maintained raw tables, and the public workbook should be able to answer:

1. what problem the rework is solving
2. what each resource family is meant to measure
3. how target rows and comparator rows are built
4. how caps are calculated
5. how evidence quality is handled
6. what still remains formula-driven, and what remains explicit policy

The human-readable output is [RESOURCES.xlsx](./RESOURCES.xlsx). The machine-readable outputs sit under [data/derived](./data/derived/README.md).

## Why

We reworked the resource package because vanilla resources become inconsistent once the Southern Africa region is split into SB states.

There are three recurring problems:

1. Vanilla capacities are attached to much larger state scopes than the SB map uses.
2. Vanilla often mixes actual 1836 setup, later industrial development, and loose gameplay balance without making the boundary between them explicit.
3. Some industries that matter historically or counterfactually in Southern Africa are missing, while other rows inherit values that make sense only at a much larger geography.

So the goal here is not to preserve vanilla totals mechanically. The goal is to produce a coherent SB-state resource map with:

- clear target-side evidence
- clear comparator-side logic
- clear cap arithmetic
- clear rules for when a row is formula-driven, and when it stays an explicit exception

## Methodology

### Scope

The package covers these 14 SB states:

- Cape Colony
- Northern Cape
- Eastern Cape
- West Transvaal
- Eastern Transvaal
- Northern Transvaal
- Transorangia
- Zululand
- Drakensberg
- Botswana
- Lourenço Marques
- Zambezi
- Hereroland
- Namaqualand

The public workbook also reports aggregate changes for these regional tags:

- `CAP` = Cape states
- `TRN` = Transvaal states
- `SAF` = South African states
- `SWA` = Namibian states

### State binding rule

Every SB state is audited against its **full split-state footprint first**. Only after that do we localize specific rows to narrower belts, districts, corridors, estates, or mineral fields.

That distinction is strict:

- full-state scope defines what geography is in scope for the row family
- row-level localization narrows evidence **inside** that footprint
- a localized belt must never redefine the state itself

This matters especially for the split and corridor states:

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

When a row note later says something like `Eastern Highlands`, `Maputo-Gaza lowland`, `Otavi-Grootfontein pocket`, or `KwaZulu-Natal littoral`, that is row localization only. It is not the state definition.

### Common cap formula

Across all numeric resource rows we use the same public cap formula:

```text
F = X + Y - Z
cap = ceil(F / denominator)
```

Where:

- `X` is the direct target-side quantity
- `Y` is a bounded addition for a specifically identified omitted block
- `Z` is a bounded downward haircut where the raw target-side quantity overstates a plausible cap

Not every family uses all three terms. In the land-capacity families, `X` usually does almost all of the work and `Y` / `Z` are rare.

### Family split

We do not treat the package as one universal model. Different resource families are trying to measure different things, so we separate them.

#### 1. Non-land output families

These remain output-based:

- `Coal Mine`
- `Iron Mine`
- `Gold Fields`
- `Gold Mine`
- `Lead Mine`
- `Sulfur Mine`
- `Fishing`

These rows use:

- standardized target-side output
- a representative-year selector
- normalization into a common `1940-equivalent` output frame
- comparator-derived denominators

#### 2. Land-capacity families

These do not use realized output as the main cap basis. We use them to measure effective commercial land:

- `Arable Land`
- `Wood`
- `Rubber (undiscovered)`

These rows use:

- direct target-side effective hectares
- comparator-side effective hectares per vanilla cap
- no GDP-selected output transform as the main cap driver

#### 3. Explicit exception families or rows

Some rows still remain explicit policy rather than fake formulas:

- `Whaling`
- `Oil`
- `Rubber (discovered)`

We keep those as explicit exceptions because the package still does not contain a localized quantitative chain strong enough to justify formula-driven `X`.

### Non-land protocol

#### Target-side output

For the non-land families, we take a real-world output series and standardize it into a canonical unit.

The maintained target-side sources are:

- [historical_anchors.csv](./data/raw/historical_anchors.csv)
- [modern_maxima.csv](./data/raw/modern_maxima.csv)

Each row is:

1. mapped into a resource family
2. standardized into a common unit
3. assigned to a growth family
4. normalized into a `1940-equivalent` output value

The `1940-equivalent` frame is the live v3 baseline. Year selection and output normalization now use the same target horizon, which removes the older mixed selector/normalization split.

#### What `1940-equivalent` means

`1940-equivalent` does not mean we are literally trying to set every non-land row to a 1940 output target.

It means that target rows and comparator rows are translated into one common normalization frame before denominator arithmetic is done. That lets one comparator pool be used coherently even when the raw observations come from different years.

This is why the generated outputs still refer to fields such as:

- `normalized_1940_output`
- `wheat_equivalent_1940_output`
- `historical_1940_equivalent_output`

That naming is intentional. The generated schema now reflects the same `1940-equivalent` frame the builder actually uses.

#### GDP selector: now anchored to GBR 1940

The representative-year selector for non-land families is GDP-based, but GDP is only used to select the target year. We do not use GDP to rescale output directly.

The GDP source is the frozen Maddison Project derivative chain:

- [mpd2023_web.xlsx](./data/raw/mpd2023_web.xlsx)
- [gdp_reference_anchor.csv](./data/raw/gdp_reference_anchor.csv)
- [gdp_per_capita_series.csv](./data/raw/gdp_per_capita_series.csv)
- [gdp_geography_map.csv](./data/raw/gdp_geography_map.csv)

In v3, the reference anchor is:

```text
Great Britain, 1940
```

We replaced the older postwar British anchor for methodological rather than cosmetic reasons:

- many of the SB target geographies never reach the later postwar British level in a way that gives a stable representative year
- the immediate postwar decade adds war noise that is not useful as a universal selector target
- `GBR 1940` is reachable for a larger share of the relevant African target series while still representing substantial development above a strict 1836 frame

The selection rule is:

1. collect the candidate output years from the row package
2. map the target geography to the frozen GDP series where possible
3. compare each candidate year’s GDP per capita to the frozen `GBR 1940` anchor
4. select the candidate year whose GDP per capita is closest to that anchor

That is the live rule. We do **not** use a generic band search around the GDP match.

#### Peak override

We do retain a peak override, but we keep it constrained.

The live rule is:

- keep the representative-year selector described above
- allow an explicit peak row only where the sector clearly has depletion, recovery, or comparable structural distortion
- keep the materiality threshold at the current live level rather than replacing it with a free-form peak search

In practical terms, we keep the existing `>15%` style peak materiality gate unless later evidence forces a different constant. A peak row is not a general excuse to cherry-pick the highest number in a nearby range.

#### Comparator pools

The non-land comparator registry is:

- [non_arable_benchmark_cases.csv](./data/raw/non_arable_benchmark_cases.csv)

For each comparator row:

1. the historical and optional peak observations are standardized
2. each is normalized to a `1940-equivalent` output
3. the representative comparator year is selected by the `GBR 1940` GDP rule
4. the selected normalized output is divided by the comparator’s vanilla cap

The family denominator is then:

```text
A_family = mean_i( selected_1940_equivalent_output_i / vanilla_cap_i )
```

Where possible, we build the comparator family around 20 comparator rows.

### Arable Land protocol

For `Arable Land`, we no longer use realized crop output as the main cap basis.

It measures:

```text
potential effective commercial agricultural hectares
```

#### Arable classes and weights

The current arable classes are stored in [arable_land_class_weights.csv](./data/raw/arable_land_class_weights.csv):

- `irrigated_perennial = 1.25`
- `reliable_rainfed_crop = 1.00`
- `mixed_farming = 0.75`
- `commercial_pasture = 0.40`
- `marginal_grazing = 0.15`
- `desert_or_unusable = 0.00`

These are weighted classes rather than raw-hectare classes. We do that deliberately:

- fertile but underdeveloped land should still count
- large dry states should not inflate only because they cover a lot of ground

#### Arable target rows

Target-side arable rows are maintained in [arable_target_capacity_rows.csv](./data/raw/arable_target_capacity_rows.csv).

For each maintained row:

```text
effective_area_ha = raw_area_ha * effective_weight * localization_discount
```

For each state:

```text
X_state = sum( effective_area_ha )
```

#### Arable comparators

Arable does not use one global comparator pool. We use state-local analogue sets.

The comparator ranking source is:

- [agri_rankings.csv](./data/raw/agri_rankings.csv)

The maintained comparator table is:

- [arable_comparator_capacity_rows.csv](./data/raw/arable_comparator_capacity_rows.csv)

Each SB state receives a ranked set of 20 agricultural analogues. Those analogues are weighted by rank band. The denominator logic is:

```text
U_s,k = comparator_effective_hectares / comparator_vanilla_arable_cap
B_s = weighted_mean_k( U_s,k )
A_arable = mean_s( B_s )
```

That produces the shared arable denominator used in the public outputs.

#### Arable crop baskets

The arable basket still exists, but it no longer drives arable cap arithmetic.

The maintained basket file is:

- [arable_baskets.csv](./data/raw/arable_baskets.csv)

In v3 its role is:

- gameplay audit
- crop plausibility
- mismatch reporting against live enabled resources

It does **not** set the arable cap.

### Wood protocol

For `Wood`, we no longer measure observed forestry estate area or generic forest cover.

It measures:

```text
potential effective commercial forestry hectares
```

#### Wood classes and weights

The current wood classes are stored in [wood_land_class_weights.csv](./data/raw/wood_land_class_weights.csv):

- `high_suitability_plantation = 1.00`
- `moderate_suitability_plantation = 0.65`
- `restorable_commercial_forest = 0.40`
- `marginal_forestry = 0.20`
- `noncommercial_wooded_land = 0.05`
- `arid_or_unusable = 0.00`

#### Plantation-first model with capped restoration

Wood is a plantation-first model, but we allow bounded restoration where a historically workable forestry belt was later depleted.

The restoration allowance is hard-capped:

```text
restorable_effective_ha <= 0.5 * (high_effective_ha + moderate_effective_ha)
```

We apply this cap on both the target side and the comparator side. The point is to stop broad “this used to be wooded” claims from becoming a substitute for actual commercial forestry potential.

#### Wood target rows and denominator

The maintained wood target rows are:

- [wood_target_capacity_rows.csv](./data/raw/wood_target_capacity_rows.csv)

The maintained wood comparator table is:

- [wood_comparator_capacity_rows.csv](./data/raw/wood_comparator_capacity_rows.csv)

The legacy seed source remains:

- [wood_comparator_cases.csv](./data/raw/wood_comparator_cases.csv)

The denominator is:

```text
A_wood = mean_i( effective_commercial_forestry_hectares_i / benchmark_vanilla_wood_cap_i )
```

### Rubber protocol

In v3, `Rubber (undiscovered)` joins the land-capacity family.

It now measures:

```text
potential effective commercial plantation hectares
```

`Rubber (discovered)` does **not** join that family in v3. We keep it as an explicit exception unless a separate localized discovered-estate chain is frozen later.

#### Rubber classes and weights

The maintained rubber land classes are stored in [rubber_land_class_weights.csv](./data/raw/rubber_land_class_weights.csv):

- `high_suitability_plantation = 1.00`
- `moderate_suitability_plantation = 0.60`
- `marginal_suitability_plantation = 0.20`
- `unsuitable_or_noncommercial = 0.00`

This is a latent-rubber model. The question is not “where was latex already being exported at scale in 1836?” The question is “where is there a bounded, commercially workable plantation slot that vanilla already treats as latent rubber potential?”

#### Rubber target rows

The maintained target-side rubber table is:

- [rubber_target_capacity_rows.csv](./data/raw/rubber_target_capacity_rows.csv)

The same effective-hectare logic is used:

```text
effective_area_ha = raw_area_ha * effective_weight * localization_discount
X_state = sum( effective_area_ha )
```

We only let this become formula-driven where the evidence is localized enough to support a bounded plantation slot.

#### Rubber comparators

The maintained comparator table is:

- [rubber_comparator_capacity_rows.csv](./data/raw/rubber_comparator_capacity_rows.csv)

The denominator is:

```text
A_rubber = mean_i( effective_rubber_hectares_i / benchmark_vanilla_rubber_cap_i )
```

This is now a dedicated comparator family. We no longer route rubber through the generic non-arable output benchmark path.

### Evidence and provenance rules

Formula-driving target rows carry explicit validation metadata.

The main fields are:

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

1. `state_localized` rows may drive `X` directly.
2. `regional_proxy` and `national_fallback` may drive `X` only when they support a distinct slot and are explicitly discounted.
3. `broad_potential_only` rows do not drive `X`.
4. an indirect or broad regional claim does not silently become local support
5. target-side discounted values, not the undisciplined broad claim, are what feed cap arithmetic

This is the main safeguard against over-reading broad national claims into local SB-state caps.

### Comparators and denominators

We use three denominator systems because the families are genuinely different:

1. global output comparator families for the non-land output rows
2. local ranked agricultural analogue sets for `Arable Land`
3. dedicated hectare-based comparator families for `Wood` and `Rubber (undiscovered)`

That split is intentional. It avoids forcing land-capacity families through output-denominator logic that was built for mines and fisheries.

### Exceptions, defended zeroes, and adjustments

#### `Y`

We use `Y` only where a specifically identified omitted block needs to be added back.

Valid cases are things like:

- an omitted irrigation belt
- an omitted plantation belt
- an omitted plateau block

It is not a generic uplift for “this feels too low”.

#### `Z`

`Z` is now a universal chronology moderator for quantity resources.

It is used where an accepted mine, fishery, or other quantity row is real, but the raw target-side quantity still reflects commercial emergence or a representative benchmark that arrives too late relative to the package target.

The rule uses:

- `e = earliest commercial activity year`
- `r = representative GDP-equivalent year`
- `late_start = max(0, e - 1940)`
- `proxy_lag = max(0, r - max(e, 1940))`

Then:

`penalty = min(1, 0.00275 * late_start * ln(1 + late_start) + 0.01 * proxy_lag)`

and:

`Z = X * penalty`

This is a chronology rule, not a balancing knob. The late-start term is nonlinear and the representative-year lag is linear, so very late proxy years are moderated without reintroducing the earlier double-penalty problem. It does not apply to hectare-based land-capacity families such as `Arable Land`, `Wood`, and `Rubber (undiscovered)`.

#### Explicit exceptions

Some rows remain explicit exceptions because a weak fake formula would be worse than an explicitly documented zero or policy row.

In v3, the clearest examples are:

- `Whaling`
- `Oil`
- `Rubber (discovered)`

#### Defended zeroes

A defended zero does not mean nothing was researched.

It means:

1. the row was reviewed
2. evidence did not justify a distinct commercial slot
3. neighboring or national claims were not allowed to substitute for local support

## Analysis

The package now produces three different kinds of result.

### 1. Output-based non-land rows

These still behave most like the earlier benchmark model, but with a cleaner representative-year selector:

- frozen Maddison GDP
- `GBR 1940` anchor
- constrained peak override
- comparator denominator

### 2. Land-capacity rows

This is now the main place where the package differs structurally from vanilla:

- `Arable Land` is based on effective commercial agricultural land
- `Wood` is based on effective commercial forestry land
- `Rubber (undiscovered)` is now based on effective commercial plantation land

### 3. Remaining explicit-policy rows

We keep these conservative where the source chain is still weaker than a real formula:

- `Whaling`
- `Oil`
- `Rubber (discovered)`

The public workbook presents those outcomes in a readable form, while the detailed audit logic remains in the raw and derived tables.

## Problems And What We Did

### Vanilla areas are too large for the SB split

We rebuilt caps at SB-state scope instead of trying to subdivide vanilla by intuition.

### Vanilla often mixes development and geography

For `Arable Land`, `Wood`, and now `Rubber (undiscovered)`, the package moved away from realized output and toward effective land-capacity models.

### Earlier iterations blurred year selection and output normalization

The v3 protocol makes the distinction explicit:

- the output normalization frame is now `1940-equivalent`
- the GDP selector that chooses the representative year now anchors to `GBR 1940`
- the package keeps peak override, but only as a constrained depletion/recovery tool

### Earlier iterations also let README and code drift apart

This document is meant to stop that drift.

It describes the live protocol:

- the family split
- the GDP selector
- the peak override rule
- the comparator logic
- the provenance rules
- the explicit exception policy

### Current limits

The package still has limits.

The main ones are:

- `Whaling` and `Oil` remain explicit-exception heavy
- `Rubber (discovered)` is still held outside the land-capacity model
- the second counterfactual state-by-state audit still needs to be rerun on the v3 baseline

## How To Modify / Run

### Maintained raw inputs

If you want to change the package, start from the maintained raw tables under [data/raw](./data/raw/README.md).

The most important ones are:

- [historical_anchors.csv](./data/raw/historical_anchors.csv)
- [modern_maxima.csv](./data/raw/modern_maxima.csv)
- [adjustment_inputs.csv](./data/raw/adjustment_inputs.csv)
- [counterevidence_cases.csv](./data/raw/counterevidence_cases.csv)
- [non_arable_benchmark_cases.csv](./data/raw/non_arable_benchmark_cases.csv)
- [arable_land_class_weights.csv](./data/raw/arable_land_class_weights.csv)
- [arable_target_capacity_rows.csv](./data/raw/arable_target_capacity_rows.csv)
- [arable_comparator_capacity_rows.csv](./data/raw/arable_comparator_capacity_rows.csv)
- [wood_land_class_weights.csv](./data/raw/wood_land_class_weights.csv)
- [wood_target_capacity_rows.csv](./data/raw/wood_target_capacity_rows.csv)
- [wood_comparator_capacity_rows.csv](./data/raw/wood_comparator_capacity_rows.csv)
- [rubber_land_class_weights.csv](./data/raw/rubber_land_class_weights.csv)
- [rubber_target_capacity_rows.csv](./data/raw/rubber_target_capacity_rows.csv)
- [rubber_comparator_capacity_rows.csv](./data/raw/rubber_comparator_capacity_rows.csv)

### Evidence policy

Do not delete sourced rows from the append-only evidence tables. Supersede them.

The point of the package is that a later reviewer can still see:

- what used to drive the row
- what replaced it
- why it changed

### Rebuild the package

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' build
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

### Sync accepted changes to the live state file

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' sync-live
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

### State-by-state counterfactual audit

The package also supports the state-pass loop:

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' state-pass
```

The normal sequence during the loop is:

1. select the next state from the tracker
2. apply the accepted row updates for that pass
3. rebuild
4. test
5. stop

Live sync is not part of the ordinary one-state loop. We only run `sync-live`, then test again, once the full loop is accepted and we are ready to release.

## References

### External dataset and frozen GDP derivatives

- [mpd2023_web.xlsx](./data/raw/mpd2023_web.xlsx)
- [gdp_reference_anchor.csv](./data/raw/gdp_reference_anchor.csv)
- [gdp_per_capita_series.csv](./data/raw/gdp_per_capita_series.csv)
- [gdp_geography_map.csv](./data/raw/gdp_geography_map.csv)

### Maintained raw evidence tables

- [historical_anchors.csv](./data/raw/historical_anchors.csv)
- [modern_maxima.csv](./data/raw/modern_maxima.csv)
- [adjustment_inputs.csv](./data/raw/adjustment_inputs.csv)
- [counterevidence_cases.csv](./data/raw/counterevidence_cases.csv)
- [non_arable_benchmark_cases.csv](./data/raw/non_arable_benchmark_cases.csv)
- [arable_land_class_weights.csv](./data/raw/arable_land_class_weights.csv)
- [arable_target_capacity_rows.csv](./data/raw/arable_target_capacity_rows.csv)
- [arable_comparator_capacity_rows.csv](./data/raw/arable_comparator_capacity_rows.csv)
- [arable_baskets.csv](./data/raw/arable_baskets.csv)
- [agri_rankings.csv](./data/raw/agri_rankings.csv)
- [wood_land_class_weights.csv](./data/raw/wood_land_class_weights.csv)
- [wood_target_capacity_rows.csv](./data/raw/wood_target_capacity_rows.csv)
- [wood_comparator_cases.csv](./data/raw/wood_comparator_cases.csv)
- [wood_comparator_capacity_rows.csv](./data/raw/wood_comparator_capacity_rows.csv)
- [rubber_land_class_weights.csv](./data/raw/rubber_land_class_weights.csv)
- [rubber_target_capacity_rows.csv](./data/raw/rubber_target_capacity_rows.csv)
- [rubber_comparator_capacity_rows.csv](./data/raw/rubber_comparator_capacity_rows.csv)

### Public outputs

- [RESOURCES.xlsx](./RESOURCES.xlsx)
- [final_resource_caps.csv](./data/derived/final_resource_caps.csv)
- [resource_denominators.csv](./data/derived/resource_denominators.csv)
- [row_audit.csv](./data/derived/row_audit.csv)
- [target_observations.csv](./data/derived/target_observations.csv)
- [state_resource_deltas.csv](./data/derived/state_resource_deltas.csv)
- [state_delta_summary.csv](./data/derived/state_delta_summary.csv)

### Earlier reasoning retained in the repo

- [resource_proposal.md](../../References/resource_proposal.md)
- [resource_upperbound_audit.md](../../References/resource_upperbound_audit.md)
