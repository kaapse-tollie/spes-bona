# Spes Bona Override Manifest

Target game version: Victoria 3 `1.14.0` Open Beta 1 (Steam build `25081502`, Steam branch `1.14-openbeta`, core depot manifest `3868129321396195520`).

Pinned dependency: Community Mod Framework `1.66.0`, commit `807c32ff42b75714a3a0e090c0db3357b5e46ed7`. The launcher relationship is `1.66.*`. Static validation uses the official GitHub `release-1.66.0.zip` asset with SHA-256 `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`; it does not treat the temporarily reverted Workshop payload as authoritative.

The canonical machine-readable inventory is `Docs/compatibility/override_inventory.json`. It records every exact-path collision and keyed override with ownership, intended delta, load-order semantics, review date, and pinned source hashes. The complete OB1 semantic decisions are recorded in `Docs/compatibility/1_14_0_open_beta_1_rebase.md`.

Run the complete local gate from the repository root:

```sh
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework' \
  --tiger
```

The validator reads the exact CMF tag, asset, and digest from the inventory and synchronizes only that verified GitHub release. It fails closed on a different tag, asset, digest, metadata version, installed Steam build, branch, or core depot manifest. `--skip-cmf-sync` is available for offline work only. Tiger's current Victoria 3 `1.14` schema coverage is advisory; the repository's semantic and hash gates remain authoritative.

On Depro's development machine, the canonical CMF path is `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`. Its contents remain byte-for-byte from the verified GitHub release asset rather than carrying launcher-specific local metadata edits.

## Inventory Surface

The OB1 lock covers:

- `37` exact-path files;
- `109` keyed `REPLACE`, `TRY_REPLACE`, or `REPLACE_OR_CREATE` objects;
- `18` intentionally changed state-region blocks;
- one registered additive `zz_` override;
- all eight localization replace files plus key-level, multi-source pins for the 20 previously silent Vanilla key collisions; and
- no approved `replace_path` directives.

The exact-path set includes Southern African history, the Highveld event baseline, the regional state file, the province raster, terrain, locators, and spline network. Generated and binary files use hash parity; textual files also require a reviewed source diff. Every OB1 source-only drift result is repinned only after a recorded semantic decision.

`common/history/treaties/00_historical_treaties.txt` remains an exact-path Vanilla shadow because startup treaty rows cannot be removed additively. It is pinned to the exact `1.14.0` OB1 payload; uniquely named third-party treaty files remain additive. SB does not replace or register `on_treaty_ports_inherited`, leaving Vanilla's inheritance prompt and market reconnection path untouched.

`common/history/diplomacy/00_relations.txt` retains the OB1 relation baseline except for three explicit startup corrections: it disables the whole Vanilla `c:SAF` block, removes ORA's relation to TRN, and disables the whole Vanilla `c:TRN` block because SAF and TRN do not exist in 1836. Later TRN relations remain story-authored.

## Additive Overrides And Localization Replace Files

Two further override surfaces are inventoried and hash-checked alongside the exact-path collisions above:

1. **Additive `zz_` files** (`additive_overrides`): SB-authored files whose name uses the `zz_sb_*` / `zzz_sb_*` convention but which create new objects instead of replacing an upstream key (currently only `common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt`). Each entry pins the mod file hash and states intent and owner.
2. **Localization replace files** (`localization_replace_files`): every file under `localization/english/replace/`. Entries that shadow an upstream localization file (`country_flavor_text`, `dynamic_state_and_hub_names`, `map/states`) pin both the upstream and mod hashes; SB-authored names record `upstream_file: null` and state why they live in `replace/`.
3. **Key-level Vanilla localization collisions**: every real collision whose source is not represented by a single replace-file path has its key, source file, and source hash pinned. Multiple Vanilla sources for the same SB replace file are tracked separately, so a future change cannot hide behind `upstream_file: null` or a secondary source.

The checker fails on any unregistered `zz_` override-style file, unregistered `replace/` localization, unregistered key collision, or stale source/mod hash. None of these surfaces may bypass the compatibility contract.

## Dependency Rebases

