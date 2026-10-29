# Zulu court: prominence and household follow-up

20 October 2026. Source implementation of DP's latest court feedback and the two household clarifications. New campaigns remain the supported baseline. No game launch, save migration, dependency patch or wider country rollout was performed.

## Approved behaviour

- Great Houses shows a named leader and named members, summing eligible adult members' native prominence once. The leader's constitutional preference and personal/succession commitments represent the combined house. A change of head retains the surviving house, but does not inherit the previous head's promises.
- Every adult court member who is not a house leader receives −10 native Prominence, including unaffiliated councillors. Shared-house leadership is ranked before that penalty, preventing subordinate status from entrenching itself. Repeated recalculation does not stack modifiers.
- Eligible adult princes contribute their own prominence and receive +5 native Prominence while their claims remain eligible. A prince without a named shared house leads a personal branch. Minor candidates can receive pledges but contribute no adult house weight. Accession, renunciation or institutional exit removes the claimant bonus as appropriate.
- The princes section shows total, pledged and unpledged prominence, each coalition's prominence and its fraction of the pledged total. The existing 25% major-challenger threshold continues to divide the entire total, including unpledged backing. These are deliberately different denominators.
- Procedural adult politicians, commanders, agitators, magnates and executives enter the local registry unaligned and personally uncommitted. Authored identities and existing commitments take priority. No historical house is inferred from a generated surname. Unaffiliated councillors appear separately from Great Houses and contribute individually.
- ZUL begins with no designated heir. Mpande remains a living politician and eligible prince. Character history sets the existing court-owned CMF heir block; later authored appointments and release conditions retain their existing handling.

No new Prerogative requirement, coercion probability or purchase price is added. Existing claimant-war gates remain test-only; the newly counted backing can now make a prince a major rival. The expanded representative pool does not make active claimants purchasable or allow their self-counted branches to be promised to another prince. Each domestic agitator's prominence is excluded from additional scripted movement recruitment, including junior members of a combined house.

## Presentation and evidence

Court rows now show current offices and native prominence. Princes are excluded from Great Houses; unaffiliated councillors appear under Other Councillors. Traditionalist movement highlights are removed from the JE, while its movement mechanics remain in place. Confrontation tooltips explain failed coercion, flight versus death, the five-year Popularity penalty and the once-per-rival-per-reign limit.

Character buttons now perform only the native OpenCharacterPanel action. Previously they also collapsed the list supplying their Character context. This is a plausible explanation for intermittent navigation, not an engine-verified diagnosis. The supplied error log contains six `FindChild('interest_group_top').TriggerAnimation('show')` failures at 23:52:19. That expression is present in Vanilla's politics-panel and outliner GUI; the log does not identify the court as its caller. No Vanilla panel override was introduced.

No current `autosave.v3` was available in the local save directory or the inspected Steam user data. The screenshots and log were inspected, but older retained February–April checkpoints were not presented as evidence for this playtest. The pre-edit source/log snapshot is retained at `/tmp/sb-court-polish-2026-10-20/`.

## Compatibility review

Baseline remains SB 0.20.2, Victoria 3 1.14.5 build 25629520, and CMF 1.66.0 + `sb-1.14.3-r1`.

Only two existing override contracts change: the SB ZUL character-history hash records the opening heir block and Mpande's politician role; the keyed Mpande template hash records removal of `heir = yes`. Upstream hashes and dependency contracts remain unchanged. Installed Vanilla character role getters and OpenCharacterPanel calls were used as presentation references. No shared Vanilla/CMF GUI or character-interaction definition was overridden.

Localisation changes are general, unreviewed keys tracked in the review queue. The pre-existing reviewed-prose mismatch in `sb_klip_river_county.060`, `.080` and `sb_natal_crisis.050` is outside this change. Their source file is byte-identical to the pre-edit snapshot, SHA-256 `55e494dd832d6d063afb759c9dfc58c128c77a1e18a0fffb615a9959a9295a63`; no approval baseline was regenerated.

## Verification

Focused source-execution checks pass: **85 tests**, including summed houses, replacement leadership, native prominence modifiers, minor eligibility, generated-cast registration, distinct coalition denominators, junior-agitator exclusions and a displaced head's stale purchase quote. These checks model script execution and do not certify native GUI rendering or callback order.

Full discovery: **629 tests; 620 passed, 8 historical-input skips and 1 existing failure; no errors**. The remaining failure is the aggregate validation test reporting the reviewed-localisation mismatch above. No new test failures remain.

Full validator: **15/17 gates passed, warned or skipped**. The two failed gates are unit validation and localisation, both reporting that same pre-existing mismatch. CMF installed-tree verification, override inventory/comparison, map/naval connectivity, runtime script contracts and delayed-event checks pass. The live CMF release-sync check was intentionally skipped; the pinned installed payload remains verified. Five existing deferred gates remain BC-20, BC-22, CP-07, QUAL-09 and SUP-05.

Advisory Tiger: **0 fatal, 1,066 errors, 146 warnings, 1 untidy and 1 tip**. No diagnostic identifies the changed court statements. Tiger still targets 1.13.5 against installed 1.14.5 and retains the known Vanilla/CMF schema limitations; this is not an engine certification. The initial run emitted one fewer warning, with the difference in an unchanged Bechuanaland scope path.

Logs: `/tmp/sb-court-polish-focused.txt` and `/tmp/sb-court-polish-validation-final.txt`. Hashes and the changed-source inventory are in [the evidence record](evidence/zulu_court_households_2026_10_20.json).

## DP handoff

Every new engine scenario remains **pending DP** in the updated [court runtime matrix](../zulu_court_runtime_matrix_2026_10_19.md). Prioritise a fresh ZUL start with no heir, visible +5/−10 modifiers and matching totals; a shared house with a changed leader; new generated councillors; repeated character-panel navigation; and domestic/foreign court rendering. The native same-constitution war probe remains unresolved and explicitly test-only.

The mandatory parallel-review rule is suspended in AGENTS.md while DP reconsiders it. No reviewer sub-agent was spawned for this follow-up; source self-review and static checks were performed.
