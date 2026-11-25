# Spes Bona Override Manifest

Target game version: Victoria 3 `1.15.2` (Steam build `26763837`, Steam branch `public`, core depot manifest `5942745929618312121`).

Pinned dependency: Community Mod Framework `1.67.9`, commit `9103c9cb4130d46cb18204d588def1266e5c1555`, plus `sb-1.15.2-r1`. The launcher relationship is `1.67.*`. Static validation uses the official GitHub `release-1.67.9.zip` asset with SHA-256 `2c702bbf99fd96804366896521832d18519a6a33e94519d49160de0ece7e04ae`; moving latest/Workshop payloads are not substituted.

The canonical machine-readable inventory is `Docs/compatibility/override_inventory.json`. It records every exact-path collision and keyed override with ownership, intended delta, load-order semantics, review date, and pinned source hashes. The complete OB1 semantic decisions are recorded in `Docs/compatibility/1_14_0_open_beta_1_rebase.md`. Schema version 3 also locks otherwise silent key/source collisions and non-shadowed upstream caller contracts.

Native 1.15.2 scopes both Paralegal event AI checks through the optional state owner.
SB now inherits the event. The inventory contains 40 exact-path files.

Run the complete local gate from the repository root:

```sh
python3 -B tools/validate.py \
  --game-root '/path/to/Victoria 3/game' \
  --cmf-root '/path/to/Community Mod Framework' \
  --tiger
```

The validator reads the exact CMF tag, asset, and digest from the inventory and verifies that release plus the pinned compatibility patch. It fails closed on a different tag, asset, digest, metadata version, installed Steam build, branch, or core depot manifest. `--skip-cmf-sync` is available for offline work only. Installed Tiger 1.19.0 lacks the new JE/event schema and is not a 1.15 target validator. Repository semantic/hash checks remain mandatory, with engine verification separate.

On Depro's development machine, the canonical CMF path is `/Users/depro/Documents/Paradox Interactive/Victoria 3/mod/Community Mod Framework`. Its contents are rebuilt from the verified GitHub release asset plus patch `sb-1.15.2-r1`. Upstream metadata remains unchanged; the patch revision and full installed-tree hash are locked separately.

## Inventory Surface

The current lock covers:

- `40` exact-path files;
- `156` keyed `REPLACE`, `TRY_REPLACE`, or `REPLACE_OR_CREATE` objects;
- `18` intentionally changed state-region blocks;
- one registered additive `zz_` override;
- all eight localization replace files plus key-level, multi-source pins for the 20 previously silent Vanilla key collisions;
- two non-shadowed current AI caller/scoring contracts (`ai_strategy_default` and `state_transfer`); and
- no approved `replace_path` directives.

The exact-path set includes Southern African history, the Highveld event baseline, the regional state file, the province raster, terrain, locators, and spline network. Generated and binary files use hash parity; textual files also require a reviewed source diff. Every OB1 source-only drift result is repinned only after a recorded semantic decision.

## Current 1.15.2 port