The five retained political-movement replacements are pinned to CMF `1.66.0` and reviewed against Victoria 3 `1.14.0` OB1. Their CMF source files and object bodies are unchanged across this dependency rebase. Cultural Supremacy retains the upstream unowned-homeland and neighbouring-movement scope fixes; the only SB-specific delta is CAP creation/disband exclusion. The other retained movement deltas remain the documented CAP exclusion or Anglo-African utilitarian eligibility.

The company replacements are intentionally narrow:

- `company_mozambique_company` retains the OB1 level-five player eligibility and presentation. POR/IBE AI may establish from an existing level-two cotton or tea plantation, may pursue construction before incorporation, and receives a total AI weight of `100`.
- `company_de_beers` retains the OB1 structure while replacing gold-field requirements and targets with SB diamond mines.

Vanilla's additive `on_company_disbanded` handler remains untouched. SB registers exactly one separate Mozambique cleanup handler.

The Armed Forces definition is a keyed OB1 rebase. Its executable token stream is unchanged upstream; the source drift is comments and formatting only. Its sole SB delta consumes Imperial Administration's displayed flat `+50` Aristocrat attraction modifier. CMF `1.66.0` does not replace this object. Source and object hashes are pinned so later military-interest-group changes require an explicit rebase.

All three OB1 AI incorporation triggers are exact replacements around one narrow helper. `sb_regional_ai_should_incorporate` admits only AI NAL owning `STATE_ZULULAND`, AI CAP owning `STATE_BECHUANALAND` or `STATE_GRIQUALAND_WEST`, and AI ORA owning `STATE_DRAKENSBERG`; each match requires `owner = root`. It is intentionally independent of NAL's narrative lease, population, adjacency, full-state ownership, homeland time, and starting country type. Both ordinary and colonial `will` paths receive the helper because NAL and CAP can cross those country-type branches. `ai_can_incorporate_state` remains a value/transfer-scoring caller rather than the command that starts incorporation. The `will` overrides improve willingness and candidate priority but cannot bypass affordability or code-side candidate validity.

The Colonial Racialism amendment is a keyed OB1 rebase. Its only SB delta permits Rural Folk carrying Settler Colonialist to sponsor the amendment; Vanilla's approval gate and existing Armed Forces and Industrialist sponsors remain unchanged.

Vanilla's internal `nguni` culture key is retained for compatibility but narrowed to the Central African Ngoni represented by Maseko. SB's separate Zulu, Swazi, Ndebele, and Shangaan cultures make the former generic label unnecessary; Ngoni keeps Southern Bantu heritage and the Nguni language family, receives its own historical name pool, and gains no state-wide Zambezia homeland.

The `pink_map` decision is pinned to its OB1 object. Its DLC, independence, Portuguese Colonialism, and one-use gates remain unchanged; SB adds only colonial/company-subject colonization eligibility and routing through the durable Bechuanaland terminal outcome. The Vanilla Pink Map JE, presentation, modifiers, and favour transaction remain authoritative.

## Focused 1.14 Open Beta Rebase

OB1 changed the global war-support and war-goal contracts, subject restoration, AI incorporation callers, pathfinding spline, and naval network. SB adopts those contracts only where an owned object or authored route requires them; it does not tune the new Vanilla war-support, wage, hiring, construction, state-value, naval, or AI balance numbers.

The focused override decisions are:

- BIC's retained pact query uses the evaluated `scope:actor`; SB's responsible-colony tiers remain. SAF's complete custom naming block intentionally supersedes Vanilla.
- The Vanilla dominion replacement gains `re_establish_war_goal = make_dominion` while retaining SB's deliberate `join_overlord_wars = no`. Each of the seven custom SB subject types maps to its own exact restoration goal.
- Every SB story war goal declares an explicit mirror or assent policy. Timer enforcement records pending state only; terminal story mutation waits for the authoritative war-end or pre-war-back-down resolver.
- The global spline is a structured three-way merge that keeps the OB1 European/pathfinding records and SB's Southern African records. The exact merge report and depot delta are versioned compatibility evidence rather than inferred from filenames.
- The Zulu chiefdom diplomatic action uses the existing OB1 `puppet_15.dds` icon. No missing `puppet.dds` path remains.

## CMF 1.66 Integration

