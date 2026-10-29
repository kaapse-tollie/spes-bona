# Victoria 3 1.14.5 rebase — SB 0.20.2

Date: 2026-10-16. Supported baseline: new campaigns. DP performs game launches
and engine verification. ORA–BST's workaround remains **ON HOLD**; the proposed
Zulu ideology/Chiefdoms redesign and Victoria 3 1.15 are outside this rebase.

## Target and evidence

| Component | Identity |
|---|---|
| Victoria 3 | 1.14.5; Steam build 25629520; branch 1.14-openbeta |
| Core depot | 529341; manifest 5521822647051867164 |
| SB | 0.20.2 in both metadata and descriptor |
| CMF | Official 1.66.0 plus the unchanged sb-1.14.3-r1 patch; launcher relationship 1.66.* |

The [Paradox announcements](https://steamcommunity.com/app/529340/announcements/?l=english)
describe the beta's AI, naval, war-goal and capitulation changes. The installed
beta retains war-goal expiry: a goal cannot be dropped before the war has lasted
24 months; the uncontested-goal threshold is 12 months since creation or last
contest, with a three-month warning. These are goal-expiry gates, not a fixed
24-month deadline for ending every war. The announced
expiry reversal concerns the forthcoming 1.15 release; it is not backported here.

Steam no longer retains the 1.14.3 core manifest. This report does **not** claim a
complete 1.14.3→1.14.5 depot comparison. Two complementary records cover the rebase:

- [Retained 1.14.4→1.14.5 depot delta](1_14_4_to_1_14_5_depot_delta.json):
  **147 changed files, two additions, no removals**. Both manifest identities,
  byte sizes and SHA-256 hashes are checked before comparison; all 149 current
  payloads are checked against their manifest sizes and SHA-1 hashes.
- [SB's complete pinned-source comparison](1_14_3_to_1_14_5_contract_review.json):
  all **175 Vanilla source contracts** from the 1.14.3 inventory at checkpoint
  `2d4106cdc0ccf17ddebe389e0c87af0134253347`, recording old/current hashes before
  repinning. This includes 39 exact paths, 109 Vanilla-backed keyed objects,
  five localisation replace sources, 20 localisation collisions and two AI
  caller objects. The remaining three keyed objects have no Vanilla source.
  Mod-only replacement prose, the additive override, CMF dependency baselines,
  and all 16 CMF upstream contracts remain independently checked by the inventory.

Reproduce the depot record with:

```sh
python3 -B tools/build_1_14_5_depot_delta.py --game-root '/path/to/Victoria 3/game'
```

The old manifest is 2774789085913801937 (1.14.4, build 25483263). Its provenance
is Steam's retained manifest and the completed update recorded in Steam's
content log. Historical reports and patch payloads remain unchanged.

## Semantic review before repinning

| Surface | Comparison and decision |
|---|---|
| Three AI incorporation triggers | Adopt complete 1.14.5 bodies. Eligibility adds ≥50% primary culture, or ≥25% beside an incorporated state owned by the evaluating country. Ordinary incorporation now calls eligibility plus the population minimum. Colonial incorporation retains same-region/owned-incorporated adjacency and also admits eligibility, with the population minimum. Keep the four AI-only, correct-owner SB exceptions. |
| Colonial claims | Adopt the acquire-states regional objective's +0.05 chance, +20 state weight and target-priority qualification. The only SB difference is the existing Boer-culture exclusion for its 17 authored regions. No new infamy change. |
| Scramble for Africa | Port Vanilla's is_at_war = no failure guard. Preserve SB's growth modifier, weekly presence check and completion/failure cleanup. No peace condition is added to any SB story settlement. |
| European military formations | The exact-path source changed across the pinned baseline. Restore 14 native early troop-ship additions; retain all five existing Portuguese armies, including the redistribution and African formations. Every other parsed formation and every fleet now matches Vanilla. |
| Other 38 exact paths, including maps and splines | Upstream hashes unchanged. Retain SB payloads, locators, province raster and structured spline fixes. The retained 1.14.4→1.14.5 delta alone has no exact-path SB collision; the older pinned contract comparison is what exposes the formation gap. |
| Highveld | Native JE body changed, but SB deliberately disables the entire Vanilla JE. Repin the source; preserve the disabling replacement unchanged. |
| Default AI strategy | Inherit current regional-objective, resource and state valuation. Preserve native ordinary/colonial dispatch. Eligibility contributes to owned-state value, cession reluctance and foreign-state value; it now also contributes indirectly to incorporation through the new trigger bodies. SB does not replace the strategy. |
| State transfer | Inherit native ai_state_value scoring and regional-objective acquisition preference. The source-side neighboring incorporated/eligible state check remains native. SB adds no treaty-scoring override. |
| Ruler/retirement interactions | Containing source changed; grant_command_to_ruler, remove_command_from_ruler and retire_commander object hashes did not. Keep SB's existing deltas and refresh source-file pins only. |
| Society technology | Containing source changed; civilizing_mission and malaria_prevention object hashes did not. Keep SB's existing changes and refresh source-file pins only. |
| Dominion localisation | Six collided keys occur in changed containing files. Current Vanilla's ordinary dominion text remains different from SB's deliberate 10% income and optional overlord-war policy. Preserve SB wording and refresh source-file pins; no approvals are regenerated. |
| Other keyed/source contracts | Unchanged pinned objects/files. No unrelated gameplay changes are imported into SB-owned definitions. |
| Naval network | Verify the current graph before repinning: **6,641 nodes, 7,192 connections, all 33 SB ports connected**. SHA-256 e19541f8334abb62db079b2cff4120df208db229ec5f7a7de58bfdbfc8d6f636. SB still supplies no network shadow. Malformed-network and disconnected-port rejection remain tested. |

## Dependency and bookkeeping

[CMF 1.66.0](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.66.0)
remains the latest release checked for this rebase. Its three later unreleased
commits concern a Manaflow placeholder, yes/no localisation and an author name;
none requires a compatibility payload change. All **16** current upstream
contracts match, including territorial goals, seven ideology categories and GUI
types. The five payloads and patch manifest remain byte-identical. The installed
tree retains digest `f4b46205218db8305952208577977f2c28bac7d5c53ae1a6d7ae994733ae559f`.
Territorial definitions still differ from Vanilla only by CMF's land-grab hook.
Read-only checks, staged installation, original/result hashes, rollback, forced
patched installation and rejection of --latest remain unchanged.

DP explicitly approved the current working-tree text of `sb_boer_conventions.141`.
Only that exact event namespace is added to the regression baseline: five key
lines, 708 bytes, SHA-256
`8e6d62ea3e3d6f6afc98f0377b991a68d8a9c833eec7303a70345c840ac2c756`.
Its wording and REVIEWED marker are untouched. Tests reject later unapproved
edits and keep underscore suffixes/neighboring event namespaces outside approval.
All other baseline rows remain unchanged.

The Shepstone test no longer prohibits an unrelated indenture goal label. Its
300-month repeal lock and independence from the indenture JE remain tested. A
separate check covers the existing goal text, live population counter and
100,000 population target; no runtime content changes for this correction.

## Validation and limits

Current build identity, manifest integrity and installed payload checks are
mandatory in the compatibility checker and current-target tests. Historical
report structure remains mandatory; reproduction may skip only when its exact
historical inputs are absent, and historical installed-payload comparisons run
only on the matching build. CMF's active compatibility tests remain unconditional
even though the retained patch was authored for 1.14.3.

Before the ports, the new claim/Scramble/formation parity checks all failed and
the AI tests rejected the obsolete eligibility bodies. After the four ports,
all 20 focused AI/current-target/port checks pass. The expanded focused run
passes 65 tests with three historical skips. No engine success is inferred from
static results.

Every fresh-game case in [the DP runtime matrix](1_14_5_runtime_matrix.md) remains
**Engine pending — DP**. Story settlements, deliberate infamy exemptions and
native expiry/capitulation behavior are preserved, with partial/expired/reversed
demands requiring explicit engine checks. No game launch, save migration,
dependency rewrite or 1.15 behavior backport is part of this rebase.

## Completed static verification

The full validator completed successfully: **15 PASS, two WARN, zero FAIL and
zero skipped gates**. The warnings are the five existing deferred gates and
advisory Tiger diagnostics. Evidence is retained in
[evidence/1_14_5_rebase_2026_10_16](evidence/1_14_5_rebase_2026_10_16/README.md).

- Complete unit discovery passed. The suite contains **487 cases**; eight
  historical checks skip for the explicitly recorded reasons below. The validator
  suppresses successful unit subprocess output, so the evidence separately records
  suite discovery and the exact historical skip results.
- The current 1.14.5 build/manifest/payload tests, all 175 pinned-source contracts,
  retained CMF definitions and all 16 CMF upstream contracts pass. Direct inventory:
  39 exact paths, 112 keyed overrides, 18 state-region blocks, one additive
  override, nine localisation replace files, 20 key collisions and two AI callers.
- Dependency tests cover clean patched installation, repeated/read-only and forced
  sync, pristine/partial/altered-tree rejection, payload/original hashes,
  installation failure rollback, unchanged upstream files and --latest rejection.
  The live dependency passed read-only verification and was not reinstalled.
- Local map validation, structured spline checks, naval structure/all 33 ports,
  localisation review boundaries, on-action routing, stale/unused symbols,
  runtime script contracts, 86 scripted war-goal blocks and delayed lifecycle pass.
- DP's `.141` file is byte-identical to the initial working copy; every other
  localisation baseline row is unchanged. Maps, graphics, story/event scripts,
  all CMF patch payloads and historical reports are unchanged. The working diff
  passes whitespace checks; new diagnostic transcripts trim trailing whitespace
  only, without removing any diagnostic.

### Explicit historical skips

| Evidence test | Missing prerequisite |
|---|---|
| 1.14.0→1.14.2 report reproduction | Exact retained 1.14.0/1.14.2 manifests |
| Installed 1.14.2 payload | That exact historical build is not installed |
| 1.14.2→1.14.3 report reproduction | Exact retained 1.14.2/1.14.3 manifests |
| Historical 1.14.3 manifest tamper rejection | The 1.14.3 manifest is not retained |
| Installed 1.14.3 payload | That exact historical build is not installed |
| Original OB1 depot report reproduction | Exact retained old/OB1 manifests |
| Original old-manifest tamper rejection | The old manifest is not retained |
| Installed OB1 payload | That exact historical build is not installed |

The retained 1.14.4→1.14.5 reproduction ran successfully. Current-target manifest
absence/tampering and missing/altered installed payloads are failure cases, not
historical skips. The three added historical skips replace the old assumptions
that 1.14.3 is still installed/retained; its active CMF checks still run.

### Tiger and deferred work

Tiger reports that its schema targets **1.13.5**, while the game is **1.14.5**.
Its complete result is **0 fatal, 1,061 errors, 130 warnings, one untidy and one
tip**. This is advisory, not a clean parser certification. Exact mod/CMF load
sentinels and the final summary were verified by the validator.

All seven error diagnostics touching the edited runtime files refer to native
1.14.5 constructs: three regional-objective calls in colonial claims and four
primary-culture comparison diagnostics in incorporation. Full-body parity checks
confirm those constructs match current Vanilla. Fleet warnings concern repeated
native ship blocks or unchanged Vanilla character/name/supply-hub definitions;
AI scope warnings likewise concern the native explicit-country API. The
single-item AND tip reflects the existing wrapper used to preserve native bodies.
None justifies replacing current native syntax with the older schema. Other
Tiger diagnostics are retained without claiming they are all schema false positives.

The five release gates remain **BC-20, BC-22, CP-07, QUAL-09, SUP-05**. The separate
resource-content item remains deferred too. Runtime certification, CAP deployment,
war-goal expiry/reversal and all 21 matrix rows remain pending DP.

## DP launch-log follow-up — 16 October 2026

The supplied 19:21 launch log identifies three write-only Chiefdoms variables:
`sb_zululand_thirteen_chiefdoms_route_var`, `sb_zululand_nal_scope` and
`sb_zululand_zul_scope`. Each had one assignment and no script, localisation,
GUI or CMF reader. Removed those three writes only; the resolved-state marker,
country selection, container counters and settlement effects remain unchanged.
The stale-symbol gate rejects their reintroduction. All 45 focused Zululand,
movement-contest and Klip tests pass after removal.

This is a follow-up cleanup to the four runtime rebase ports above. The supplied
log also retains CMF blocker notices, the known spline/harbor warnings, redundant
indenture `_goal` localisation, the orphaned original Portuguese event, and an
unset `enforced_by_timer` event-target warning. These are separate from the three
unused variables and were not changed by this cleanup. The launch is therefore
not certified clean; a fresh log after DP restarts remains pending.
