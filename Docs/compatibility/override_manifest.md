# Spes Bona Override Manifest

Target game version: `1.13.9` (Steam build `23897342`)

This document explains the policy. The canonical machine-readable inventory is `Docs/compatibility/override_inventory.json`; it records every exact-path collision and keyed override with owner, scope, intended delta, load-order semantics, rebase date, and pinned upstream/mod hashes.

Run the mandatory portable gate from the repository root:

```sh
python3 tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/3385002128' \
  --tiger
```

The suite runs unit, resource, override, map-connectivity, localisation, stale-symbol, and delayed-event lifecycle checks. With proprietary dependencies available, it also compares Vanilla/CMF baselines and runs Tiger. Missing proprietary dependencies report `SKIP`; CI does not require them.

The override gate fails on an unmanifested or stale collision/replacement, upstream drift, mod/object drift, changed state-region membership, dependency-baseline drift, or descriptor version/`replace_path` drift. Hash updates are review actions, not an automatic acceptance workflow.

## Directory replacement policy

No `replace_path` directive is approved. In particular, treaty history must not replace its directory: that would delete uniquely named treaty files from lower-priority mods.

`common/history/treaties/00_historical_treaties.txt` remains an exact-path Vanilla shadow because startup treaties cannot be removed with a keyed `REPLACE`. It is pinned to Vanilla `1.13.9` and changes the Southern African startup block. `common/history/treaties/sb_treaties.txt` is additive. Another mod that owns the exact `00_historical_treaties.txt` path remains a last-writer conflict and requires a compatibility patch if both deltas are wanted.

## Exact-path Vanilla files

The inventory currently locks **37** exact-path files. It includes all of the following compatibility surfaces rather than only the narrow regional exceptions:

- Southern African building, population, state, country, character, military-formation, and treaty histories.
- The Vanilla Highveld event baseline.
- `map_data/state_regions/04_subsaharan_africa.txt`, `map_data/province_terrains.txt`, and the full `map_data/provinces.png` raster.
- All five generated map-object locator files and the full spline-network baseline.
- Both global journal GUI files.

The raster, terrain, locator, spline, and GUI copies are global file-level collisions even where the authored delta is Southern African. Mods changing the same files require explicit compatibility work. The JSON hash pair is the parity lock for binary/generated copies; textual files are also reviewable with an ordinary pinned-upstream diff.

## State regions intentionally changed or added

The inventory mechanically enforces these **17** blocks in `map_data/state_regions/04_subsaharan_africa.txt`:

- `STATE_BECHUANALAND`
- `STATE_BOTSWANA`
- `STATE_CAPE_COLONY`
- `STATE_DRAKENSBERG`
- `STATE_EASTERN_CAPE`
- `STATE_EAST_TRANSVAAL`
- `STATE_GRIQUALAND_WEST`
- `STATE_HEREROLAND`
- `STATE_LOURENCO_MARQUES`
- `STATE_NAMAQUALAND`
- `STATE_NORTHERN_CAPE`
- `STATE_NORTHERN_TRANSVAAL`
- `STATE_TRANSVAAL`
- `STATE_VRYSTAAT`
- `STATE_ZAMBEZI`
- `STATE_ZAMBEZIA`
- `STATE_ZULULAND`

The retired North Africa and Middle East state-region copies remain absent.

## Additive state-trait assignments

`common/history/global/sb_state_traits.txt` changes malaria by scoped history effects rather than additional map-file overrides. Severe malaria is assigned to Eastern/Western Mali, Volta, Hausaland/Outer/East Hausaland, Bornu, Nigeria, North Cameroon, Waddai, North Angola, Lindi, Tanganyika, Kazembe, Rift Valley, and Uganda; Gabon is adjusted in the opposite direction.

## Keyed overrides

The JSON currently locks **101** `REPLACE`, `TRY_REPLACE`, and `REPLACE_OR_CREATE` objects individually, including their source paths and object hashes. The surface includes:

- Southern African character templates, country definitions, names, flags, CoAs, regions, state names, companies, and Highveld replacements.
- Global dominion action/type, stake-colonial-claim, abolish-monarchy, commander-retirement, law, ideology, technology, state-trait, and movement objects whose compatibility risk cannot be described as regional file ownership.
- Three `REPLACE_OR_CREATE` CMF detection triggers.

The five retained political-movement replacements are additionally pinned to Community Mod Framework `1.58.2` baselines; their only SB deltas are the documented CAP creation/disband exclusions and Anglo-African utilitarian eligibility. Religious-majority is no longer replaced because it had no authored SB delta.

A manifest entry means “reviewed and mechanically contained,” not that every broad override is ideal. Open compatibility findings continue to track objects that should be rebased, narrowed, or upstreamed to CMF.

## History baseline rules

Touched state scopes purge/recreate their startup populations and buildings so Vanilla rows do not double-load. Portugal and Southern African military-formation histories remain exact-path baselines where the engine offers no keyed row-removal mechanism. New Vanilla-name history/map files are prohibited until added to the inventory with an explicit intent and parity review.

## Naming and interoperability

Additive definitions use `sb_<feature>_*`. Intentional late keyed replacements use `zz_sb_*` or `zzz_sb_*` and carry a local reason. Internal milestone names are not active API. Event IDs remain stable.

CMF detection is provided by:

- `spes_bona_is_active`
- `spes_bona_southern_africa_map_rework_active`
- `spes_bona_population_rework_active`

Tiger remains useful for parser validation, but fresh-start logs and focused engine tests remain authoritative for runtime and load-order behavior.
