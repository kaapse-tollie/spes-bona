# Klip River colonial delivery repair — 13 September 2026

## Held-popup repair after the 16:54 reproduction

The next 1851.2.1 autosave contains two open `.060` events, created on 6 and
27 January. Natal is now pending rather than resolved, but both events and
Natal's generation variable reference container `16777216`, which no longer
exists. The earlier colonial-permission correction did not eliminate this
independent failure of the container-backed delivery. Evidence is retained in
`/private/tmp/sb-klip-duplicate-2026-09-13/`.

Opening either event removed its dispatch marker. Consequently the monthly
queue could dispatch another copy while the first remained open. The missing
container also selected a fallback option without the original tooltip.

The current implementation removes the two delivery containers and their orphan
references. Each once-only follow-up binds directly to its original Natal
country. Pending/resolved markers and the existing exact-play checks still
prevent repeat launches. Formation locks retain the pending, active and play
markers; retag cleanup runs on the original marker holder, not a replacement NAL.

Both `.050` and `.060` now have one original option with its original tooltip.
Dispatch requires launch preflight. The short dispatch marker expires if delivery
never happens; on opening it is replaced by an untimed reservation until the
option is answered. Answering releases it and revalidates the route before
launching. A busy participant leaves the route pending for a later ready pulse.
Each event also supplies the Zulu localization scope directly. No new prose,
options or recovery events were added.

Validation: 85 focused tests pass, including reservation checks at days 21, 51
and 81, lost-dispatch retry, busy-participant deferral, country identity and
existing story-war contracts. The full static suite has zero failures and the
five existing deferred warnings; output is
`/private/tmp/sb-klip-held-delivery-validation.txt`. `git diff --check` passes.
DP subsequently confirmed that the corrected Klip follow-up works. Broader
war-outcome and later settlement scenarios remain subject to engine testing.
Existing duplicate popups retain their old container references and are not
converted by this repair.

The following sections record the preceding colonial-permission and refugee
repairs. Their references to retaining container initialization describe that
earlier attempt; the held-popup repair above supersedes it.

## Observed failure

DP reproduced the ordinary route from a checkpoint: choose the Klip River claim,
switch to ZUL, reject via `.020.c`, then leave Natal's `.060` unanswered.
The 1851.2.1 autosave confirms:

- Natal is country `16777670`, a British colony under GBR (`3`), through the
  `colony` pact dated 1850.2.1. ZUL is country `481`.
- `.060` was created on 1851.1.6, expires on 1851.4.6, and remains open. Its
  saved receipt points to container `16777216`; its saved Zulu scope is correct.
- `.081` was created on 1851.1.27 and is also open. This was not `.060` expiring.
- Natal has `sb_klip_river_county_resolved_var`, punitive outcome pending, and
  final evidence `0`, while the old punitive launch-pending marker remains.
- Container `16777216` is destroyed and Natal no longer holds its generation
  variable. No Klip punitive play is present in the inspected play records.

Evidence is retained under `/private/tmp/sb-klip-failure-2026-09-13/`.

## Cause and correction

The added preflight and permanent-invalidity checks required ordinary aggressive
play permission on Natal, despite this chain requiring Natal to be a British
colony. Vanilla `subject_type_colony` has `can_start_own_diplomatic_plays = no`.
The installed executable's trigger help defines the permission check in terms of
independence or permission to start one's own plays. Both custom Klip plays
already use `blocked_by_diplomatic_status = no`.

Consequently the ordinary colonial actor failed launch preflight and satisfied
permanent invalidity. Monthly housekeeping could call punitive cancellation,
record evidence `0`, call the white-peace finalizer, queue `.081`, and destroy
`.060`'s receipt before the player answered it.

The repair removes the contradictory Natal permission check from both routes'
preflight and permanent-invalidity triggers. Zulu independence/permission,
physical ownership, busy-participant and exact-play checks remain. Unlaunched
punitive cancellation now closes the pending route without calling a war-result
finalizer or queuing an outcome event. Both terminal cleanup helpers remove the
pending launch marker, preventing later retries of a terminated route.

The reported refugee errors come through `.081`'s hidden option effect into
`sb_trigger_natal_refugee_migration_effect`. Its counter is initialized during
execution, but was read unconditionally during tooltip evaluation. All five
counter comparisons now sit inside a separate existence-guarded branch. The
migration fractions and recipient selection are unchanged.

## Earlier failed response

The initial tooltip-only response added waiting/cancelled/outdated labels to four
conditional options. DP correctly rejected this as narrative filler for an
implementation failure. All six added keys and their review-queue entries have
been removed; the original option labels and approved prose remain. The prior
container initialization and retry-localization-scope corrections are retained.
No new event content or fallback options are added by this repair.

## Validation and limits

- 63 focused tests pass. The new fixture evaluates the actual trigger expressions
  with colonial Natal and independent Zulu; both routes remain valid, while a
  busy participant delays rather than permanently invalidates them.
- Four new regression tests produce six failing assertions/subtests against the
  retained pre-change scripts, with zero test errors.
- `git diff --check` passes.
- Full static validation: 16/16 checks passed or warned, zero failures; the five
  existing deferred gates remain warnings. Output:
  `/private/tmp/sb-klip-colonial-delivery-validation.txt`.
- Engine confirmation remains with DP. Replay from before Zulu's rejection with
  the corrected scripts loaded; hold `.060` across the next monthly pulse, then
  launch, and check the resulting settlement and refugee tooltips.

The inspected save has already been marked resolved and its receipt destroyed.
This code repair does not rewrite that save or recreate its lost runtime state.
