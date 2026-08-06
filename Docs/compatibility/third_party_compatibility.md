# Third-Party Compatibility Notes

Target game version: `1.13.9`

Validation note: Tiger is useful for parser validation on 1.13.9, but launch logs and fresh-start smoke tests remain authoritative for runtime compatibility.

Spes Bona is a Southern Africa map, population, and flavor overhaul. It should not change Japan, Australia, North Africa, the Middle East, or other non-SB map scopes.

## Detection

Other mods can detect Spes Bona with:

```txt
spes_bona_is_active = yes
spes_bona_southern_africa_map_rework_active = yes
spes_bona_population_rework_active = yes
```

These are CMF-style triggers defined with `REPLACE_OR_CREATE`.

## Main Compatibility Risks

Spes Bona changes these state regions:

`STATE_CAPE_COLONY`, `STATE_EASTERN_CAPE`, `STATE_NORTHERN_CAPE`, `STATE_VRYSTAAT`, `STATE_TRANSVAAL`, `STATE_EAST_TRANSVAAL`, `STATE_NORTHERN_TRANSVAAL`, `STATE_DRAKENSBERG`, `STATE_ZULULAND`, `STATE_BOTSWANA`, `STATE_BECHUANALAND`, `STATE_GRIQUALAND_WEST`, `STATE_NAMAQUALAND`, `STATE_HEREROLAND`, `STATE_ZAMBEZI`, `STATE_ZAMBEZIA`, and `STATE_LOURENCO_MARQUES`.

Mods editing those region blocks need a compatibility patch. Spes Bona also ships global province-raster, terrain, locator, spline-network, and journal-GUI baselines, so an otherwise unrelated map or UI mod can still collide at file level. The exhaustive, hash-pinned surface is recorded in `override_inventory.json` and enforced by `tools/check_override_inventory.py`.

## Treaty History Compatibility

Spes Bona does not replace the treaty-history directory. Its exact-path `common/history/treaties/00_historical_treaties.txt` shadows the Vanilla file and changes only the South African startup treaty block; uniquely named third-party treaty files remain additive. SB-only treaties live in `common/history/treaties/sb_treaties.txt`.

A mod that also supplies `common/history/treaties/00_historical_treaties.txt` remains an exact-path conflict: the higher-priority file wins, so combining both sets of changes requires a compatibility patch. Directory-level `replace_path` is prohibited because it would discard every uniquely named treaty file from lower-priority mods.

## Keyed Global Overrides

Several SB definitions are global keyed replacements even when their design goal is Southern African: dominion action/type, stake-colonial-claim, abolish-monarchy, commander retirement, frontier-colonization and slavery laws, ideologies, technologies, state traits, and political movements. The inventory identifies each object and its upstream source. The retained movement objects are rebased to Community Mod Framework `1.58.2`; mods that replace the same keys after SB may supersede the CAP exclusions.

## File Naming Rule

SB-specific additive content uses `sb_<feature>_*` filenames. Intentional load-order overrides use `zz_sb_<feature>_override(s)` or `zzz_sb_<feature>_override(s)` when the file must load after other overrides. New Vanilla-name history/map files require an entry in the machine-checked override inventory.

Milestone names such as `phase2`, `phase3`, `wave`, or `misc` should not be used for active script files, scripted effects, variables, or comments. Event IDs are treated as stable public API and should not be renamed during hygiene passes.