The Bechuanaland Corridor uses CMF `1.66.0`'s journal-scope and International Situation interfaces:

- the CMF title setters project both titles for the situation widgets; and
- `com_container` is the supported test-time inspector.

The engine exposes the corridor as one contextless JE shared by its involved countries, so SB addresses that singleton through the standard `je:` link and projects its container-backed actor scopes and score directly. Its launcher dependency is pinned to `1.66.*`, so an older or later CMF minor line is intentionally unsupported rather than maintained through duplicate inline implementations.

One named container, `sb_bechuanaland_corridor_state`, owns all shared active-crisis state. SB ships no journal GUI replacement and no container debug UI.

CMF `1.66.0` containerizes an internal custom progress-bar backend, but SB calls none of the removed dictionary/structure APIs. The validator pins SB's used CMF APIs and Vanilla's treaty-port/company-disband hooks. Upstream removal or signature drift fails validation instead of silently changing behavior.

## 1.14.0 Open Beta 1 Inherited Surface

SB does not shadow `common/production_methods/04_plantations.txt`, `events/tech_events/military_tech_events.txt`, the new `common/travel_network/naval_network.txt`, or OB1's naval UI. Vanilla's Banana Plantation fix, **A Doctrine of Iron and Steam** outcomes, naval-network graph, ship panel, and naval messages therefore apply directly.

OB1's hiring, wage, construction, state-value, ship-selling, and multiplayer-backend changes are Vanilla/engine-owned. No file below `common/buildings`, `common/building_groups`, production methods, or Sub-Saharan starting buildings changed in the target depot. SB adds no balance shadow for these systems. Runtime smoke tests still cover indirect interactions, especially broad treaty matchers around mixed ship-transfer treaties.

## State And Naming Policy

The changed state regions are `STATE_BECHUANALAND`, `STATE_BOTSWANA`, `STATE_CAPE_COLONY`, `STATE_DRAKENSBERG`, `STATE_EASTERN_CAPE`, `STATE_EAST_TRANSVAAL`, `STATE_GRIQUALAND_WEST`, `STATE_HEREROLAND`, `STATE_LOURENCO_MARQUES`, `STATE_NAMAQUALAND`, `STATE_NATAL`, `STATE_NORTHERN_CAPE`, `STATE_NORTHERN_TRANSVAAL`, `STATE_TRANSVAAL`, `STATE_VRYSTAAT`, `STATE_ZAMBEZI`, `STATE_ZAMBEZIA`, and `STATE_ZULULAND`.

`STATE_NATAL` is ID `1213`, split from the former combined Zululand block. Its hub locators are separately keyed from reduced `STATE_ZULULAND`; the province raster, terrain, and Southern African locator positions remain unchanged in OB1. The existing Natal port and wood anchors stay reindexed from `25703` and `25704` to `121303` and `121304`, changing only their logical state ownership.

The OB1 global spline changed outside SB's region, so the live binary starts from OB1 and imports only the proven old-Vanilla-to-SB records through the strict structured merger. `STATE_LOURENCO_MARQUES.port` is `x54CDC5`, matching the unchanged port locator and a connected OB1 naval-network node; the old `x361897` value had no naval node. SB does not shadow the naval-network file.

The legacy `geographic_region_southern_africa_old` mirror is extended with the SB split states because Vanilla's dynamic state-and-hub naming dispatcher still uses that legacy region as its routing gate. The OB1 `geographic_region_krakatoa_tsunami_zone` list is preserved with `STATE_NATAL` added beside reduced `STATE_ZULULAND`, ensuring Krakatoa's coastal-state filter reaches both halves of the split.

Additive definitions use `sb_<feature>_*`. Intentional late keyed replacements use `zz_sb_*` or `zzz_sb_*`. Stable event and public script keys are not renamed during cleanup.

CMF-style detection remains available through:

- `spes_bona_is_active`
- `spes_bona_southern_africa_map_rework_active`
- `spes_bona_population_rework_active`

Static parity does not certify engine behavior. Required OB1 launch checks are maintained in `Docs/compatibility/1_14_0_open_beta_1_runtime_matrix.md`. `Docs/compatibility/1_13_11_runtime_matrix.md` remains unchanged as historical evidence and is not evidence for this target.
