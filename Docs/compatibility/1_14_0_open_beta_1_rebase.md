# Victoria 3 1.14.0 Open Beta 1 Rebase Evidence

## Status and evidence boundary

This document records the static rebase review for the exact Victoria 3 `1.14.0`
Open Beta 1 payload installed on 2026-09-04. The target is Steam build `25081502`,
branch `1.14-openbeta`, core depot `529341`, manifest
`3868129321396195520`. The SB implementation baseline is
`51c98bf32fc9f9049c99f858f5a558bdfde0dffe`.

The manifest comparison and source review are static evidence. They are not proof that
an engine path works. Every cold-launch, save/reload, AI-choice, war-resolution,
pathfinding, naval, GUI, DLC, and multiplayer claim remains **Engine pending** until it
is run and recorded in `1_14_0_open_beta_1_runtime_matrix.md`. A failed runtime case is
a blocker, not a pending pass.

This is a new-game compatibility target. It does not promise migration of a live 1.13
save. Because the beta is rolling, a build, branch, or manifest change invalidates this
review and requires a new depot delta before release.

## Implementation discoveries

- The approved per-route war work exposed enough duplicated 0/1/2 accepted-side logic
  that implementation added `common/scripted_effects/sb_story_war_effects.txt` as the
  shared, idempotent Humiliation recorder/resolver. This is an implementation-discovered
  file, not a mechanics expansion: timer callbacks remain non-authoritative, while
  terminal resolution still runs only from the authored play's final back-down or
  war-end path.
- `sb_griqualand_west.249` was retired as an executable event and dispatch when the
  dead one-play claim-revocation route was replaced by the approved two-phase `.254`
  sequence. Its existing DP-reviewed English localization block remains byte-for-byte
  archived in `sb_griqualand_west_l_english.yml`; it is intentionally historical prose,
  not a live dispatch or an unreviewed replacement.
- Post-integration hostile review found that type-only terminal hooks and post-create
  play searches could consume or mutate unrelated plays. The convergence patch binds
  the affected routes to pre-create leases and saved actual-play scopes, makes Phase-B
  claim revocation independently idempotent, and derives timer-safe Warren/total-war
  outcomes only from unambiguous final subject or ownership predicates. These are
  correctness repairs to the approved mechanics, not new outcomes.
- Three-month held popups could outlive the old 45/90-day dispatch markers. The
  implementation therefore separates short scheduling leases from four-month popup
  receipts and, where a name can be reused, binds the receipt to a unique container
  generation. Stale options are inert, valid-but-busy routes retry, and permanent
  invalidity cancels without inventing a narrative victory.
- Blood River required a second transaction after the exact play closes: `.070`,
  `.080`, and `.081` now carry a saved terminal result plus exact recipient and
  counterparty. This lets a live retagged recipient consume the result after play
  cleanup, while dead-recipient recovery clears it without reward. The documented
  diplomatic-play `initiator` and `target` links, not callback-only aliases, bind the
  transaction on back-down.
- Zulu firearms and royal continuity use different lifetimes. The firearms archive
  may refresh while the exact annex play remains active, but ruler/heir/house identity
  freezes once at exact admission (or immediately before a direct annex). Monthly and
  wargoal callbacks no longer rewrite the royal snapshot. Both archives survive a
  no-NAL British annex and transfer once when Natalia is later created.
- Martinus coercive and legal offers, Griqualand `.261`, Klip secession/punitive
  offers, TRN-ZPB crackdown, Xhosa 7/8/9 delivery, Natal refusal/guns, and the
  Zululand chiefdom terminals now use generation-bound authority. Exact victory may
  reserve a deferred Martinus union install after ambition resolution; the reservation
  clears only after the authored pact is observed.
- TRN-ZPB crackdown needs two distinct physical records. Its launch-time TRN state
  footprint configures goals, while the separately frozen ZPB Northern Transvaal
  state proves the authored succession endpoint together with TRN extinction. Route
  cleanup globally removes the singleton country and state markers so a retagged
  backer or transferred state cannot retain authority.
