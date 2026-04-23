# Resource Extension Spec

This note records the implementation direction for resource behavior that should sit outside the base cap workbook.

The base resource package answers:

- what resource rows exist
- what their caps are
- what evidence justifies those caps

This extension layer answers a different question:

- when a resource should become usable
- when a resource should stay present but gated
- how a Southern Africa-specific company should specialize that resource

## Core rule

For arable crops, we do not try to mutate the state's `arable_resources` list at runtime.

Reason:

- the state-region layer is static
- the exposed state effects include `add_arable_land`, `activate_building`, `deactivate_building`, and `remove_building`
- there is no exposed `add_arable_resource` or `remove_arable_resource` effect for plantation crop types
- vanilla resource discovery is a separate system used for discoverable resource groups like gold, oil, and rubber, not tea

So for crop extensions, the correct pattern is:

1. keep the crop in the state's `arable_resources` if the state has that long-run potential
2. gate actual building access through the building definition with `unlocking_technologies`, `possible`, or `can_build`

This keeps the map logic static and the gameplay logic dynamic.

## Chosen extension layers

### 1. Tech-gated arable extensions

Use this when a state should have the long-run potential for a crop, but should not be able to build it from day 1.

Implementation direction:

- state-region file: include the crop in `arable_resources`
- building definition: gate construction by technology in `possible` or `can_build`
- scope: state-aware, not global, when the gate is only meant for one SB state

This is the chosen pattern for Cape tea.

### 2. Company extensions

Use this when a state or regional economy should be differentiated through a named firm, charter, or specialization bonus instead of higher raw caps.

Implementation direction:

- define a flavored company type in `common/company_types/`
- give it a Southern Africa `potential` and a state or region-specific `possible`
- use `preferred_headquarters` where the geography is part of the identity
- localize the company name and any prestige-good text in `localization/english/`

### 3. Prestige-good extensions

Use this when the goal is not a brand-new market good, but a recognized premium or regional specialty inside an existing good family.

This is the preferred path for rooibos.

Reason:

- it keeps the market model simple
- it matches the existing company/prestige-goods surface better than inventing a full new good chain
- it avoids expanding pop needs, production chains, and AI behavior for a one-region specialty

If we later decide that `rooibos` needs to be a real standalone good instead of a prestige specialization of `tea`, that is a separate economic-expansion project and should not be mixed into this first extension pass.

## Cape Colony tea

### Decision

Cape Colony tea should be treated as a tech-gated arable extension, not as a runtime-discovered resource.

### Chosen pattern

- `STATE_CAPE_COLONY` may carry `building_tea_plantation` in `arable_resources`
- access to `building_tea_plantation` in Cape Colony should then be gated through the building definition
- the gate should be state-specific, so existing tea states are not unintentionally slowed down

### Why this pattern

It solves the gameplay problem cleanly:

- the state has the potential
- the player cannot exploit it immediately
- the gate can be tied to technology instead of fake low caps or late event-driven slot edits

### Implementation hooks

- [`/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Spes Bona - A Southern Africa Flavour Pack/map_data/state_regions/04_subsaharan_africa.txt`](/Users/depro/Documents/Paradox%20Interactive/Victoria%203/mod/Spes%20Bona%20-%20A%20Southern%20Africa%20Flavour%20Pack/map_data/state_regions/04_subsaharan_africa.txt)
- vanilla reference for tea building unlock:
  [`/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/04_plantations.txt`](/Users/depro/Library/Application%20Support/Steam/steamapps/common/Victoria%203/game/common/buildings/04_plantations.txt)
- vanilla building trigger surface:
  [`/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/buildings/buildings.md`](/Users/depro/Library/Application%20Support/Steam/steamapps/common/Victoria%203/game/common/buildings/buildings.md)

### Implementation rule

The building gate should follow this shape:

```txt
possible = {
    OR = {
        NOT = { state_region = s:STATE_CAPE_COLONY }
        owner ?= { has_technology_researched = <chosen_tech> }
    }
}
```

This is the rule being specified here. The exact technology key is an implementation choice to be fixed when the extension is actually built.

## Southern Africa company expansion

### Decision

We should expand companies for the SB scope as a separate flavor and specialization layer.

This layer should not be used to hide weak resource methodology. It should be used where a named firm, product tradition, or export niche is the right expression of regional identity.

### First target: Rooibos Ltd

`Rooibos Ltd` is the first explicit company candidate.

### Chosen pattern

`Rooibos Ltd` should be a flavored Southern Africa company built on the tea plantation chain, with `rooibos` treated as a special tea product rather than as a brand-new base market good.

That means:

- company type anchored to Cape geography
- tea plantations as the core building type
- optional extension building types only if they support the same Cape export profile
- a prestige-good style specialization path for `rooibos`

### Why this pattern

It captures the point of the mechanic:

- Cape gets a distinctive tea-related export identity
- the company layer expresses product differentiation
- the resource layer stays responsible only for whether tea can exist there at all

### Implementation hooks

- mod company definitions:
  `common/company_types/`
- mod dynamic names:
  `common/dynamic_company_names/`
- country/company history if we want a start-date or scripted grant:
  `common/history/countries/`
- prestige-good reference surface:
  [`/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/journal_entries/05_prestige_goods.txt`](/Users/depro/Library/Application%20Support/Steam/steamapps/common/Victoria%203/game/common/journal_entries/05_prestige_goods.txt)
- vanilla company references:
  [`/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/company_types/99_basic_companies.txt`](/Users/depro/Library/Application%20Support/Steam/steamapps/common/Victoria%203/game/common/company_types/99_basic_companies.txt)
  [`/Users/depro/Library/Application Support/Steam/steamapps/common/Victoria 3/game/common/company_types/00_companies_soi.txt`](/Users/depro/Library/Application%20Support/Steam/steamapps/common/Victoria%203/game/common/company_types/00_companies_soi.txt)

### Rooibos Ltd shape

The intended company shape is:

- `flavored_company = yes`
- `preferred_headquarters = { STATE_CAPE_COLONY }`
- `building_types = { building_tea_plantation }`
- Southern Africa or Cape-specific `potential`
- Cape-specific `possible`
- prosperity bonus or prestige-good path tied to tea specialization

If prestige-goods support is available in the active content setup, `rooibos` should be implemented as a prestige-good style specialization attached to the company.

If prestige-goods support is not available, the fallback is:

- keep `Rooibos Ltd` as a flavored tea company
- use prosperity modifiers and localization flavor only
- do not create a fake standalone `rooibos` good

## Scope boundaries

This spec does not change the current resource workbook methodology.

It only defines how future extensions should be layered on top of it.

Specifically:

- resource caps still belong to the resource package
- tech-gated crop access belongs to the extension layer
- named companies and prestige specializations belong to the company layer

## Chosen direction

The decisions locked by this spec are:

1. Cape tea, if added, should be present as a state potential and gated through the tea building, not discovered dynamically.
2. Southern Africa should get a dedicated company-expansion pass.
3. `Rooibos Ltd` should be treated as a Cape flavored tea company.
4. `rooibos` should be implemented first as a prestige-good style tea specialization, not as a standalone good.
