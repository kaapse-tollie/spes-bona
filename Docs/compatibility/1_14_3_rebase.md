# Victoria 3 1.14.3 rebase — SB 0.20.1

Date: 2026-09-19. Scope: new campaigns and the existing maintenance batch.
ORA–BST's two-stage workaround remains **ON HOLD**. No save migration or game launch.

## Exact target and evidence

| Component | Pinned identity |
|---|---|
| Victoria 3 | 1.14.3, Steam build 25347710, branch 1.14-openbeta |
| Core depot | 529341, manifest 5228357714133991559 |
| Previous depot | 1.14.2, manifest 2887980275526736263 |
| SB | 0.20.1; supported game 1.14.3 |
| CMF | Official 1.66.0 plus sb-1.14.3-r1 |

Paradox's [Open Beta Update 2 announcement](https://steamcommunity.com/app/529340/announcements/?l=english)
describes infamy, diplomatic AI, state values, and conquest de-radicalization.
Installed launcher metadata and Steam's app manifest identify the exact target.
[CMF 1.66.0](https://github.com/Victoria-3-Modding-Co-op/Community-Mod-Framework/releases/tag/1.66.0)
remains the latest release checked on this date. Its two later main-branch commits
only add a Manaflow event window and yes/no localization keys.

Reproduce the separate depot report with:

```sh
python3 -B tools/build_1_14_3_depot_delta.py --game-root '/path/to/Victoria 3/game'
```

Both retained manifest identities and byte hashes are verified before comparison.
The result is **92 changed files, three additions, and no removals**. All 95
current changed/added file payloads match their manifest sizes and SHA-1 hashes.
The 1.14.0 and 1.14.2 reports and patch evidence remain unchanged.

## Semantic review before repinning

| Surface | Decision and evidence |
|---|---|
| SB's 37 exact-path overrides, including map/spline assets | No upstream change. Retain existing source and mod hashes. |
| Territorial goals in CMF | Replace old infamy formulas with 1.14.3 state_infamy_value/country_infamy_value. Removing only CMF's land-grab hook makes all three effective definitions match current Vanilla. Control, effects, and territorial mirrors remain Vanilla-owned. |
| Cultural-majority movement in CMF and SB | Migrate six primary_cultures_percent_state comparisons to target_country = owner and one value to primary_cultures_percent_state(owner). Confirmed against current Vanilla and help embedded in the installed executable, without launching it. Keep all CMF additions and SB's only delta: CAP creation/disband exclusions. |
| Cultural minority and minority rights | No API migration required. Preserve their CMF bodies and SB exclusions; only containing-file/dependency hashes change. |
| Seven ideology categories | All seven Vanilla object hashes are unchanged. Preserve the previous payload; repin only the changed containing source file. |
| Regional incorporation | All three Vanilla trigger bodies are unchanged. Keep NAL/Zululand, CAP/Bechuanaland, CAP/Griqualand West, and ORA/Drakensberg priorities with their owner/root guard. |
| Default AI strategy | Inherit updated Vanilla scoring. Ordinary/colonial incorporation dispatch remains intact; ai_can still participates in owned-state value, cession reluctance, and foreign-state value. State-transfer source remains unchanged. |
| GUI | The changed map-list source overlaps CMF's construction_interaction_item_full type. Its only differences are the intended production-method scroll widget. Both previously pinned building-browser types are unchanged. Preserve GUI customizations and pin the additional type. |
| CMF on-action wrappers | Current Vanilla heir-born and country-formed effect bodies are still present unchanged within CMF's blocker wrappers. No new blocker rewrite. |
| Dominion localization | Five keys overlap changed source files. SB's deliberate 10% income/war-participation descriptions remain consistent with its subject policy. Refresh source hashes; do not edit approved prose. |
| Other changed files | Inherit Vanilla's AI strategies, diplomacy/treaty scoring, non-shadowed goals, infamy values, UI, messages, and definitions. No extra balance overrides. |

SB's story goals and exact-subject restoration goals deliberately retain zero
infamy; fixed narrative infamy effects also remain unchanged. Klip's two primary
demands and once-only government settlement are not redesigned.

The current control declarations are unchanged: Annex uses
control_half_target_country_states; Conquer/Return use control_target_state.
This does not certify engine occupation/timer behavior or resolve ORA–BST's
previous report. That scenario remains on hold and awaiting DP's retest.

## Dependency packaging

The official CMF archive and pristine tree are verified before building five
replacement payloads. The new manifest pins all original/resulting hashes and
sixteen Vanilla objects/types. The patch defaults, inventory, and installed-tree
verification move together to sb-1.14.3-r1; neither ordinary sync nor --force may
restore pristine or older-patched CMF. --check remains read-only and --latest is
rejected. Installation stages all validation before replacing the live tree and
retains the existing rollback path.

The three independent review diffs live in patches/cmf/sb-1.14.3-r1 alongside its
manifest and README. The old patch is historical evidence; no upstream PR is sent.

## Verification and limits

Before implementation, the full static audit ran 440 tests with one error and
three historical skips. Its two failed gates were expected compatibility drift
and the historical 1.14.0 manifest no longer being retained by Steam. Other
structural, map, localization, routing, lifecycle, and naval checks passed.

Historical report structure remains tested unconditionally. Rebuilding old
reports requires their exact retained inputs; installed-payload comparison runs
only on the corresponding exact historical build. The current 1.14.3 build,
manifests, and changed payload checks are mandatory.

Post-rebase static results are recorded below. Engine scenarios are
tracked separately in 1_14_3_runtime_matrix.md. All launches and campaign checks
remain with DP; static equality cannot certify timers, AI choices, pop changes,
or event delivery.

## Completed static and packaging verification

- The complete validator, including the installed patched dependency, passes all
  mandatory gates: **17/17 passed or warned, zero failed**. Map data, naval
  connectivity, localization, delayed lifecycle, runtime contracts, exact build,
  Vanilla/CMF inventory, and unit-test discovery pass.
- Focused compatibility/AI/Klip tests: 44 run, two explicit historical skips, no
  failures. Dependency/synchronizer tests: 23 run, two historical skips, no
  failures. These sets overlap; their counts are not additive.
- Before changes, the new current-target tests rejected all three old territorial
  definitions and the old patch identity. The final tests establish full Vanilla
  goal parity except the CMF hook, all six explicit-country comparisons, preserved
  CMF extensions/sibling movements, and SB's only CAP exclusions.
- The old installed sb-1.14.2-r1 tree was rejected by the new read-only check.
  The verified archive was installed through the existing staging/rollback
  function; repeated ordinary sync and read-only checking both report current.
  Tests cover pristine/partial/altered rejection, payload/original hash mismatch,
  forced patched installation, unchanged files, and failed-installation rollback.
- All three review diffs apply to the pristine official archive and reproduce
  exactly the same tree as the replacement payloads. An omitted final newline in
  the upstream ideology file required Git's explicit no-newline marker in its
  review diff; this was corrected and rechecked before delivery.
- Installed CMF tree SHA-256:
  `f4b46205218db8305952208577977f2c28bac7d5c53ae1a6d7ae994733ae559f`.
  Exactly the five declared files differ from the official release. CMF metadata,
  every GUI file, and all other release files are preserved.
- The SB before/after audit confirms the cultural-majority override is the only
  changed runtime script. Existing maps, events, reviewed localization, historical
  reports, and the old CMF patch are unchanged. Inventory counts remain 37 exact
  paths, 109 keyed overrides, 18 state-region blocks, eight localization replace
  files, 20 key collisions, and two Vanilla caller contracts. git diff --check
  passes.

The five existing deferred gates remain **BC-20, BC-22, CP-07, QUAL-09, SUP-05**.
Tiger is advisory and is **not a clean parser certification**: zero fatal,
1,079 errors, 107 warnings, one untidy diagnostic, and one tip. It flags the new
primary-culture value accessor despite that accessor matching current Vanilla;
its output is not grounds for reverting to the obsolete API. Other diagnostics
are retained without claiming that every item is caused by beta-schema lag.

Full output and focused/dependency summaries are retained under
`evidence/1_14_3_rebase_2026_09_19/`. No engine scenario, fresh-launch log audit,
or campaign outcome is marked passed. DP performs those checks using
`1_14_3_runtime_matrix.md`.
