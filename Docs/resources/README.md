# Spes Bona Southern Africa Resource Rework

## Introduction

This document presents the resource rework for the Spes Bona Southern Africa state set in *Victoria 3*. The aim is straightforward: when Southern Africa is split into smaller and more specific state scopes, vanilla resource values stop behaving consistently. Some states inherit caps that are too large because they represent a much bigger undivided vanilla area; others end up looking too weak because vanilla captures realized output rather than underlying regional potential.

The readable summary of the proposal is [RESOURCES.xlsx](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/RESOURCES.xlsx). The workbook shows the vanilla baseline beside the proposed SB update for the whole SB scope, for the major regional tags, and for each SB state individually.

## Why

The vanilla map works at a broader level of aggregation than the SB state layout. Once that larger structure is divided, three inconsistencies become visible.

1. A single vanilla cap often covers several distinct SB regions.
   The Cape, Transvaal, and Namibian splits are the clearest examples. A broad vanilla number can be reasonable for the old state, but disproportionate once that same space is divided into smaller scopes.
2. Vanilla often reflects realized development more than regional potential.
   This matters most for `Arable Land` and `Wood`. Fertile but underdeveloped regions can look too poor, while land-poor but highly developed regions can look too strong if only output is considered.
3. Resource identity is uneven across the SB scope.
   Some states are broad mixed economies, some are enclave mining regions, and some are dry pastoral systems. A single vanilla-style heuristic does not handle all three well.

The rework therefore aims to make the SB states internally consistent first, and only then comparable to vanilla.

## Methodology

### Scope

The rework covers these 13 SB state scopes:

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

### Core approach

The proposal separates resource families by what they are actually trying to represent.

- Non-land families continue to use observed target evidence and comparator-derived denominators.
- `Arable Land` is treated as **potential effective commercial agricultural hectares**, not as realized crop output.
- `Wood` is treated as **potential effective commercial forestry hectares**, not as surviving plantation estate alone.
- Arable crop yes/no rows are handled separately as gameplay availability rather than as cap drivers.

The public cap formula remains:

```text
final = X + Y - Z
```

Where:

- `X` is the direct target-side quantity
- `Y` is a named upward addition where a bounded missing block must be restored
- `Z` is a downward plausibility haircut where a raw figure overstates a plausible historical ceiling

### Evidence standard

The evidence standard is bounded rather than absolute.

- State-localized evidence is preferred.
- Regional evidence is acceptable only where it clearly overlaps the SB footprint and is explicitly discounted where necessary.
- National claims may appear as context, but broad potential alone does not create a cap.

That standard is especially important for rows like `Lourenço Marques / Wood`, where a national Mozambique forestry claim is not the same thing as a state-specific commercial forestry slot.

### Main data used

The principal maintained inputs are:

- [historical_anchors.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/historical_anchors.csv)
- [modern_maxima.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/modern_maxima.csv)
- [arable_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_target_capacity_rows.csv)
- [arable_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_comparator_capacity_rows.csv)
- [wood_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_target_capacity_rows.csv)
- [wood_comparator_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_comparator_capacity_rows.csv)
- [adjustment_inputs.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/adjustment_inputs.csv)
- [non_arable_benchmark_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/non_arable_benchmark_cases.csv)

## Analysis

The public workbook is organized for comparison rather than for pipeline inspection.

- `Overview` shows SB-wide vanilla totals versus the proposed SB totals.
- The same sheet then aggregates the major regional tags:
  - `CAP` = Cape states
  - `TRN` = Transvaal states
  - `SAF` = South African states
  - `SWA` = Namibian states
- Each state sheet then shows:
  - the vanilla total
  - the proposed SB total
  - the full resource-by-resource comparison
  - the arable-resource yes/no set beside the numeric cap rows

The main machine-readable outputs remain available for anyone who wants to inspect the proposal in more detail:

- [final_resource_caps.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/final_resource_caps.csv)
- [state_delta_summary.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/state_delta_summary.csv)
- [state_resource_deltas.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/state_resource_deltas.csv)

## Problems And What We Did

### Vanilla area inheritance

Several SB states inherit numbers from vanilla spaces that are much larger than the state they now represent. The rework therefore recalculates resource totals at SB-state level instead of simply subdividing vanilla by intuition.

### Vanilla development bias

`Arable Land` and `Wood` were the clearest cases where vanilla-style output logic distorted regional potential. The rework replaced those two families with land-capacity models:

- `Arable Land` now measures potential effective commercial agricultural land
- `Wood` now measures potential effective commercial forestry land

That prevents fertile but underdeveloped regions from reading as barren, while also preventing desert-heavy or scrub-heavy regions from inflating simply because they are large.

### Split-state consistency

The proposal also tries to make neighboring SB states behave consistently as a set. The Cape states, Transvaal states, and Namibian states are therefore shown both individually and as grouped totals in the workbook.

### Remaining limits

Some resource families are still better represented as explicit policy rows than as forced formulas. At present this mainly affects:

- `Whaling`
- `Oil`
- `Rubber`

Those rows stay conservative until stronger localized evidence exists.

## How To Modify / Run

If the resource package needs to be updated:

1. edit the relevant maintained input in [data/raw](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/README.md)
2. rebuild:

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' build
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

If the result should also update the live SB file:

```bash
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' sync-live
python3 '/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/Docs/resources/scripts/resources.py' test
```

The workbook and CSV outputs are regenerated by `build`. The live state file changes only on `sync-live`.

## References

References are stored with the rows they support rather than in a detached bibliography.

- non-land observation references live in [historical_anchors.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/historical_anchors.csv) and [modern_maxima.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/modern_maxima.csv)
- arable references live in [arable_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/arable_target_capacity_rows.csv)
- wood references live in [wood_target_capacity_rows.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/wood_target_capacity_rows.csv)
- adjustment and exception references live in [adjustment_inputs.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/adjustment_inputs.csv)
- counterevidence and defended-zero references live in [counterevidence_cases.csv](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/counterevidence_cases.csv)

For the full file map:

- [data/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/README.md)
- [data/raw/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/raw/README.md)
- [data/derived/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/data/derived/README.md)
- [audit/README.md](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/Docs/resources/audit/README.md)
