# Klip River: false incomplete settlement after the Chiefdoms choice

Initial investigation and subsequent authorised source correction, 17 October
2026. The saved evidence and original diagnosis below precede the correction.
DP's edits to `.060.d`, `.060.a` and `.080.d` are preserved. No localisation,
dependency or save changes; no game launch. Corrected engine delivery is pending.

## Saved result

The 1 July 1850 autosave confirms a successful territorial/subjugation outcome
followed by a false incomplete-settlement notification. Manager-bounded extracts
and source save hashes are recorded in
[the evidence file](evidence/klip_punitive_handoff_2026_10_17.json).

Country IDs are GBR `3`, ZUL `481`, NAL `16777900`. The exact punitive play is
`134217728`, started on 26 August 1849.

| Date | Saved evidence |
|---|---|
| 1 March–1 May 1850 | Britain leads the play. GBR's Make Protectorate and NAL's Return State are primary demands; ZUL's Return State is secondary. NAL's original Make Protectorate is already discarded. |
| 27 May 1850 | Both allied demands execute by `occupation_timer`, reaching 100. Natal's merged state records transfer from ZUL on this date. ZUL becomes GBR's protectorate. The play ends at `1850.5.27.6`. |
| 1 June 1850 | ZUL remains GBR's protectorate. NAL still holds the active punitive-play reference and ended marker; no Klip final result has been recorded. |
| 2 June 1850 | The later NAL–ZUL subject pact starts on this date; the British handoff is subsequently marked resolved. The pact retains this start date after changing subject type. |
| 9 June 1850 | ZUL gains `sb_zululand_chiefdoms_subject_dependence`, applied by the Thirteen Chiefdoms option. |
| 11 June 1850 | `.081` is created for NAL. It remains open in the July save, with expiry 11 September. |
| 1 July 1850 | ZUL is NAL's `sb_zulu_chiefdoms` subject. NAL has the government-choice resolved flag, Klip resolved flag, **final evidence 0**, and pending Klip outcome delivery. |

## Cause

1. `sb_klip_river_punitive_demands_fulfilled` requires both the returned provinces
   and **exactly a direct NAL protectorate**. A GBR protectorate does not pass.
2. The native play's actual goal holder is GBR. The generic British postwar route
   handles this: `sb_zululand_settlement.001.a` calls
   `sb_zululand_handoff_to_natal`, which transfers the live ZUL subject to NAL.
3. That handoff schedules `sb_natal_interwar.030` without first finalizing the
   still-active Klip result. The government choice can therefore precede Klip's
   next monthly reconciliation.
4. Chiefdoms changes ZUL from protectorate to the special puppet-category subject.
   The subsequent Klip check fails its exact protectorate condition, sees the
   play has ended, records evidence 0 and queues `.081` through the white-peace
   finalizer. This matches the saved 9 June / 11 June sequence.

The Crown choice would leave the protectorate predicate true; Chiefdoms and direct
annexation can invalidate it. That source consequence is not a separate engine
test of those other options. Reconciliation before the British handoff is also
capable of treating that intermediate GBR protectorate as an incomplete result.

`.081` is intended for terminal outcomes where NAL retains its core but has not
secured both demands: white peace or a partial settlement. It must not be used
for this full victory. Its reviewed statement that neither frontier changed is
also too narrow for genuine partial territorial outcomes.

## War-goal priorities and beneficiary

The September two-demand plan deliberately made both NAL demands primary so Zulu
backdown would concede both. The current source still opens with Make Protectorate
and adds NAL's Return State with `primary_demand = yes`. It adds ZUL's counter-demand
without that field. No recent priority change appears in these source definitions.

The retained saves additionally show NAL's opening protectorate goal `83886102`
discarded and GBR's replacement `150994944` active, then executed. Britain is the
play leader. The first retained checkpoint is already during the war: it proves
the replacement, but not its exact timing or whether a native takeover or later
AI goal handling caused it. CMF does not override Make Protectorate.

DP initially proposed reciprocal primary Return State and secondary GBR Make
Protectorate, then withdrew that change. The confirmed decision retains both
allied demands as primary and ZUL's Return State as secondary. No war-goal
priority or definition changes are part of this correction.

DP suggested that NAL's lack of responsible government explains the replacement.
Installed Vanilla's `subject_type_colony` explicitly has `can_have_subjects = yes`,
as does SB's responsible colony. Ordinary protectorate eligibility instead admits
only great, major and minor powers; saved NAL is an insignificant power. Rank and
British play leadership are therefore leads, not proof of the engine's reason for
replacing the demand. Neither SB nor CMF overrides those two native subject types.

