# Zulu national movement after early Klip River annexation

Investigation and authorized follow-up, 17 October 2026. The original investigation
below describes the original source and retained saves. The attraction-only
attempt and its replacement are recorded below; no dependency or saves changed
and no game launched. Registered as `PT-20261017-09`.

Latest status: **DP reports early replacement B works; three-modifier preservation
implemented; engine testing TODO, explicitly deferred by DP on 17 October 2026**. After A failed and direct assignment of
2,500 existing peasants proved unavailable, DP authorized movement replacement.
The latest follow-up retains the remaining Initial Enthusiasm and both Shepstone
attraction grants through that replacement. See [the current preservation
contract](#authorized-modifier-preservation); earlier sections preserve the failed
attempt, original evidence and replacement-only baseline.

## Finding

The direct-administration branch **reuses an old movement**, rather than creating
a new post-annexation movement. The saves confirm that it disbands ten days after
annexation. Native low-support disbanding after the enlarged population dilutes
its backing is the leading explanation; the exact support calculation on the
day of removal is not retained in these saves.

The inspected target is Victoria 3 1.14.5, build `25629520`, with CMF 1.66.0 plus
`sb-1.14.3-r1`. Save hashes and selected records are in the
[evidence file](evidence/zulu_national_movement_2026_10_17.json).

## Confirmed timeline

NAL is country `16777900`; its Zulu cultural movement is `16777961`.

| Date | Evidence |
|---|---|
| 27 October 1839 | Movement's saved `start_date`; its initial-enthusiasm modifier starts on the same date. |
| 1 June 1850 | Movement is alive with 23 supporting pop records. NAL has 127,695 Zulu people and already carries `sb_zulu_national_movement_initial_enthusiasm_var`. |
| 6 June 1850 | Zululand's saved `last_owner_change`; subsequent NAL flags confirm the direct-administration choice. |
| 16 June 1850 | Movement manager's `dead.dead_objects` explicitly records this movement's `death_date`. |
| 1 July 1850 | Latest `autosave.v3`: NAL has 399,737 Zulu people, including 269,615 in Zululand. The old movement remains as a dead database record, with its supporter list cleared. |
| 1 August 1850 | Retained `autosave_1.v3`: old movement has been removed from the database, with no replacement Zulu cultural movement in NAL. |

The latest file by modification time is the July autosave; the August rotation
is a retained later-game checkpoint. Both July checkpoints agree on the removal
date. The 23 June supporter pop records still exist in July, retain Zulu culture
and their Natal location, and can still support other movements. Their missing
Zulu-movement support is **a consequence of disbanding**, not evidence that they
all abandoned it before 16 June.

## Source path at investigation and native rules

1. `sb_zululand_choose_direct_natal_administration` in
   `common/scripted_effects/sb_zululand_settlement_effects.txt` annexes the live
   ZUL subject, adds Zulu radicals and calls
   `sb_natal_create_zulu_national_movement`.
2. That shared helper, in `common/scripted_effects/sb_natal_interwar_effects.txt`,
   creates a cultural movement only if one does not already exist. It does not
   restart an existing movement's age or seed its membership in the new state.
   Its one-time country flag also prevents another initial-enthusiasm grant.
   The existing decaying enthusiasm modifier itself has not expired: its end
   date is 27 October 1859.
3. The effective movement is CMF's `REPLACE:movement_cultural_minority` in
   `common/political_movements/ycom_02_cultural_movement.txt`. Its territorial/
   culture disband trigger and eligible-pop trigger match current Vanilla.
   Zulu remains non-primary in NAL, and NAL owns strongly Zulu-populated homelands
   in Natal and Zululand. The saved conditions do not satisfy that scripted
   disband trigger. Nationalism affects weight, not basic creation eligibility.
4. Native `movement_category_cultural` requires **10% support within its cultural
   identity** to survive. `MOVEMENT_MIN_SUPPORT_GRACE_MONTHS = 12` protects only
   the first year after creation. The 1839 movement is long past this grace.
   Neither SB nor CMF replaces these category/grace rules.

Read-only inspection of the installed arm64 executable's named functions
`CPoliticalMovement::ShouldDisband` and `CalcPopSupportData` confirms that the
engine has a low-support removal check separate from the scripted trigger. It
compares movement age, backing-character presence and the category threshold;
cultural support uses country-wide culture-specific popular, military and
wealth denominators. The saved movement has no backing characters. The native
update calculates support before checking whether to disband.

Thus annexing roughly 270,000 additional Zulu people can lower the existing
movement's measured backing before those people join it. Adding radicals does
not directly assign movement membership. Reusing the movement grants no fresh
grace while that support adjusts. This fits the observed ten-day disappearance.

This is **not an exact reconstructed 16 June support percentage**. Monthly saves
do not retain that day's score or an explicit reason for disbanding. Raw supporter
counts divided by total population would be misleading: native movement support
also includes military and wealth components. No SB movement-deletion effect or
movement-specific script error was found to explain this result. The native
annexation path was not executed or modified during this investigation.

## Investigation follow-up, before implementation

Investigate a local post-annexation support treatment for the existing movement,
including the newly acquired population. Do not assume that refreshing an
attraction modifier also resets the native grace period, or that merely relaxing
the movement's scripted disband trigger bypasses the native minimum-support
check. Recreating the movement would discard its identity/history and should not
be introduced as an incidental repair.

Before choosing a correction, DP can replay the retained 1 June checkpoint and
inspect the movement's native support breakdown immediately before annexation,
immediately after, and before 16 June. That would establish the exact crossing
of the 10% threshold. Both the aged-existing-movement case and a genuinely absent
movement need verification because the shared helper has other callers.

Only evidence/documentation checks were run for this investigation. No corrected
engine behavior or new runtime test is claimed.

## Authorized implementation — attraction only

DP authorized proposal A after the guard investigation. The direct-Natal
administration choice now branches on actual movement existence, after annexing
the ZUL protectorate:

- Existing native Zulu cultural movement: add `sb_zulu_annexation_movement_attraction`
  (**Annexation of Zululand**), +100% pop attraction decaying over twenty years.
  Preserve the movement, its supporters/activism and any remaining Initial Enthusiasm.
- Absent movement: use the existing creation helper and ensure this new instance
  receives native Initial Enthusiasm even if Natal retains its old country grant
  marker. It receives no additional annexation bonus.

The existing settlement-resolved gate provides once-only execution. Shepstone
refusal/repeal synchronization remains in both branches. The shared foundation
helper and GBR's direct-rule branch are unchanged. No country marker is removed,
new recovery lifecycle added, membership assigned or native grace renewed.

The touched choice's annexation check now identifies `c:NAL` explicitly rather
than event `ROOT`, matching its NAL-only eligibility trigger. This ensures a
foreign-root invocation still annexes the actual protectorate before applying
the recruitment treatment. Source fixtures cover NAL, ZUL, GBR and diplomatic-play
roots, including other countries' and other types/cultures of movement.

The modifier has a new name/description in the general localisation review queue.
The revised `.030.a.tt` describes both branches under its existing event namespace's
`TO REVIEW` marker, also noted in the queue. Reviewed prose is unchanged.

The new regression module failed against the old treatment (including absence of
enthusiasm with the old country marker and the foreign-root annexation skip).
After the change, all **87 focused tests passed** across the new movement tests,
Klip punitive settlement, Natal interwar, postwar settlement and Natal/Zululand
contracts. These execute source branches and record effect calls; they do not
simulate native recruitment, support calculations or disbanding.

Final full validation: **515 unit cases, one failure, eight historical skips**.
The failure is `test_repository_manifests_are_current` in `tests/test_validate.py`.
The validator's
separate localisation gate reports the same pre-existing reviewed-baseline drift
in `sb_klip_river_county.060`, `sb_klip_river_county.080` and
`sb_natal_crisis.050`, all in the untouched `sb_natal_crisis_l_english.yml`.
Their prose and approval baseline were not changed for this task. The new
modifier review group and revised unreviewed tooltip introduce no remaining
localisation errors.

The final non-Tiger validator has **12 PASS, one WARN, one SKIP, two FAIL**:
the two failing gates above share that localisation issue. CMF installation,
override inventory/parity, map/naval checks, runtime contracts, symbol checks,
on-action routing, release invariants and delayed lifecycle pass. The warning
is the five existing deferred-release gates; dependency sync was deliberately
skipped while installed patched CMF was verified read-only. Advisory Tiger also
ran: **0 fatal, 1,061 errors, 130 warnings, one untidy and one tip**, matching the
recorded aggregate from the 1.14.5 rebase. Its old schema lacks native container
and other beta APIs; no diagnostic targets the changed annexation block or new
modifier. It is not a clean engine certification.

Validation transcripts are `/private/tmp/sb-zulu-annexation-focused.txt`,
`/private/tmp/sb-zulu-annexation-validation-final.txt` and the separate advisory
run `/private/tmp/sb-zulu-annexation-validation.txt`. The final command used
`tools/validate.py --skip-cmf-sync` with explicit installed game/CMF roots;
the advisory run additionally used `--tiger`. Working-tree whitespace checks pass.

**Engine pending — DP:** restart with the updated scripts and replay a checkpoint
before the direct-administration choice. In the early example, retain movement
16777961 and its 1859 enthusiasm expiry, observe the new bonus, then continue
past 16 June and through several monthly updates. Record native identity support
before/after annexation and whether the movement survives. Separately test a late
existing movement and an absent movement with the old grant marker; save/reload
must not refresh the twenty-year duration. A post-disappearance checkpoint cannot
test preserving the old instance. See `B145-26` in the runtime matrix.

The attraction change is implemented, **not a verified cure for rapid native
disbanding**. One-time recovery B remains deferred if DP's replay reproduces it.

## DP replay and `.030` follow-up

DP reports that the attraction-only change did not prevent disappearance and
requested assigning 2,500 peasants in Zululand to the movement, if possible,
without documenting that internal seeding step in the option tooltip. No new
removal-day support/date was supplied; the original save evidence above is not
relabeled as evidence from this replay.

Rechecked the installed 1.14.5 executable's registered movement/pop/support
effects and native `political_movements.md` / `political_movement_pop_support.md`.
The movement definitions expose eligibility and attraction weights, not an
effect assigning existing supporters. The effect registry exposes movement
creation and defeat handling, geographic pop moves and IG-support recalculation;
none assigns 2,500 existing peasants to this movement. No such command, pop
creation, save edit, recovery B or tooltip seeding text was introduced. The
movement-disappearance issue remains open.

DP's two additional `.030` changes are implemented:

- All three option tooltips use available native/CMF/SB concepts for incorporation,
  states, pops, radicals/loyalists, rulers, cultural movements, subject types,
  Chiefdoms, International Situations and relations where applicable. There is
  **no dedicated Pop Attraction concept** in the installed concept definitions;
  the phrase now opens Vanilla's `political_movement_pop_attraction_mult_desc`
  through the same rich-tooltip form used by Vanilla's Eastern Crisis text.
- Control the Crown replaces only ZUL's +10% Zulu loyalists with **+15 relations
  between ZUL and NAL, and +15 between ZUL and GBR**. NAL retains its own +10%
  Zulu loyalists. Crown identities, protectorate status and the once-only settlement
  gate remain unchanged. `.030.c.tt` reflects these actual effects.

The new source-driven regression fails against the old Crown effect and passes
with the change, checking both relation pairs, NAL-only loyalists, repeated
execution, preserved protectorate status and four event-root contexts. All
**88 focused tests pass** (`/private/tmp/sb-crown-relations-focused.txt`). Every
concept reference in the three tooltips and the native attraction-description key
resolves against installed definitions. No game was launched; actual hover
presentation and Crown rewards remain **Engine pending — DP**. The movement
test is **DP reported failure**, not pending or passed.

Targeted runtime-script, stale/unused-symbol and local-inventory checks pass.
The localisation check still reports only the previously recorded reviewed-baseline
drift in Klip `.060`/`.080` and Natal Crisis `.050`; those files and approvals
were not changed for this follow-up. Working-tree whitespace checks pass.

## Authorized replacement — B

DP's final instruction is: disband the existing movement, if present, and recreate
it. This is proactive replacement at annexation, superseding A and the earlier
provisional proposal to wait for a disappearance during a first-year window.

After NAL annexes ZUL, the once-only direct-administration option marks only its
Zulu `movement_cultural_minority` instance. The CMF-derived replacement definition
adds this marked NAL/Zulu case to the existing disband conditions. Its native
`on_disbanded` callback sets a pending marker on the **owner**, then queues hidden
`sb_natal_interwar.031` for the following day. That receipt consumes its marker
before creation. If no movement existed at annexation, creation is immediate.

The fresh instance receives native Initial Enthusiasm (+100% pop attraction,
decaying over twenty years) despite Natal's old country grant marker. It gets a
new creation date and native first-year minimum-support grace. Old supporters,
activism, identity, history and remaining enthusiasm are not copied. Existing
Shepstone attraction synchronization remains in the shared creation helper. The
separate Annexation of Zululand modifier, its two localisation keys and queue
rows are removed as obsolete. The attraction tooltip is retained without exposing
internal deletion/recreation. Other movement callers and GBR direct rule are
unchanged. No monthly recovery, invented membership effect or visible event is
added; later ordinary disbanding does not recreate the replacement again.

Native ordering was checked against the installed 1.14.5 arm64 executable:

- `CPoliticalMovement::DisbandMovement` calls `OnDisbanded` before the manager's
  `KillPoliticalMovement`. Recreating in the callback itself would be too early.
- `CPoliticalMovement::OnDisbanded` constructs a movement top scope (type `0x3c`,
  this movement's ID) for both the type callback and the documented movement-root
  on-action. The owner scope used by the receipt is therefore NAL; it is not the
  foreign event root that originally chose the settlement.
- `CCreatePoliticalMovementEffect::ExecuteDerived` calls the manager's explicit
  `CreatePoliticalMovement`, which rejects duplicate live identities but does not
  use `TryCreatePoliticalMovement`'s spontaneous-formation support threshold.
- The type parser rejects rereading an existing disband trigger with “Trigger
  section already read earlier.” A full CMF-body replacement is therefore used,
  with full token parity outside the one disband alternative and callback.

The override inventory pins both the Vanilla and installed CMF object/file hashes;
the dependency installation itself is unchanged. Temporary native evidence is
under `/private/tmp/sb-zulu-movement-2026-10-17/replacement-*.txt`.

**Verification:** 91 focused tests pass. The new tests execute the source branches
for early/late and missing movements, old country markers, foreign roots,
unrelated cultures/countries/types, reload during delivery, duplicate delivery,
intervening native recreation and later natural death. The intended replacement
test failed against A before the change. They supply native callback-before-deletion
ordering explicitly; they do not simulate recruitment or prove engine delivery.

Advisory Tiger 1.13.5 reports 0 fatal, 1,063 errors, 132 warnings, one untidy item
and one tip against the 1.14.5 scripts. Compared with the prior aggregate, the new
CMF-derived file adds two existing `days_since_movement_defeated` schema errors,
one inherited Hail Columbia localisation warning, and a callback-country-scope
warning. The latter is contradicted by the installed native callback setup above;
Vanilla's own Absolutist `on_disbanded` also enters `owner`. No diagnostics were
suppressed or gameplay rules changed to accommodate the older checker.

**Engine pending — DP:** restart and replay a checkpoint before selecting direct
administration. The old movement should disband at its native update and a fresh
movement appear one day after the callback. Record its changed ID/start date,
Initial Enthusiasm and native identity support; continue through monthly updates
and beyond the first year. Also test absence at annexation, the later Anglo-Zulu
route, and save/reload while the receipt is pending. This implementation does not
guarantee survival indefinitely after normal native support checks resume.

Final complete validation runs **519 tests: 510 pass, one pre-existing failure,
eight historical-input skips**. The failure is the reviewed-localisation regression
for Klip `.060`/`.080` and Natal Crisis `.050`; the separate localisation gate
reports the same drift. These approvals and texts were not rewritten. Across
16 gates: 12 pass, one deferred-gate warning, one deliberate read-only dependency
sync skip, two failures attributable to that existing review-baseline issue.
CMF installation verification, compatibility inventory, runtime contracts, delayed
lifecycle, map/naval and stale/unused-symbol checks pass. The new override's review
date/count assertion was updated explicitly and passes in the final run.

Transcripts: `/private/tmp/sb-zulu-replacement-before.txt`,
`/private/tmp/sb-zulu-replacement-focused.txt`,
`/private/tmp/sb-zulu-replacement-validation-final.txt`, and
`/private/tmp/sb-zulu-replacement-tiger.txt`. Trailing whitespace copied from CMF
was removed from the new override only; token parity and its exact inventory hash
were rechecked afterward. No launch or corrected survival result is claimed.


## Authorized modifier preservation

DP confirms the early replacement works and authorizes preserving **only Initial
Enthusiasm, Shepstone refusal and Shepstone repeal** for now. Broader Vanilla/mod
modifier copying is outside this change. The creation/disband handoff stays as
implemented in B; the fresh attraction grant and old grants are now distinct.

| Grant | Original attraction | Script duration | Replacement behavior |
|---|---:|---:|---|
| Initial Enthusiasm | +100% | 20 years = 7,300 days | Restore its tracked remaining fraction and expiry under its native name. |
| Shepstone refusal | +100% | 300 months = 9,000 days | Restore its tracked remainder; retain the country applied flag. |
| Shepstone repeal | +50% | 120 months = 3,600 days | Restore its tracked remainder; retain the country applied flag. |
| Annexation of Zululand | +100% | 20 years = 7,300 days | One fresh grant on the replacement, separate from all old bonuses. |

The only new localisation is the ordinary annexation modifier name. Event text,
option tooltips and choices are unchanged; no preservation explanation or popup
is added. Movement supporters, activism, backing characters and identity are not
copied. Grace still comes from the new native creation date.

### Timing and scope contract

1. The keyed Initial Enthusiasm helper preserves Vanilla's grant verbatim, then
   records `game_date + 7300` only on a NAL-owned Zulu cultural-minority movement.
   The two existing Shepstone grant helpers similarly record their actual expiry.
   Other countries, cultures and movement types receive no bookkeeping.
2. In the marked movement's `on_disbanded`, copy only supported modifiers that
   still exist and have a timing record to the **owner**. The snapshot contains
   numbers, not a reference to the movement about to be destroyed. Grants removed
   before disbanding are not restored.
3. The hidden receipt creates a new movement if needed, removes any fresh native
   Initial Enthusiasm, and restores each tracked old grant with:
   `remaining_days = original_expiry - game_date`,
   `multiplier = remaining_days / original_duration`, `is_decaying = yes`.
   This retains its original expiry and linear decay slope instead of restarting
   either. Non-positive remainders are omitted, including expiry during delivery.
4. Add the fresh Annexation of Zululand bonus. Consume owner snapshots and scratch
   values; retain each restored expiry on the new movement. Keep Shepstone's
   applied flags intact. A previously unapplied Shepstone consequence may still
   receive its legitimate first grant through the existing synchronization.

The existing consumed receipt and resolved settlement gates prevent duplicate
replacement or renewal. No periodic observer or global movement/pop scan is
added. Grant bookkeeping touches one movement; replacement checks three named
bonuses and the owner's existing movement list only once. Temporary values and
pending delivery survive ordinary save/reload.

### Native evidence and verification limits

Read-only inspection of the installed 1.14.5 arm64 binary establishes:

- `CGameDateTrigger::GetLeftHandSideValue` (`0x10357bc18`) supplies an integer game
  day; its comparison-value constructor (`0x10357b890`) uses the integer value
  contract. No date strings or guessed current year are used in arithmetic.
- `CJominiScriptDuration::Read` uses days = 1, months = 30, years = 365.
  `CAddModifierEffect::ExecuteDerived` evaluates scripted duration and multiplier
  in the current scope, and passes the decay setting through.
- `CTimedModifier::CalculateMultiplier` applies linear remaining-day decay to the
  stored multiplier, at native fixed-point precision (five decimal places).
- `CModifierValueLink::GetScope` (`0x103862aa0`) has no political-movement branch.
  `modifier:` cannot be used to read a movement's aggregate attraction here.
  GUI `GetTimedModifiers`/`GetRemainingDuration` do not provide a script iterator.

The expiry ledger preserves **whole game days**, with fixed-point rounding of
strength. It does not preserve sub-day timestamps; a grant and replacement at
different native hours may shift expiry within one day. Pre-change checkpoints
lack these records. Untracked grants are skipped, never renewed with an invented
full duration. This is a new-grant contract, not save migration. All three grants
have fixed original multipliers in the covered sources; edits adding other grant
paths or changing durations must update their timing records and tests together.

Native inspection transcripts remain under
`/private/tmp/sb-zulu-movement-2026-10-17/preserve-*.txt`. The inventory separately
pins the new enthusiasm helper to current Vanilla; full effective CMF parity
outside the existing two movement hooks remains required. CMF is unmodified.

**Focused verification:** 31 tests pass across preservation, annexation lifecycle,
Klip punitive settlement and colonial delivery. The new regression initially
failed on the lost Shepstone grants. Source-driven cases cover different grant
ages, next-day or delayed delivery, save/reload, expiry during delivery, stale or
missing records, removed modifiers, native enthusiasm at recreation, first-time
Shepstone synchronization, regrants, duplicate delivery, foreign roots and
unrelated countries/cultures/types. Tests use actual script bodies and native
whole-day/fixed-point arithmetic; they do not simulate native recruitment.

**TODO — engine testing deferred by DP, 17 October 2026:** when resumed, use grants made under these scripts. Record each of the
three modifiers before annexation, then compare its remaining strength and expiry
on the replacement alongside the fresh twenty-year annexation bonus. Check early
and later routes, expiry during delivery and a saved pending receipt. Restarting
from an old checkpoint containing untracked modifiers cannot test preservation.
No game was launched or save altered for this implementation.


**Complete validation:** 527 tests, **518 pass**, eight historical-input skips,
and the same pre-existing reviewed-localisation failure for Klip `.060`/`.080`
and Natal Crisis `.050`. The separate localisation gate reports that same drift;
no approval baseline or reviewed wording was changed. Compatibility/dependency,
local override inventory, map/naval, lifecycle, runtime contracts and unused/stale
symbol checks pass. Five existing deferred release gates remain warnings; CMF
sync was deliberately skipped while installed-tree verification remained active.

The advisory Tiger run found the new helper lacked the repository's UTF-8 BOM;
that encoding was corrected, then focused tests and the full inventory passed
again. The final Tiger run reports **0 fatal, 1,063 errors, 128 warnings, one
untidy item, one tip** with its older 1.13.5 schema against 1.14.5. It introduces
no new diagnostic relative to the prior replacement baseline. Four existing
CMF illustration scope warnings did not recur in the final run; no CMF change is
claimed. No diagnostics were suppressed. Whitespace checks pass.

Transcripts: `/private/tmp/sb-zulu-modifier-preservation-validation.txt` and
`/private/tmp/sb-zulu-modifier-preservation-tiger.txt`. The former includes the
subsequently corrected BOM warning; the latter is the final advisory recheck.