- Klip River county creation is now a fail-closed local transaction. The creation
  lease remains until all three provinces verify under the exact newly created country;
  a failed verification restores only provinces still owned by that exact object to
  their saved pre-attempt owners and never selects a replacement `KLR`, `NAL`, or
  `ZUL` tag.
- SAF/STA/NGN formation and both imperial/confederated formation and expansion
  branches now call one shared story-transaction lock. It covers all live generation
  containers, popup receipts, launch/play leases, terminal deliveries, and frozen
  state evidence, including orphan recovery after actor death or retag.
- Four older selectors outside the approved Step 8 file set still use
  `random_diplomatic_play`. They were not silently redesigned in this patch and are
  registered as `OB1-07`; none is used as evidence for the exact-launch claims below.

## Frozen static validation snapshot

The post-convergence tree was validated after all route and formation fixes:

- `uv run python -m unittest discover -s tests -q`: **388 tests passed**.
- `tools/validate.py --skip-cmf-sync` with the explicit OB1 game root and a fresh
  extraction of the verified CMF asset: **16/16 checks, 0 failed**; the five declared
  deferred gates remain warnings.
- Delayed-event lifecycle inventory: **442 dispatches**, SHA-256
  `bb3ec8d44de7cc00e329762ddbe19eb57e241835c9925b714f2c9452d843618c`, with every
  destination classified.
- Override inventory: **37** same-path files, **109** keyed overrides, **18** changed
  state blocks, **0** `replace_path` directives, **1** additive override, **8**
  localisation replacements, **20** key collisions, and **2** upstream contracts.
- Reviewed localisation: **105** namespaces match the byte baseline; **174** remain
  explicitly `TO REVIEW`.
- Naval validation: **6,641** nodes, **7,191** connections, and all **33** SB state
  ports connected. The merged spline is 1,650,134 bytes with SHA-256
  `9fd9d83f0b651284d5ef22066d19239fd9e1127d25c14c0763eca3bbade5ef8c`.
- A fresh `vic3-tiger` run loaded SB plus the disposable exact CMF extraction, exited
  zero, and ended with `fatal: 0, error: 1109, warning: 103, untidy: 1, tips: 1`.
  Its validator-owned ordered output SHA-256 is
  `708bbcea675e055fa84a63cc3f3f2c5a986040c253127eb09a3c6abbdd8ab701`.
  Tiger identifies itself as a 1.13.5 schema against OB1 and flags 1.14 constructs
  such as `container_exists`; completed diagnostics are therefore advisory warnings,
  not runtime certification.

All 52 engine scenarios remain `Engine pending`; none of these static results is
reported as a cold-launch or save/load pass.

## Sources

Sources were fetched or inspected on 2026-09-04.

- Paradox, [Developer Diary 185](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1841579228665685): announced the war-support and war-goal work, pathfinding, naval UI,
  hiring/wage changes, AI construction, and AI state-value/incorporation work.
- Paradox, [Developer Diary 186](https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1842846814440413): announced further Open Beta work, AI ship selling, and the default
  multiplayer backend change from Nakama to Steam.
- Community Mod Framework,
  [release 1.66.0](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.66.0), commit
  `807c32ff42b75714a3a0e090c0db3357b5e46ed7`; official asset
  `release-1.66.0.zip`, 22,369,471 bytes, SHA-256
  `79dd0d434e6ffb617147ad1b91b73e6306139adfffcadf6774eeb32db3a09b8b`.
