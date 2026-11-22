# Dunn's judgement, new reigns and wartime provisions

Implemented against 1.14.5 / CMF 1.66.0 + sb-1.14.3-r1. No launch,
dependency change or save migration. This supersedes the earlier August
retirement, automatic Mthonga introduction/declaration and 150% provisions
defaults; the earlier design and test reports remain historical evidence.

## Dunn

The actual admitted Dunn remains protected during the qualifying
Cetshwayo-over-Mbuyazi victory. Judgement is now scheduled **three days after
acknowledging One Royal Homestead (`sb_court_succession.005`)**. The victory
receipt is consumed before scheduling, preventing repeat acknowledgements from
duplicating it. Event delivery and resolution revalidate Dunn, Cetshwayo and
the judging country.

`sb_court_dunn.003`, **An Unwelcome Intermediary**, retains its two-character
window and presents the victors' resentment alongside Dunn's usefulness:

| Choice | Consequences on selection |
| --- | --- |
| Execute | Dunn dies; ruler receives **+10 Popularity for five years**; GBR relations **−10**; Dunn's deliveries end. |
| Retain | Dunn supports the king; GBR relations **+5**; unfinished Firearms deliveries continue where British Natal remains available; Mthonga is introduced and declares his claim. |
| Banish | Dunn leaves for Natal, then CAP if Natal is unavailable, otherwise exile; his court support and deliveries end, without a relations penalty. |

Mthonga receives the existing Claimant trait (+25 Prominence), without a free
backer. Remove the separate 1855 introduction and 1857 automatic declaration.
Reuse an eligible existing identity; do not recreate a dead/foreign prince or
undo renunciation/retirement. His template's age of 18 remains an authored
estimate. Hamu's availability and foreign bargain are unchanged.

Dunn's template is Industrialists. His visit and a newly opened judgement also
normalise the existing identity's IG without changing its recorded allegiances.
An already-open saved popup does not rerun its opening effects: replay from
before victory for this event check.

Used the **victoria-3-events** skill, reading the complete installed
`shogunate.2` script/localisation for coalition tradeoffs and concrete stakes.
The existing native `event_window_2char` shows the king and trader. The Mthonga
paragraph is conditional on an available claim. Popularity uses the native
modifier preview; background sequencing remains hidden. These are authored
alternate-history choices, not historical quotations. All changed namespaces
remain **TO REVIEW**; no reviewed wording or approval baseline was changed.

## Succession and calendar

A new sovereign starts at **0 Prerogative**, including peaceful succession,
minority succession and ordinary native fallback in the authored country.
Both new princes start at zero in a contested death/retirement. Repeated
installation, a regent's replacement and the same sovereign reaching majority
do not reset an existing reign. A living incumbent defeating a challenger
retains his Prerogative; the existing victory acknowledgement adds **10** once.

Mpande's retirement eligibility moves to **1 July 1856**. The latest trial
created its movement on 20 August and reached target support on sample 20,
consistent with a January outbreak. Moving the lead-in one month earlier aims
at December. Five-point weekly activism, support readiness, the 26-sample bound,
eligibility and popup acknowledgement remain authoritative; the date is not
guaranteed by a forced war.

## Food relief and observed replay

The same `sb_court_wartime_provisions` modifier now provides **+75% Food
Security**, replacing +150%. It applies to both actual claimant-war countries,
player or AI, after either a native one-state split or scripted multi-state
muster. It is independent of the AI supply-consumption discount. Exact-war end,
cancellation/finalisation and missing-war reconciliation clear it. It cannot
stack with an obsolete second modifier.

This is partial relief. Native food prices and severe shortages can still leave
Pops starving; the modifier neither produces grain nor restores casualties.
No population or army redistribution was changed in this follow-up.

The April–August 1857 autosaves confirm a **four-province/five-province** split
in STATE_ZULULAND. The actual rebel's target was **57.275%**; the log's twentieth
sample reached **57.781%** total support, with **52.545%** military support.
This is successful support convergence for one trial, not proof of repeatable
25/50/75% force scaling.

Cached strata populations fall from 139,917 to 134,558 in the original faction
and from 178,004 to 168,863 in the rebels between April and August. Those totals
do not isolate starvation from casualties, migration or earlier losses. Neither
country had the old muster-only relief. DP reports severe famine; the new 75%
relief needs an in-game comparison. [Save/log evidence and hashes](compatibility/evidence/zulu_second_succession_convergence_2026_10_31.json).

## Acceptance

**160 focused tests pass**, independently reproduced by the requested
Sol 6.1 Max reviewer with no blocking finding. They cover acknowledgement/delay,
all choices, stale and repeated outcomes, identity guards, succession resets
and exceptions, both faction assignments, both relief paths and cleanup.
Native food arithmetic explicitly permits residual starvation at this tuning.

Full discovery: **1,014 tests — 1,005 passed, eight historical skips, one
unchanged localisation-review failure, no errors**. The full validator remains
**15/17** gates passed/warned; unit/localisation gates both report the existing
dangling Swazi `.098.prerogative_after_blood_river` review row and reviewed
wording drift in Natal `.050` and Klip `.060`/`.080`. Their source and
approvals are untouched.

CMF verification, compatibility inventory, map/naval checks, delayed-event
lifecycle and script contracts pass. The delay manifest records 444 dispatches,
including the new three-day judgement and its cancellation/receipt contract.
Advisory Tiger: **0 fatal, 1,076 errors, 148 warnings, one untidy, one tip**.
Its 1.13.5 parser remains behind the installed 1.14.5 game. Compared with the
preceding run, the warning-count change is scope deduction in untouched
Bechuanaland/story helpers; no diagnostic names the changed Dunn, succession,
dynastic or modifier files. Whitespace validation passes.

Full output: `/private/tmp/sb-dunn-succession-followup-acceptance-20261031.txt`.
DP engine checks are numbered **156–159** in the
[runtime matrix](zulu_court_runtime_matrix_2026_10_19.md). All newly changed
timing, UI and famine scenarios remain pending DP.
