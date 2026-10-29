# Zulu institutions — DP launch follow-up, 18 October 2026

Baseline: SB 0.20.2, Victoria 3 1.14.5, CMF 1.66.0 + `sb-1.14.3-r1`.
Input: DP's `Victoria 3/logs/error.log`, beginning at 21:15:09; SHA-256
`6cf21fc5b431ae09ec1dd75ae5706c6534da77cafba19d7ee9de442284d1f460`.
The input contains both load-time diagnostics and errors after entering play.
No game was launched and no save was changed during this repair.

## Corrections

| Observed diagnostic | Source correction | Verification |
|---|---|---|
| Three `Named value not found` errors in movement-modifier restoration | Replace the bare `days = var:…` duration with the named formula `sb_natal_movement_remaining_days`. Keep the original expiry, multiplier, decay and one-off receipt. | Existing three-modifier lifecycle/expiry tests now reject bare duration links and execute the named formula. Native duration parsing/evaluation inspected read-only; runtime remains pending. |
| Unsupported `should_be_pinned_by_default` on the coup JE | Use the documented `should_be_pinned_by_default_uninvolved_or_context`. | Source contract checks the accepted field. |
| Eight explicit-stance warnings for the two chiefly laws | Make Federated Chiefdoms and Chiefly Council independent laws. Their approved modifiers and ideology matrices are unchanged. | Tests reject a parent on these laws. In particular, Chiefly Council no longer inherits Autocracy's contrary stances via Elder Council. |
| 168 script errors removing absent Prerogative modifiers | Guard both optional components during recalculation and cleanup. Apply the same correction to this implementation's optional following and coup modifiers. | Source-executing fixtures now reject absent removal; repeated neutral updates, exit and re-entry pass. |
| 940 successor-list warnings | Replace twelve positional queries with one ordered, bounded iteration, filling only available candidate slots. Clear previous menu selections first. | Zero/one/two/three/twelve/fourteen candidates, dead/underage exclusions, unique ordering and foreign-root isolation are covered. |
| Two duplicate opening Zulu JE warnings | The law-activation callback waits for the existing post-lobby marker, allowing country history to author the opening JE first. | A history-law callback followed by history insertion and repeated reconciliation adds the entry once. Engine ordering still needs DP confirmation. |
| Two redundant `_goal` localisation warnings | Coup objective text moves unchanged to the displayed status field. Remove only the duplicate indenture `_goal`; its identical progress description and explicit 100,000 completion tooltip remain. | Goal/progress and coup presentation contracts retain the existing content and conditions. |

The independent Federated Chiefdoms law no longer qualifies for Vanilla's
hereditary Chiefdom government. Its former exclusion override is therefore
removed, along with that inventory entry. The dedicated council-selected
government remains. Current inventory: 38 same-path files, 118 keyed replacements
and eight localisation replacement files; no upstream or dependency hashes were
refreshed.

## Amabutho stance decision resolved

DP approved Traditionalist strong approval for the shared Peasant Levies family.
The stance now targets `law_peasant_levies`; the rejected explicit Amabutho entry
is removed. Amabutho retains its parent and inherits `++`, as do the family's
other variants. This supersedes the original ordinary-Peasant-Levies N/A position.
The regression contract checks the approved matrix and Amabutho's inherited
stance. After this decision, all 45 laws, institutional-core and court-politics
tests passed, and `git diff --check` passed. The broader validation below predates
this one-line stance change. Fresh-launch confirmation remains pending DP.

## DP interface follow-up

DP's screenshots exposed raw variable/list requirements, duplicated court
buttons and the old dynamite icon. Court requirements and the Social Mobility
restriction now use named tooltips. The four negotiation blockers, Prerogative
costs and eligible-character checks remain separate readable requirements.
The extra CMF button widget is removed; the default grid retains all four court
actions. The icon now uses Japan's `event_scales.dds`, inspected as the gavel.
New court/Chiefdoms text uses British spelling, recorded in `AGENTS.md`.

Removing only the tooltip wrappers produces the same parsed conditions and
effects as before, including state-owner scope and Vanilla's decree restrictions.
The decree's inventory hash was refreshed after that comparison; upstream pins
and CMF are unchanged. All **48 focused tests** and override-inventory validation
pass. Localisation validation reports only the existing review-baseline drift
for `.050`, `.060` and `.080` listed below. The ten new general tooltip keys are
queued for prose review. In-game tooltip/layout confirmation remains pending DP;
no game launch was performed.

## Diagnostics outside this repair

- CMF's duplicate `regency.1` and its two on-action blocker definitions originate
  in the pinned dependency. That dependency was not edited.
- The spline anchor, fifteen harbor-node notices and Cape/Benguela graphics
  warnings match the existing map/spline issue. The design hold is unchanged.
- The `enforced_by_timer` warning concerns an engine-provided callback target;
  removing its checks would alter settlement handling.
- `portuguese_colonialism.4` is the intentionally uncalled Vanilla event after
  SB routes the Pink Map chain through `sb_pink_map.040`. It is already documented
  in the [earlier launch audit](1_14_0_launch_debug_2026_09_05.md).
- Filewatcher listener notices are recorded separately from script diagnostics.

## Verification and handoff

Results are recorded in the [evidence file](evidence/zulu_institutions_launch_2026_10_18.json):

- **90 focused checks pass** across institutions, court selection, laws, movement
  preservation, annexation, Klip settlement and the Natal gameplay contract.
- **Final unit discovery: 576 tests, 567 passed, one failure, eight historical
  skips, no errors.** The sole failure is the pre-existing reviewed-localisation
  baseline drift for `sb_natal_crisis.050`, `sb_klip_river_county.060` and `.080`.
  Their wording and approval baselines were preserved.
- The full validator's compatibility, map, naval, routing, lifecycle, symbol and
  current-build gates pass. Its unit/localisation gates report the above approval
  issue. The final government-override removal briefly exposed a stale `119`
  inventory-count assertion; corrected to `118`, with its 14-test module and
  final complete unit discovery rerun.
- Installed CMF verification and dependency installation/rollback tests pass.
  Dependency synchronization was intentionally skipped; CMF was not altered.
- Advisory Tiger reported 1,066 errors and 146 warnings against its older 1.13.5
  schema. The one new encoding warning on the named-value file was corrected to
  UTF-8 BOM and checked directly afterward. The full Tiger pass preceded that
  encoding correction and removal of the redundant government override; it was
  not represented as a fresh engine validation. Other warnings retain the
  previously documented schema/native-scope limitations.
- `git diff --check` passes. Eight historical evidence skips and the five existing
  deferred release gates remain identified by the validator.

DP's next launch should check the parser output, opening Zulu JE, neutral-P
cleanup and successor menu. In a separate annexation replay, check that Initial
Enthusiasm and the two Shepstone bonuses retain their remaining strength and
expiry. The wider court/civil-war/Chiefdoms matrix remains pending; these source
fixes do not establish those engine outcomes.