The cultural-minority movement applies its Colonialist secession exclusion to the Cape and British Natal garrisons’ new Anglo-Colonialism. Its CMF dependency and vanilla baseline are pinned in the inventory. [Garrison policy](../cape_natal_armed_forces_laws_design_2026_11_24.md#anglo-colonialism-and-the-frontier-vote)

The inventory verifies all 573 changed or added core paths, 25 Vanilla contracts
for the CMF patch, and the full installed CMF tree. SB keeps its ordinary-war
participation rule for dominions. All eight subject definitions use the new
native protection behaviour. The province raster includes the Pommern correction.
[Implementation and digest comparison](1_15_2_implementation.md) · [DP replay](1_15_2_runtime_matrix.md)

## Historical 1.15.1 port

The [11 November implementation report](cmf_1_67_3_and_1_15_1_patch_2026_11_11.md)
records the four-file CMF release review and the full 1.15.0-to-1.15.1 depot delta.
The [19 November dependency update](cmf_1_67_9_update_2026_11_19.md) pins two payloads and fourteen
native contracts. CMF supplies the six secession flags and dynamic bar renderers.
The inventory tracks all 24 copied CMF definitions against this installation.

SB imports the corrected labour ideology, cultural-minority secession flag,
Armed Forces ownership attraction and colonial-claim infamy block. Native copper
is 9/21/35 in Namaqualand/Zambia/Katanga. SB's Griqua setup, map repairs and
performance changes remain intact. The 1.15.1 depot and CMF patch/native/tree
checks are mandatory in the inventory validator.

The [1.15.0 implementation](1_15_0_implementation.md) remains historical evidence.
DP acceptance for this hotfix is separate and pending in the
[1.15.1 runtime checklist](1_15_1_runtime_matrix.md).

## Earlier implementation notes (historical)

The notes below preserve earlier review decisions and follow-ups. Their version
numbers, then-current inventories, patch ownership, map topology and GUI descriptions
are historical where superseded by the 1.15 reports above; they are not current
installation instructions or runtime certification.

The Initial Enthusiasm helper retains Vanilla's exact grant and adds hidden expiry
bookkeeping only for NAL's Zulu cultural movement. Its annexation replacement
preserves the tracked remainder of that modifier and both Shepstone attraction
modifiers. Other movements' grants and the CMF dependency remain unchanged; see
the [preservation contract](zulu_national_movement_2026_10_17.md#authorized-modifier-preservation).

`common/history/treaties/00_historical_treaties.txt` remains an exact-path Vanilla shadow because startup treaty rows cannot be removed additively. Its unchanged payload is pinned against `1.14.5`; uniquely named third-party treaty files remain additive. SB does not replace or register `on_treaty_ports_inherited`, leaving Vanilla's inheritance prompt and market reconnection path untouched.

`common/history/diplomacy/00_relations.txt` retains the OB1 relation baseline except for three explicit startup corrections: it disables the whole Vanilla `c:SAF` block, removes ORA's relation to TRN, and disables the whole Vanilla `c:TRN` block because SAF and TRN do not exist in 1836. Later TRN relations remain story-authored.

## Additive Overrides And Localization Replace Files

Two further override surfaces are inventoried and hash-checked alongside the exact-path collisions above:

1. **Additive `zz_` files** (`additive_overrides`): SB-authored files whose name uses the `zz_sb_*` / `zzz_sb_*` convention but which create new objects instead of replacing an upstream key (currently only `common/history/ai/zz_sb_portuguese_kongo_secret_goal.txt`). Each entry pins the mod file hash and states intent and owner.
2. **Localization replace files** (`localization_replace_files`): every file under `localization/english/replace/`. Entries that shadow an upstream localization file (`country_flavor_text`, `dynamic_state_and_hub_names`, `map/states`) pin both the upstream and mod hashes; SB-authored names record `upstream_file: null` and state why they live in `replace/`.
3. **Key-level Vanilla localization collisions**: every real collision whose source is not represented by a single replace-file path has its key, source file, and source hash pinned. Multiple Vanilla sources for the same SB replace file are tracked separately, so a future change cannot hide behind `upstream_file: null` or a secondary source.

The checker fails on any unregistered `zz_` override-style file, unregistered `replace/` localization, unregistered key collision, or stale source/mod hash. None of these surfaces may bypass the compatibility contract.

## Dependency Rebases

The five retained political-movement replacements are pinned to CMF `1.66.0` and reviewed against Victoria 3 `1.14.5`. Cultural Supremacy migrates six primary-culture comparisons and one value accessor to Vanilla 1.14.3's explicit-country API in both CMF and SB. Other movement bodies and CMF extensions are preserved; the shared source-file pins are refreshed. Cultural Supremacy retains the upstream unowned-homeland and neighbouring-movement scope fixes; the only SB-specific delta is CAP creation/disband exclusion. The other retained movement deltas remain the documented CAP exclusion or Anglo-African utilitarian eligibility.

The 17 October annexation follow-up adds a cultural-minority replacement pinned
to the same installed CMF and Vanilla sources. Its gameplay changes are a disband
alternative for NAL's specifically marked Zulu movement and an `on_disbanded`
receipt that recreates it the next day. The 29 October deeper performance pass
also tests neighbouring insurrection before culture matching. Predicate parity
and token parity for every other field verify the preserved CMF body, including
native disband conditions, eligibility and recruitment.
The existing annexation settlement gate makes this a single replacement; no
category threshold, recurring revival or CMF dependency patch is introduced.
See the [implementation record](zulu_national_movement_2026_10_17.md#authorized-replacement--b).

The company replacements are intentionally narrow:

- `company_mozambique_company` retains the OB1 level-five player eligibility and presentation. POR/IBE AI may establish from an existing level-two cotton or tea plantation, may pursue construction before incorporation, and receives a total AI weight of `100`.
- `company_de_beers` retains the OB1 structure while replacing gold-field requirements and targets with SB diamond mines.

Vanilla's additive `on_company_disbanded` handler remains untouched. SB registers exactly one separate Mozambique cleanup handler.

The Armed Forces definition is a keyed OB1 rebase. Its executable token stream is unchanged upstream; the source drift is comments and formatting only. Its sole numerical SB delta consumes Imperial Administration's displayed flat `+50` Aristocrat attraction modifier. The 29 October performance pass also short-circuits pure guards and combines mutually exclusive wage/shared government checks, preserving scores and breakdown entries. CMF `1.66.0` does not replace this object. Source and object hashes are pinned so later military-interest-group changes require an explicit rebase.

The [29 October performance pass](../performance_pass_2026_10_29.md) also repins
SB's Absolutist creation/disband predicates and the cultural-majority neighbour
predicate after equivalent scan/condition reordering. Its
[deeper follow-up](../performance_deeper_pass_2026_10_29.md) applies the same
insurrection-first check to the cultural-minority neighbour predicate. Their CMF hooks, numerical
values and original SB exclusions remain unchanged. No dependency patch changes.

The [30 October precision pass](../performance_precision_pass_2026_10_30.md)
also evaluates the existing Boer frontier-colonisation exception first and skips
cultural-majority competing-movement searches for exactly zero-radical pops.
Support values are identical; the neutral loss tooltip contribution can disappear.
Only these two SB object hashes are repinned; upstream and dependency pins remain.

All three AI incorporation replacements wrap the complete current 1.14.5 bodies. Native eligibility includes primary-culture thresholds (50%, or 25% beside an owned incorporated state); ordinary incorporation requires eligibility and minimum population, while colonial incorporation also permits same-region or owned-incorporated adjacency. `sb_regional_ai_should_incorporate` admits only AI NAL owning `STATE_ZULULAND`, AI CAP owning `STATE_BECHUANALAND` or `STATE_GRIQUALAND_WEST`, and AI ORA owning `STATE_DRAKENSBERG`; every exception requires `owner = root`. These four exceptions retain their independence from population, adjacency and country type. Both `will` paths and `ai_can_incorporate_state` include the helper. Eligibility contributes to native incorporation and state/transfer scoring; no trigger bypasses engine affordability or candidate validity. The current `ai_strategy_default` and `state_transfer` objects remain Vanilla-owned, pinned caller/scoring contracts.

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

CMF `1.66.0` is installed with `sb-1.14.3-r1`. Its Annex Country, Conquer State, and Return State definitions still match Vanilla 1.14.5, including the GDP/population-share infamy formulas and territorial mirrors, with only CMF's land-grab validity hook added. SB has no duplicate territorial-goal shadows. The seven patched ideology categories are retained unchanged, and the cultural-majority movement uses the explicit-country API. Five replacement payloads, sixteen Vanilla source/object contracts, both tree digests, and three upstream-reviewable diffs live under `patches/cmf/sb-1.14.3-r1`. No SB-specific country or state rule is added to CMF.

`tools/sync_cmf.py` verifies the original archive and stages the complete patch before installation. Repeated sync, `--check`, and `--force` retain the patch; `--latest` is rejected for this dependency. A local unpatched or altered 1.66.0 tree fails validation. Metadata's upstream version and the launcher relationship remain unchanged; this is explicitly a patched distribution, not a new official CMF release.

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

Static parity does not certify engine behavior. Current launch checks are maintained in `Docs/compatibility/1_14_3_runtime_matrix.md`. `Docs/compatibility/1_13_11_runtime_matrix.md` remains unchanged as historical evidence and is not evidence for this target.

## 1.14.2 review (historical)

The new depot report contains 69 changed files, one addition, and no removals. No exact-path SB override or map asset changed upstream. The three AI incorporation trigger bodies are unchanged; the default strategy now also tests incorporation eligibility when calculating owned-state cession reluctance, alongside owned/foreign state values. SB keeps its owner/root guard and four existing priorities. Dominions' localisation source files changed globally; the documented custom dominion policy remains authoritative. DP's Boer Drakensberg naming edit is retained.

The historical target report and fresh-game checklist are `1_14_2_rebase.md` and `1_14_2_runtime_matrix.md`. Earlier OB1 evidence does not certify this build.

## 1.14.3 review (historical)

The separate depot report records 92 changed files, three additions, and no removals. Exact-path SB overrides and map assets are unchanged. The required runtime ports are CMF's three territorial infamy formulas and the cultural-majority primary-culture API in both CMF and SB. AI strategy changes are inherited; incorporation trigger bodies and ideology-category bodies are unchanged. CMF's construction-interaction map-list type retains its production-method customization and gains a pinned source contract. Dominion source pins are refreshed without rewriting SB prose.

The historical report and DP engine checklist are `1_14_3_rebase.md` and `1_14_3_runtime_matrix.md`. All game launches remain with DP. ORA–BST stays on hold; no custom enforcement or save migration is introduced.

## Chiefdoms movement contest (19 September 2026)

Three new keyed replacements retain the effective 1.14.3/CMF bodies except for the
Chiefdom/Elder Council allowance in ZUL's historical Chiefdoms context and the
native absolutist movement's exclusion of that context. The ZUL-only uSuthu
derivative supplies the movement there. CMF’s Bavarocrat eligibility and Grey PLP
support/state-weight hooks are retained in both movement definitions; the native
replacement is checked against CMF after removing only SB’s four lifecycle gates.
Other countries retain their existing behaviour.

`common/customizable_localization/00_ep1_custom_loc.txt` is an exact-path shadow:
customizable localization does not accept `REPLACE:`. Only the two overlord-lobby
name functions differ, adding a marked-ZUL contest branch before their native
fallbacks. All other functions are byte-preserved; the native lobby types remain
unchanged so their IG clout continues to enter native Liberty Desire. CMF has no
same-path file. The focused tests compare all functions and both fallback bodies
against installed Vanilla; the inventory pins the complete upstream/result files.

See [implementation and verification](zululand_movement_contest_2026_09_19.md).

## Goods Transfer crash safeguard (20 September 2026)

`common/treaty_articles/13_goods_transfer.txt` now shadows Vanilla. Only `possible`
changes: a `trigger_if` checks live parties and valid personal/market-owner
market-capital scopes before evaluating the complete original eligibility body.
The invalid-scope branch rejects the proposal. Valid countries retain native
reachability, adjacency, port, pricing and treaty rules; maintenance and existing
articles are unchanged. CMF has no same-path or keyed replacement. Whole-file
parity after undoing this one wrapper is regression-tested and both hashes pinned.
This is a mitigation for a repeated native AI treaty crash, awaiting DP's replay;
it is not a confirmed diagnosis of the invalidated country or Zulu capitulation.
See [crash investigation](zul_war_crash_2026_09_19.md).

## 1.14.5 review

See [the complete rebase report](1_14_5_rebase.md) and [DP's pending engine matrix](1_14_5_runtime_matrix.md). The reproducible retained 1.14.4→1.14.5 delta has 147 changes and two additions; the missing 1.14.3 manifest prevents a complete earlier depot diff. The separate comparison covers every pinned Vanilla source from SB's 1.14.3 inventory.

The four runtime ports are incorporation triggers, colonial-claim regional-objective scoring, Scramble's wartime failure guard, and 14 European fleet transport additions. Portuguese armies, regional exceptions, Boer claim restrictions, Scramble growth/cleanup, maps, splines and disabled Highveld are preserved. Interaction and technology object bodies are unchanged; updated AI scoring and Dominion source contracts are reviewed and repinned. The naval graph has 6,641 nodes, 7,192 connections and all 33 SB ports connected.

CMF 1.66.0 + sb-1.14.3-r1 remains byte-identical and all 16 upstream contracts match. Current build, current manifest and current payload checks fail on missing evidence. Historical reproduction alone may skip missing old inputs. No story redesign, ORA–BST workaround, engine launch or 1.15 expiry change is included.


## Zulu institutional implementation — 18 October 2026

The current inventory includes 39 same-path files, 118 keyed replacements and
eight localisation replacement files. Five native army-law replacements add the
customary-army firearms reform gate; one decree replacement adds institutional
eligibility while preserving native restrictions. The chiefly constitution uses
independent laws so its ideological stances apply; the hereditary Chiefdom
fallback needs no override. Generic Absolutist
eligibility retains the effective CMF body outside the authored movement lifecycle.
The political-movement history shadow excludes eligible authored institutions
from the explicit startup Absolutist call. Removing that one condition reproduces
Vanilla 1.14.5 byte for byte after BOM decoding; every other movement and country
keeps its original setup.
Old blanket Chiefdom/Elder Council and fixed-lobby display replacements are removed.

See the [semantic contract review](zulu_institutions_contract_review_2026_10_18.json),
[native coup contracts](zulu_court_vanilla_contracts_1_14_5.json), and
[implementation / DP matrix](../zulu_institutions_implementation_2026_10_18.md).
The installed CMF payload and existing patch hashes remain unchanged.
See the [launch follow-up](zulu_institutions_launch_2026_10_18.md) for the
parent-law correction and removal of the now-redundant government replacement.
The [court presentation follow-up](zulu_court_presentation_2026_10_18.md) records
the startup history comparison and independent allegiance traits.

### 27 October claimant career correction

The ZUL character-history override delegates Mpande's politician role to his template, which then extends the role career. The keyed Mpande override changes no starting traits, Popularity, noble status or mortality. Gqugqu's SB-only template receives the same career protection. Only those two changed override hashes are refreshed; game and CMF pins remain unchanged. See [save evidence and verification](zulu_outcome_options_harvest_2026_10_27.md).

**27 October follow-up — Fecund:** DP subsequently requested a unique starting trait for Mpande, supplementing the earlier package with +5% Health, +10 Popularity and +5 Prominence. Only the `REPLACE:ZUL_mpande_zulu` object hash is refreshed for this addition; its upstream contract, the game/CMF pins, role career and other template fields remain unchanged. The new [rabbit card and prompt](../../output/imagegen/fecund_special_2026_10_27/README.md) use the established Vanilla special gold frame. This supersedes the no-trait-change statement for the earlier career-only patch above.

## Zulu names-only culture override — 29 October 2026

`common/cultures/sb_zulu_names.txt` replaces Vanilla's `zulu` definition solely to revise its four name pools. All non-name fields, including the current treaty-seal texture, remain identical to installed 1.14.5. The keyed inventory pins both definitions; `tests/test_zulu_names.py` checks non-name parity, unique pool entries, localisation and retained royal template identities. See the [names/traits evidence brief](../zulu_royal_names_traits_2026_10_29.md). No CMF patch change is required.