The current narrative handoff is Britain deciding to place conquered Zululand
beneath Pietermaritzburg. GBR receives **The Government of Conquered Zululand**;
its default/AI choice is **Place Zululand beneath Natal**. `transfer_subject`
preserves the living country, followed by Natal's three administration choices.

## Initial correction requirements and verification limits

- Complete the earned Klip victory before the government choice can alter its
  subject-status predicate. Retain a once-only terminal result afterwards.
- Distinguish an earned British protectorate awaiting the authorised handoff from
  a missing subjugation demand; do not grant unearned demands or bypass the actual
  territorial result. Keep genuine partial settlements and defeats separate.
- Preserve the subsequently confirmed priorities; test both directions of
  backdown as well as timer and negotiated outcomes.
- Add lifecycle coverage for GBR protectorate → NAL handoff → each government
  choice → delayed monthly reconciliation. Existing tests model the final NAL
  protectorate directly and do not cover this intervening route.

All 19 existing focused Klip tests pass. A read-only evaluation using their actual
source-condition evaluator reproduces: British protectorate = terminal failure;
NAL protectorate = government event eligible; Chiefdoms before reconciliation =
terminal failure again. This verifies the script-logic defect, not native goal
replacement or a repaired engine run. The inspected logs contain no Klip routing
exception explaining the false result; the incorrect branch is valid script.

## Implemented correction

Only two runtime changes were needed:

1. The actual-outcomes predicate accepts ZUL as GBR's protectorate while NAL is
   a British subject, as well as the existing direct NAL protectorate. All four
   Natal province-owner checks and the exact protectorate-type check remain.
   Thus the real allied victory is recognised before Britain's handoff, without
   granting a missing territorial or subject demand.
2. `sb_zululand_handoff_to_natal` calls the existing Klip reconciler in NAL scope
   before scheduling the government choice. This records victory and clears the
   active punitive markers before Chiefdoms or annexation can invalidate the
   protectorate predicate. The generic handoff still works without an active
   Klip route; no new flags, event content or peace requirements were added.

Natal's government event still requires the direct NAL protectorate, so recognising
the British-held victory does not open that choice before the transfer. The
existing once-only dispatch markers prevent the reconciler and handoff from
scheduling it twice. Subsequent monthly reconciliation leaves the earned result
intact after any of the three government choices.

Regression tests read the actual script branches, retain GBR as foreign event
ROOT and track each country's markers. They reproduced eight failing subcases
before the runtime correction. Afterwards all **130 focused tests pass**, covering
monthly reconciliation before/after handoff, all three government choices,
ordinary non-Klip handoff, missing outcomes and unrelated overlords. These tests
do not emulate native war-goal enforcement or character/economy packages.

Full validation (`python3 -B tools/validate.py --skip-cmf-sync --tiger`) reports
**15/17 gates passed, warned or skipped; two failed**. Unit discovery ran 509
tests: 500 passed, eight skipped and one failed. Both failing gates concern the
existing reviewed-localisation baseline differences for `.060`, `.080` and
`sb_natal_crisis.050`; the former two are DP's edits, the latter an existing
Pretoriius/Pretorius spelling correction. No prose or approval hashes were
changed to hide those failures. Compatibility, map/naval, runtime contracts and
delayed-event lifecycle checks pass. Dependency sync was deliberately skipped;
installed patched-CMF verification passed. The five deferred release gates
remain warnings. Tiger is advisory and reports 0 fatal, 1,061 errors, 130 warnings,
one untidy and one tip, including its known unsupported container API diagnostics;
it reports no diagnostic at the two changed runtime blocks. Full output:
`/private/tmp/sb-klip-081-validation-2026-10-17.txt`.

DP should restart with this source and replay from before victory/handoff; the
retained 1 June 1850 checkpoint still has the unfinalized British protectorate.
For complete play setup/backdown verification, start before the punitive play.
Check `.080` once, the government choice once after transfer, and no `.081` after
choosing Chiefdoms and advancing across monthly pulses. Crown and direct-rule
replays remain pending too. The July save's already-recorded incomplete outcome
is not migrated or repaired.

The occupation-rule workaround remains **ON HOLD**. DP reports the same 50%
occupation issue in Klip River and ORA–BST and intends another Paradox follow-up.
A possible local patch after next weekend is a later decision, not implemented
or scheduled here. Existing partial/defeat handling is retained; no new partial
settlement mechanic was introduced.
