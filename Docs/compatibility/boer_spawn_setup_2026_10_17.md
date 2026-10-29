# Boer country creation — 17 October 2026

Target: SB 0.20.2, Victoria 3 1.14.5, CMF 1.66.0 + `sb-1.14.3-r1`.
Scope: Natalia technology inheritance and duplicate armies, with other spawned
Boer tags checked. GDP values remain a polish TODO. No game launch or save edit.

## Retained save evidence

Read `save games/autosave.v3` and the four earlier rotating autosaves under
Victoria 3's user-data directory. The latest game date is **1839-11-01**.

| Country | Country ID | Completed technologies | Live armies in latest save |
|---|---|---|---|
| ORA | 474 | 16 | Potgieter Commando |
| TRN | 16777592 | Same 16 | Pretorius Commando, three units; no surviving empty army observed |
| NAL | 16777900 | Same 16 | Natalia Commando, two units, plus an empty default army |

All three completed sets contain `enclosure`, `standing_army`, `urbanization`,
`mandatory_service`, `military_drill`, `line_infantry`, `rationalism`,
`tech_bureaucracy`, `democracy`, `romanticism`, `international_trade`, `navigation`,
`international_relations`, `colonization`, `urban_planning` and `academia`.
None contains `empiricism`.

ORA's Empiricism record is unfinished (`is_researched=no`), with progress 2500
in the latest save. The July, August, September and October autosaves show
unfinished progress of 1600, 1850, 2050 and 2250 respectively. NAL is absent in
those earlier saves. These records do not reproduce loss of a completed
technology. Keep native `origin` inheritance; do not add fixed grants or an
invented copy effect. DP confirmed on 17 October that the completed technology
was Academia and asked to clear the flag. `PT-20261016-04` is closed as a
mistaken observation; no further technology-loss investigation is required.

NAL's formation `838861841` is unnamed/default, ordinal 1, with no units.
Formation `889193466` is `natalia_commando`, ordinal 2, with one dragoon and
one line-infantry unit. Both were created on **1839-10-27.18**. This confirms
the reported extra army. It does not establish that every other Boer tag had
the same runtime symptom.

## Source correction and route audit

The old NAL route transferred/created Pretorius before creating the intended
commando. The peaceful route commissioned its ruler and transferred/created
Retief first. TRN and the ZPB/LYD shared baseline also commissioned generals
before creating their authored formations. Muster first, complete character
setup, then assign the intended commander. Preserve the original unit packages.

| Tag / route | Technology origin | Army handling |
|---|---|---|
| NAL, Blood River | ORA | Move the two-unit muster before Pretorius transfer/creation; assign final ruler afterwards. |
| NAL, peaceful / guns bargain | ORA | Move the existing three-unit peaceful or two-unit war branch before baseline/Retief setup; assign final ruler afterwards. |
| TRN, all six creation provinces | ORA | Seed the commando before baseline/cast; retain later Andries/Marthinus selection and assignment, then generated-commander cleanup. |
| ZPB | ORA | Shared commando creation now precedes ruler commissioning; retain the existing Schoeman handoff. |
| LYD | TRN | Same shared ordering fix; retain Potgieter handoff and the existing guarded muster fallback. |
| KLR | ORA | Unchanged: Spies is a civilian founder, and the authored muster already requires no army and no prior muster marker. |
| NRP | TRN | Unchanged: its setup has no second authored army; the shared ZPB/LYD muster excludes it. |
| SGO, both founding systems | Actual founder | Unchanged: no second authored army; saved-creator and direct-button `root` origins retain the actual sponsor. |

The separate direct British Natal route retains CAP as origin. No fixed
technology grants or resets were found in the audited successor setup paths.
Existing technology regression tests cover the origin choices and absence of
fixed technology floors; they cannot certify the engine's inheritance behavior
for an unplayed route.

Reference patterns inspected: installed Vanilla's formation/commander setup,
Hail Columbia's Seminole `osceola_warband` creation before Osceola, and Gates of
the Bosphorus's assignment of Reshid Mehmed to an existing formation. No new
script API or blanket empty-army deletion is introduced.

## Verification and DP handoff

**92 focused tests passed**, including technology-origin contracts, founding
order, the Natal routes, frontier setup and Klip scope checks. All five new
army regressions fail against the original runtime source and pass after the
correction. Every formation definition and unit payload in the three edited
runtime files matches its original definition; UTF-8 BOMs and the 25,000 GDP
gate are preserved. `git diff --check` passed.

Full discovery ran **497 tests: 488 passed, eight historical skips, one failure**.
The failure is unrelated reviewed-localisation bookkeeping: the pre-existing
`sb_natal_crisis.050.f` spelling correction from `Pretoriius` to `Pretorius` no
longer matches its approved-text regression baseline. This task changes neither
that prose nor its approval baseline. The eight skips remain the historical
manifest/build prerequisites listed in the [rebase report](1_14_5_rebase.md#explicit-historical-skips).

The full validator with `--skip-cmf-sync --tiger` reports **12 PASS, two WARN,
one SKIP and two FAIL**. Both failures represent the same localisation mismatch
(the unit-test gate and the localisation gate). CMF verification, compatibility
inventory, map/naval checks, script contracts, routing and lifecycle checks pass.
Dependency synchronization was deliberately skipped; installed CMF was verified
read-only. Warnings are the existing five deferred gates and advisory Tiger.
Tiger's totals match the rebase report: 0 fatal, 1,061 errors, 130 warnings,
one untidy and one tip; its schema targets 1.13.5. No diagnostic's primary
location is in the three runtime files changed here. This is not engine
certification. The full diagnostic transcript remains in
`/tmp/sb-boer-spawn-validation-final.txt`.

DP should restart with the corrected scripts and load a checkpoint **before
the affected country is created**. Check one intended army, its units and its
commander on each route. Existing saved empty armies are not removed by this
correction. Runtime row `B145-22` tracks the pending army checks; `B145-23`
records closure of the mistaken technology-loss report.
