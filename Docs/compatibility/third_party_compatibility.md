# Third-Party Compatibility Notes

Target game version: `1.13.8`

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

`STATE_CAPE_COLONY`, `STATE_EASTERN_CAPE`, `STATE_NORTHERN_CAPE`, `STATE_VRYSTAAT`, `STATE_TRANSVAAL`, `STATE_EAST_TRANSVAAL`, `STATE_NORTHERN_TRANSVAAL`, `STATE_DRAKENSBERG`, `STATE_ZULULAND`, `STATE_BOTSWANA`, `STATE_NAMAQUALAND`, `STATE_HEREROLAND`, `STATE_ZAMBEZI`, `STATE_ZAMBEZIA`, and `STATE_LOURENCO_MARQUES`.

Mods editing those regions need a compatibility patch. Mods editing unrelated regions should not need map compatibility work.

## Treaty Replace Path

Spes Bona still uses:

```txt
replace_path="common/history/treaties"
```

This is intentional. The replacement file is rebased to vanilla `1.13.8` and only changes the South African startup treaty block. Additive SB treaties live in `common/history/treaties/sb_treaties.txt`.

## File Naming Rule

SB-specific additive content uses `sb_<feature>_*` filenames. Intentional load-order overrides use `zz_sb_<feature>_override(s)` or `zzz_sb_<feature>_override(s)` when the file must load after other overrides. Vanilla-name history/map files should not be added except for the approved treaty override.

Milestone names such as `phase2`, `phase3`, `wave`, or `misc` should not be used for active script files, scripted effects, variables, or comments. Event IDs are treated as stable public API and should not be renamed during hygiene passes.
