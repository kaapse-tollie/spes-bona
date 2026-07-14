# Spes Bona Override Manifest

Target game version: `1.13.9`

Migration validation rule: Tiger is again useful for parser validation on 1.13.9, but launch logs and fresh-start smoke tests remain authoritative for runtime compatibility.

This file tracks intentional compatibility risks. New broad vanilla-file copies should not be added without updating this manifest.

## Approved Replace Path

`replace_path="common/history/treaties"`

Reason: vanilla starts several Southern African treaty relationships that Spes Bona suppresses or reshapes before gameplay begins. Treaty history has no keyed `REPLACE` equivalent that cleanly removes vanilla startup treaties without runtime notification spam.

Current rule: `common/history/treaties/00_historical_treaties.txt` must stay rebased to vanilla `1.13.9`, with only the South African treaty block intentionally different. Additional SB-only treaties belong in `common/history/treaties/sb_treaties.txt`.

## Same-Path Vanilla Files

Same-path vanilla files are allowed only when the engine loads vanilla data alongside additive SB data and there is no safe keyed suppression path. These files must stay rebased to vanilla `1.13.9`, with only the documented country or Southern Africa blocks changed.

Approved same-path exceptions:

- `map_data/state_regions/04_subsaharan_africa.txt`: required because state-region keys/provinces are not safe as additive definitions; additive SB state regions duplicate vanilla province cache entries.
- `common/history/pops/04_subsaharan_africa.txt`: required to replace vanilla starter pop rows in SB-touched state scopes without double-loading vanilla rows.
- `common/history/buildings/04_subsaharan_africa.txt`: required to suppress vanilla TRN/SAF regional startup buildings and replace SB-touched state scopes.
- `common/history/military_formations/07_military_formations_subsaharan_africa.txt`: required to suppress vanilla SAF startup formations while preserving unaffected regional formations.
- `common/history/military_formations/00_military_formations_europe.txt`: required to redistribute Portugal's fixed starting battalions into Angola and Zambezia; military-formation history has no keyed country replacement or scriptable unit-removal effect. The file is vanilla `1.13.9` except for the `POR` block.
- `common/history/states/00_states.txt`: required because vanilla state history creates old province ownership against SB split state regions, producing cross-region `create_state` errors.
- `common/history/characters/saf - south africa.txt`: required to keep SAF as a formable-only tag and prevent vanilla SAF characters from spawning at game start.

The following broad files remain retired:

- `map_data/state_regions/03_north_africa.txt` -> removed
- `map_data/state_regions/08_middle_east.txt` -> removed

## State Regions Intentionally Replaced

`map_data/state_regions/04_subsaharan_africa.txt` replaces only these SB state-region blocks:

- `STATE_BOTSWANA`
- `STATE_CAPE_COLONY`
- `STATE_DRAKENSBERG`
- `STATE_EASTERN_CAPE`
- `STATE_EAST_TRANSVAAL`
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

Compatibility impact: mods that also redefine these state regions need a manual compatibility patch. Other 1.13 map regions should remain vanilla-owned.

## History Baselines Intentionally Replaced

State ownership/history is limited to the same Southern African scope in `common/history/states/00_states.txt`.

Population baseline replacements are in `common/history/pops/04_subsaharan_africa.txt`. Each touched `region_state` clears vanilla starter pops before recreating SB rows. `STATE_KAZEMBE` is included only to remove a vanilla umbrella `nguni` starter row and replace it with a concrete local culture.

Building baseline replacements are in `common/history/buildings/04_subsaharan_africa.txt`. Each touched `region_state` calls `sb_purge_starting_buildings_effect` before recreating SB rows.

## CMF Detection Triggers

Spes Bona exposes these `REPLACE_OR_CREATE` triggers for Community Mod Framework interoperability:

- `spes_bona_is_active`
- `spes_bona_southern_africa_map_rework_active`
- `spes_bona_population_rework_active`

## Naming Conventions

Additive files should use `sb_<feature>_*` names that identify the system they implement. Intentional load-order overrides should use `zz_sb_<feature>_override(s)` or `zzz_sb_<feature>_override(s)` and carry a short header explaining why keyed replacement or late load order is required.

Do not use internal milestone names such as `phase2`, `phase3`, `wave`, or `misc` in active script filenames, scripted effects, variables, or comments. Event IDs are stable public API and should not be renamed in cleanup passes.

## Hard `REPLACE` Categories

The remaining hard `REPLACE`/`REPLACE_OR_CREATE` usage is intentionally limited to keyed script objects where vanilla behavior must be altered:

- Boer/Natal/SAF dynamic country names and flags.
- Southern African country-definition tier/culture overrides.
- Boer slavery-law replacements and frontier colonization-law replacement.
- Vanilla Highveld JE/scripted-button disablement.
- Southern Africa dynamic state-name dispatcher.
- Southern Africa strategic/geographic region overrides.
- Character template and interaction overrides for SB ruler/general handling.
- Political movement overlap overrides where CMF has no narrower hook yet.
- `state_trait_severe_malaria` adjustment used by the SB map/resource pass.

Any new hard replacement should include a local comment explaining why additive script or a CMF hook was insufficient.

Current feature-specific override files include:

- `common/character_interactions/zz_sb_commander_retirement_override.txt`
- `common/country_definitions/zz_sb_southern_africa_country_definition_overrides.txt`
- `common/ideologies/zz_sb_reformer_ideology_override.txt`
- `common/journal_entries/zz_sb_highveld_vanilla_overrides.txt`
- `common/scripted_buttons/zz_sb_highveld_vanilla_overrides.txt`
- `common/political_movements/zz_sb_cultural_majority_movement_override.txt`
- `common/political_movements/zz_sb_minority_rights_movement_override.txt`
- `common/political_movements/zz_sb_religious_majority_movement_override.txt`
- `common/political_movements/zzz_sb_cape_political_movement_overrides.txt`
