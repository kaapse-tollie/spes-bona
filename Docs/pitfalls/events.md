# Event scheduling, choices and cleanup

Read when: Delayed events, open choices, retries, receipts or cancellation.

[Topic index](../../common_pitfalls.md) · [Repository instructions](../../AGENTS.md)

Engine-specific claims concern investigated Victoria 3 1.14.x builds. Recheck
against the target build and preserve each rule's evidence limits; see the
[version and evidence guidance](../../common_pitfalls.md#evidence-and-version-limits).

<a id="evt-01"></a>

## EVT-01 — Dispatch, open popup, answered choice and terminal outcome are distinct

A dispatch timeout may permit retry before an event opens. Once open, its
reservation must last until answer, expiry or cancellation. Clearing it in
`immediate` can allow the next pulse to queue a duplicate. Model only the
states the route actually needs; containers and extra flags are not mandatory.

<a id="evt-02"></a>

## EVT-02 — Cancelling a route does not retract a queued event or open popup

Delayed
effects must check their original reservation at delivery. Where the same
actors can appear in consecutive episodes, actor identity alone cannot
distinguish an old choice from a new one. Keep the episode identity through
dismissal and prevent duplicate queued retries.

An episode may have multiple delivery attempts. If a cancelled request can be
retried under the same ID, validate the active attempt's identity or forbid reuse
of the cancelled ID. Check this at delivery and acceptance; an open reservation
for the same recipient and episode is not sufficient. Test the sequence
open → cancel → retry the same ID → accept the old popup: the old popup must be
rejected. A passing in-memory fixture does not establish identity persistence
across save/load or engine callbacks.

<a id="evt-03"></a>

## EVT-03 — Revalidate at the point of effect

Ownership, ruler, subject relationship,
participant eligibility and the tracked conflict can change while an event is
waiting. Share the relevant target rules between selection, preview and
execution. Do not silently substitute a new person beneath an existing choice.

An ultimatum response belongs to its deciding overlord. Revalidate that recipient
while the popup is open and after refusal if native play creation is delayed.
A subject changing overlord must not drag its new overlord into a predecessor's
unexecuted decision. Source-executed fixtures cover held popups and changed
overlords; native diplomatic routing still requires engine verification.

<a id="evt-04"></a>

## EVT-04 — Choose when a consequence belongs

An event's `immediate` runs when it
opens, before the answer. An acknowledgement of an automatic settlement must
not apply that settlement again; a reward promised for a choice must wait for
the valid option. Consume the once-only receipt at the intended phase and
test repeated callbacks and repeated answers.

<a id="evt-05"></a>

## EVT-05 — Set re-entry guards before effects that can call back into the system

Reserve the once-only receipt or cooldown before invoking cleanup, ruler
changes, notifications or helpers that can re-enter the controller. Waiting
until a later acknowledgement leaves a window for immediate retriggering.
Exercise a callback during the first application, not only a second call after
the helper returns.

<a id="evt-06"></a>

## EVT-06 — Displayed offers need a consistent execution contract

Decide whether a
price or probability is frozen or recalculated. Debit the stored quote when
it is frozen; seek a fresh choice if a recalculated offer changes what was
displayed. Revalidate participants independently of price. Display and roll
the same rounded probability.

<a id="evt-07"></a>

## EVT-07 — Changing an option can invalidate its timeout default

Review the default
whenever a cost or eligibility condition changes; a formerly free, always-valid
option may no longer be suitable. Revalidate before charging, and allow an
invalidated scene to close without charging for its dismissal. Test the default
and stale-choice paths separately from an ordinary valid selection; native
timeout delivery still requires engine verification.

<a id="evt-08"></a>

## EVT-08 — Eligibility checks must admit the intended scenario

A blanket peace,
independence or no-active-play condition can block a route intended for
subjects or countries in unrelated wars. Check the relevant actors and
confrontation. Scope-validity guards do not justify new gameplay restrictions.

<a id="evt-09"></a>

## EVT-09 — Finalise results before dependent actions change their evidence

A later
government choice, ownership transfer or subject conversion can invalidate
the predicate that established the original victory. Record the earned result
before scheduling that choice. Keep setup helpers separate from notification
scheduling when setup is also called from an option.

<a id="evt-10"></a>

## EVT-10 — Store durable outcomes separately from temporary context

An AI hint,
popup-context flag or shared "resolved" marker does not identify a particular
winner or choice. Keep the outcome needed by later mechanics after temporary
delivery state is cleared.

An earned territorial receipt must survive its source container and delayed
reunion. Reserve the actual participants before cleanup, and distinguish the
authenticated defeated faction from a genuine third-party owner. A competing
route must not resell the same land while the first cession remains pending.
Source-executed fixtures cover these receipts; native reunion order remains an
engine check.

<a id="evt-11"></a>

## EVT-11 — A missing object is not proof of success

`has_variable` only proves that
a reference was stored, not that its target still exists. Recovery must use
authenticated result evidence and the original participants. Cancellation,
disappearance and incomplete peace terms must not become victory by default.
Aborting a pending launch is not white peace: delivery cleanup must not call a
war-result finaliser for a conflict that never started.

<a id="evt-12"></a>

## EVT-12 — Cleanup must cover every owned entry path

Clear launch-pending state as
well as active state, so retries cannot restart a finished route. Release only
locks owned by that controller. A scheduled expiry of a paid commitment must
still run after its target dies or the originating feature ends.

<a id="evt-13"></a>

## EVT-13 — AI decisions have multiple stages

Interaction weights influence whether
the AI opens an event; option weights govern its subsequent choice, and the
selected helper may have further gates. Apply continuing eligibility at
selection and payment, and test AI execution as well as human execution.
Weight identities when the preference concerns named actors; their menu
positions can change. Rank-based weighting is appropriate when the preference
concerns rank. Verify that ordering and weights implement the intended rule.

<a id="evt-14"></a>

## EVT-14 — Fix routing failures in the implementation

Missing internal references
should not become invented story content, redundant choices or recurring
notices asking the player to repair delivery.