- CMF [PR #150](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/pull/150) contains its 1.14 work.
- The CMF [Workshop change log](https://steamcommunity.com/sharedfiles/filedetails/changelog/3385002128) says “Reverted to 1.13 version” after an earlier “Update for 1.14 Open
  Beta” entry. The Workshop payload is therefore not the authority for this rebase.

The diaries describe intended behavior. The retained Steam manifests establish the
exact files, sizes, and content SHA-1s delivered in these two builds. Local source and
inventory audits refine which announced changes intersect SB.

## Exact depot evidence

| Baseline | Steam build | Core manifest | Created (UTC) | Bytes | Manifest SHA-256 |
|---|---:|---:|---|---:|---|
| Victoria 3 `1.13.11` | `24799966` | `4498977168532327663` | 2026-08-18 13:02:33 | 4,732,224 | `5ffcff6dab4ad7d8008618c50413bb3dcaeb12608cbe9d3e93872fa287fc4ddc` |
| Victoria 3 `1.14.0` OB1 | `25081502` | `3868129321396195520` | 2026-09-01 09:43:27 | 4,733,748 | `1c76bc89eebffc465999a90cfc8ded5c1e771c089bbecb05c86b0d4f6bde4977` |

The standard-library decoder in `tools/build_steam_depot_delta.py` verifies those full
input sizes, SHA-256s, depot IDs, manifest IDs, creation times, and entry counts before
writing anything. It does not query “latest.” The artifact was generated with:

```sh
python3 -B tools/build_steam_depot_delta.py \
  --old-manifest "$HOME/Library/Application Support/Steam/depotcache/529341_4498977168532327663.manifest" \
  --new-manifest "$HOME/Library/Application Support/Steam/depotcache/529341_3868129321396195520.manifest" \
  --game-root "$HOME/Library/Application Support/Steam/steamapps/common/Victoria 3/game" \
  --output Docs/compatibility/1_13_11_to_1_14_0_ob1_depot_delta.json
```

The normalized output is
`Docs/compatibility/1_13_11_to_1_14_0_ob1_depot_delta.json`. It contains exactly:

| Change kind | Paths |
|---|---:|
| Content changed | 182 |
| Added | 13 |
| Removed | 2 |
| **Total reviewed delta** | **197** |

Every row carries the normalized manifest path, explicit old and new size/content
SHA-1 records, subsystem, SB-collision boolean, and review disposition. A missing side
is represented by explicit `null` values rather than an omitted field. Entries are
unique and sorted by path. The seven `sb_collision: true` rows are the one changed
exact-path shadow and the six changed upstream source files used by keyed SB
overrides. Upstream contracts used by SB but not shadowed remain non-collisions; their
`adapt-sb-contract-runtime-pending` disposition keeps that dependency visible.

For audit readability, the artifact groups its 197 rows as follows:

| Subsystem | Entries |
|---|---:|
| Localization | 61 |
| War support and war goals | 47 |
| Events and content | 17 |
| Interface and graphics | 15 |
| Core script | 12 |
| Politics and society | 12 |
| Naval and military | 11 |
| AI and economy | 8 |
| Diplomacy and subjects | 7 |
| Map and pathfinding | 3 |
| Paradox scripted tests | 3 |
| Audio | 1 |

These are review groupings, not inferences about file contents. The old/new SHA-1
records remain the authoritative delta evidence.

## Grouped semantic review

### War support and war goals

- Vanilla removes `common/script_values/war_exhaustion_values.txt` and adds
  `common/script_values/war_support_values.txt`. War support now runs from 0 to 100;
  the old `-100` automatic-capitulation design is gone. New factors cover goals,
  occupation, battles, casualties, devastation, finances, lobbies, rivals, turmoil,
  and war length. The SB source audit found no use of the removed script tokens.
- All 34 pre-existing Vanilla war-goal definitions changed, and five definitions were
  added: personal union, chartered company, crown land, break enforced treaties, and
  release as subject. OB1 definitions explicitly declare `mirrored_wargoal` or
  `assent_required`; the default enforcement rate is five points per week.
- `on_wargoal_enforced` now supplies `scope:enforced_by_timer` and
  `scope:war_goal_enforced`. This is not a direct file collision, but SB's custom story
  goals and terminal callbacks depend on the changed contract. They require the
  separate war-pipeline adaptation and remain **Engine pending**.

### Subjects and restoration

- `common/subject_types/00_subject_types.txt` adds `re_establish_war_goal` contracts.
  Selected low-autonomy types also gain `forced_into_overlord_revolution`.
- SB replaces Vanilla `subject_type_dominion` and owns seven custom subject types that
  predate this contract. The Vanilla dominion restoration mapping must be merged while
  preserving SB's deliberate `join_overlord_wars = no`. Each custom relation needs its
  exact restoration goal. Restoration, revolution-side behavior, and no-auto-join
  behavior remain **Engine pending**.

### AI, state values, construction, hiring, and wages

- OB1 adds AI control of government and military wages, revises construction
  budgeting, and exposes localized state-value reasons.
- The ordinary `ai_will_incorporate_state` route remains for non-colonial countries.
  Colonial and company countries now call the new
  `ai_colony_will_incorporate_state`; `ai_strategy_default` selects between those
  routes. `ai_can_incorporate_state` feeds state-value and transfer-state scoring, not
  the start command. The inventory pins the unchanged `ai_strategy_default` caller and
  `state_transfer` valuation object as non-shadowed upstream contracts.
- The two old focused Vanilla incorporation-trigger objects are unchanged even though
  their shared source file changed. SB still needs the new sibling path because NAL and
  CAP can traverse both country-type branches. Willingness does not bypass
  affordability, code-side validity, or highest-candidate selection. All actual AI
  selection and completion claims remain **Engine pending**.
- The changed economy numbers live in engine defines, not building or production-
  method overrides: hire profit target `0.25 -> 0.15`, raise-wage target
  `0.25 -> 0.20`, lower-wage and cash-withdrawal targets `0.15 -> 0.10`, and the
  same-type average-productivity wage threshold `0.5 -> 0.75`. Expected-SoL wage
  targeting is added. No file below `common/buildings`, `common/building_groups`,
  production methods, or Sub-Saharan starting buildings changed.

### Naval, pathfinding, and interface

- Vanilla adds `common/travel_network/naval_network.txt`: 469,492 bytes, SHA-256
  `bca18518598f55d7f1b2b07d04ed88e8389d4db807fa49bdcd53d8bc48ca061f`,
  with 6,641 nodes and 7,191 connections. SB does not ship an exact-path shadow for it.
- The global spline changes from Vanilla SHA-256
  `91c0957b4898ca4db6b66584d0ab1db1a6039825e9fd635b7a5c1e69068cf2b1`
  to `ac58f5fb4cd408cf8dba8ad41c5f3a322a12c5372f055694eb85f528e650c28c`.
  SB exact-shadows that global binary, so a record-keyed structured three-way rebase is
  required. The reviewed candidate is 1,650,134 bytes, has counts
  `33,857 / 4,283 / 4,281`, and SHA-256
  `9fd9d83f0b651284d5ef22066d19239fd9e1127d25c14c0763eca3bbade5ef8c`.
  It reported zero record conflicts and identical forward/reverse merge output.
- `map_data/adjacencies.csv` changes only for a Kyushu sea connection. Southern African
  province raster, terrain, state-region source, and map-object locators are unchanged.
- The new network has no node for SB's current Lourenço Marques port `x361897`; it has
  a connected node for Vanilla's `x54CDC5`. DP selected `x54CDC5` as the state port.
  Static topology evidence does not certify embarkation, invasion, supply, repair, or
  rerouting; those rows remain **Engine pending**.
- OB1 changes the ship panel, naval messages, icons, and supporting localization, but
  none collides with an SB GUI or localization-file shadow. Rendering and interaction
  remain **Engine pending**.

### AI ship selling and treaty interaction

Vanilla changes `common/treaty_articles/31_ship_transfer.txt` so the AI can value and
request obsolete-ship treaty bundles. SB neither shadows nor references
`ship_transfer`. SB's existing broad compact-renewal withdrawal matcher can, however,
remove a mixed treaty containing unrelated articles. This is a pre-existing SB risk
made more reachable by the new upstream behavior. No untested narrowing is imported;
the mixed-treaty and ship-sale cases remain **Engine pending**.

### Country, history, and ideology surfaces

- Vanilla country definitions, Southern African state regions, state history,
  character history, Sub-Saharan building history, military formations, province
  raster, terrain, and map-object locators are unchanged.
- `common/history/global/00_global.txt` changes generic non-monarchy Landowners from
  paternalistic to republican-paternalistic. SB does not shadow the file. A fresh
  ORA/TRN start may be affected, so the observed starting ideology remains
  **Engine pending**.
- `common/coat_of_arms/coat_of_arms/02_countries.txt` and `02_countries_2.txt` differ
  only by a newly added UTF-8 BOM. The focused ZUL coat-of-arms object is unchanged.
- The focused Armed Forces executable token stream is unchanged; upstream changed
  comments/formatting. SB keeps its one Aristocrat-attraction consumer.

### Localization and multiplayer

All declared Vanilla localization-file shadows and the 20 separately audited key-level
collisions are semantically unchanged in OB1. The changed English and translated
localization files in the depot artifact are upstream-owned and do not authorize edits
to DP-reviewed SB prose.

The Nakama-to-Steam default backend change is an announced engine/backend change, not a
script, metadata, GUI, or localization collision in SB. Static depot evidence cannot
prove host/join compatibility. The two-client Steam host/join row remains **Engine
pending**.

## Decision for every OB1 override diagnostic

The pre-rebase override checker emitted 18 diagnostics. The table accounts for every
diagnostic; grouped rows show their diagnostic count. “Repin” means refresh the
reviewed source/object hash only after the stated decision is implemented. It does not
mean accepting the whole changed source file blindly.

| SB surface | Diagnostics | Reviewed upstream result | Rebase decision | Runtime evidence |
|---|---:|---|---|---|
| Exact-path `gfx/map/spline_network/spline_network.splnet` | 1 | Global Vanilla binary changed; strict record merge reports zero conflicts. | Use the verified structured three-way merge, preserve both OB1 European and SB Southern African records, then refresh exact-file pins. | **Engine pending** for world/Southern African travel and naval routing. |
| `REPLACE:ZUL` in `common/coat_of_arms/coat_of_arms/sb_countries.txt` | 1 | Upstream source gained a BOM; the ZUL object is unchanged. | Retain the SB object and repin the source file. | Static asset identity only; launch remains **Engine pending**. |
| `REPLACE:BHT` dynamic name | 1 | Focused object unchanged; shared source file changed. | Retain the SB object and repin its source. | No new behavior claimed. |
| `REPLACE:BIC` dynamic name | 2 | Vanilla changes the retained pact query from `who = c:BIC` to `who = scope:actor`. | Merge only the evaluated-actor query and retain SB responsible-colony tiers; refresh source/object/mod pins. | Evaluated-actor transition is **Engine pending**. |
| `REPLACE:NAL` dynamic name | 1 | Focused object unchanged; shared source file changed. | Retain the SB object and repin its source. | No new behavior claimed. |
| `REPLACE:ORA` dynamic name | 1 | Focused object unchanged; shared source file changed. | Retain the SB object and repin its source. | No new behavior claimed. |
| `REPLACE:SAF` dynamic name | 2 | Vanilla's deleted tier receives the evaluated-actor fix; SB intentionally replaces the complete block with custom naming. | Record intentional supersession, keep SB's custom SAF block, and refresh source/object pins. | Custom-name transitions are **Engine pending**. |
| `REPLACE:TRN` dynamic name | 1 | Focused object unchanged; shared source file changed. | Retain the SB object and repin its source. | No new behavior claimed. |
| `REPLACE:ig_armed_forces` | 2 | Upstream object differs only in comments/formatting; executable tokens are unchanged. | Retain the executable SB delta and its Aristocrat-attraction consumer; refresh source/object pins. | Startup ideology behavior remains **Engine pending**. |
| `REPLACE:ai_can_incorporate_state` | 1 | Focused Vanilla object unchanged; new sibling trigger changed the source file. | Preserve the OB1 body outside the exact SB owner/state OR; register and repin it as a scoring caller dependency. | AI selection/completion is **Engine pending**. |
| `REPLACE:ai_will_incorporate_state` | 1 | Focused Vanilla object unchanged; colonial/company countries now use a sibling trigger. | Preserve the OB1 body outside the exact SB owner/state OR; add the colonial sibling override and pin the unchanged caller. | Both country-type branches are **Engine pending**. |
| `REPLACE:subject_type_dominion` | 2 | Vanilla adds `re_establish_war_goal = make_dominion`. | Merge that restoration contract and retain SB's deliberate `join_overlord_wars = no`; refresh pins. | Restoration/revolution/no-auto-join are **Engine pending**. |
| `TRY_REPLACE:civilizing_mission` | 1 | Focused technology object unchanged; source file changed for other OB1 work. | Retain the SB object and repin its source. | No new behavior claimed. |
| `TRY_REPLACE:malaria_prevention` | 1 | Focused technology object unchanged; source file changed for other OB1 work. | Retain the SB object and repin its source. | No new behavior claimed. |
| **Total** | **18** |  |  |  |

The other 36 exact-path files and all other pre-existing keyed objects are unchanged
upstream. All declared Vanilla localization shadows are semantically unchanged. Those
surfaces are retained and repinned to the exact OB1 sources during the exhaustive
inventory refresh; no unreviewed core-balance change is imported.

## Other SB-relevant non-collision decisions

| Upstream surface | SB relation | Decision | Runtime status |
|---|---|---|---|
| All 34 changed and five added war-goal definitions, plus enforcement on-actions | SB custom goals and story-war handlers consume the changed contract but do not shadow these paths. | Give every custom goal an explicit mirror or assent policy; keep irreversible story Humiliation assent-required; reconcile terminal outcomes at the final route state. | **Engine pending** across timer, mirror, peace, back-down, and save/reload cases. |
| New `war_support_values.txt`; removed `war_exhaustion_values.txt` | No removed SB token use. | Do not copy Vanilla values or tune core balance. Add a stale-token regression gate. | War-support behavior is **Engine pending**. |
| New `common/travel_network/naval_network.txt` | No exact shadow, but it consumes the global map/spline and port identities. | Keep the Vanilla network; correct the proven Lourenço Marques port mismatch and validate connected SB ports. | **Engine pending** for every naval route operation. |
| `common/treaty_articles/31_ship_transfer.txt` | No shadow/reference; pre-existing broad SB withdrawal matcher can affect mixed treaties. | Keep Vanilla ship-sale logic and register/test the SB matcher risk instead of silently changing balance. | **Engine pending**. |
| `common/history/global/00_global.txt` | No shadow; generic republican setup can affect Boer starts. | Keep upstream behavior and smoke-test ORA/TRN starts. | **Engine pending**. |
| Economy and AI defines | No building, building-group, production-method, or Sub-Saharan startup-building collision. | Keep OB1 values; do not tune them in the rebase. | Observer hiring/wage/construction checks are **Engine pending**. |
| Naval GUI/messages/localization and state-value UI | No SB GUI or localization-file shadow. | Keep upstream files; test rendering and absence of SB errors. | **Engine pending**. |
| Multiplayer backend | No depot script/metadata collision. | No SB port. Test Steam host/join with identical checksums. | **Engine pending**. |

## CMF 1.66.0 decision

The verified GitHub `1.66.0` release supports `1.14.*`. The exact archive is
22,369,471 bytes and contains 589 files; its extracted payload was verified byte-for-byte
against the canonical local 1.66.0 install before implementation. Its five political-
movement objects retained by SB are semantically unchanged from CMF 1.65.0. The
SB-used Situation and journal-entry public API is also unchanged. CMF's internal custom
progress-bar backend is containerized, but SB calls none of the removed old dict/struct
APIs.

Use only the exact GitHub tag, commit, asset name, and SHA-256 pinned above for this
rebase. Do not substitute the ambiguous Workshop payload or a later GitHub “latest”
release. Static object equality does not certify widget rendering; CMF/SB startup and
Situation UI remain **Engine pending**.

## Release gate

Before any release or runtime-certification claim:

1. Recheck Steam branch `1.14-openbeta`, build `25081502`, and manifest
   `3868129321396195520`.
2. Rebuild the depot artifact. It must be byte-identical and retain counts
   `182 / 13 / 2`.
3. Run the complete static suite and override checker against the exact installed OB1
   payload and verified CMF 1.66.0 asset.
4. Rotate stale 1.13 logs, cold-launch 1.14, and complete every required runtime-matrix
   row. Record commands, timestamps, and log hashes.

Until step 4 is complete, the correct certification label is **Engine pending**.
