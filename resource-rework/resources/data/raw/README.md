# Raw Inputs

These are the maintained inputs for the public resource package.

Maintained evidence rows now carry lifecycle metadata during the state-audit loop:

- `row_id`
- `row_status`
- `supersedes_row_id`
- `state_pass_index`
- `changed_on`
- `change_reason`

The rule is append-only for the maintained evidence tables that drive or constrain public rows. New evidence supersedes old rows; it does not delete them.

## Formula-driving

- `historical_anchors.csv`
  - frozen target and comparator observations for non-land families
- `modern_maxima.csv`
  - modern target and comparator observations for non-land families
- `arable_target_capacity_rows.csv`
  - target-side potential effective commercial agricultural hectares
- `arable_comparator_capacity_rows.csv`
  - comparator-side effective agricultural hectares per cap
- `wood_target_capacity_rows.csv`
  - target-side potential effective commercial forestry hectares
- `wood_comparator_capacity_rows.csv`
  - comparator-side effective commercial forestry hectares per cap
- `adjustment_inputs.csv`
  - explicit `Y`, `Z`, floor, constrained-zero, and exception policy
- `non_arable_benchmark_cases.csv`
  - authoritative comparator registry for non-land families
- `gdp_reference_anchor.csv`
  - frozen GBR 1940 anchor for non-land year selection
- `gdp_per_capita_series.csv`
  - non-land GDP selector series
- `gdp_geography_map.csv`
  - entity-to-GDP geography mapping
- `family_normalising_constants.csv`
  - fixed public constants used by the builder

## Supporting Source Material

- `growth_anchor_series.csv`
  - non-land growth scaffolding
- `agri_rankings.csv`
  - ranked local comparator sets for arable
- `arable_baskets.csv`
  - crop-suitability and gameplay audit layer
- `arable_land_class_weights.csv`
  - arable effective-hectare class weights
- `wood_land_class_weights.csv`
  - wood effective-hectare class weights
- `counterevidence_cases.csv`
  - defended counterevidence and explicit-zero cases
- `vanilla_priors.csv`
  - vanilla baseline for caps and crop yes/no rows
- `state_metadata.csv`
  - SB state ids, sheet keys, and vanilla proxies
- `wood_comparator_cases.csv`
  - retained only as seed material for the maintained wood comparator-capacity table

Use [../README.md](../README.md) for the package-level classification rule.
