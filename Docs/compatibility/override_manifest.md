# Spes Bona Override Manifest

Target game version: `1.13.10` (Steam build `24689003`)

Minimum tested dependency: Community Mod Framework `1.63.0`, commit `bd92022`. The launcher relationship is `1.63.*`, accepting patch releases while requiring an explicit rebase before a later CMF minor line is permitted.

The canonical machine-readable inventory is `Docs/compatibility/override_inventory.json`. It records every exact-path collision and keyed override with ownership, intended delta, load-order semantics, review date, and pinned source hashes.

Run the complete local gate from the repository root:

```sh
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --tiger
```

The validator first queries GitHub's latest stable CMF release and synchronizes its verified official asset into `../Community Mod Framework`. A newly published minor release is installed normally and then fails SB's pinned compatibility gate, deliberately forcing a rebase. `--skip-cmf-sync` is available for offline work only. Missing game or Tiger installations report `SKIP`; a release build must run the explicit comparison against Victoria 3 `1.13.10` and the synchronized CMF installation.

On Depro's development machine, the canonical path is `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`. Its contents remain byte-for-byte from the latest verified GitHub release asset rather than carrying launcher-specific local metadata edits.

## Inventory Surface

The current lock covers:

- `36` exact-path files;
- `102` keyed `REPLACE`, `TRY_REPLACE`, or `REPLACE_OR_CREATE` objects;
- `17` intentionally changed state-region blocks; and
- no approved `replace_path` directives.

The exact-path set includes Southern African history, the Highveld event baseline, the regional state file, the province raster, terrain, locators, and spline network. Generated and binary files use hash parity; textual files also require a reviewed source diff.

`common/history/treaties/00_historical_treaties.txt` remains an exact-path Vanilla shadow because startup treaty rows cannot be removed additively. It is pinned to Vanilla `1.13.10`; uniquely named third-party treaty files remain additive. SB does not replace or register `on_treaty_ports_inherited`, leaving the new 1.13.10 inheritance prompt and market reconnection path to Vanilla.

`common/history/diplomacy/00_relations.txt` retains Vanilla's `1.13.10` relation baseline and removes only ORA's relation to TRN. SB does not create TRN at game start, so the upstream row otherwise attempts to create a relation with an invalid country; later TRN diplomacy remains story-authored.

## Dependency Rebases

The five retained political-movement replacements are pinned to CMF `1.63.0`. Cultural Supremacy includes CMF 1.63's Vanilla 1.13.10 unowned-homeland and neighbouring-movement scope fixes; the only SB-specific delta is CAP creation/disband exclusion. The other retained movement deltas remain the documented CAP exclusion or Anglo-African utilitarian eligibility.

The company replacements are intentionally narrow:

- `company_mozambique_company` retains Vanilla level-five player eligibility and presentation. POR/IBE AI may establish from an existing level-two cotton or tea plantation, may pursue construction before incorporation, and receives a total AI weight of `100`.
- `company_de_beers` retains the Vanilla 1.13.10 structure while replacing gold-field requirements and targets with SB diamond mines.

Vanilla's additive `on_company_disbanded` handler remains untouched. SB registers exactly one separate Mozambique cleanup handler.

The Armed Forces definition is a keyed Vanilla `1.13.10` rebase. Its only SB delta consumes Imperial Administration's displayed flat `+50` Aristocrat attraction modifier; CMF `1.63.0` does not replace this object. The upstream source and object hashes are pinned so later military-interest-group changes require an explicit rebase.

The Colonial Racialism amendment is a keyed Vanilla `1.13.10` rebase. Its only SB delta permits Rural Folk carrying Settler Colonialist to sponsor the amendment; Vanilla's approval gate and existing Armed Forces and Industrialist sponsors remain unchanged.

The `pink_map` decision is pinned to its Vanilla 1.13.10 object. Its DLC, independence, Portuguese Colonialism, and one-use gates remain unchanged; SB adds only colonial/company-subject colonization eligibility and routing through the durable Bechuanaland terminal outcome. The Vanilla Pink Map JE, presentation, modifiers, and favour transaction remain authoritative.

## CMF 1.63 Integration

The Bechuanaland Corridor uses CMF 1.63.0's journal-scope and International Situation interfaces:

- the CMF title setters project both titles for the situation widgets; and
- `com_container` is the supported test-time inspector.

The engine exposes the corridor as one contextless JE shared by its involved countries, so SB addresses that singleton through the standard `je:` link and projects its container-backed actor scopes and score directly. Its launcher dependency is pinned to `1.63.*`, so an older CMF build is intentionally unsupported rather than maintained through duplicate inline implementations.

One named container, `sb_bechuanaland_corridor_state`, owns all shared active-crisis state. SB ships no journal GUI replacement and no container debug UI.

The validator pins these CMF APIs and Vanilla's treaty-port/company-disband hooks. Upstream removal or signature drift fails validation instead of silently changing SB behavior.

## State And Naming Policy

The changed state regions are `STATE_BECHUANALAND`, `STATE_BOTSWANA`, `STATE_CAPE_COLONY`, `STATE_DRAKENSBERG`, `STATE_EASTERN_CAPE`, `STATE_EAST_TRANSVAAL`, `STATE_GRIQUALAND_WEST`, `STATE_HEREROLAND`, `STATE_LOURENCO_MARQUES`, `STATE_NAMAQUALAND`, `STATE_NORTHERN_CAPE`, `STATE_NORTHERN_TRANSVAAL`, `STATE_TRANSVAAL`, `STATE_VRYSTAAT`, `STATE_ZAMBEZI`, `STATE_ZAMBEZIA`, and `STATE_ZULULAND`.

Additive definitions use `sb_<feature>_*`. Intentional late keyed replacements use `zz_sb_*` or `zzz_sb_*`. Stable event and public script keys are not renamed during cleanup.

CMF-style detection remains available through:

- `spes_bona_is_active`
- `spes_bona_southern_africa_map_rework_active`
- `spes_bona_population_rework_active`

Static parity does not certify engine behavior. Required launch checks are maintained in `Docs/compatibility/1_13_10_runtime_matrix.md`.
